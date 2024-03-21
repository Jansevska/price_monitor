import asyncio
from playwright.async_api import async_playwright
import pandas as pd


username='brd-customer-hl_af14656f-zone-scraping_browser1'
password='otp8h37o1mmq'
auth=f'{username}:{password}'
host = 'brd.superproxy.io:9222'
browser_url = f'wss://{auth}@{host}'

async def scrape_amazon_bdata():
    async with async_playwright() as pw:
        print('connecting')
        # Launch new browser
        browser = await pw.chromium.connect_over_cdp(browser_url)
        print('connected')
        page = await browser.new_page()
        print('navigating')
        # Go to Amazon URL
        await page.goto('https://www.amazon.com/s?i=fashion&bbn=115958409011', timeout=600000)
        print('data extraction in progress')
        # Extract information
        results = []
        listings = await page.query_selector_all('div.a-section.a-spacing-small')
        for listing in listings:
            result = {}
            # Product name
            name_element = await listing.query_selector('h2.a-size-mini > a > span')
            result['product_name'] = await name_element.inner_text() if name_element else 'N/A'

            # Price
            price_element = await listing.query_selector('span.a-price > span.a-offscreen')
            result['price'] = await price_element.inner_text() if price_element else 'N/A'
            if(result['product_name']=='N/A' and result['price']=='N/A'):
                pass
            else:
                results.append(result)
        # Close browser
        await browser.close()

        return results
# Run the scraper and save results to a CSV file
results = asyncio.run(scrape_amazon_bdata())
df = pd.DataFrame(results)
df.to_csv('amazon_products_bdata_listings.csv', index=False)