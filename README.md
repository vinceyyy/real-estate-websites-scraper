# Real Estate Listings Website Scraper

A scraper for streeteasy.com, buzzbuzzhome.com, and cityrealty.com.

This is my first Object Oriented Programming project. 

The first part, streeteasy.com scraper, was originally written as Process Oriented Program. After it was done and tested, I realized that I have to write similar code for the other two website, therefore I decided to rewrite the whole project using OOP.

### Dependency
#### undetected-chromedriver
* https://github.com/ultrafunkamsterdam/undetected-chromedriver
* Super helpful. 
* Streeteasy uses Distil anti-scraping and oh boy ain't that powerful. I struggled two days, getting detected everytime using requests, and CAPTCHA a million times using selenium. With undetected-chromedriver I still get CAPTCHA here or there, but after manually solving it the cookie works for several minutes with is enough for this size of scraping. 

#### requests
* For http requests.
* Obviously.


#### beautifulsoup
* For parsing html.
* Obviously.

### Modules
#### webpage.py
* Using undetected-chromedriver to get cookies, and send http requests with it.

#### sqlite.py
* Receive dict data and write them into sqlite.
* From: {"name": name, "address": address, "area": area, "type": typ,
                    "units": units, "year": year, "developer": dev, "agency": agency} 
* To: 
  
                id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                name        TEXT UNIQUE,
                address     TEXT,
                units       INTEGER,
                year        INTEGER,
                area_id     INTEGER,
                developer_id        INTEGER,    
                type_id     INTEGER,
                agency_id      INTEGER,
                FOREIGN KEY (area_id) REFERENCES Area(id),
                FOREIGN KEY (developer_id) REFERENCES Developer(id),
                FOREIGN KEY (type_id) REFERENCES Type(id),
                FOREIGN KEY (agency_id) REFERENCES Agency(id)