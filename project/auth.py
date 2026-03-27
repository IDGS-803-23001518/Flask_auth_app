from flask import Flask, render_template, Blueprint, url_for, redirect, request, flash, current_app
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
    logger = current_app.logger_app
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        
        logger.warning(
            f"LOGIN FALLIDO | email='{email}' | ip={request.remote_addr}"
        )
        flash('El correo o la contraseña son incorrectas')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    
    logger.info(
        f"LOGIN EXITOSO | id={user.id} | email='{user.email}' | ip={request.remote_addr}"
    )
    return redirect(url_for('main.profile'))

@auth.route('/register')
def register():
    return render_template('/security/register.html')

@auth.route('/register', methods=['POST'])
def register_post():
    logger = current_app.logger_app
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        logger.warning(
            f"REGISTRO FALLIDO | email ya existente='{email}' | ip={request.remote_addr}"
        )
        flash('Ese correo electronico ya existe')
        return redirect(url_for('auth.register'))

    new_user = user_datastore.create_user(
        name=name, email=email,
        password=generate_password_hash(password, method='pbkdf2:sha256')
    )
    db.session.commit()

    logger.info(
        f"REGISTRO EXITOSO | id={new_user.id} | email='{email}' | nombre='{name}' | ip={request.remote_addr}"
    )
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    from flask_security import current_user
    logger = current_app.logger_app
    logger.info(
        f"LOGOUT | id={current_user.id} | email='{current_user.email}'"
    )
    logout_user()
    return redirect(url_for('auth.login'))