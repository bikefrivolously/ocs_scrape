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
            
            vids = c.execute("SELECT variant_id FROM product_variant WHERE product_id = ?", (pid,)).fetchall()
            for vid in vids:
                c.execute("SELECT * FROM variant WHERE id = ?", (vid,))
                variant = dict((c.description[i][0], val) for i, val in enumerate(c.fetchone()))
                
                c.execute('''SELECT price, quantity, time FROM variant_stock WHERE id = ? AND 
                    time = (SELECT MAX(time) FROM variant_stock WHERE id = ?)''', (vid, vid))
                price, quantity, t = c.fetchone()
                variant['price'] = price
                variant['quantity'] = quantity
                variant['time'] = t
                prod['variants'].append(variant)

        c.close()
        print(prod)
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
        pass
