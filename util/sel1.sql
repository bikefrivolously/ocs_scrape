SELECT p.vendor, p.strain, v.weight, vs.price, vs.time
FROM product AS p
JOIN product_variant as pv
ON p.id = pv.product_id
JOIN variant as v
ON v.id = pv.variant_id
JOIN variant_stock AS vs
ON vs.id = v.id
;
