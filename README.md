# PubMed 食管癌文献爬取与 AI 总结

一个从 PubMed 自动检索食管癌相关文献，筛选 Nature、Cell、Science 系列期刊，并使用 Deepseek AI 进行智能总结的工具。

## 功能特点

- **文献检索**: 通过 PubMed API 自动搜索食管癌相关学术文献
- **期刊筛选**: 智能筛选 Nature、Cell、Science 三大出版社旗下的顶级期刊
- **AI 总结**: 使用 Deepseek API 对每篇文献进行结构化总结
- **多格式输出**: 生成 Markdown 报告和 Excel 数据表格

## 项目结构

```
pubmed-trail/
├── main.py              # 主程序入口
├── config.py            # 配置文件（API 密钥、搜索参数等）
├── pubmed_crawler.py    # PubMed 爬取模块
├── journal_filter.py    # 期刊筛选模块
├── summarizer.py        # AI 总结模块
├── output/              # 输出目录（自动生成）
│   ├── report.md        # Markdown 报告
│   └── articles.xlsx    # Excel 数据文件
└── README.md            # 说明文档
```

## 安装依赖

```bash
pip install biopython openpython requests
```

## 配置

在运行前，需要编辑 `config.py` 文件配置以下参数：

### 必填配置

```python
# Deepseek API 密钥
DEEPSEEK_API_KEY = "your-api-key-here"

# PubMed 联系邮箱
PUBMED_EMAIL = "your-email@example.com"
```

### 可选配置

```python
# 搜索词（默认搜索食管癌相关术语）
SEARCH_TERMS = [
    "esophageal cancer",
    "esophageal carcinoma",
    "esophagus cancer"
]

# 搜索起始日期
SEARCH_START_DATE = "2025/09/01"

# 输出目录和文件名
OUTPUT_DIR = "output"
REPORT_FILE = "report.md"
EXCEL_FILE = "articles.xlsx"
```

## 运行程序

```bash
python main.py
```

## 运行流程

程序执行分为四个步骤：

1. **搜索文献**: 使用 PubMed API 搜索食管癌相关文章
2. **筛选期刊**: 从搜索结果中筛选 Nature、Cell、Science 系列期刊
3. **AI 总结**: 调用 Deepseek API 对每篇文章生成结构化总结
4. **保存输出**: 生成 Markdown 报告和 Excel 文件

## 输出文件

### Markdown 报告 (report.md)

包含：
- 整体统计信息（文章数量、出版社分布、期刊分布）
- 每篇文章的详细信息（PMID、标题、期刊、作者、摘要、AI 总结）

### Excel 文件 (articles.xlsx)

包含结构化的文献数据，列包括：
| 序号 | PMID | 标题 | 期刊 | 出版社 | 发表日期 | DOI | 作者 | 摘要 | AI 总结 |

## AI 总结格式

每篇文献的 AI 总结包含以下内容：
- **研究类型**: 基础研究、临床研究、综述、队列研究等
- **主要发现**: 核心发现的简要概括
- **研究方法**: 使用的实验或分析方法
- **临床意义**: 对食管癌诊疗的意义

## 目标期刊

程序筛选以下三大出版社的期刊：

- **Nature 系列**: Nature, Nature Medicine, Nature Cancer, Nature Communications 等
- **Cell 系列**: Cell, Cancer Cell, Cell Stem Cell, Cell Reports 等
- **Science 系列**: Science, Science Translational Medicine, Science Advances 等

完整期刊列表见 `config.py` 中的 `JOURNALS` 配置。

## 注意事项

1. **API 限制**: PubMed API 有请求频率限制，程序已内置延迟控制
2. **API 费用**: Deepseek API 为付费服务，请确保账户有足够余额
3. **编码问题**: 程序已处理 Unicode 编码，确保中文正常显示
4. **失败重试**: API 请求失败时会自动重试（最多 3 次）

## 依赖库

| 库名 | 用途 |
|------|------|
| biopython | PubMed API 调用 |
| openpyxl | Excel 文件生成 |
| requests | HTTP 请求（Deepseek API） |

## 许可证

MIT License
