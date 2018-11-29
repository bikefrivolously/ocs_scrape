import datetime
import requests
from time import sleep

from ocs_product import OCSProduct

class OCSScraper:
    DELAY = 1

    def __init__(self, url):
        self.url = url
        self.products = []

    def get_products(self):
        url = self.url + '/products.json'
        page = 1
        self.time = datetime.datetime.now(datetime.timezone.utc)
        with requests.Session() as s:
            r = s.get(url, params={'page': page})
            while r.ok and r.json()['products']:
                products = r.json()['products']
                print('Found {} products on page {}'.format(len(products), page))
                for p in self.filter(products, lang='en', product_type='dried_flower'):
                    self.products.append(OCSProduct(p))            
                page += 1
                sleep(self.DELAY)
                r = s.get(url, params={'page': page})


    def filter(self, products, lang=None, product_type=None):
        if lang == 'en':
            filter_lang = 'language--en'
        elif lang == 'fr':
            filter_lang = 'language--fr'
        else:
            filter_lang = None

        if product_type == 'dried_flower':
            filter_type = 'subcategory--Dried Flower'
        else:
            filter_type = None

        print('filter:', filter_lang, filter_type)

        for p in products:
            if (filter_lang is None or filter_lang in p['tags']) and (filter_type is None or filter_type in p['tags']):
                    d = {}
                    d['id'] = p['id']
                    d['vendor'] = p['vendor']
                    d['strain'] = p['title']
                    d['product_type'] = p['product_type']
                    d['subcategory'] = next((t.rsplit('--', maxsplit=1)[1] for t in p['tags'] if t.startswith('subcategory--')))
                    d['subsubcategory'] = next((t.rsplit('--', maxsplit=1)[1] for t in p['tags'] if t.startswith('subsubcategory--')))
                    d['plant_type'] = next((t.rsplit('--', maxsplit=1)[1] for t in p['tags'] if t.startswith('plant_type--')))
                    d['cbd_min'] = next((t.rsplit('--', maxsplit=1)[1] for t in p['tags'] if t.startswith('cbd_content_min--')))
                    d['cbd_max'] = next((t.rsplit('--', maxsplit=1)[1] for t in p['tags'] if t.startswith('cbd_content_max--')))
                    d['thc_min'] = next((t.rsplit('--', maxsplit=1)[1] for t in p['tags'] if t.startswith('thc_content_min--')))
                    d['thc_max'] = next((t.rsplit('--', maxsplit=1)[1] for t in p['tags'] if t.startswith('thc_content_max--')))
                    d['ocs_created_at'] = datetime.datetime.strptime(p['created_at'], '%Y-%m-%dT%H:%M:%S%z')
                    d['ocs_published_at'] = datetime.datetime.strptime(p['published_at'], '%Y-%m-%dT%H:%M:%S%z')
                    d['ocs_updated_at'] = datetime.datetime.strptime(p['updated_at'], '%Y-%m-%dT%H:%M:%S%z')
                    d['url'] = self.url + '/products/' + p['handle']
                    d['variants'] = []
                    for v in p['variants']:
                        e = {}
                        e['id'] = int(v['id'])
                        e['title'] = v['title']
                        try:
                            e['weight'] = float(v['option1'][:-1])
                        except ValueError:
                            e['weight'] = 0.0
                        e['sku'] = v['sku']
                        e['available'] = v['available']
                        e['ocs_created_at'] = datetime.datetime.strptime(v['created_at'], '%Y-%m-%dT%H:%M:%S%z')
                        e['ocs_updated_at'] = datetime.datetime.strptime(v['updated_at'], '%Y-%m-%dT%H:%M:%S%z')
                        e['price'] = float(v['price'])
                        e['time'] = self.time
                        d['variants'].append(e)
                    yield d
