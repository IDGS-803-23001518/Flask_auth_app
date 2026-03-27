from flask import Blueprint, render_template, current_app
from flask_security import login_required, current_user
from flask_security.decorators import roles_required
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

# ← Manejadores de error globales
@main.app_errorhandler(404)
def not_found(e):
    current_app.logger_app.warning(f"ERROR 404 | ruta='{e}' | url={e}")
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def server_error(e):
    current_app.logger_app.error(f"ERROR 500 | detalle='{e}'")
    return render_template('500.html'), 500

# flask --app project:create_app run --debug