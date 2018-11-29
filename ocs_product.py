import json

from db import DBReader

class OCSProduct:
    def __init__(self, attr):
        valid_attr = [
                'id',
                'vendor',
                'strain',
                'product_type',
                'subcategory',
                'subsubcategory',
                'plant_type',
                'cbd_min',
                'cbd_max',
                'thc_min',
                'thc_max',
                'ocs_created_at',
                'ocs_published_at',
                'ocs_updated_at',
                'removed',
                'url',
                'variants'
                ]
        for a in valid_attr:
            setattr(self, a, None)
        for k, v in attr.items():
            if k in valid_attr:
                setattr(self, k, v)

    @classmethod
    def from_db(cls, database, pid):
        if type(database) is DBReader:
            db = database
        else:
            db = DBReader(database)
        return cls(db.get_product(pid))

