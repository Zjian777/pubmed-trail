"""
PubMed爬取模块 - 使用Biopython的Entrez模块搜索Pubmed
"""

import time
from Bio import Entrez
from typing import List, Dict, Optional
import config


class PubMedCrawler:
    def __init__(self, email: str = None, api_key: str = None):
        """
        初始化PubMed爬虫

        Args:
            email: 用于PubMed API联系的邮箱
            api_key: PubMed API密钥(可选)
        """
        self.email = email or config.PUBMED_EMAIL
        self.api_key = api_key or config.PUBMED_API_KEY
        Entrez.email = self.email
        if self.api_key:
            Entrez.api_key = self.api_key

    def search_articles(self, search_terms: List[str], start_date: str, max_results: int = 1000) -> List[int]:
        """
        搜索PubMed文章

        Args:
            search_terms: 搜索词列表
            start_date: 开始日期 (YYYY/MM/DD格式)
            max_results: 最大返回结果数

        Returns:
            文章ID列表
        """
        # 构建搜索查询
        search_query = " OR ".join([f'("{term}"[Title/Abstract] OR {term}[MeSH Terms])'
                                     for term in search_terms])

        # 添加日期限制
        date_query = f'("{start_date}"[Date - Publication] : "3000/12/31"[Date - Publication])'
        full_query = f"({search_query}) AND {date_query}"

        print(f"搜索查询: {full_query}")

        try:
            handle = Entrez.esearch(
                db="pubmed",
                term=full_query,
                retmax=max_results,
                sort="date"
            )
            result = Entrez.read(handle)
            handle.close()

            id_list = result.get("IdList", [])
            print(f"找到 {len(id_list)} 篇文章")
            return id_list

        except Exception as e:
            print(f"搜索错误: {e}")
            return []

    def fetch_article_details(self, pmids: List[int], batch_size: int = 100) -> List[Dict]:
        """
        获取文章详细信息

        Args:
            pmids: PubMed ID列表
            batch_size: 每批获取的数量

        Returns:
            文章信息字典列表
        """
        articles = []
        total = len(pmids)

        for i in range(0, total, batch_size):
            batch = pmids[i:i+batch_size]
            print(f"获取文章 {i+1}-{min(i+batch_size, total)}/{total}...")

            try:
                handle = Entrez.efetch(
                    db="pubmed",
                    id=batch,
                    rettype="medline",
                    retmode="xml"
                )
                records = Entrez.read(handle)
                handle.close()

                for record in records.get("PubmedArticle", []):
                    article_info = self._parse_article(record)
                    if article_info:
                        articles.append(article_info)

                # 避免请求过快
                time.sleep(config.DELAY_BETWEEN_REQUESTS)

            except Exception as e:
                print(f"获取文章详情错误: {e}")
                continue

        return articles

    def _parse_article(self, record: Dict) -> Optional[Dict]:
        """
        解析单篇文章记录

        Args:
            record: PubMed文章记录

        Returns:
            解析后的文章信息字典
        """
        try:
            # 获取PMID
            pmid = str(record.get("PMID", ""))

            # 获取标题
            article = record.get("MedlineCitation", {}).get("Article", {})
            title = article.get("ArticleTitle", "")

            # 获取期刊信息
            journal = article.get("Journal", {})
            journal_title = journal.get("Title", "")
            journal_issue = journal.get("JournalIssue", {})
            pub_date = ""
            if journal_issue.get("PubDate"):
                pub_date = journal_issue["PubDate"].get("Year", "")
                if journal_issue["PubDate"].get("Month"):
                    pub_date += f"-{journal_issue['PubDate']['Month']}"

            # 获取摘要
            abstract = ""
            if article.get("Abstract"):
                abstract_texts = article["Abstract"].get("AbstractText", [])
                if isinstance(abstract_texts, list):
                    abstract = " ".join(abstract_texts)
                else:
                    abstract = str(abstract_texts)

            # 获取作者
            authors = []
            author_list = article.get("AuthorList", [])
            for author in author_list:
                if isinstance(author, dict):
                    last_name = author.get("LastName", "")
                    fore_name = author.get("ForeName", "")
                    if last_name:
                        authors.append(f"{fore_name} {last_name}".strip())

            # 获取DOI
            article_id_list = record.get("PubmedData", {}).get("ArticleIdList", [])
            doi = ""
            for aid in article_id_list:
                if aid.attributes.get("IdType") == "doi":
                    doi = str(aid)

            if not title:
                return None

            return {
                "pmid": pmid,
                "title": title,
                "journal": journal_title,
                "pub_date": pub_date,
                "abstract": abstract,
                "authors": "; ".join(authors[:10]),  # 限制作者数量
                "doi": doi
            }

        except Exception as e:
            print(f"解析文章错误: {e}")
            return None

    def get_articles(self, search_terms: List[str] = None, start_date: str = None) -> List[Dict]:
        """
        获取所有符合条件的文章

        Args:
            search_terms: 搜索词列表
            start_date: 开始日期

        Returns:
            文章列表
        """
        search_terms = search_terms or config.SEARCH_TERMS
        start_date = start_date or config.SEARCH_START_DATE

        # 搜索文章ID
        pmids = self.search_articles(search_terms, start_date)

        if not pmids:
            print("未找到符合条件的文章")
            return []

        # 获取文章详细信息
        articles = self.fetch_article_details(pmids)

        print(f"成功获取 {len(articles)} 篇文章的详细信息")
        return articles


if __name__ == "__main__":
    # 测试
    crawler = PubMedCrawler()
    articles = crawler.get_articles()
    print(f"\n总共获取 {len(articles)} 篇文章")
    if articles:
        print(f"第一篇文章: {articles[0]['title'][:100]}...")