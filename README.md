# Yahoo Finance Scraper

This Python application provides a robust solution for scraping financial data from Yahoo Finance. It uses Playwright for browser automation and supports concurrent scraping of multiple financial sections including income statements, cash flow statements, and balance sheets.

## Features

The scraper comes with several sophisticated features designed to ensure reliable data collection:

- Multi-threaded scraping for improved performance
- Automated popup and consent form handling
- Comprehensive error handling and logging
- Currency value formatting (B for billions, M for millions)
- Configurable retry mechanisms and timeouts
- JSON output with clean, formatted data

## Prerequisites

Before running the scraper, ensure you have the following installed:

- Python 3.7 or higher
- Playwright
- BeautifulSoup4
- Required Python packages (install via pip):
```bash
pip install playwright beautifulsoup4
```

After installation, you'll need to install the Playwright browsers:
```bash
playwright install firefox
```

## Installation

1. Clone the repository or download the source code
2. Navigate to the project directory
3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

To run the scraper:

```bash
python main.py
```

When prompted, enter the stock ticker symbol you want to analyze. The scraper will automatically collect data from three main sections:
- Income Statement (financials)
- Cash Flow Statement
- Balance Sheet

### Output

The scraper generates three JSON files in the `files` directory (default):
- `{ticker}_financials.json`: Income statement data
- `{ticker}_cash_flow.json`: Cash flow statement data
- `{ticker}_balance_sheet.json`: Balance sheet data

Each file contains cleaned and formatted financial data with appropriate currency notation (B for billions, M for millions).

## Configuration

The `ScrapingConfig` class provides several configurable parameters:

```python
class ScrapingConfig:
    max_retries: int = 3           # Maximum number of retry attempts
    retry_delay: int = 2           # Delay between retries (seconds)
    page_timeout: int = 60000      # Page load timeout (milliseconds)
    navigation_timeout: int = 60000 # Navigation timeout (milliseconds)
    selector_timeout: int = 30000   # Element selector timeout (milliseconds)
```

You can modify these values by creating a custom configuration when initializing the scraper.

## Logging

The application maintains detailed logs in `scraper.log`, which includes:
- Scraping progress and timing
- Error messages and exceptions
- Popup handling events
- Data processing status

Logs are also displayed in the console for real-time monitoring.

## Error Handling

The scraper includes comprehensive error handling for common scenarios:
- Network timeouts and connection issues
- Missing or malformed data
- Popup and consent form interference
- Navigation failures
- Data parsing errors

Each error is logged with appropriate context for debugging.

## Performance

The scraper uses threading to concurrently process multiple financial sections, significantly reducing total execution time. The headless mode can be enabled for improved performance in production environments.

## Limitations

- The scraper is designed for Yahoo Finance's current layout (as of 2025)
- Rate limiting may be necessary for large-scale scraping
- Some financial data might be missing or shown as '--' in the output
- The scraper requires a stable internet connection

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This scraper is for educational purposes only. Please review and comply with Yahoo Finance's terms of service and robots.txt before using this tool. Ensure you have proper authorization before scraping any website.