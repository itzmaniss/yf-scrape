# FinSheet Harvester

A high-performance financial statement extraction tool that automatically collects and structures company financial data from Yahoo Finance. Built with enterprise-grade reliability, concurrent processing, and intelligent error handling.

## Overview

FinSheet Harvester transforms raw financial web data into clean, structured JSON outputs. It concurrently scrapes income statements, balance sheets, and cash flow statements while handling complex web elements like dynamic loading and consent forms.

## Key Features

- Concurrent extraction of multiple financial statements
- Intelligent currency formatting (billions/millions)
- Built-in retry mechanisms and comprehensive error handling
- Automated popup and consent management
- Detailed logging and execution monitoring
- Clean JSON output with standardized formatting

## Prerequisites

- Python 3.7 or higher
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/finsheet-harvester.git
```

2. Navigate to the project directory:
```bash
cd finsheet-harvester
```

3. Install all dependencies:
```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:
```bash
playwright install firefox
```

## Usage

Run the harvester:
```bash
python main.py
```

Enter the stock ticker when prompted. The tool automatically collects:
- Income Statement
- Cash Flow Statement
- Balance Sheet

### Output

Generated JSON files are saved in the `files` directory:
- `{ticker}_financials.json`: Income statement data
- `{ticker}_cash_flow.json`: Cash flow statement data
- `{ticker}_balance_sheet.json`: Balance sheet data

Each file contains cleaned and formatted financial data with appropriate currency notation (B for billions, M for millions).

## Configuration

Customize the harvester's behavior through `ScrapingConfig`:

```python
class ScrapingConfig:
    max_retries: int = 3           # Maximum retry attempts
    retry_delay: int = 2           # Delay between retries (seconds)
    page_timeout: int = 60000      # Page load timeout (ms)
    navigation_timeout: int = 60000 # Navigation timeout (ms)
    selector_timeout: int = 30000   # Element selector timeout (ms)
```

## Logging

The harvester maintains detailed logs in `scraper.log`, tracking:
- Extraction progress and timing
- Error messages and exceptions
- Popup handling events
- Data processing status

## Error Handling

Built-in handling for common scenarios:
- Network timeouts
- Connection issues
- Missing/malformed data
- Popup interference
- Navigation failures
- Data parsing errors

## Performance

Utilizes threading for concurrent processing of financial statements. Enable headless mode for improved performance in production environments.

## Limitations

- Designed for Yahoo Finance's current layout (as of 2025)
- Rate limiting may be necessary for large-scale extraction
- Some financial data might be unavailable (shown as '--')
- Requires stable internet connection

## Contributing

Contributions welcome! Please open an issue first to discuss proposed changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational purposes only. Review and comply with Yahoo Finance's terms of service before use. Ensure you have proper authorization for data collection.