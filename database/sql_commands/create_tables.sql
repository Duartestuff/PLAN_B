CREATE TABLE IF NOT EXISTS product_list (

    ref INTEGER PRIMARY KEY NOT NULL,
    descripcion VARCHAR(100) NOT NULL,
    precio INTEGER NOT NULL

);


CREATE TABLE IF NOT EXISTS product_inventory (

    inventory_id VARCHAR(10) PRIMARY KEY NOT NULL,
    talla_6 INTEGER,
    talla_8 INTEGER,
    talla_10 INTEGER,
    talla_12 INTEGER,
    talla_14 INTEGER,
    talla_16 INTEGER,
    talla_18 INTEGER,
    talla_XS INTEGER,
    talla_S INTEGER,
    talla_M INTEGER,
    talla_L INTEGER,
    talla_XL INTEGER,
    talla_XXL INTEGER

);

CREATE TABLE IF NOT EXISTS products (

    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    ref INTEGER NOT NULL,
    color VARCHAR(100) NOT NULL,
    inventory_id VARCHAR(10),
    FOREIGN KEY (ref) REFERENCES product_list(ref),
    FOREIGN KEY (inventory_id) REFERENCES product_inventory(inventory_id)
);

CREATE TABLE IF NOT EXISTS orders (

    order_id VARCHAR(10) PRIMARY KEY NOT NULL,
    ref INTEGER NOT NULL,
    talla VARCHAR(100) NOT NULL,
    color VARCHAR(100) NOT NULL,
    cantidad INTEGER,
    precio INTEGER,
    realizado INTEGER CHECK(realizado IN(0, 1)),
    FOREIGN KEY (ref) REFERENCES products(ref),
    FOREIGN KEY (color) REFERENCES products(color)
);