import subprocess
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
import threading
import time
import json


def scrape(sub, ticker):
    command = ["node", "scraper.js", ticker, sub]
    text = subprocess.run(command,capture_output=True ,check=True).stdout.decode("utf-8")
    soup = BeautifulSoup(text, "html.parser")
    table = soup.findAll("span")
    final = list()
    lst = list()
    for span in table:
        if span.text[0].isalpha():
            if span.text == "ttm":
                lst.append(span.text)
            else:
                final.append(lst)
                lst = [
                    span.text,
                ]
        else:
            lst.append(span.text)
    final.append(lst)
    final = final[1:]
    re_organised = reorg(final)[1:]
    with open(f"./files/{ticker}_{sub}.json", "w") as file:    
        json.dump(re_organised, file, indent=4)


def get_data(link):
    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page()
        # increased timeout to reduce timout error
        page.goto(link, timeout=100000)
        text = page.content()
        browser.close()
    return text


def reorg(data):
    x = len(data[0])
    org = list()
    for i in range(x - 1):
        dic = dict()
        for y in data:
            try:
                if "/" not in y[i] and y[i].lstrip("-")[0].isdigit():
                    dic[y[0]] = float(y[i].replace(",", ""))
                else:
                    dic[y[0]] = y[i]
            except IndexError:
                dic[y[0]] = "N/A"
        org.append(dic)
    return org


def regex(pattern, text):
    match = re.search(pattern, text, re.DOTALL)
    if match:
        extracted_text = match.group(1)
        return extracted_text

    else:
        print("No match found!")
        raise Exception("DATA NOT FOUND")


def get_market_capitalisation(link, sub):
    div_id = "quote-summary"
    # Using playwright to extract data
    data = get_data(link)
    soup = BeautifulSoup(data, "html.parser")
    # Find the table of data needed
    target_div = soup.find("div", {"id": div_id})
    # Find all the rows within the table
    table_rows = target_div.find_all("tr")

    # Initialize an empty dictionary to store the data
    table_data = {}

    # Iterate through rows and extract data
    for row in table_rows:
        columns = row.find_all("td")
        if len(columns) == 2:  # Ensure it's a data row
            key = columns[0].get_text(strip=True)
            value = columns[1].get_text(strip=True)
            table_data[key] = value

    # Save the extracted data as a JSON file
    with open(f"./files/{ticker}_summary_data.json", "w") as json_file:
        json.dump([table_data,], json_file, indent=4)


if __name__ == "__main__":
    start = time.time()
    # ticker = input("Enter the ticker: ")
    ticker = "AAPL"
    t1 = threading.Thread(
        target=scrape,
        args=(
            "financials",
            ticker,
        ),
    )
    t2 = threading.Thread(
        target=scrape,
        args=(
            "cash-flow",
            ticker,
        ),
    )
    t3 = threading.Thread(
        target=scrape,
        args=(
            "balance-sheet",
            ticker,
        ),
    )
    t4 = threading.Thread(
        target=get_market_capitalisation,
        args=(
            f"https://finance.yahoo.com/quote/{ticker}?p={ticker}",
            ticker,
        ),
    )
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    # scrape("balance-sheet", ticker)
    end = time.time()
    print(f"Done! only took {end-start} seconds")
