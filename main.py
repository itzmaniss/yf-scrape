from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.firefox.launch()
    page = browser.new_page()
    page.goto("https://sg.finance.yahoo.com/quote/OV8.SI/cash-flow?p=OV8.SI&guccounter=1")
    text = page.content()
    browser.close()
    with open("example.txt", "w") as file:
        file.write(text)