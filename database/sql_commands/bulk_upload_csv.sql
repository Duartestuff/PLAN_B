.mode csv
.separator ;
PRAGMA foreign_keys=OFF;
.import originalFiles/product_list.csv product_list
.import originalFiles/product_inventory.csv product_inventory
.import originalFiles/products.csv products
PRAGMA foreign_keys=ON;