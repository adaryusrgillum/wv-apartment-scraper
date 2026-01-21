# wv-apartment-scraper
A Python-based apartment scraper for West Virginia (Zillow, Craigslist, Apartments.com). Collects rental listings from Morgantown, Buckhannon, and other WV areas with SQLite storage, price tracking, and Raspberry Pi deployment support.

## Features

- **Multi-Source Scraping**: Collects apartments from Zillow, Craigslist, Apartments.com, and local WV realty sites
- **Automatic Data Collection**: Scheduled scraping with configurable intervals
- **SQLite Database**: Stores all listings with price history tracking
- **Price Monitoring**: Tracks price changes over time for each listing
- **JSON API Export**: RESTful API to export and query listings
- **Raspberry Pi Support**: Optimized for low-power devices
- **Robust Error Handling**: Retry logic, user-agent rotation, and request delays
- **Anti-Detection**: Playwright stealth mode, random delays, proper headers

## Quick Start

### Prerequisites

- Python 3.8+
- pip or poetry
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/wv-apartment-scraper.git
cd wv-apartment-scraper

# Install dependencies
pip install -r requirements.txt
python -m playwright install chromium

# Create data directories
mkdir -p data logs
```

### Configuration

1. Create a `.env` file in the project root:

```env
DB_NAME=wv_apartments.db
DB_PATH=./data
LOG_LEVEL=INFO
LOG_FILE=./logs/scraper.log
API_HOST=0.0.0.0
API_PORT=5000
API_DEBUG=False
```

2. Edit `config.py` to customize:
   - Target cities
   - Request delays
   - Scheduling intervals
   - Playwright settings

### Running the Scraper

```bash
# Run a single scrape cycle
python main.py

# Start the scheduler (runs periodically)
python main.py --schedule

# Start API server
python api.py
```

## Project Structure

```
wv-apartment-scraper/
├── config.py                 # Configuration settings
├── database.py              # Database operations
├── main.py                  # Main orchestrator
├── scrapers/
│   ├── craigslist.py       # Craigslist scraper
│   ├── zillow.py           # Zillow scraper  
│   ├── apartments_com.py   # Apartments.com scraper
│   └── base_scraper.py     # Base class for scrapers
├── api.py                   # Flask REST API
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── data/                    # SQLite database directory
└── logs/                    # Log files
```

## Deployment

### On Raspberry Pi

1. Install Raspberry Pi OS Lite (64-bit recommended)
2. Install Python 3.9+: `sudo apt-get install python3.9 python3-pip`
3. Follow installation steps above
4. Add to crontab for scheduling:

```bash
crontab -e
# Add: 0 9,18 * * * /usr/bin/python3 /home/pi/wv-apartment-scraper/main.py
```

### On Linux Server

Use systemd service file (see DEPLOYMENT.md)

### On Docker

```bash
docker build -t wv-scraper .
docker run -v $(pwd)/data:/app/data wv-scraper
```

## API Endpoints

- `GET /api/listings` - Get all active listings
- `GET /api/listings?city=Morgantown` - Filter by city
- `GET /api/listings?min_price=800&max_price=1500` - Filter by price
- `GET /api/export/json` - Export all data as JSON
- `GET /api/stats` - Get scraping statistics

## Legal Notice

This tool respects `robots.txt` and implements delays between requests. However:

- **Zillow & Apartments.com** have aggressive anti-scraping measures. For production use, consider their official APIs
- **Craigslist** allows scraping but monitor their ToS
- Always follow the website's Terms of Service

## Important Notes

⚠️ **Anti-Detection Measures**: The scraper uses:
- User-Agent rotation
- Random request delays (2-10 seconds)
- Proper HTTP headers
- Playwright stealth mode
- Headless browser emulation

⚠️ **Rate Limiting**: If blocked, the scraper will:
- Retry with exponential backoff
- Pause for extended periods
- Log all errors
- Exit gracefully

## Troubleshooting

### "Connection blocked" error
- The website is detecting the scraper. Wait 24-48 hours before retrying
- Consider using residential proxies (BrightData, Smartproxy)
- Increase delays in config.py

### "Playwright timeout"
- Increase `PLAYWRIGHT_TIMEOUT` in config.py
- Check internet connection
- Reduce concurrent scraping

### Database errors
- Delete `data/wv_apartments.db` to reset
- Check file permissions on data/ directory

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new scrapers
4. Submit a pull request

## Future Improvements

- [ ] Support for Rent.com
- [ ] Email alerts for price drops
- [ ] Web dashboard for data visualization
- [ ] Support for Apartments.com and Hotpads
- [ ] Mobile app
- [ ] Discord bot integration

## License

MIT License - See LICENSE file

## Disclaimer

This tool is for educational purposes. Use responsibly and respect website ToS. The authors are not responsible for misuse or legal consequences. Always check local laws regarding web scraping.
