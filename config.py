"""
配置文件 - PubMed食管癌文献爬取与AI总结
请在此文件中配置您的API密钥和设置
"""

# Deepseek API配置
DEEPSEEK_API_KEY = ""  # 替换为您的Deepseek API Key
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = "deepseek-chat"

# PubMed配置
PUBMED_EMAIL = "your-email@example.com"  # 用于PubMed API联系
PUBMED_API_KEY = ""  # 可选：如果有PubMed API Key请填写

# 搜索配置
SEARCH_TERMS = [
    "esophageal cancer",
    "esophageal carcinoma",
    "esophagus cancer"
]
SEARCH_START_DATE = "2025/09/01"  # 开始日期 (YYYY/MM/DD)
SEARCH_END_DATE = ""  # 结束日期 (YYYY/MM/DD)，留空则为当前日期
MAX_SEARCH_RESULTS = 100  # 最大搜索篇数
MAX_WORKERS = 5  # 并发总结的线程数

# 三大杂志社期刊列表
JOURNALS = {
    "Nature": [
        "Nature",
        "Nature Medicine",
        "Nature Cancer",
        "Nature Communications",
        "Nature Genetics",
        "Nature Reviews Cancer",
        "Nature Reviews Clinical Oncology",
        "Nature Reviews Gastroenterology & Hepatology",
        "Nature Biotechnology",
        "Nature Cell Biology",
        "Nature Immunology",
        "Nature Reviews Disease Primers",
        "Nature Reviews Drug Discovery",
        "Nature Reviews Gastroenterology",
        "Nature Reviews Molecular Cell Biology",
        "Nature Reviews Immunology",
        "Nature Structural & Molecular Biology",
        "Nature Reviews Endocrinology",
        "Nature Reviews Urology",
        "Nature Reviews Neuro科学",
        "Nature Cardiovascular Research",
        "Nature Aging",
        "Nature Metabolism",
        "Nature Food",
        "Nature Immunology",
        "Nature Communications",
        "Scientific Reports",
        "npj Precision Oncology",
        "npj Cancer Research",
        "Cell Death & Differentiation",
        "Oncogene",
        "British Journal of Cancer",
        "Gene Therapy",
        "Cancer Gene Therapy",
        "International Journal of Cancer",
        "European Journal of Cancer",
        "Cancer Letters",
        "Carcinogenesis",
        "Molecular Cancer",
        "Molecular Cancer Therapeutics",
        "Molecular Cancer Research",
        "Cancer Biology & Therapy",
        "Cancer Immunology Research",
        "Cancer Research",
        "Clinical Cancer Research",
        "Journal of Clinical Oncology",
        "JAMA Oncology",
        "Annals of Oncology",
        "Gut",
        "Journal of the National Cancer Institute",
    ],
    "Cell": [
        "Cell",
        "Cancer Cell",
        "Cell Stem Cell",
        "Cell Reports",
        "Cell Host & Microbe",
        "Cell Metabolism",
        "Cell Death & Disease",
        "Cell Research",
        "Cellular & Molecular Gastroenterology and Hepatology",
        "Cell Reports Medicine",
        "Cell Reports Methods",
        "Cell Systems",
        "Cell Stem Cell Reports",
        "Molecular Cell",
        "Developmental Cell",
        "Immunity",
        "Neuron",
        "Gene & Development",
        "Plant Cell",
        "Current Biology",
        "Journal of Cell Biology",
        "Journal of Cell Science",
        "Cell Calcium",
        "Cell Cycle",
        "Cell Cycle",
        "Cellular and Molecular Life Sciences",
        "Cellular & Molecular Gastroenterology and Hepatology",
    ],
    "Science": [
        "Science",
        "Science Translational Medicine",
        "Science Advances",
        "Science Signaling",
        "Science Robotics",
        "Science Immunology",
        "Science Medicine",
        "Science Reports",
        "Science China Life Sciences",
        "Cell",
        "New England Journal of Medicine",
        "Lancet",
        "Lancet Oncology",
        "Lancet Gastroenterology & Hepatology",
        "JAMA",
        "JAMA Oncology",
        "Nature Medicine",
        "Gut",
        "Journal of Clinical Oncology",
    ]
}

# 输出配置
OUTPUT_DIR = "output"
REPORT_FILE = "report.md"
EXCEL_FILE = "articles.xlsx"
REVIEW_FILE = "literature_review.md"  # 文献综述单独文件

# 请求配置
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
DELAY_BETWEEN_REQUESTS = 1  # 秒