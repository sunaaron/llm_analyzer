"""Constants used throughout the web scraping application."""

ZNJY_CATEGORY = 'znjy'

# Default page number
DEFAULT_PAGE_NUMBER = 1

# MySQL Database Configuration
MYSQL_HOST = '192.168.86.55'
MYSQL_PORT = 3306
MYSQL_DATABASE = 'wxc_crawler'
MYSQL_USER = 'crawler_admin'
MYSQL_PASSWORD = '123'

# Table Configuration
WXC_POSTS_TABLE = 'wxc_posts'

# Date Format
DATE_FORMAT_MMDDYYYY = '%m%d%Y'
DATE_FORMAT_MMDAYYYYY = '%m/%d/%Y'

# Crawler Configuration
MIN_PAGE_NUMBER = 1
MAX_PAGE_NUMBER = 10

# Default Values
DEFAULT_CATEGORY = 'general'

# LLM Analysis Constants
LLM_IRRELEVANT_RESPONSE = 'irrelevant'
