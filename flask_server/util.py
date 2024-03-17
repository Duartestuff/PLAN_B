def check_inventory(quantity, inventory):
    if inventory < quantity:
        return False
    else:
        return True
    
def create_new_order_url(data):

    return f'/process_order?product_id={data['product_id']}&quantity={data['quantity']}&size={data['size']}&color={data['color']}'
