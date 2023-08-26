const puppeteer = require("puppeteer");
const fs = require("fs");

const ticker = process.argv[2];
const sub = process.argv[3];

(async () => {
    const browser = await puppeteer.launch({ headless: "new" });
    const page = await browser.newPage();

    await page.goto(`https://sg.finance.yahoo.com/quote/${ticker}/${sub}?p=${ticker}`);
    const required = await page.evaluate(() => {
        const text = document.querySelector(".M\\(0\\).Whs\\(n\\).BdEnd.Bdc\\(\\$seperatorColor\\).D\\(itb\\)").innerHTML;
        return text;
    });
    await browser.close();
    console.log(required)
})();