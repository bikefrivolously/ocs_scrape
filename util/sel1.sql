SELECT p.vendor, p.strain, v.weight, vs.price, vs.available, vs.time
FROM product AS p
JOIN variant as v
ON v.product_id = p.id
JOIN variant_stock AS vs
ON vs.id = v.id
;
