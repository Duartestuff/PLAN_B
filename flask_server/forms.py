from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(2, 50)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class ProcessOrder(FlaskForm):
    add_inventory = SubmitField('Añadir inventario')
    create_order = SubmitField('Crear orden')
    cancel_order = SubmitField('Cancelar orden')

class AdjustInventory(FlaskForm):

    new_quantity = IntegerField('Nuevo inventario', validators=[InputRequired(), NumberRange(min=1)])
    submit = SubmitField('Cambiar inventario')