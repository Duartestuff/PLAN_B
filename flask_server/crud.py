import sqlite3
import traceback

def get_users(username, password):

    conn = sqlite3.connect('../database/users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    if result is not None:
        return result
    else:
        return 0

def get_product_info(order):

    product_id = int(order['product_id'])
    color = order['color']
    size = f'talla_{order['size']}'

    query = f"""
            SELECT products.ref, product_list.descripcion, product_list.precio, {size}
            FROM products
            JOIN product_inventory ON products.inventory_id = product_inventory.inventory_id
            JOIN product_list ON products.ref = product_list.ref
            WHERE products.ref = {product_id} AND products.color = '{color}';
            """

    conn = sqlite3.connect('../database/productos.db')
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result

def add_inventory(new_inventory, new_quantity):

    ref = int(new_inventory['product_id'])
    color = new_inventory['color']
    size = f'talla_{new_inventory['size']}'

    query = f"""
            UPDATE product_inventory
            SET {size} = {new_quantity}
            WHERE inventory_id IN (
                SELECT products.inventory_id
                FROM products
                JOIN product_list ON products.ref = product_list.ref
                WHERE products.ref = {ref} AND products.color = '{color}')
                ;
            """

    try:
        conn = sqlite3.connect('../database/productos.db')
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()

        cursor.close()
        conn.close()
        return f'Cantidad de producto: {ref} con color: {color} y talla: {size}, cambiada a {new_quantity}'
    except Exception as e:
        traceback.print_exc()
        return 'Error cambiando valores en la base de datos'

def save_order(order):

    product_query = f'SELECT precio FROM product_list WHERE ref = {order['product_id']}'

    conn = sqlite3.connect('../database/productos.db')
    cursor = conn.cursor()
    cursor.execute(product_query)
    precio = cursor.fetchone()
    precio_final = precio * int(order['quantity'])
    
    cursor.close()
    conn.close()

    query = f"""
        INSERT INTO orders (ref, color, talla, cantidad, precio, realizado)
        VALUES ({order['product_id']}, {order['color']}, {str(order['size'])}, {int(order['quantity'])}, {precio_final}, 0);
            """

    conn2= sqlite3.connect('../database/orders.db')
    cursor2 = conn2.cursor()
    cursor2.execute(query)
    conn2.commit()

    cursor2.close()
    conn2.close()

    return 'Orden guardada satisfactoriamente'