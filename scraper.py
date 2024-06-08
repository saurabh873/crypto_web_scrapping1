

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class CoinMarketCapScraper:
    def __init__(self):
        self.base_url = "https://coinmarketcap.com/currencies/"
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def scrape_coin_data(self, coin):
        url = f"{self.base_url}{coin}/"
        self.driver.get(url)

        try:
            data = {
                "price": self._get_element_text(By.CSS_SELECTOR, 'div.priceValue span'),
                "price_change": self._get_element_text(By.CSS_SELECTOR, 'span.sc-15yy2pl-0'),
                "market_cap": self._get_element_text(By.XPATH, '//div[contains(text(), "Market Cap")]/following-sibling::div'),
                "market_cap_rank": self._get_element_text(By.XPATH, '//div[contains(text(), "Market Cap Rank")]/following-sibling::div'),
                "volume": self._get_element_text(By.XPATH, '//div[contains(text(), "Volume 24h")]/following-sibling::div'),
                "volume_rank": self._get_element_text(By.XPATH, '//div[contains(text(), "Volume / Market Cap")]/following-sibling::div'),
                "volume_change": self._get_element_text(By.XPATH, '//div[contains(text(), "Volume Change")]/following-sibling::div'),
                "circulating_supply": self._get_element_text(By.XPATH, '//div[contains(text(), "Circulating Supply")]/following-sibling::div'),
                "total_supply": self._get_element_text(By.XPATH, '//div[contains(text(), "Total Supply")]/following-sibling::div'),
                "diluted_market_cap": self._get_element_text(By.XPATH, '//div[contains(text(), "Fully Diluted Market Cap")]/following-sibling::div'),
                "contracts": self._get_contracts(),
                "official_links": self._get_official_links(),
                "socials": self._get_social_links(),
            }

            return data
        except Exception as e:
            return {"error": str(e)}

    def _get_element_text(self, by, value):
        try:
            element = self.driver.find_element(by, value)
            return element.text if element else None
        except:
            return None

    def _get_contracts(self):
        contracts = []
        elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.sc-1cczdzi-0 a')
        for element in elements:
            name = element.text
            address = element.get_attribute('href')
            contracts.append({"name": name, "address": address})
        return contracts

    def _get_official_links(self):
        links = []
        elements = self.driver.find_elements(By.CSS_SELECTOR, 'ul.sco1ol-0 a')
        for element in elements:
            name = element.text
            link = element.get_attribute('href')
            links.append({"name": name, "link": link})
        return links

    def _get_social_links(self):
        socials = []
        elements = self.driver.find_elements(By.CSS_SELECTOR, 'ul.sco1ol-0 a')
        for element in elements:
            name = element.get_attribute('title')
            url = element.get_attribute('href')
            socials.append({"name": name, "url": url})
        return socials

    def close(self):
        self.driver.quit()
