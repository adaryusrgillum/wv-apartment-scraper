"""Configuration file for WV Apartment Scraper"""
import os
from dotenv import load_dotenv

load_dotenv()

# Database
DB_NAME = os.getenv('DB_NAME', 'wv_apartments.db')
DB_PATH = os.getenv('DB_PATH', './data')

# Locations to scrape
TARGET_CITIES = ['Morgantown', 'Buckhannon', 'Charleston', 'Huntington']
TARGET_STATE = 'WV'

# Scraper settings
REQUEST_TIMEOUT = 30
RETRY_ATTEMPTS = 3
RETRY_DELAY = 5  # seconds

# Request delays (in seconds)
MIN_DELAY = 2
MAX_DELAY = 10

# Playwright settings
PLAYWRIGHT_HEADLESS = True
PLAYWRIGHT_TIMEOUT = 60000  # 60 seconds

# Craigslist settings
CRAIGSLIST_BASE_URL = 'https://{location}.craigslist.org/search/apa'

# Zillow settings
ZILLOW_BASE_URL = 'https://www.zillow.com/{city}-{state}/rentals/'

# Apartments.com settings
APARTMENTS_BASE_URL = 'https://www.apartments.com/{city}-{state}/'

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', './logs/scraper.log')

# Scheduling
SCHEDULE_INTERVAL_HOURS = int(os.getenv('SCHEDULE_INTERVAL_HOURS', '12'))

# API settings (for Flask app)
API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('API_PORT', '5000'))
API_DEBUG = os.getenv('API_DEBUG', 'False').lower() == 'true'
