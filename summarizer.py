"""
Deepseek API总结模块 - 对文章摘要进行AI总结
"""

import requests
import time
import sys
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import config


def safe_print(*args, **kwargs):
    """安全打印，处理编码问题"""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        # 如果编码失败，尝试只打印ASCII字符
        ascii_args = [str(arg).encode('ascii', 'replace').decode('ascii') for arg in args]
        print(*ascii_args, **kwargs)


class ArticleSummarizer:
    def __init__(self, api_key: str = None, base_url: str = None, model: str = None):
        """
        初始化文章总结器

        Args:
            api_key: Deepseek API密钥
            base_url: API基础URL
            model: 模型名称
        """
        self.api_key = api_key or config.DEEPSEEK_API_KEY
        self.base_url = base_url or config.DEEPSEEK_BASE_URL
        self.model = model or config.DEEPSEEK_MODEL
        self.session = requests.Session()

    def summarize_article(self, title: str, abstract: str, pmid: str = "") -> Optional[str]:
        """
        对单篇文章进行总结

        Args:
            title: 文章标题
            abstract: 文章摘要
            pmid: PubMed ID

        Returns:
            总结文本，如果失败返回None
        """
        if not abstract:
            return "No abstract available"

        prompt = self._build_prompt(title, abstract, pmid)

        for attempt in range(config.MAX_RETRIES):
            try:
                response = self._call_api(prompt)
                if response:
                    return response

            except Exception as e:
                safe_print(f"Summarization error (attempt {attempt + 1}/{config.MAX_RETRIES}): {e}")
                time.sleep(2 ** attempt)  # 指数退避

        return "Summarization failed"

    def _build_prompt(self, title: str, abstract: str, pmid: str = "") -> str:
        """
        构建提示词

        Args:
            title: 文章标题
            abstract: 文章摘要
            pmid: PubMed ID

        Returns:
            提示词
        """
        return f"""请分析以下关于食管癌的学术论文摘要，并按以下格式提供总结：

## 文章信息
- PMID: {pmid}
- 标题: {title}

## 摘要
{abstract}

## 总结要求
请提供以下信息：
1. **研究类型**: (如基础研究、临床研究、综述、队列研究等)
2. **主要发现**: (用1-2句话概括核心发现)
3. **研究方法**: (简述使用的实验或分析方法)
4. **临床意义**: (如果有，简要说明对食管癌诊疗的意义)

请用中文回答。"""

    def _call_api(self, prompt: str, timeout: int = None, max_tokens: int = None) -> Optional[str]:
        """
        调用Deepseek API

        Args:
            prompt: 提示词
            timeout: 超时时间(秒)，默认使用配置值
            max_tokens: 最大token数，默认使用配置值

        Returns:
            API响应文本
        """
        timeout = timeout or config.REQUEST_TIMEOUT
        max_tokens = max_tokens or 1000

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": max_tokens
        }

        response = self.session.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=timeout
        )

        if response.status_code == 200:
            result = response.json()
            return result.get("choices", [{}])[0].get("message", {}).get("content", "")
        else:
            safe_print(f"API error: {response.status_code} - {response.text}")
            return None

    def optimize_search_terms(self, user_topic: str) -> List[str]:
        """
        使用AI优化搜索词

        Args:
            user_topic: 用户输入的搜索主题

        Returns:
            优化后的搜索词列表
        """
        prompt = f"""用户想要搜索关于「{user_topic}」的学术文献。

请根据PubMed医学文献数据库的检索规则，生成5-10个优化的检索词。

要求：
1. 包含主题词(MeSH Terms)和自由词
2. 包含同义词和常见变体
3. 使用布尔运算符(AND/OR)组织
4. 考虑不同的拼写方式(如color vs colour)
5. 输出格式：每行一个检索词，不要编号

例如，如果用户输入"食管癌免疫治疗"，输出可能是：
esophageal cancer immunotherapy
esophageal carcinoma immunotherapy
esophagus cancer AND immune therapy
ESCC AND immune checkpoint
食管癌 AND 免疫治疗
等等

请输出优化后的检索词列表："""

        for attempt in range(config.MAX_RETRIES):
            try:
                response = self._call_api(prompt)
                if response:
                    # 解析返回的检索词
                    terms = []
                    for line in response.strip().split('\n'):
                        line = line.strip()
                        # 过滤掉空行和编号
                        if line and not line.startswith(('#', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.')):
                            terms.append(line)
                    return terms[:10]  # 最多返回10个

            except Exception as e:
                safe_print(f"优化检索词错误 (attempt {attempt + 1}/{config.MAX_RETRIES}): {e}")
                time.sleep(2 ** attempt)

        # 如果失败，返回原始主题作为搜索词
        return [user_topic]

    def polish_search_topic(self, user_topic: str) -> str:
        """
        使用AI润色搜索主题，生成更适合学术综述的表述

        Args:
            user_topic: 用户输入的原始搜索主题

        Returns:
            润色后的搜索主题
        """
        prompt = f"""请将以下搜索主题润色为更适合生成学术文献综述的表述。

原始主题: {user_topic}

要求：
1. 使用更学术化的表达方式
2. 包含关键词的中英文对照（如适用）
3. 保持主题的核心研究领域不变
4. 输出格式：直接输出润色后的主题，不要添加解释或其他内容
5. 长度控制在20-50字之间

例如：
- 原始: 食管癌免疫治疗
- 润色: 食管癌免疫治疗研究进展（Esophageal Cancer Immunotherapy）

请润色以下主题："""

        for attempt in range(config.MAX_RETRIES):
            try:
                response = self._call_api(prompt, timeout=60, max_tokens=500)
                if response:
                    # 清理返回的内容
                    polished = response.strip()
                    # 移除可能的引号
                    polished = polished.strip('"\'「」')
                    return polished

            except Exception as e:
                safe_print(f"润色主题错误 (尝试 {attempt + 1}/{config.MAX_RETRIES}): {e}")
                time.sleep(2 ** attempt)

        # 如果失败，返回原始主题
        return user_topic

    def _summarize_single_article(self, article: Dict) -> Dict:
        """
        总结单篇文章（线程安全）

        Args:
            article: 文章字典

        Returns:
            添加了summary的文章字典
        """
        title = article.get('title', '')[:50]
        summary = self.summarize_article(
            title=article.get("title", ""),
            abstract=article.get("abstract", ""),
            pmid=article.get("pmid", "")
        )
        article["summary"] = summary
        return article

    def summarize_articles(self, articles: List[Dict], max_workers: int = None) -> List[Dict]:
        """
        批量总结文章（多线程并发）

        Args:
            articles: 文章列表
            max_workers: 最大并发线程数

        Returns:
            添加了总结的文章列表
        """
        max_workers = max_workers or config.MAX_WORKERS
        total = len(articles)
        safe_print(f"\nSummarizing {total} articles with {max_workers} threads...")

        # 使用ThreadPoolExecutor进行并发总结
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任务
            future_to_article = {
                executor.submit(self._summarize_single_article, article): article
                for article in articles
            }

            # 收集结果
            completed = 0
            for future in as_completed(future_to_article):
                completed += 1
                try:
                    future.result()
                except Exception as e:
                    safe_print(f"Error summarizing article: {e}")

                # 显示进度
                title = future_to_article[future].get('title', '')[:30]
                safe_print(f"[{completed}/{total}] {title}...")

        safe_print(f"Completed summarization of {total} articles")
        return articles

    def generate_overall_summary(self, articles: List[Dict]) -> str:
        """
        生成整体总结报告

        Args:
            articles: 文章列表

        Returns:
            整体总结文本
        """
        if not articles:
            return "没有找到符合条件的文章"

        # 统计信息
        total = len(articles)
        publishers = {}
        journals = {}

        for article in articles:
            publisher = article.get("publisher", "Unknown")
            journal = article.get("journal", "Unknown")

            publishers[publisher] = publishers.get(publisher, 0) + 1
            journals[journal] = journals.get(journal, 0) + 1

        # 构建总结
        summary = f"""# 食管癌文献总结报告

## 概述
本报告汇总了最近半年内（{config.SEARCH_START_DATE}至今）发表在Nature、Cell、Science系列期刊上的食管癌相关研究文献。

## 统计信息
- **总文章数**: {total} 篇
- **出版社分布**:
"""

        for publisher, count in sorted(publishers.items(), key=lambda x: x[1], reverse=True):
            summary += f"  - {publisher}: {count} 篇\n"

        summary += "\n## 期刊分布\n"
        for journal, count in sorted(journals.items(), key=lambda x: x[1], reverse=True)[:15]:
            summary += f"- {journal}: {count} 篇\n"

        return summary

    def generate_literature_review(self, articles: List[Dict], search_topic: str, start_date: str, end_date: str) -> str:
        """
        生成带引用的文献综述

        Args:
            articles: 文章列表
            search_topic: 搜索主题
            start_date: 搜索开始日期
            end_date: 搜索结束日期

        Returns:
            文献综述文本
        """
        if not articles:
            return "没有找到符合条件的文章来生成文献综述。"

        safe_print("\n正在生成文献综述...")

        # 准备文章信息用于生成综述（优化：减少摘要长度）
        articles_info = []
        for i, article in enumerate(articles):
            # 只取摘要前200字符，避免prompt过长
            abstract = article.get('abstract', '')[:200]
            summary = article.get('summary', '')

            info = f"""文献 {i+1}:
- 标题: {article.get('title', '')}
- 作者: {article.get('authors', '')}
- 期刊: {article.get('journal', '')}
- 发表日期: {article.get('pub_date', '')}
- DOI: {article.get('doi', '')}
- 摘要: {abstract}"""
            articles_info.append(info)

        articles_text = "\n---\n".join(articles_info)

        prompt = f"""请基于以下{len(articles)}篇关于「{search_topic}」的学术论文，生成一篇结构化的文献综述。

## 搜索条件
- 主题: {search_topic}
- 时间范围: {start_date} 至 {end_date}

## 文章列表
{articles_text}

## 综述要求
提示词：
我正在撰写一篇关于{search_topic}的文献综述，准备投稿给SCI期刊。
基于我给你的相关文献材料，如果必要可以用你的知识库进行补充
我的背景： 我是一名生物医学领域的研究生/科研人员，需要一篇逻辑严密、引用规范的综述草稿。
请根据以下大纲和要求进行写作：
1.	结构要求： 请包含摘要、引言、主体部分（分3-4个小标题）、讨论与展望、参考文献。
2.	核心观点： 主体部分需要重点讨论相关观点，聚焦于相关的参考文献材料凝聚成核心论点。
3.	语言风格： 请模仿《Nature Reviews Cancer》综述文章的语言风格和段落长度，语言要高度精炼，使用正式、客观的学术语言，句子结构保持简洁清晰，避免过度冗长。
4.	文献引用： 请用规范格式标注参考文献，第一次在正文出现相关引用文献时，请按照正规文献格式做好标注

请用中文撰写，确保专业性和学术性。"""

        # 优化：增加超时时间和token数量
        review_timeout = 120  # 120秒超时
        review_max_tokens = 2000  # 文献综述需要更多token

        for attempt in range(config.MAX_RETRIES):
            try:
                safe_print(f"正在生成文献综述 (尝试 {attempt + 1}/{config.MAX_RETRIES})...")
                response = self._call_api(prompt, timeout=review_timeout, max_tokens=review_max_tokens)
                if response:
                    safe_print("文献综述生成完成")
                    return response

            except Exception as e:
                safe_print(f"生成文献综述错误 (尝试 {attempt + 1}/{config.MAX_RETRIES}): {e}")
                # 指数退避等待
                wait_time = min(2 ** attempt * 2, 30)  # 最多等待30秒
                safe_print(f"等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)

        # 如果失败，返回基本信息
        return f"""# {search_topic} 文献综述

## 概述
本综述涵盖了在{start_date}至{end_date}期间发表的{len(articles)}篇关于{search_topic}的学术论文。

## 统计信息
- 总文章数: {len(articles)} 篇

## 期刊分布
"""



def test_api():
    """测试API连接"""
    summarizer = ArticleSummarizer()

    test_abstract = """
    Esophageal cancer is a malignancy with poor prognosis. We performed whole-exome sequencing
    of 149 esophageal squamous cell carcinomas (ESCCs) and identified 8 significantly mutated genes.
    TP53 was the most frequently mutated gene (91% of cases). We also found novel mutations in
    NOTCH1, NOTCH2, and NOTCH3. Functional studies showed that NOTCH1 acts as a tumor suppressor
    in ESCC. Our findings provide new insights into the molecular pathogenesis of esophageal cancer.
    """

    summary = summarizer.summarize_article(
        title="Exome sequencing of esophageal squamous cell carcinoma reveals novel driver mutations",
        abstract=test_abstract,
        pmid="12345678"
    )

    safe_print("测试总结结果:")
    safe_print("-" * 50)
    safe_print(summary)


if __name__ == "__main__":
    test_api()