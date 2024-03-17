UPDATE product_inventory
SET talla_10 = 15
WHERE inventory_id IN (
    SELECT products.inventory_id
    FROM products
    JOIN product_list ON products.ref = product_list.ref
    WHERE products.ref = 588 AND products.color = 'Cafe'

);