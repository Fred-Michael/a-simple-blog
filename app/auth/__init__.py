from flask import Blueprint

bp = Blueprint('auth', __name__, template_folder="auth_templates")

from app.auth import routes
