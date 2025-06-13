from dotenv import dotenv_values
import utils
import logging
import aiohttp
from bs4 import BeautifulSoup as BS
import asyncio
from playwright.async_api import async_playwright
from db.database import Database
from db.models import Cars


logging.basicConfig(level=logging.INFO)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}
CONFIG = dotenv_values(".env")


class Parser:    
    def __init__(self, headers: dict, target: str, page_limit: int, start_time: str):
        self.headers = headers
        self.target = target
        self.page_limit = page_limit
        self.start_time = start_time
        self.items_queue = None
        self.db_driver = None
        self.items_skip = None


    async def get(self, url: str):
        # Async HTTP GET request with aiohttp, with error handling
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    return await response.text()
        except aiohttp.ClientError as err:
            logging.error(f"An error occurred: {err}")
            raise RuntimeError(f"Request failed: {err}") from err


    @staticmethod
    def check_block(block, name: str, recursive=True):
        # Extract text or log absence of a block
        if block is None:
            logging.info(f"No {name} is listed.")
        else:
            if not recursive:
                block = block.find(string=True, recursive=False)
            else:
                block = block.text
        return block


    @staticmethod
    def prepare_data(data: dict):
        # Clean string fields and format phone number if present
        for key in data:
            if isinstance(data[key], str):
                data[key] = data[key].strip()
            if key == "phone_number" and data[key]:
                data[key] = utils.converted_phone(data[key])
        return data


    async def start(self):
        if self.start_time != utils.converted_time("hours-minutes"):
            raise utils.StartTimeException("Wrong start time.")

        self.items_queue = []

        Database.setup()
        self.db_driver = Database.get_driver()

        # Prepare a set of URLs already in DB to skip duplicates
        self.items_skip = {}
        cars_data = self.db_driver.query(Cars).all()
        for car in cars_data:
            self.items_skip[car.url] = 1

        # Fetch all catalog pages concurrently
        catalog_tasks = [self.parse_catalog(page_num) for page_num in range(1, self.page_limit + 1)]
        await asyncio.gather(*catalog_tasks)
        logging.info(f"Found {len(self.items_queue)} items.")

        '''

        Potential approach for async items data fetching (takes too much memory):

        item_tasks = [self.parse_item(item_url) for item_url in self.items_queue]
        await asyncio.gather(*item_tasks)

        '''
        
        # Sequentially parse each item
        for item_url in self.items_queue:
            await self.parse_item(item_url)


    async def parse_catalog(self, page_num: int):
        logging.info(f"Parsing page #{page_num} of {self.target}.")
        catalog_url = self.target + f"?page={page_num}"
        catalog_html = await self.get(catalog_url)
        catalog_soup = BS(catalog_html, "html.parser")

        items_div = catalog_soup.find("div", {"id": "searchResults"})
        if items_div is None:
            raise utils.ParsingException("Items div is not located.")
        
        for item_div in items_div.find_all("div", {"class": "content-bar"}):
            item_url = item_div.find("a", {"class": "m-link-ticket"}).get("href")
            if item_url not in self.items_skip:
                self.items_queue.append(item_url)     


    async def parse_item(self, item_url: str):
        logging.info(f"Parsing item {item_url}.")
        item_html = None

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto(item_url)
            try:
                # Accept cookie consent and reveal phone number, handle timeouts gracefully
                await page.click("button.fc-cta-consent")
                await page.click("a.phone_show_link", timeout=10000)
                await page.wait_for_timeout(1000)
            except Exception as e:
                logging.error("Error:", e)
                return

            item_html = await page.content()
            await browser.close()
        
        item_soup = BS(item_html, "html.parser")
        item_data = {}

        if item_soup.find("div", {"class": "notice_head"}):
            logging.info(f"Item {item_url} is not active, skipping.")
            return

        try:
            # Extract data, carefully handle missing fields if necessary
            item_data["url"] = item_url
            item_data["title"] = item_soup.find("h1", {"class": "head"}).text
            item_data["price_usd"] = int(item_soup.find("div", {"class": "price_value"}).find("strong").text.replace(" ", "")[:-1]) #Remove last symbol of currency
            item_data["odometer"] = int(item_soup.find("div", {"class": "base-information"}).find("span").text) * 1000
            item_data["username"] = self.check_block(item_soup.find(["div", "h4"], {"class": "seller_info_name"}), "username")
            item_data["phone_number"] = item_soup.find("span", {"class": "phone"}).text
            item_data["image_url"] = item_soup.find("div", {"id": "photosBlock"}).find("img").get("src")
            item_data["images_count"] = int(item_soup.find("div", {"class": "count-photo"}).find("span", {"class": "mhide"}).text.replace("из ", ""))
            item_data["car_number"] = self.check_block(item_soup.find("span", {"class": "state-num"}), "car number", False)
            item_data["car_vin"] = self.check_block(item_soup.find("span", {"class": ["label-vin", "vin-code"]}), "car VIN")
            item_data["datetime_found"] = utils.converted_time("full")
            
            item_data = self.prepare_data(item_data)
            
            # Create ORM object and commit to DB
            car = Cars(**item_data)
            self.db_driver.add(car)
            self.db_driver.commit()
        except Exception as e:
            logging.error("Error:", e)


worker = Parser(
    HEADERS, CONFIG["TARGET_PAGE"],
    int(CONFIG["PAGE_LIMIT"]), CONFIG["START_TIME"]
)
asyncio.run(worker.start())