from flask import render_template
from . import main

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/create_spam')
def create_spam():
    return render_template('create_spam.html')