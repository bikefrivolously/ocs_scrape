#!/usr/bin/env python3

import json
import sys

def

def main():
    if len(sys.argv) != 2:
        sys.exit(1)

    fn = sys.argv[1]

    all_handles = set()

    with open(fn) as f:
        js = json.load(f)
        products = js['products']
        for p in products:
            all_handles.add(p['handle'])

    for h in all_handles:
        print('https://ocs.ca/products/{}'.format(h))

if __name__ == '__main__':
    main()
