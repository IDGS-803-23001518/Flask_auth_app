from flask import Flask, render_template, Blueprint, url_for, redirect, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required
from flask_security.utils import login_user, logout_user

from .models import User
from . import db, user_datastore

auth = Blueprint('auth', __name__, url_prefix='/security')

@auth.route('/login')
def login():
    return render_template('/security/login.html')

@auth.route('/login', methods=['POST'])

def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    #Consultamos si existe un usuario
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('El correo o la contraseña son incorrectas')
        return redirect(url_for('auth.login'))
    
    #Logueamos al usuario
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/register')
def register():
    return render_template('/security/register.html')

@auth.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    #Consultar si existe un usuario con ese email
    user = User.query.filter_by(email=email).first()

    if user:
        flash('Ese correo electronico ya existe')
        return redirect(url_for('auth.register'))
    
    user_datastore.create_user(name=name, email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
    db.session.commit()
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    #Cerramos la sesion
    logout_user()
    return redirect(url_for('main.login'))
