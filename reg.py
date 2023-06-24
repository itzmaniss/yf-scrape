import re

pattern1 = r'<div class="M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)">'
pattern = r'<div id="mrt-node-Col1-1-Financials" data-locator="subtree-root">(.*?)<script>'

def regex(pattern, text, filename):
    match = re.search(pattern, text, re.DOTALL)
    if match:
        extracted_text = match.group(1)
        with open(filename, "w") as file:
            file.write(extracted_text)

    else:
        print("No match found!")
