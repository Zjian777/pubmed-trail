# PubMed文献搜索与AI总结工具

基于PubMed数据库的学术文献爬取与AI智能分析工具，可自动搜索文献、筛选高影响力期刊、AI优化检索词、多线程总结文章，并生成结构化的文献综述。

## 功能特性

### 1. 自定义搜索
- 用户输入搜索主题，AI自动优化为更精确的检索词
- 可配置搜索日期范围和最大篇数
- 支持命令行参数和交互式两种模式

### 2. 智能检索词优化
- 调用AI分析用户输入的主题
- 生成包含MeSH主题词、同义词、布尔运算符的优化检索策略

### 3. 高影响力期刊筛选
- 自动筛选Nature、Cell、Science系列期刊
- 支持自定义期刊列表

### 4. 多线程AI总结
- 使用ThreadPoolExecutor并发调用Deepseek API
- 并发数量可配置，大幅提升总结效率

### 5. AI文献综述生成
- 自动润色搜索主题（添加英文对照）
- 生成SCI级别的结构化文献综述
- 包含：摘要、引言、主体讨论、参考文献

## 安装依赖

```bash
pip install biopython requests openpyxl
```

## 配置说明

编辑 `config.py` 文件：

```python
# Deepseek API配置（必填）
DEEPSEEK_API_KEY = "your-api-key"  # 替换为您的Deepseek API Key

# PubMed配置（建议填写真实邮箱）
PUBMED_EMAIL = "your-email@example.com"
PUBMED_API_KEY = ""  # 可选：有PubMed API Key请填写

# 搜索配置
MAX_SEARCH_RESULTS = 100  # 最大搜索篇数
MAX_WORKERS = 5  # 并发线程数
```

获取Deepseek API Key: https://platform.deepseek.com/

## 使用方法

### 命令行模式（推荐）

```bash
# 基本用法
python main.py -t "食管癌免疫治疗"

# 完整参数
python main.py -t "食管癌免疫治疗" -s 2024/01/01 -e 2025/12/31 -m 30 -w 5
```

参数说明：
- `-t, --topic`: 搜索主题（必填）
- `-s, --start-date`: 开始日期 (YYYY/MM/DD)
- `-e, --end-date`: 结束日期 (YYYY/MM/DD)
- `-m, --max-results`: 最大搜索篇数
- `-w, --workers`: 并发总结线程数

### 交互式模式

```bash
python main.py --interactive
```

按提示输入搜索主题、日期范围等参数。

## 输出文件

程序运行后在 `output/` 目录下生成：

| 文件 | 说明 |
|------|------|
| `report.md` | 文章详细信息和AI总结 |
| `literature_review.md` | **文献综述（单独文件）** |
| `articles.xlsx` | Excel格式数据 |

## 项目结构

```
.
├── main.py              # 主程序入口
├── config.py            # 配置文件
├── pubmed_crawler.py    # PubMed爬虫模块
├── summarizer.py        # AI总结模块
├── journal_filter.py    # 期刊筛选模块
├── output/              # 输出目录
│   ├── report.md
│   ├── literature_review.md
│   └── articles.xlsx
└── README.md
```

## 工作流程

```
用户输入主题 → AI优化检索词 → PubMed搜索 → 期刊筛选 →
多线程AI总结 → AI润色主题 → 生成文献综述 → 保存文件
```

## 注意事项

1. 需要有效的Deepseek API Key
2. 确保网络可以访问PubMed和Deepseek API
3. 建议合理设置搜索篇数，避免API调用过于频繁
4. 文献综述生成时间较长，请耐心等待

## 示例输出

### AI优化检索词
```
优化后的检索词:
  1. esophageal neoplasms AND immunotherapy
  2. esophageal cancer AND immune checkpoint inhibitors
  3. esophageal carcinoma OR ESCC AND PD-1 OR PD-L1
  ...
```

### 生成的文献综述结构
```
## 食管癌免疫治疗研究进展

### 1. 研究概述
...

### 2. 主要研究进展
  2.1 围手术期免疫联合治疗
  2.2 肿瘤微环境研究
  ...

### 3. 研究方法分析
...

### 4. 临床意义和展望
...

### 5. 参考文献
[APA格式引用]
```

## 许可证

MIT License