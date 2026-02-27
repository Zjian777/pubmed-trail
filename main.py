"""
PubMed食管癌文献爬取与AI总结 - 主程序
"""

import os
import sys
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter

import config
from pubmed_crawler import PubMedCrawler
from journal_filter import JournalFilter
from summarizer import ArticleSummarizer


def create_output_dir():
    """创建输出目录"""
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)


def save_markdown_report(articles: list, output_path: str, overall_summary: str = ""):
    """
    保存Markdown报告

    Args:
        articles: 文章列表
        output_path: 输出文件路径
        overall_summary: 整体总结
    """
    with open(output_path, "w", encoding="utf-8") as f:
        # 写入整体总结
        if overall_summary:
            f.write(overall_summary)
            f.write("\n\n")

        # 写入每篇文章的详细信息
        f.write("---\n\n")

        for i, article in enumerate(articles, 1):
            f.write(f"## 文章 {i}: {article.get('title', '无标题')}\n\n")

            f.write(f"**PMID**: {article.get('pmid', 'N/A')}\n\n")
            f.write(f"**期刊**: {article.get('journal', 'N/A')}\n\n")
            f.write(f"**出版社**: {article.get('publisher', 'N/A')}\n\n")
            f.write(f"**发表日期**: {article.get('pub_date', 'N/A')}\n\n")
            f.write(f"**DOI**: {article.get('doi', 'N/A')}\n\n")

            authors = article.get('authors', '')
            if authors:
                f.write(f"**作者**: {authors}\n\n")

            # 摘要
            abstract = article.get('abstract', '')
            if abstract:
                f.write("**摘要**:\n\n")
                f.write(f"{abstract}\n\n")

            # 总结
            summary = article.get('summary', '')
            if summary and summary != "无摘要":
                f.write("**AI总结**:\n\n")
                f.write(f"{summary}\n\n")

            f.write("---\n\n")

        # 写入时间戳
        f.write(f"\n*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")

    print(f"Markdown报告已保存到: {output_path}")


def save_excel(articles: list, output_path: str):
    """
    保存Excel文件

    Args:
        articles: 文章列表
        output_path: 输出文件路径
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "食管癌文献"

    # 定义表头
    headers = ["序号", "PMID", "标题", "期刊", "出版社", "发表日期", "DOI", "作者", "摘要", "AI总结"]

    # 样式
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    # 写入表头
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment

    # 写入数据
    for row, article in enumerate(articles, 2):
        ws.cell(row=row, column=1, value=row-1)  # 序号
        ws.cell(row=row, column=2, value=article.get("pmid", ""))
        ws.cell(row=row, column=3, value=article.get("title", ""))
        ws.cell(row=row, column=4, value=article.get("journal", ""))
        ws.cell(row=row, column=5, value=article.get("publisher", ""))
        ws.cell(row=row, column=6, value=article.get("pub_date", ""))
        ws.cell(row=row, column=7, value=article.get("doi", ""))
        ws.cell(row=row, column=8, value=article.get("authors", ""))
        ws.cell(row=row, column=9, value=article.get("abstract", ""))
        ws.cell(row=row, column=10, value=article.get("summary", ""))

    # 调整列宽
    column_widths = {
        1: 6,   # 序号
        2: 12,  # PMID
        3: 60,  # 标题
        4: 30,  # 期刊
        5: 10,  # 出版社
        6: 12,  # 发表日期
        7: 25,  # DOI
        8: 40,  # 作者
        9: 80,  # 摘要
        10: 100 # AI总结
    }

    for col, width in column_widths.items():
        ws.column_dimensions[get_column_letter(col)].width = width

    # 冻结首行
    ws.freeze_panes = "A2"

    # 保存
    wb.save(output_path)
    print(f"Excel文件已保存到: {output_path}")


def main():
    """主函数"""
    print("=" * 60)
    print("PubMed食管癌文献爬取与AI总结")
    print("=" * 60)

    # 创建输出目录
    create_output_dir()

    # 步骤1: 从PubMed爬取文章
    print("\n[步骤1] 从PubMed搜索食管癌相关文章...")
    crawler = PubMedCrawler()
    all_articles = crawler.get_articles()

    if not all_articles:
        print("未找到相关文章，程序退出")
        return

    # 步骤2: 筛选目标期刊
    print("\n[步骤2] 筛选Nature、Cell、Science系列期刊...")
    journal_filter = JournalFilter()
    filtered_articles = journal_filter.filter_articles(all_articles)

    if not filtered_articles:
        print("筛选后没有符合条件的文章，程序退出")
        return

    # 步骤3: 使用Deepseek API进行总结
    print("\n[步骤3] 使用Deepseek API总结文章...")
    summarizer = ArticleSummarizer()

    # 生成整体统计
    overall_summary = summarizer.generate_overall_summary(filtered_articles)

    # 批量总结每篇文章
    summarized_articles = summarizer.summarize_articles(filtered_articles)

    # 步骤4: 保存输出文件
    print("\n[步骤4] 保存输出文件...")

    # 保存Markdown报告
    report_path = os.path.join(config.OUTPUT_DIR, config.REPORT_FILE)
    save_markdown_report(summarized_articles, report_path, overall_summary)

    # 保存Excel文件
    excel_path = os.path.join(config.OUTPUT_DIR, config.EXCEL_FILE)
    save_excel(summarized_articles, excel_path)

    print("\n" + "=" * 60)
    print("完成!")
    print(f"找到 {len(summarized_articles)} 篇符合条件的文章")
    print(f"报告文件: {report_path}")
    print(f"数据文件: {excel_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()