#!/usr/bin/env python3

import sqlite3

db1 = sqlite3.connect('ocs_v1.db')
db2 = sqlite3.connect('ocs_v2.db')

c1 = db1.cursor()
c2 = db2.cursor()

# Just straight up copy over the products table
print('Copying "products"')
rows = c1.execute('''SELECT * from product''').fetchall()
c2.executemany('''INSERT INTO product VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', rows)
print('Done')

print('Copying "product_attributes"')
# Copy over product_attributes
rows = c1.execute('''SELECT * from product_attributes''').fetchall()
c2.executemany('''INSERT INTO product_attributes VALUES (?, ?, ?, ?, ?, ?)''', rows)
print('Done')


# variant
# drop the available column
# add the product_id column
print('Copying "variant"')
rows = c1.execute('''SELECT id, title, weight, sku, ocs_created_at, ocs_updated_at FROM variant''').fetchall()
for var in rows:
    vid = var[0]
    pid = c1.execute('''SELECT product_id FROM product_variant WHERE variant_id = ?''', (vid,)).fetchone()[0]
    print('For vid {}, found pid {}'.format(vid, pid))
    new_row = list(var)
    new_row.append(pid)
    print('new_row: {}'.format(new_row))
    c2.execute('''INSERT INTO variant (id, title, weight, sku, ocs_created_at, ocs_updated_at, product_id) VALUES (?, ?, ?, ?, ?, ?, ?)''', new_row)
print('Done')

# variant_stock
# Add in the available column as default False
print('Copying variant_stock')
rows = c1.execute('''SELECT * from variant_stock''').fetchall()
for r in rows:
    new_row = list(r)
    new_row.append(False)
    print('new_row: {}'.format(new_row))
    c2.execute('''INSERT INTO variant_stock (id, price, quantity, time, available) VALUES (?, ?, ?, ?, ?)''', new_row)
print('Done')

# Commit the changes to the new DB
db2.commit()

c1.close()
db1.close()
c2.close()
db2.close()
