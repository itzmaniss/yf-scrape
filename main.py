from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
import threading


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
    re_organised = str(reorg(final)[1:])
    write_file(re_organised, "./files", f"{sub}_reorged.txt")


def get_data(link):
    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page()
        # increased timeout to reduce timout error
        page.goto(link, timeout=100000)
        text = page.content()
        browser.close()
    return text


def write_file(text, folder, filename):
    with open(f"./{folder}/{filename}", "w") as file:
        file.write(text)


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


def regex(pattern, text, filename):
    match = re.search(pattern, text, re.DOTALL)
    if match:
        extracted_text = match.group(1)
        return extracted_text

    else:
        print("No match found!")


if __name__ == "__main__":
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
    print("Done!")
