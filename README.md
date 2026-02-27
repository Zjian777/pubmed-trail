# PubMed 文献搜索与 AI 总结工具

基于 PubMed 数据库的学术文献智能分析系统，支持 CLI 命令行和 Web 界面两种使用方式。集成 Deepseek AI 大模型，可自动优化检索策略、筛选高影响力期刊、并发总结文献，并生成符合 SCI 标准的文献综述。

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![API](https://img.shields.io/badge/API-Deepseek-purple.svg)

## 功能亮点

- **AI 智能检索优化**：自动将用户输入转换为包含 MeSH 主题词、同义词的专业检索策略
- **权威期刊筛选**：精准筛选 Nature、Cell、Science 三大顶级出版社系列期刊
- **高并发处理**：多线程并发调用 AI API，大幅提升文献总结效率
- **文献综述生成**：自动生成结构化学术综述，包含引言、讨论、参考文献等完整章节
- **双模式支持**：同时提供 CLI 命令行工具和现代化 Web 界面

---

## 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户界面层                                │
│  ┌─────────────────────────┐  ┌─────────────────────────────┐  │
│  │      CLI 命令行模式       │  │       Web 界面 (Vue3)        │  │
│  │      (main.py)          │  │    (web/app.py + Flask)     │  │
│  └───────────┬─────────────┘  └──────────────┬──────────────┘  │
└──────────────┼────────────────────────────────┼────────────────┘
               │                                │
               └────────────┬───────────────────┘
                            │
┌───────────────────────────▼───────────────────────────────────┐
│                        核心服务层                              │
│  ┌────────────────┐ ┌────────────────┐ ┌──────────────────┐  │
│  │ PubMed 爬虫     │ │  期刊过滤器     │ │   AI 总结引擎     │  │
│  │ (pubmed_crawler│ │ (journal_filter│ │  (summarizer.py) │  │
│  │     .py)       │ │      .py)      │ │                  │  │
│  └────────┬───────┘ └────────┬───────┘ └─────────┬────────┘  │
└───────────┼──────────────────┼───────────────────┼───────────┘
            │                  │                   │
┌───────────▼──────────────────▼───────────────────▼───────────┐
│                        配置与外部服务                          │
│  ┌────────────────┐ ┌────────────────┐ ┌──────────────────┐  │
│  │   config.py    │ │  PubMed API    │ │  Deepseek API    │  │
│  │   (集中配置)    │ │  (Biopython)   │ │  (HTTP/REST)     │  │
│  └────────────────┘ └────────────────┘ └──────────────────┘  │
└───────────────────────────────────────────────────────────────┘
```

---

## 项目结构

```
.
├── main.py                     # CLI 主程序入口
├── config.py                   # 全局配置文件（API Keys、搜索参数等）
├── pubmed_crawler.py           # PubMed 文献爬取模块
├── journal_filter.py           # 期刊筛选与分类模块
├── summarizer.py               # AI 总结与综述生成模块
├── web/                        # Web 应用目录
│   ├── app.py                  # Flask 后端服务
│   ├── requirements.txt        # Web 服务依赖
│   ├── static/
│   │   └── index.html          # Vue3 前端页面
│   └── output/                 # Web 端输出目录
├── output/                     # CLI 端输出目录
│   ├── report.md               # 详细文献报告
│   ├── literature_review.md    # 文献综述
│   └── articles.xlsx           # Excel 数据表
└── README.md
```

---

## 安装指南

### 环境要求

- Python 3.8+
- 有效的 Deepseek API Key

### 安装依赖

```bash
# 基础依赖（CLI 模式）
pip install biopython requests openpyxl

# Web 模式额外需要
pip install flask flask-cors
```

### 配置 API Key

编辑 `config.py` 文件：

```python
# Deepseek API 配置（必填）
DEEPSEEK_API_KEY = "your-api-key-here"
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = "deepseek-chat"

# PubMed 配置（建议填写真实邮箱）
PUBMED_EMAIL = "your-email@example.com"
PUBMED_API_KEY = ""  # 可选

# 搜索参数
MAX_SEARCH_RESULTS = 100  # 最大搜索篇数
MAX_WORKERS = 5           # 并发线程数
```

获取 Deepseek API Key: [https://platform.deepseek.com/](https://platform.deepseek.com/)

---

## 使用方法

### CLI 命令行模式

```bash
# 基本用法
python main.py -t "esophageal cancer immunotherapy"

# 完整参数示例
python main.py -t "esophageal cancer" \
    -s 2024/01/01 \
    -e 2025/12/31 \
    -m 50 \
    -w 10

# 交互式模式
python main.py --interactive
```

**参数说明：**

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-t, --topic` | 搜索主题（必填） | - |
| `-s, --start-date` | 开始日期 (YYYY/MM/DD) | 2025/09/01 |
| `-e, --end-date` | 结束日期 (YYYY/MM/DD) | 当前日期 |
| `-m, --max-results` | 最大搜索篇数 | 100 |
| `-w, --workers` | 并发线程数 | 5 |
| `--interactive` | 启用交互式模式 | - |

### Web 界面模式

```bash
# 启动 Web 服务
cd web
pip install -r requirements.txt
python app.py
```

访问：http://localhost:5000

Web 界面提供：
- 可视化搜索配置
- 实时进度显示
- 在线查看文献综述
- 一键下载 Excel/Markdown 文件

---

## 工作流程

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ 1. 用户输入  │ ──► │ 2. AI 优化   │ ──► │ 3. PubMed   │
│   搜索主题   │     │   检索词     │     │   文献搜索   │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
                                              ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ 7. 保存输出 │ ◄── │ 6. 生成     │ ◄── │ 5. 多线程   │
│   文件      │     │   文献综述   │     │   AI 总结    │
└─────────────┘     └─────────────┘     └─────────────┘
```

### 详细步骤说明

1. **AI 优化检索词**：将用户输入转换为专业的 PubMed 检索策略
2. **PubMed 搜索**：使用 Biopython 的 Entrez 模块检索文献
3. **期刊筛选**：按照 Nature/Cell/Science 三大出版社标准过滤
4. **AI 总结**：多线程并发调用 Deepseek API 总结每篇文献
5. **综述生成**：AI 生成结构化文献综述（Nature Reviews 风格）
6. **文件输出**：生成 Markdown 报告、Excel 表格、文献综述

---

## 输出文件说明

运行完成后在 `output/` 目录生成以下文件：

| 文件 | 格式 | 内容说明 |
|------|------|----------|
| `report.md` | Markdown | 每篇文献的详细信息（PMID、作者、摘要、AI 总结） |
| `literature_review.md` | Markdown | 结构化文献综述（含引言、讨论、参考文献） |
| `articles.xlsx` | Excel | 结构化数据表，支持筛选和进一步分析 |

### 输出示例

**AI 总结示例：**
```markdown
## 文章 1: Pembrolizumab plus Chemotherapy in Advanced Esophageal Cancer

**PMID**: 38123456
**期刊**: Journal of Clinical Oncology
**出版社**: Science
**发表日期**: 2024-11
**DOI**: 10.1200/JCO.2024.123456

**AI 总结**:
1. 研究类型：III 期随机对照临床试验
2. 主要发现：帕博利珠单抗联合化疗显著改善晚期食管癌患者总生存期
3. 研究方法：多中心、双盲、安慰剂对照 III 期试验 (n=736)
4. 临床意义：支持免疫联合治疗作为晚期食管癌一线标准治疗
```

**文献综述结构：**
```markdown
# 食管癌免疫治疗研究进展 (Esophageal Cancer Immunotherapy)

## 摘要
...

## 1. 引言
...

## 2. 研究现状
  2.1 免疫检查点抑制剂单药治疗
  2.2 免疫联合化疗
  2.3 新辅助免疫治疗
  2.4 生物标志物研究

## 3. 讨论与展望
...

## 参考文献
[1] Author et al. Journal Name, 2024. DOI: ...
```

---

## 可配置期刊列表

在 `config.py` 中可自定义目标期刊，默认涵盖三大出版社：

- **Nature 系列**：Nature, Nature Medicine, Nature Cancer, Nature Communications 等 50+ 期刊
- **Cell 系列**：Cell, Cancer Cell, Cell Stem Cell, Cell Reports 等 25+ 期刊
- **Science 系列**：Science, Science Translational Medicine, Science Advances 等 10+ 期刊

---

## 技术细节

### 并发处理

```python
# 使用 ThreadPoolExecutor 实现并发总结
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = {
        executor.submit(summarize_article, article): article
        for article in articles
    }
    for future in as_completed(futures):
        # 处理结果
```

### API 调用优化

- 指数退避重试机制
- 请求超时控制
- 会话复用（requests.Session）

### 检索词优化

AI 生成的检索词包含：
- MeSH 主题词
- 自由词/关键词
- 同义词和变体
- 布尔运算符组合

---

## 常见问题

**Q: API 调用失败怎么办？**

A: 检查网络连接和 API Key 配置，程序内置了自动重试机制（最多 3 次）。

**Q: 如何修改目标期刊列表？**

A: 编辑 `config.py` 中的 `JOURNALS` 字典。

**Q: 文献综述生成时间过长？**

A: 可增加 `MAX_WORKERS` 提高并发数，或减少 `MAX_SEARCH_RESULTS`。

**Q: 支持其他研究领域吗？**

A: 支持。修改搜索主题即可，程序会自动适配医学领域检索。

---

## 许可证

MIT License

---

## 致谢

- PubMed/MEDLINE 数据库
- Deepseek AI API
- Biopython 项目
