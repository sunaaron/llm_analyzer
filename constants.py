"""Constants used throughout the web scraping application."""

# Category constants
ZNJY_CATEGORY = 'znjy'
TZLC_CATEGORY = 'tzlc'

DEFAULT_PAGE_NUMBER = 1
DEFAULT_CATEGORY = 'general'

# MySQL Database Configuration
MYSQL_HOST = '192.168.86.55'
MYSQL_PORT = 3306
MYSQL_DATABASE = 'wxc_crawler'
MYSQL_USER = 'crawler_admin'
MYSQL_PASSWORD = '123'

# Table Configuration
WXC_POSTS_TABLE = 'wxc_posts'

# Crawler Configuration
MIN_PAGE_NUMBER = 1
MAX_PAGE_NUMBER = 10

# LLM Analysis Constants
LLM_IRRELEVANT_RESPONSE = 'irrelevant'
ZNJY_PROMPT = f"""这是一个来自文学城子女教育的论坛帖子。请首先判断这个帖子是否与教育, 留学, 升学, 育儿, 择校, 职业规划, 心理健康等相关，如果不是，请直接返回"{LLM_IRRELEVANT_RESPONSE}"。如果是，请务必用中文总结这篇论坛的帖子。根据原贴的题目和内容，以及回帖的内容，给出讨论的话题和结论。注意 1. 不要返回英文的总结. 2. 不用在回复中再解释为什么这篇帖子是相关的或者不相关的. """
TZLC_PROMPT = f"""这是一个来自文学城投资理财的论坛帖子。请首先判断这个帖子是否与金融, 投资, 房地产, 股市, 基金, 保险, 证券, 期货, 信托, 债券, 人民币, 外汇, 股票, 科技, 贵金属, 银行, 公司产品, 公司基本面，如果不是，请直接返回"{LLM_IRRELEVANT_RESPONSE}"。如果是，请务必用中文总结这篇论坛的帖子。根据原贴的题目和内容，以及回帖的内容，给出讨论的话题和结论。注意 1. 不要返回英文的总结. 2. 不用在回复中再解释为什么这篇帖子是相关的或者不相关的. """

# TTS Configuration
TTS_VOICE_NAMES = ['zh-CN-XiaoxiaoNeural', 'zh-CN-YunyangNeural']  # Example voice name for TTS
TTS_OUTPUT_DIR = '/Users/aaronsun/Dropbox/Audio/wxc/'  # Directory to save TTS audio files