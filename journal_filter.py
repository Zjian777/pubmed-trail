"""
期刊筛选模块 - 筛选Nature、Cell、Science杂志社的刊物
"""

import re
from typing import List, Dict
import config


class JournalFilter:
    def __init__(self):
        """初始化期刊过滤器"""
        self.journals = self._build_journal_dict()

    def _build_journal_dict(self) -> Dict[str, set]:
        """
        构建期刊字典，将期刊名称标准化并分类

        Returns:
            期刊字典，键为出版社名，值为期刊名集合
        """
        journal_dict = {}

        for publisher, journal_list in config.JOURNALS.items():
            normalized_journals = set()
            for journal in journal_list:
                # 标准化期刊名：转为小写，去除多余空格
                normalized = self._normalize_journal_name(journal)
                normalized_journals.add(normalized)
            journal_dict[publisher] = normalized_journals

        return journal_dict

    def _normalize_journal_name(self, name: str) -> str:
        """
        标准化期刊名称

        Args:
            name: 期刊原始名称

        Returns:
            标准化后的名称
        """
        # 转小写，去除首尾空格
        normalized = name.strip().lower()
        # 移除常见的后缀如 ".", "-", etc.
        normalized = re.sub(r'[.\-\s]+', ' ', normalized)
        return normalized.strip()

    def is_target_journal(self, journal_name: str) -> bool:
        """
        检查期刊是否为目标期刊（Nature、Cell、Science系列）

        Args:
            journal_name: 期刊名称

        Returns:
            是否为目标期刊
        """
        if not journal_name:
            return False

        normalized_input = self._normalize_journal_name(journal_name)

        for publisher, journals in self.journals.items():
            # 精确匹配
            if normalized_input in journals:
                return True

            # 部分匹配（例如 "Nature Medicine" 包含 "Nature"）
            for journal in journals:
                if normalized_input == journal or normalized_input in journal or journal in normalized_input:
                    return True

        return False

    def get_publisher(self, journal_name: str) -> str:
        """
        获取期刊所属的出版社

        Args:
            journal_name: 期刊名称

        Returns:
            出版社名称，如果不是目标期刊返回"Unknown"
        """
        if not journal_name:
            return "Unknown"

        normalized_input = self._normalize_journal_name(journal_name)

        for publisher, journals in self.journals.items():
            for journal in journals:
                if normalized_input == journal or normalized_input in journal or journal in normalized_input:
                    return publisher

        return "Unknown"

    def filter_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        筛选出目标期刊的文章

        Args:
            articles: 文章列表

        Returns:
            筛选后的文章列表
        """
        filtered = []

        for article in articles:
            journal = article.get("journal", "")
            if self.is_target_journal(journal):
                # 添加出版社信息
                article["publisher"] = self.get_publisher(journal)
                filtered.append(article)

        print(f"筛选前: {len(articles)} 篇")
        print(f"筛选后: {len(filtered)} 篇")

        # 统计各出版社文章数量
        publisher_counts = {}
        for article in filtered:
            publisher = article.get("publisher", "Unknown")
            publisher_counts[publisher] = publisher_counts.get(publisher, 0) + 1

        print(f"出版社分布: {publisher_counts}")

        return filtered

    def get_all_target_journals(self) -> List[str]:
        """
        获取所有目标期刊列表

        Returns:
            期刊名称列表
        """
        all_journals = []
        for publisher, journals in self.journals.items():
            all_journals.extend(list(journals))
        return sorted(all_journals)


def print_journal_list():
    """打印所有目标期刊"""
    filter = JournalFilter()
    journals = filter.get_all_target_journals()
    print("目标期刊列表:")
    print("-" * 50)
    for j in journals:
        print(f"  - {j}")
    print(f"\n总计: {len(journals)} 种期刊")


if __name__ == "__main__":
    # 测试
    filter = JournalFilter()

    test_journals = [
        "Nature",
        "Nature Medicine",
        "Cell",
        "Cancer Cell",
        "Science",
        "Science Translational Medicine",
        "JAMA",
        "Gut",
        "Lancet Oncology"
    ]

    print("期刊筛选测试:")
    print("-" * 50)
    for journal in test_journals:
        is_target = filter.is_target_journal(journal)
        publisher = filter.get_publisher(journal) if is_target else "N/A"
        print(f"{journal}: 是目标期刊={is_target}, 出版社={publisher}")