from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from reg import regex
from tabulate import tabulate

# with sync_playwright() as p:
#     browser = p.firefox.launch()
#     page = browser.new_page()
#     page.goto("https://sg.finance.yahoo.com/quote/OV8.SI/cash-flow?p=OV8.SI&guccounter=1")
#     text = page.content()
#     browser.close()

with open("main_page.txt", "r") as file:
    text = file.read()

pattern = r'<div id="mrt-node-Col1-1-Financials" data-locator="subtree-root">(.*?)<script>'
regex = regex(pattern, text, "first_reg.txt")

# text = ""
# with open("example.txt", "r") as file:
#     text = file.read()

# soup = BeautifulSoup(text, "html.parser").text.replace("Show:Income statementBalance sheetCash flowAnnualQuarterlyCash flowAll numbers in thousands",  "")

#i need to change the data in soup to form a list of lists

# print(soup)






