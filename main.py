import logging
from pathlib import Path
from typing import Dict, List, Optional, Union
from playwright.sync_api import sync_playwright, TimeoutError
from bs4 import BeautifulSoup
import json
import time
import sys
from dataclasses import dataclass
import threading

# Set up logging with more detail
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

@dataclass
class ScrapingConfig:
    """Configuration settings for the scraper."""
    max_retries: int = 3
    retry_delay: int = 2
    page_timeout: int = 60000  # Increased timeout
    navigation_timeout: int = 60000
    selector_timeout: int = 30000

class YahooFinanceScraper:
    def __init__(self, output_dir: str = "./files", headless: bool = False):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.config = ScrapingConfig()
        self.headless = headless

    def _handle_popups(self, page):
        """Handle any consent or notification popups."""
        try:
            # Handle cookie consent popup
            consent_btn = page.get_by_role("button", name="Accept all")
            if consent_btn.is_visible(timeout=5000):
                consent_btn.click()
                logging.info("Clicked consent button")

            # Handle other potential popups
            try:
                page.wait_for_selector('button[type="button"]', timeout=5000)
                buttons = page.query_selector_all('button[type="button"]')
                for button in buttons:
                    if "consent" in (button.get_attribute("class") or "").lower():
                        button.click()
                        logging.info("Clicked additional consent button")
            except TimeoutError:
                pass

        except Exception as e:
            logging.info(f"No popups found or error handling popups: {str(e)}")

    def scrape_financial_data(self, ticker: str, section: str) -> Optional[List[Dict]]:
        """Scrape financial data with improved page interaction handling."""
        with sync_playwright() as p:
            browser = p.firefox.launch(headless = self.headless,  # Set to True if you don't need to see the browser
                args=['--start-maximized', '--disable-web-security'],  # Additional browser arguments
                timeout=30000)
            
            page = browser.new_page()

            page.goto(f"https://sg.finance.yahoo.com/quote/{ticker}/{section}?p={ticker}")
            data = page.locator('[class="tableContainer yf-9ft13"]').inner_html()
        return data


    def clean_financial_data(self, html_content: str) -> List[Dict[str, Union[str, float]]]:
        """
        Parse and clean financial data from Yahoo Finance HTML content.
        
        Args:
            html_content (str): Raw HTML string containing financial data
            
        Returns:
            List[Dict]: List of dictionaries containing cleaned financial data
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all rows in the table
        rows = soup.find_all('div', class_='row')
        
        # Initialize variables
        headers = []
        financial_data = []
        
        # Get headers from the first row
        header_row = rows[0]
        header_cols = header_row.find_all('div', class_='column')
        
        # Extract and clean headers
        for col in header_cols:
            header_text = col.text.strip()
            if header_text != 'Breakdown':  # Skip the 'Breakdown' column header
                headers.append(header_text)
        
        # Process each data row
        for row in rows[1:]:  # Skip header row
            cols = row.find_all('div', class_='column')
            
            # Get the metric name (first column)
            metric_name = cols[0].find('div', class_='rowTitle')
            if not metric_name:
                continue
                
            metric_name = metric_name.text.strip()
            
            # Create a data entry for this metric
            entry = {'Metric': metric_name}
            
            # Process each value column
            for i, col in enumerate(cols[1:]):  # Skip first column (metric name)
                if i >= len(headers):
                    break
                    
                value = col.text.strip()
                
                # Convert string numbers to float, handling special cases
                if value == '--':
                    value = None
                elif value.replace(',', '').replace('.', '').replace('-', '').isdigit():
                    value = float(value.replace(',', ''))
                    
                entry[headers[i]] = value
                
            financial_data.append(entry)
        
        return financial_data

    def format_currency(self, value: Union[float, None]) -> Union[str, None]:
        """
        Format currency values with appropriate suffixes (B for billions, M for millions).
        
        Args:
            value (float): The numerical value to format
            
        Returns:
            str: Formatted string with appropriate suffix
        """
        if value is None:
            return None
            
        if value >= 1_000_000_000:
            return f"${value/1_000_000_000:.2f}B"
        elif value >= 1_000_000:
            return f"${value/1_000_000:.2f}M"
        else:
            return f"${value:.2f}"

    def process_financial_data(self, html_content: str, output_file: str = 'financial_data.json') -> None:
        """
        Process financial data and save to JSON file with formatted values.
        
        Args:
            html_content (str): Raw HTML string containing financial data
            output_file (str): Path to save the output JSON file
        """
        # Parse and clean the data
        financial_data = self.clean_financial_data(html_content)
        
        # Format currency values
        for entry in financial_data:
            for key, value in entry.items():
                if key != 'Metric' and isinstance(value, (int, float)):
                    entry[key] = self.format_currency(value)
        
        # Save to JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(financial_data, f, indent=2)
        
        print(f"Financial data has been processed and saved to {output_file}")


    def _save_data(self, data: dict, filename: str):
        """Save the processed data to a JSON file."""
        output_file = self.output_dir / filename
        with output_file.open("w") as f:
            json.dump(data, f, indent=4)
def scrape_section(scraper, ticker, section, output_file):
    """Helper function to run in thread for each section"""
    try:
        logging.info(f"Starting to scrape {section} for {ticker}")
        html_content = scraper.scrape_financial_data(ticker, section)
        
        if html_content:
            output_path = Path(scraper.output_dir) / output_file
            scraper.process_financial_data(html_content, output_path)
            logging.info(f"Successfully processed {section} data and saved to {output_file}")
        else:
            logging.error(f"Failed to retrieve data for {section}")
            
    except Exception as e:
        logging.error(f"Error processing {section}: {str(e)}")

def main():
    """
    Main function to run the Yahoo Finance scraper with threading.
    Handles multiple sections and provides detailed logging.
    """
    start_time = time.time()
    logging.info("Starting Yahoo Finance scraper")
    
    try:
        # Initialize scraper with headless=False for debugging
        scraper = YahooFinanceScraper(headless=True)
        ticker = input("Enter Ticker: ")
        
        # Dictionary to map sections to their output filenames
        sections = {
            "financials": f"{ticker}_financials.json",
            "cash-flow": f"{ticker}_cash_flow.json",
            "balance-sheet": f"{ticker}_balance_sheet.json"
        }
        
        # Create threads for each section
        threads = []
        for section, output_file in sections.items():
            thread = threading.Thread(
                target=scrape_section,
                args=(scraper, ticker, section, output_file)
            )
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        duration = time.time() - start_time
        logging.info(f"Scraping completed in {duration:.2f} seconds")
        
    except Exception as e:
        logging.error(f"Critical error in main function: {str(e)}")
        raise

if __name__ == "__main__":
    main()