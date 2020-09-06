from sqlite import DataRow
from webpage import WebDrive, WebPage
import re


# global var
url = "https://streeteasy.com/buildings/nyc/new_development:new%20development%7Carea:100,300,400,200"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15"
}
webdrive = WebDrive()
webdrive.set_headless(False)
cookies = webdrive.get_cookie("https://streeteasy.com", wait=1)
database = "streeteasy"


WebPage.headers = headers
WebPage.cookies = cookies


class IndexPage(WebPage):
    """Index page on streeteasy.com

    Args:
        WebPage (string): index page url
    """
    url_count = 0
    # find the maxium page number
    def get_max_page(self):
        """Find the maximum page for this section.

        Returns:
            int: maximun page number
        """
        nav = self.get_soup().findAll('span', {"class": "page"})
        page_index = []
        for page in nav:
            page_index.append(page.text.strip())
        max_page = page_index[len(page_index)-1]
        return int(max_page)

    def get_all_page_urls(self):
        """Generate all index page urls

        Returns:
            list: all index page urls as a list
        """
        # create pages url list
        page_urls_list = []
        for i in range(1, int(self.get_max_page())+1):
            page_url = f"https://streeteasy.com/buildings/nyc/new_development:new%20development%7Carea:100,300,400,200?page={i}"
            page_urls_list.append(page_url)
        print("All pages identified, max page = ", self.get_max_page())
        return page_urls_list

    # def get_single_page_urls(self, page_num):
    #     single_page_urls = []
    #     if page_num <= self.get_max_page():
    #         page_url = self.get_all_page_urls()[page_num - 1]
    #         single_page = WebPage(page_url)
    #         building_url_list = single_page.get_soup().findAll(
    #             'a', {"se:clickable:target": "true"})
    #         for building in building_url_list:
    #             building_url = "https://streeteasy.com" + building.get("href")
    #             single_page_urls.append(building_url)
    #         return single_page_urls
    #     else:
    #         print("!!!EXCEEDED MAXIMUM PAGE!!!")

    def get_all_urls(self):
        """Get all building urls from all index pages.

        Returns:
            dict: {"page 1": [url1, url2, url3 ...], "page 2": [...], ...}
        """
        all_url_list = {}
        page_count = 0
        for page_url in self.get_all_page_urls():
            single_page_urls = []
            page_count += 1
            building_url_list = WebPage(page_url).get_soup().findAll(
                'a', {"se:clickable:target": "true"})
            for building in building_url_list:
                building_url = "https://streeteasy.com" + building.get("href")
                single_page_urls.append(building_url)
                IndexPage.url_count += 1
            all_url_list[f"page {page_count}"] = single_page_urls
            print(f"Retrived all url on page {page_count}")
        print("=============================")
        print(f"RETRIVED ALL URLS FOR {page_count} PAGES")
        print(f"TOTAL URLS IDENTIFIED: ", IndexPage.url_count)
        return all_url_list


class DetailPage(WebPage):
    """Each building's page.

    Args:
        WebPage (string): each building's url
    """

    num_of_page = 0
    def __init__(self, url):
        DetailPage.num_of_page += 1
        super().__init__(url)
        

    def get_dev_info(self):
        """Parse building's page html to extract info

        Returns:
            dict: {"name": name, "address": address, "area": area, "type": typ,
                    "units": units, "year": year, "developer": dev, "agency": agency}
        """
        
        soup = self.get_soup()
        # name
        try:
            name = soup.find('title').text.strip().split(":")[0].strip()
        except:
            print("!!!DETECTED!!!")
            exit()
        # address
        try:
            address = soup.find(
                'span', {'class': "Text u-color-white"}).text.strip()
        except:
            address = soup.find('h2', {'class': "subtitle"}).text.strip()
        # area
        area = address.split(",")[len(address.split(","))-3].strip()
        # type
        try:
            plain = soup.findAll('div', {"class": "details_info"})
            typ = plain[1].find('a').text
            if " " in typ:
                typ = typ.split(" ")[0]
        except:
            typ = soup.find(
                'a', {"class": "NewDevelopmentPremium-detailLink"}).text.strip()
            try:
                typ = typ.split(" ")[0]
            except:
                pass
        # fact table
        facts_table = soup.find(
            'table', {"class": "clean_table legible"}).findAll('td')
        # units
        try:
            units = int(soup.find(
                'span', {'class': "detail_cell first_detail_cell"}).text.split(" ")[0])
        except:
            units = None
        # year
        try:
            year = soup.find('span', text=re.compile(
                'Built in.+')).text.split(" ")[2]
        except:
            year = None
        # dev
        try:
            dev = soup.find(
                "td", text="Developer:").next_sibling.next_sibling.get_text().strip()
        except:
            dev = None
        # agency
        try:
            agency = soup.find(
                "td", text=re.compile('.+ and marketing:')).next_sibling.next_sibling.get_text().strip()
        except:
            agency = None

        dev_info = {"name": name, "address": address, "area": area, "type": typ,
                    "units": units, "year": year, "developer": dev, "agency": agency}

        # print("FINISH ", name)
        return dev_info


if __name__ == "__main__":
    all_urls = IndexPage(url).get_all_urls()
    for page in all_urls:
        for url in all_urls[page]:
            datarow = DataRow(DetailPage(url).get_dev_info())
            datarow.write_sqlite(database)
            print(f"{datarow.name},  SAVED. TOTAL SAVED: {DetailPage.num_of_page} / {IndexPage.url_count}")
        print(f"{page} FINISHED".upper())


