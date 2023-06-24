from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re


def main(link):
    get_data(link)
    text = read_file("files", "main_page.txt")
    pattern = r'<div class="M\(0\) Whs\(n\) BdEnd Bdc\(\$seperatorColor\) D\(itb\)">(.*?)<script>'
    regex = regex(pattern, text, "first_reg.txt")
    text = read_file("files", "first_reg.txt")
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
    write_file(str(final), "./files", "data.txt")


def get_data(link):
    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page()
        page.goto(link)
        text = page.content()
        browser.close()
    write_file(text, "files", "main_page.txt")


def write_file(text, folder, filename):
    with open(f"./{folder}/{filename}", "w") as file:
        file.write(text)


def read_file(folder, filename):
    with open(f"./{folder}/{filename}", "r") as file:
        text = file.read()
    return text


def reorg(data):
    x = len(data[0])
    org = list()
    for i in range(x - 1):
        print(i)
        dic = dict()
        for y in data:
            print(y)
            try:
                dic[y[0]] = y[i]
            except IndexError:
                dic[y[0]] = "N/A"
        org.append(dic)


def regex(pattern, text, filename):
    match = re.search(pattern, text, re.DOTALL)
    if match:
        extracted_text = match.group(1)
        with open(filename, "w") as file:
            file.write(extracted_text)

    else:
        print("No match found!")


if __name__ == "__main__":
    link = input("Enter the link: ")
    main(link)
