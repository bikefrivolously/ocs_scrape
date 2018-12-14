CREATE TABLE product (
id INTEGER PRIMARY KEY,
vendor TEXT,
strain TEXT,
product_type TEXT,
subcategory TEXT,
subsubcategory TEXT,
plant_type TEXT,
ocs_created_at DATETIME,
ocs_published_at DATETIME,
ocs_updated_at DATETIME,
removed BOOLEAN,
url TEXT
);
CREATE TABLE product_attributes (
id INTEGER,
cbd_min REAL,
cbd_max REAL,
thc_min REAL,
thc_max REAL,
time DATETIME
);
CREATE TABLE variant (
id INTEGER PRIMARY KEY,
product_id INTEGER,
title TEXT,
weight REAL,
sku INTEGER,
ocs_created_at DATETIME,
ocs_updated_at DATETIME
);
CREATE TABLE variant_stock (
id INTEGER,
price REAL,
quantity INTEGER,
available BOOLEAN,
time DATETIME
);
