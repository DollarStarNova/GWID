from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pathlib import Path
from PIL import Image
import requests
import os


class GWImageGrabber():
    def __init__(self, productCode: int or list):
        if type(productCode) == int:
            self.productCode = [productCode]
        else:
            self.productCode = productCode

        self.notfoundimage = Image.open("imagenotfound.jpg")
        self.driver = webdriver.Chrome("chromedriver.exe")
        self.driver.get("https://trade.games-workshop.com/resources/")
        self.driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "onetrust-accept-btn-handler")))
        self.driver.find_element_by_xpath('//*[@id="overlay-submit"]').click()
        self.searchbox = self.driver.find_element_by_name("filter_keywords")
        self.search_and_download(self.productCode)

    def search_and_download(self, productCode):
        assert type(productCode) == list, "GWImageGrabber.search(" + productCode + ") argument type is not list!"
        self.url_list = []
        for code in productCode:
            self.searchbox.clear()
            self.searchbox.send_keys(str(code))
            self.searchbox.send_keys(Keys.RETURN)
            url = None
            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "media-tile__link")))
            except(TimeoutException):
                url = None

            if "No results." in self.driver.page_source:
                url = None

            else:
                url = self.driver.find_element_by_class_name("media-tile__link").get_attribute("href")

            self.url_list.append(
                [code, url]
            )
        self.driver.close()

        self.download(self.url_list)

    def download(self, url_list, folder=Path.home()):
        print(url_list)
        for item in url_list:
            myimage = self.notfoundimage
            if item[1] is not None:
                myimage = Image.open(requests.get(item[1], stream=True).raw) or self.notfoundimage
            location = os.path.join(folder, "Desktop", "GWImages")
            imagelocation = os.path.join(location, str(item[0])) + '.jpg'
            if not os.path.exists(location):
                os.makedirs(location)
            myimage.save(imagelocation)


if __name__ == "__main__":
    GWImageGrabber([4357534, 60040199131, 99120204019, 99120113063])
