import asyncio
from playwright.async_api import async_playwright
import pandas as pd
from config import Config


# auth=f'{Config.USERNAME}:{Config.PASSWORD}'
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
        await page.goto('https://www.amazon.com/2021-Apple-10-2-inch-iPad-Wi-Fi/dp/B09G9FPHY6/ref=sr_1_1_sspa?crid=3C0GSCZB3YQT0&dib=eyJ2IjoiMSJ9.x37hw5scXMlLBGdXY-8Ogz8jtKP3hiT2MdS8aUVAAk-weR0YeoUQkBeHdqfTUEv1DyhJG1166Mv0ZK4r-eBLPbe5oV4jlg-cRVcvjMopR-CCEJBdDQ2_T7RlVUanGw0mYDoBljmZ7A08GSgDxnyzy6n2LA4J4m8FqUNiG_VpcqvFrrfDnE6dRKywSxfXo73cal7ksuisKbHObaU1h8O26IQuqxZek1UWzKfuwPv68Pw.OU38E8vqzDXvuGGtQY_iFzPagpY5RFnwWiDpuotniPI&dib_tag=se&keywords=ipad&qid=1710985458&sprefix=ipad%2Caps%2C220&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1', timeout=600000)
        print('data extraction in progress')
        # Extract information
        results = []
        listings = await page.query_selector_all('div.a-container')
        for listing in listings:
            result = {}
            # Product name
            name_element = await listing.query_selector('h1.a-size-large > span.a-size-medium')
            result['product_title'] = await name_element.inner_text() if name_element else 'N/A'

            # Price
            price_element = await listing.query_selector('span.a-price > span.a-offscreen')
            result['price'] = await price_element.inner_text() if price_element else 'N/A'
            if(result['product_title']=='N/A' and result['price']=='N/A'):
                pass
            else:
                results.append(result)
        # Close browser
        await browser.close()

        return results
    
print('data extraction completed')

# Run the scraper and save results to a CSV file
results = asyncio.run(scrape_amazon_bdata())
df = pd.DataFrame(results)
df.to_csv('amazon_iPad_bdata.csv', index=False)