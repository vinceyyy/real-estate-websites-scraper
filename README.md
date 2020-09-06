# Real Estate Listings Website Scraper

A scraper for scraping developments's information from streeteasy.com and buzzbuzzhome.com ~~and cityrealty.com~~. By default the collected developments' info includes name, adress, units, year, area, developer, type and the marketing agency.

(This is my first Object Oriented Programming project. The first part, streeteasy.com scraper, was originally written as Process Oriented Program. After it was done and tested, I realized that I have to write similar code for every website, therefore I decided to rewrite the whole project using OOP.)

## Dependency
### undetected-chromedriver
* https://github.com/ultrafunkamsterdam/undetected-chromedriver
* Super helpful. 
* Streeteasy uses Distil anti-scraping and oh boy ain't that powerful. I struggled two days, getting detected everytime using requests, and CAPTCHA a million times using selenium. With undetected-chromedriver I still get CAPTCHA here or there, but after manually solving it the cookie works for several minutes with is enough for this size of scraping. 

### Requests
* For http requests.
* Obviously.

### beautifulsoup
* For parsing html.
* Obviously.

## Modules
### webpage.py
* Using undetected-chromedriver to get cookies, and send http requests with it.

### sqlite.py
* Receive dict data and write them into sqlite.
* Do what you want with this part. I was trying to practice my SQL skill.
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

## How to use
1. Change the urls in two main.py files to the urls you want to scrape from.
2. Run it.
3. For buzzbuzzhome.com:
  * Done.
4. For Streeteasy.com:
  1. Make thru the nightmare CAPTCHA.
  2. Wait for it running until get busted by CAPTCHA.
  3. Make thru the nightmare CAPTCHA aging.