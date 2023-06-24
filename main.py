from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from reg import regex
from tabulate import tabulate

link = "https://sg.finance.yahoo.com/quote/BABA/financials?p=BABA"

def get_data(link):
    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page()
        page.goto(link)
        text = page.content()
        browser.close()
    return text

def write_file(text, folder, filename):
    with open(f"./{folder}/{filename}", "w") as file:
        file.write(text)

def read_file(folder, filename):
    with open(f"./{folder}/{filename}", "r") as file:
        text = file.read()
    return text

# text = read_file("baba_files", "main_page.txt")

# pattern = r'<div class="M\(0\) Whs\(n\) BdEnd Bdc\(\$seperatorColor\) D\(itb\)">(.*?)<script>'
# regex = regex(pattern, text, "first_reg.txt")

text = read_file("baba_files", "first_reg.txt")

soup = BeautifulSoup(text, "html.parser")

table = soup.find("table", {"class": "W(100%) Bdcl(c) "})

write_file(str(table), "baba_files", "table.txt")






