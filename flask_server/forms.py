from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(2, 50)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class ProcessOrder(FlaskForm):
    add_inventory = SubmitField('Añadir inventario')
    create_order = SubmitField('Crear pedido')
    cancel_order = SubmitField('Cancelar pedido')

class AdjustInventory(FlaskForm):
    new_quantity = IntegerField('Nuevo inventario', validators=[InputRequired(), NumberRange(min=1)])
    submit = SubmitField('Cambiar inventario')

class ConfirmOrder(FlaskForm):
    confirm = SubmitField('Confirmar pedido')
    view_orders = SubmitField('Ver lista de pedidos')

class DisplayOrders(FlaskForm):
    order_id = StringField('Order_id')
    confirm = SubmitField('Confirmar orden')
    delete = SubmitField('Cancelar orden')