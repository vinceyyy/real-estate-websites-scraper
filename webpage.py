import undetected_chromedriver as uc
import requests
from bs4 import BeautifulSoup as bs
import time
import random

class WebDrive:
    def __init__(self):
        # prepare WebDriver
        self.options = uc.ChromeOptions()
        self.options.headless = False
        self.options.add_argument(
            '/Users/vincentyan/Library/Application Support/Google/Chrome')
        self.options.add_argument(
            'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"')
        self.driver = uc.Chrome(options=self.options)

    def set_headless(self, headless):
        if headless == True:
            self.headless.options.headless = True
            self.options.add_argument('--headless')
            self.driver = uc.Chrome(options=self.options)

    def get_cookie(self, url, wait=1):
        """Get cookies using undetected-chromedriver.

        Args:
            url (string): target url to get cookies from.

        Returns:
            cookies: cookies dict that can be send to requests arg.
        """
        
        # get cookies
        if wait != 0: 
            wait = random.uniform(wait, wait+2)
        self.driver.get(url)
        time.sleep(wait)
        cookie = self.driver.get_cookies()
        time.sleep(wait)
        self.driver.quit()

        # parse and reconstruct cookies
        cookies = {}
        for i in cookie:
            cookies[i['name']] = i['value']
        return cookies

class WebPage:
    """Send a http request and do things to HTML.
    """
    cookies = None
    headers = None
    def __init__(self, url):
        self.url = url
        self.response = requests.get(url, headers=WebPage.headers, cookies=WebPage.cookies)

    def get_response(self):
        print(self.response)

    def get_html(self):
        html = self.response.text
        return html

    def get_content(self):
        content = self.response.content
        return content

    def get_soup(self):
        soup = bs(self.get_content(), 'html.parser')
        return soup
