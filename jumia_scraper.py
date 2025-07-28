from playwright.sync_api import sync_playwright
import csv

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.jumia.com.ng/catalog/?q=infinix+phones+100000", timeout=60000)
        page.wait_for_timeout(5000)

        products = page.query_selector_all('article.prd')
        data = []

        for product in products:
            name = product.query_selector('h3.name')
            price = product.query_selector('div.prc')
            if name and price:
                data.append({
                    'Product Name': name.inner_text(),
                    'Price (NGN)': price.inner_text()
                })

        with open('jumia_products.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Product Name', 'Price (NGN)'])
            writer.writeheader()
            writer.writerows(data)

        print(f"Scraped {len(data)} products.")
        browser.close()

if __name__ == "__main__":
    run()