"""
Deepseek API总结模块 - 对文章摘要进行AI总结
"""

import requests
import time
import sys
from typing import List, Dict, Optional
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

    def _call_api(self, prompt: str) -> Optional[str]:
        """
        调用Deepseek API

        Args:
            prompt: 提示词

        Returns:
            API响应文本
        """
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
            "max_tokens": 1000
        }

        response = self.session.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=config.REQUEST_TIMEOUT
        )

        if response.status_code == 200:
            result = response.json()
            return result.get("choices", [{}])[0].get("message", {}).get("content", "")
        else:
            safe_print(f"API error: {response.status_code} - {response.text}")
            return None

    def summarize_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        批量总结文章

        Args:
            articles: 文章列表

        Returns:
            添加了总结的文章列表
        """
        total = len(articles)
        safe_print(f"\nSummarizing {total} articles...")

        for i, article in enumerate(articles):
            title = article.get('title', '')[:50]
            safe_print(f"[{i+1}/{total}] {title}...")

            summary = self.summarize_article(
                title=article.get("title", ""),
                abstract=article.get("abstract", ""),
                pmid=article.get("pmid", "")
            )

            article["summary"] = summary

            # 避免请求过快
            if i < total - 1:
                time.sleep(config.DELAY_BETWEEN_REQUESTS)

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