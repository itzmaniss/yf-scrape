from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
import threading
import time
import json 


def main(link, sub):
    text = get_data(link)
    pattern = r'<div class="M\(0\) Whs\(n\) BdEnd Bdc\(\$seperatorColor\) D\(itb\)">(.*?)<script>'
    specific_text = regex(pattern, text)
    soup = BeautifulSoup(specific_text, "html.parser")
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


if __name__ == "__main__":
    start = time.time()
    ticker = input("Enter the ticker: ")
    t1 = threading.Thread(
        target=main,
        args=(
            f"https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}",
            "financials",
        ),
    )
    t2 = threading.Thread(
        target=main,
        args=(
            f"https://finance.yahoo.com/quote/{ticker}/cash-flow?p={ticker}",
            "cash-flow",
        ),
    )
    t3 = threading.Thread(
        target=main,
        args=(
            f"https://finance.yahoo.com/quote/{ticker}/balance-sheet?p={ticker}",
            "balance-sheet",
        ),
    )
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    end = time.time()
    print(f"Done! only took {end-start} seconds")
