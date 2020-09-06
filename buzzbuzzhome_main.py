from sqlite import DataRow
from webpage import WebDrive, WebPage
import re

# global var
url = "https://www.buzzbuzzhome.com/us/place/new-york-ny"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15"
}

webdrive = WebDrive()
webdrive.set_headless(True)
cookies = webdrive.get_cookie(url, wait=1)
database = "buzzbuzzhome"

WebPage.headers = headers
WebPage.cookies = cookies


class IndexPage(WebPage):
    """Get all new developments urls on index page

    Args:
        WebPage (string): index page url
    """
    url_count = 0
    def get_new_dev_block(self):
        """Locate the new developments block on index page

        Returns:
            bs4 element: new developments block
        """
        buildings_block = self.get_soup().find(
            'div', {"class": "dev separator"})
        urls_block = buildings_block.findAll('a', {"class": "center"})
        return urls_block
        
    def get_all_urls(self):
        """Parse new developments block to get all urls

        Returns:
            dict: {Building_name: Building_url}
        """
        urls_block = self.get_new_dev_block()
        all_urls = {}
        for i in urls_block:
            all_urls[i.text.strip()] = "https://buzzbuzzhome.com" + i['href']
            IndexPage.url_count += 1
        print("=============================")
        print(f"TOTAL URLS IDENTIFIED: ", IndexPage.url_count)
        return all_urls
        

class DetailPage(WebPage):
    """Parse building's url to extract info

    Args:
        WebPage (string): each building's url
    """
    def get_dev_info(self):
        """Parse building's page html to extract info

        Returns:
            dict: {"name": name, "address": address, "area": area, "type": typ,
                   "units": units, "year": year, "developer": dev, "agency": agency}
        """
        soup = self.get_soup()
    # name
        name = soup.find("title").text.strip().split(" in ")[0].strip()
    # address
        address = ", ".join(section.strip() for section in soup.find('div', {"class": "address-wrapper"}).text.replace("\n", "").split(","))
    # area
        area = soup.find('span', {"class": "hidden-xs"}).findNext('span').find(
            'a').text.strip()
        if area == "New York":
            area = "Manhattan"

        # dev summary
        dev_summary = soup.find('div', {"class": "col-xs-12 dev-summary"})
    # units    
        units = dev_summary.find(
            'span', {"class": "unit-icon"}).findNext('div').text.strip().split("\n")[0].split(" ")[0]
        
        # details table
        details = soup.find('div', {"id": "details"})
    # type    
        typ = details.find('div', text=re.compile(
             ".*Building Type.+")).findNextSibling('div').text.strip()
    # year    
        try:
            year = re.findall(r"\d+", details.find('div', text=re.compile(
            ".*Completed.+")).findNextSibling('div').text.strip())[0]
        except:
            year = None
    # dev
        if len(details.find('div', text=re.compile(
            ".*Builder.+")).findNextSibling('div').findAll('a', {"class": "developer-name"})) == 1:
            dev = details.find('div', text=re.compile(
                ".*Builder.+")).findNextSibling('div').find('a', {"class": "developer-name"}).text.strip()
        else: 
            dev = ", ".join(builder.text.strip() for builder in details.find('div', text=re.compile(
                ".*Builder.+")).findNextSibling('div').findAll('a', {"class": "developer-name"}))
    # agency
        try:
            agency = details.find('div', text=re.compile(
            ".*Marketing.+")).findNextSibling('div').find('a', {"class": "developer-name"}).text.strip()
        except:
            agency = None

        dev_info = {"name": name, "address": address, "area": area, "type": typ,
                    "units": units, "year": year, "developer": dev, "agency": agency}

        # print("FINISH ", name)
        return dev_info



if __name__ == "__main__":
    row_saved = 0
    all_urls = IndexPage(url).get_all_urls()
    commit_count = 0
    for building in all_urls:
        datarow = DataRow(DetailPage(all_urls[building]).get_dev_info())
        datarow.write_sqlite(database)
        datarow.commit_sqlite(database)
        row_saved += 1
        print(
            f"{datarow.name} SAVED. TOTAL SAVED: {row_saved} / {IndexPage.url_count}.")
    print("======== FINISHED ========")


# test block
# test_url = "https://www.buzzbuzzhome.com/us/3904-29th-street"
# print(DetailPage(test_url).get_dev_info())





