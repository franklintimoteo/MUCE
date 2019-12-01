import os
import glob
from flask import render_template, request, current_app, redirect, url_for
from . import main
from ..models import create_spam_db


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/create_spam', methods=['GET', 'POST'])
def create_spam():
    if request.method in "POST":
        subject = request.values['subject']
        template = request.values['template']
        emails = request.values['emails']
        create_spam_db(subject, template, emails)
        return redirect(url_for('.index'))

    template_folder = os.path.join(current_app.root_path, current_app.template_folder)
    template_glob = os.path.join(template_folder, "spam_*.html")
    templates = glob.glob(template_glob)
    return render_template('create_spam.html', templates=templates)
