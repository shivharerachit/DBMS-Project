from flask import render_template, redirect, url_for
from app.main import main_bp



@main_bp.route('/')
def index():
    return render_template('landing.html')