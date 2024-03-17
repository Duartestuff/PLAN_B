SELECT products.ref, product_list.descripcion, product_list.precio, talla_10
FROM products
JOIN product_inventory ON products.inventory_id = product_inventory.inventory_id
JOIN product_list ON products.ref = product_list.ref
WHERE products.ref = 588 AND products.color = 'Cafe';