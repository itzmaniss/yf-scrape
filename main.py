from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from reg import regex
from tabulate import tabulate

link = "https://sg.finance.yahoo.com/quote/BABA/balance-sheet?p=BABA"

def get_data(link):
    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page()
        page.goto(link)
        text = page.content()
        browser.close()
    write_file(text, "baba1_files", "main_page.txt")

def write_file(text, folder, filename):
    with open(f"./{folder}/{filename}", "w") as file:
        file.write(text)

def read_file(folder, filename):
    with open(f"./{folder}/{filename}", "r") as file:
        text = file.read()
    return text

get_data(link)

text = read_file("baba1_files", "main_page.txt")

pattern = r'<div class="M\(0\) Whs\(n\) BdEnd Bdc\(\$seperatorColor\) D\(itb\)">(.*?)<script>'
regex = regex(pattern, text, "first_reg.txt")

text = read_file("baba1_files", "first_reg.txt")

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
            lst = [span.text, ]
    else:
        lst.append(span.text)

final = final[1:]

table = tabulate(final, headers='firstrow', tablefmt='fancy_grid')

write_file(str(final), "./", "data.txt")
print(table)

            
