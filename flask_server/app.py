from flask import Flask
from forms import LoginForm, ProcessOrder, AdjustInventory, ConfirmOrder, DisplayOrders
from flask import Flask, render_template, redirect, url_for, flash, session, request
import crud
import util

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ef3e660493474539abaafc970a7c47f7'

@app.route('/', methods=['GET', 'POST'])
def home():
    print(session)
    if 'credentials' in session:
        session.pop('credentials')
    if 'order' in session:
        session.pop('order')
    print(session)
    return 'Ingrese la dirección con producto y cantidad para procesar'

@app.route('/process_order', methods=['GET', 'POST'])
def order():
    if not 'order' in session:
        session['order'] = {
            'product_id': request.args.get('product_id'),
            'quantity': request.args.get('quantity'),
            'color': request.args.get('color'),
            'size': request.args.get('size')
        }
    if not 'credentials' in session:
        return redirect(url_for('login'))
    else:
        order = session['order']
        session.pop('order')
        result = crud.get_product_info(order)
        price = int(order['quantity']) * result[2]
        on_hand = util.check_inventory(int(order['quantity']), result[3])
        process_order = ProcessOrder()

        return  render_template('order.html', title='Inicio', 
                                order=order, result=result, price=price, 
                                process_order=process_order, on_hand=on_hand)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if request.method == 'POST':
        user_fecth = crud.get_users(login_form.username.data, login_form.password.data)
    
        if user_fecth != 0:
            
            if login_form.validate_on_submit() and login_form.username.data == user_fecth[0] and login_form.password.data == user_fecth[1]:
                flash(f'Ingreso exitoso {user_fecth[0]}', 'success')
                session['credentials'] = {
                    'username': user_fecth[0]
                }
                return redirect(url_for('order'))
        elif login_form.validate_on_submit():
            flash('Nombre de usuario o contraseña incorrectas', 'fail')
            return render_template('login.html', title='Ingresar Credencials de nuevo', form=login_form)
        
    return render_template('login.html', title='Ingresar Credenciales', form=login_form)

@app.route('/inventory_add', methods=['GET', 'POST'])
def inventory_add():

    adjust_inventory = AdjustInventory()

    session['new_inventory'] = {
            'product_id': request.args.get('ref'),
            'quantity': request.args.get('quantity'),
            'original_qty': request.args.get('original_qty'),
            'color': request.args.get('color'),
            'size': request.args.get('size')
        }
    new_product_url = util.create_new_order_url(session['new_inventory'])

    if adjust_inventory.validate_on_submit() and request.method == 'POST':
        result_message = crud.add_inventory(session['new_inventory'], adjust_inventory.new_quantity.data)
        flash(result_message, 'success')
        new_inventory = session['new_inventory']
        session.pop('new_inventory')
        return redirect(url_for('order', 
                                product_id=new_inventory['product_id'], quantity=new_inventory['quantity'], size=new_inventory['size'], color=new_inventory['color'])) 

    return render_template('inventory_add.html', new_inventory=session['new_inventory'], adjust_inventory=adjust_inventory, new_product_url=new_product_url)

@app.route('/cancellation', methods=['GET', 'POST'])
def cancellation():

    return render_template('cancellation.html')


@app.route('/order_confirmation', methods=['GET', 'POST'])
def order_confirmation():
    confirm_order = ConfirmOrder()
    order = {
            'product_id': request.args.get('ref'),
            'quantity': request.args.get('quantity'),
            'color': request.args.get('color'),
            'size': request.args.get('size')
        }
    

    session['data'] = crud.save_order(order)
    saved_data = session['data']
    session.pop('data')

    if request.method == 'POST':

        if confirm_order.validate_on_submit():

            if confirm_order.view_orders.data:
                return redirect(url_for('view_orders'))

    return render_template('order_confirmation.html', confirm_order=confirm_order, order_data=saved_data, confirmed=0)

@app.route('/view_orders', methods=['GET', 'POST'])
def view_orders():
    order_info = []
    forms = []
    orders = crud.get_order_list()
    for order in orders:
        new_form = DisplayOrders()
        new_form.order_id.data = order[0]
        forms.append(new_form)
        order_info.append(
            {
                'order_id': order[0],
                'ref': order[1],
                'talla': order[2],
                'color': order[3],
                'cantidad': order[4],
                'precio': order[5],
                'realizado': 'No realizado' if order[6] == 0 else 'Realizado'
            }
        )
    if request.method == 'POST':
        for form in forms:
            if form.confirm.data:
                message = crud.confirm_order(form.order_id.data)
                flash(message, 'Confirmed_order')
                return redirect(url_for('view_orders', order_info=order_info, forms=forms))
            elif form.delete.data:
                message = crud.delete_order(form.order_id.data)
                flash(message, 'Delete_order')
                return redirect(url_for('view_orders', order_info=order_info, forms=forms))
    else:
        return render_template('view_orders.html', order_info=order_info, forms=forms)



if __name__ == '__main__':
    app.run(debug=True, port=8080)