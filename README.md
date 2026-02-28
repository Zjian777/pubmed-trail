# PubMed文献搜索与AI总结系统 

基于PubMed数据库的学术文献智能分析系统，集成DeepSeek AI大模型，支持文献检索、AI智能总结和文献综述生成。

## 快速开始

### 1. 安装依赖

```bash
cd web
pip install flask flask-cors biopython openpyxl requests
pip install -r requirements.txt
```

### 2. 配置

编辑 `config.py` 文件：

```python
# DeepSeek API配置 (如果使用命令行程序运行必填，web端在网页中填写即可)
DEEPSEEK_API_KEY = "your-deepseek-api-key"
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = "deepseek-chat"

# PubMed配置
PUBMED_EMAIL = "your-email@example.com"
PUBMED_API_KEY = ""  # 可选，有API Key可提高访问速度
```

### 3. 启动服务

```bash
cd web
python app.py
```

服务启动后访问 http://localhost:5000

## 项目结构

```
claude_test/
├── web/
│   ├── app.py              # Flask后端服务 (核心)
│   ├── static/
│   │   ├── index.html      # Vue3前端页面
│   │   └── js/             # 前端依赖库(本地)
│   └── output/             # 生成的文件存储目录
├── config.py               # 配置文件
├── pubmed_crawler.py       # PubMed爬虫模块
├── journal_filter.py       # 期刊筛选模块
├── summarizer.py           # AI总结模块
└── main.py                 # 命令行入口(可选)
```

## 使用说明

### 前端界面功能

1. **API设置**：在界面输入DeepSeek API密钥
2. **搜索主题**：输入要搜索的研究主题
3. **时间范围**：设置搜索的起止日期
4. **最大篇数**：设置要搜索的文献数量
5. **并发线程数**：设置AI总结的并发数
6. **期刊筛选**（可选）：
   - 启用筛选开关
   - 选择要筛选的期刊或出版社
   - 可添加自定义期刊
7. **开始搜索**：点击按钮开始搜索和AI总结
8. **暂停/继续**：搜索过程中可暂停和恢复任务

### 功能特点

- **实时显示**：搜索过程中实时显示已完成的论文总结
- **Markdown渲染**：文献综述支持Markdown格式渲染
- **多种导出**：支持下载Markdown报告和Excel表格
- **本地化部署**：前端库已下载到本地，无需外网访问


## 注意事项

1. **API密钥**：使用前需自备DeepSeek API密钥
2. **网络环境**：确保可以正常访问PubMed和DeepSeek API
3. **PubMed API**：建议申请API Key以提高访问速度

## 常见问题

**Q: 前端无法加载？**

A: 检查 `web/static/js/` 目录下的库文件是否完整，路径是否正确

**Q: PubMed搜索失败？**

A: 检查网络连接，本项目使用的是E-utilities，需要自行检测是否能够顺利连接E-utilities API

B: 测试访问https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=cancer&retmax=1&retmode=json如果内容输出，则代表连接正常

**Q: AI总结失败？**

A: 检查DeepSeek API密钥是否正确，网络是否正常

---

MIT License