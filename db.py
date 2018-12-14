import sqlite3

class DBReader:
    def __init__(self, database):
        self.database = database

        self.conn = sqlite3.connect(self.database)

    def get_product(self, pid):
        '''
        Query the database for a product ID and return an instance of the OCSProduct class
        '''
        c = self.conn.cursor()
        
        c.execute("SELECT * FROM product WHERE id = ?", (pid,))
        prod = c.fetchone()
        if prod:
            prod = dict((c.description[i][0], val) for i, val in enumerate(prod))
            prod['variants'] = []
            
            #vids = c.execute("SELECT variant_id FROM product_variant WHERE product_id = ?", (pid,)).fetchall()
            #for vid in vids:
            variants = c.execute("SELECT * FROM variants WHERE product_id =?", (pid,)).fetchall()
            for v in variants:
                vid = v[0]
                #c.execute("SELECT * FROM variant WHERE id = ?", (vid,))
                variant = dict((c.description[i][0], val) for i, val in enumerate(v))
                
                c.execute('''SELECT price, quantity, available, time FROM variant_stock WHERE id = ? AND 
                    time = (SELECT MAX(time) FROM variant_stock WHERE id = ?)''', (vid, vid))
                price, quantity, available, t = c.fetchone()
                variant['price'] = price
                variant['quantity'] = quantity
                variant['available'] = available
                variant['time'] = t
                prod['variants'].append(variant)

        c.close()
        #print(prod)
        return prod

    def get_product_ids(self):
        c = self.conn.cursor()
        c.execute("SELECT id FROM product")
        products = c.fetchall()
        c.close()
        return products


class DBWriter:
    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(self.database)

    def write(self, product):
        '''
        product: OCSProduct type
        '''
        rc = self.conn.cursor()
        rc.execute("SELECT * FROM product WHERE id = ?", (product.id,))
        existing = rc.fetchone()
        if existing:
            # The product already exists so UPDATE
            #print(product.id, 'product exists. Updating.')
            #print(existing)
            #print(product)
            rc.execute('''UPDATE product
                SET vendor = ?, strain = ?, product_type = ?, subcategory = ?,
                subsubcategory = ?, plant_type = ?,
                ocs_created_at = ?, ocs_published_at = ?, ocs_updated_at = ?,
                removed = ?, url = ? 
                WHERE id = ?''', 
                (product.vendor, product.strain, product.product_type,
                product.subcategory, product.subsubcategory, product.plant_type,
                product.ocs_created_at, product.ocs_published_at, product.ocs_updated_at,
                product.removed, product.url, product.id))
        else:
            #print(product.id, 'adding to database.')
            rc.execute(
                    '''INSERT INTO product VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (product.id, product.vendor, product.strain, product.product_type,
                    product.subcategory, product.subsubcategory, product.plant_type,
                    product.ocs_created_at, product.ocs_published_at, product.ocs_updated_at,
                    product.removed, product.url))
        rc.execute('''INSERT INTO product_attributes VALUES(?, ?, ?, ?, ?, ?)''', (
            product.id, product.cbd_min, product.cbd_max, product.thc_min, product.thc_max, product.scrape_time))

        for v in product.variants:
            rc.execute("SELECT * FROM variant WHERE id = ?", (v['id'],))
            existing = rc.fetchone()
            if existing:
                #print(v['id'], 'variant exists. Updating.')
                #print(existing)
                #print(v)
                rc.execute(
                        '''UPDATE variant
                        SET product_id = ?, title = ?, weight = ?, sku = ?, ocs_created_at = ?, ocs_updated_at = ?
                        WHERE id = ?''',
                        (product.id, v['title'], v['weight'], v['sku'], v['ocs_created_at'], v['ocs_updated_at'], v['id'])
                        )
            else:
                rc.execute(
                        '''INSERT INTO variant VALUES (?, ?, ?, ?, ?, ?, ?)''',
                        (v['id'], product.id, v['title'], v['weight'], v['sku'], v['ocs_created_at'], v['ocs_updated_at'])
                        )
            rc.execute('''INSERT INTO variant_stock (id, price, available, time) VALUES (?, ?, ?, ?)''',
                    (v['id'], v['price'], v['available'], v['time']))
        
        # TODO: clean up the variant table.. flag any unused variants for removal?
        
        self.conn.commit()

