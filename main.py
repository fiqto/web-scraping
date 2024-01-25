from flask import Flask, jsonify
import pandas as pd
import os
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

app = Flask(__name__)

def export_csv(items, path="output", file_name="items.csv"):
    df = pd.DataFrame(items)
    os.makedirs(path, exist_ok=True)  
    df.to_csv(os.path.join(path, file_name), index=False)

def parse_item(html_page):
    soup = BeautifulSoup(html_page, 'html.parser')
    items = []
    for item in soup.find_all('div' ,{ 'class': 'caption'}):
        title = item.find('a' ,{'class' : 'title'}).text
        price = item.find('h4' ,{'class' : 'float-end price card-title pull-right'}).text
        items.append({
            'title': title,
            'price': price
        })

    return items

@app.route("/")
def main():
    url = 'https://webscraper.io/test-sites/e-commerce/allinone'
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        html_page = page.inner_html('div.col-lg-9')
    items = parse_item(html_page)
    export_csv(items)

    return jsonify(items), 200

if __name__ == "__main__":
    app.run()
