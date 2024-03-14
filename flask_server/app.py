from flask import Flask
from forms import LoginForm
from flask import Flask, render_template, redirect, url_for, flash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ef3e660493474539abaafc970a7c47f7'

#credenciales de muestra para el login form
credentials = {
    'username': 'Admin',
    'password': 'Proyecto123',
    'logged': True
}

@app.route('/')
def home():
    if not credentials['logged']:
        return redirect(url_for('login'))
    else:
        return  render_template('home.html', title='Inicio')

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        print('Ingreso')
        flash('Ingreso exitoso', 'success')
        return redirect(url_for('home'))
    return render_template('login.html', title='Ingresar Credenciales', form=login_form)

if __name__ == '__main__':
    app.run(debug=True, port=8080)