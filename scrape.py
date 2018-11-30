#!/usr/bin/env python3

from ocs_scraper import OCSScraper
from db import DBWriter

def main():
    s = OCSScraper('https://ocs.ca')
    d = DBWriter('ocs_v1.db')
    s.get_products()
    for p in s.products:
        p.to_db(d)

if __name__ == '__main__':
    main()
