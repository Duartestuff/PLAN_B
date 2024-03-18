import sqlite3
import traceback
import secrets

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

    order_id = secrets.token_hex(5)
    product_query = f'SELECT precio FROM product_list WHERE ref = {order['product_id']}'

    conn = sqlite3.connect('../database/productos.db')
    cursor = conn.cursor()
    cursor.execute(product_query)
    precio = cursor.fetchone()
    precio_final = precio[0] * int(order['quantity'])
    
    cursor.close()
    conn.close()

    ref = int(order['product_id'])
    talla = f'talla_{order['size']}'
    color = order['color']
    cantidad = int(order['quantity'])

    print(ref, talla, color, cantidad, precio_final)

    query = f"""
        INSERT INTO orders (order_id, ref, talla, color, cantidad, precio, realizado)
        VALUES ('{order_id}', {ref}, '{talla}', '{color}', {cantidad}, {precio_final}, 0);
            """

    conn2= sqlite3.connect('../database/productos.db')
    cursor2 = conn2.cursor()
    cursor2.execute(query)
    conn2.commit()

    cursor2.close()
    conn2.close()

    return {
        'message': f'Orden {order_id} guardada satisfactoriamente',
        'order': get_order(order_id),
        'order_id': order_id,
        'saved': 0
    }

def get_order(id):

    query = f"SELECT ref, talla, color, cantidad, precio, realizado FROM orders WHERE order_id='{id}'"

    conn = sqlite3.connect('../database/productos.db')
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()

    realizado = ''
    if result[5] == 0:
        realizado = 'No realizado'
    elif result[5] == 1:
        realizado = 'Realizado'

    order = {
        'ref': result[0],
        'talla': result[1],
        'color': result[2],
        'cantidad': result[3],
        'precio': result[4],
        'realizado': realizado,
    }

    cursor.close()
    conn.close()

    return order

def confirm_order(id):

    order = get_order(id)

    product_qty_query = f"""
            SELECT {order['talla']}
            FROM products
            JOIN product_inventory ON products.inventory_id = product_inventory.inventory_id
            JOIN product_list ON products.ref = product_list.ref
            WHERE products.ref = {order['ref']} AND products.color = '{order['color']}';
            """

    conn = sqlite3.connect('../database/productos.db')
    cursor = conn.cursor()
    cursor.execute(product_qty_query)

    product_qty = cursor.fetchone()
    new_quantity = product_qty[0] - order['cantidad']

    modify_inventory = f"""
            UPDATE product_inventory
            SET {order['talla']} = {new_quantity}
            WHERE inventory_id IN (
                SELECT products.inventory_id
                FROM products
                JOIN product_list ON products.ref = product_list.ref
                WHERE products.ref = {order['ref']} AND products.color = '{order['color']}');
            """
    cursor.execute(modify_inventory)
    conn.commit()
    cursor.close()
    conn.close()

    close_order(id)

    return 'Orden realizada con éxito'

def close_order(id):

    query = f"UPDATE orders SET realizado = 1;"

    conn = sqlite3.connect('../database/productos.db')
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()
    
def get_order_list():

    query = 'SELECT * FROM orders;'

    conn = sqlite3.connect('../database/productos.db')
    cursor = conn.cursor()
    cursor.execute(query)

    result = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return result

def delete_order(id):

    query = f"DELETE FROM orders WHERE order_id = '{id}'"

    conn = sqlite3.connect('../database/productos.db')
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()

    return f'Pedido {id} borrado'