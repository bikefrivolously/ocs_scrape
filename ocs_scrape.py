#!/usr/bin/env python3

import json
import requests
import datetime
from time import sleep
import re

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'
SITE = 'https://ocs.ca'
PRODUCTS_JSON = '/products.json'
DELAY = 1

REFRESH_FILE = 'refresh_time.txt'
RE_QUANTITIES = r'''var inventory_quantities = {((?:\d+: \d+,?){1,})};'''

def get_variant_quantities(product_urls):
    quantities = {}
    with requests.Session() as s:
        for url in product_urls:
            print('Requesting page {}'.format(url))
            r = s.get(url)
            match = re.search(RE_QUANTITIES, r.text)
            if match:
               q = match.group(1)
               print(q)
               for variant in q.split(','):
                   vid, quantity = variant.split(': ')
                   quantities[int(vid)] = int(quantity)
            sleep(DELAY)
    return quantities

def product_urls(products, language='en'):
    if language == 'en':
        filter_lang = 'language--en'
    elif language == 'fr':
        filter_lang = 'language--fr'


    all_handles = set()
    
    for p in products:
        if not filter_lang or filter_lang in p['tags']:
            all_handles.add(p['handle'])

        else:
            print('Skipped {} due to language filter'.format(p['handle']))

    for h in all_handles:
        yield 'https://ocs.ca/products/{}'.format(h)

def get_all_products(limit=float("inf")):
    all_products = []
    url = SITE + PRODUCTS_JSON
    page = 1
    with requests.Session() as s:
        r = s.get(url, params={'page': page})
        while r.ok and r.json()['products']:
            products = r.json()['products']
            print('Found {} products on page {}'.format(len(products), page))
            all_products.extend(products)
            page += 1
            if page > limit:
                break
            sleep(DELAY)
            r = s.get(url, params={'page': page})
    return all_products

def store_refresh_time(t):
    with open(REFRESH_FILE, 'w') as f:
        f.write(str(t.timestamp()))

def get_refresh_time():
    with open(REFRESH_FILE, 'r') as f:
        t = f.readline()
        try:
            t = float(t)
        except ValueError:
            print('No previous refresh time available or invalid value stored in {}'.format(REFRESH_FILE))
            return None

    return datetime.datetime.fromtimestamp(t, tz=datetime.timezone.utc)

def find_updated(products, since):
    if since is None:
        return products

    updated = []
    
    for p in products:
        if 'updated_at' in p:
            ut = datetime.datetime.strptime(p['updated_at'], '%Y-%m-%dT%H:%M:%S%z')
            print(ut, since)
            if ut > since:
                updated.append(p)
    return updated

def main():
    start_time = datetime.datetime.now(datetime.timezone.utc)
    dt = start_time.isoformat(timespec='seconds')
    prev_refresh = get_refresh_time()

    fn = 'products_' + dt + '.json'
    all_products = get_all_products()
    print('Found {} products'.format(len(all_products)))
    with open(fn, 'w') as f:
        json.dump(all_products, f)
    
    updated = find_updated(all_products, prev_refresh)
    print('Found {} products updated since {}'.format(len(updated), prev_refresh))

    fn = 'quantities_' + dt + '.json'
    urls = list(product_urls(updated))
    quantities = get_variant_quantities(urls)
    with open(fn, 'w') as f:
        json.dump(quantities, f)

    store_refresh_time(start_time)




if __name__ == '__main__':
    main()
