import os
import glob
from flask import render_template, request, current_app, redirect, url_for, abort
from . import main
from ..models import create_spam_db, get_all_spams, get_spam, get_email, create_captured
from ..mail import send_all_emails_spam


@main.route('/')
def index():
    spams = get_all_spams()
    t_success = sum(n.success for n in spams)
    t_failed = sum(n.fail for n in spams)
    t_captured = sum(len(n.captures) for n in spams)
    return render_template('index.html', spams=spams, total_success=t_success, total_failed=t_failed, total_captured=t_captured)


@main.route('/create_spam', methods=['GET', 'POST'])
def create_spam():
    if request.method in "POST":
        subject = request.values['subject']
        template = request.values['template']
        emails = request.values['emails']
        redirect_to = request.values['redirect']
        id_spam = create_spam_db(subject, template, emails, redirect_to)
        send_all_emails_spam(id_spam)
        return redirect(url_for('.index'))

    template_folder = os.path.join(current_app.root_path, current_app.template_folder)
    template_glob = os.path.join(template_folder, "spam_*.html")
    templates = glob.glob(template_glob)
    return render_template('create_spam.html', templates=templates)


@main.route('/info_spam/<idspam>')
def info_spam(idspam):
    spam = get_spam(idspam)
    if not spam:
        abort(404)
    return render_template('info_spam.html', spam=spam)


@main.route('/redirect')
def capture():
    """
    Fake view redirect to capture
    """
    if 'em' not in request.values and 'sp' not in request.values:
        abort(403)
    idemail = request.values.get('em', '')
    idspam = request.values.get('sp')
    email, spam = "", ""

    if idemail.isdigit():
        email = get_email(int(idemail))
    if idspam.isdigit():
        spam = get_spam(idspam)
    if email:
        email = email.email
    if spam:
        params = {'usera': str(request.user_agent),
                  'ip': request.remote_addr,
                  'os': request.user_agent.platform,
                  'more_info': "Headers: {}".format(request.headers.to_list()),
                  'email': email,
                  'idspam': spam.id,
                  }
        create_captured(**params)
        return redirect(spam.redirect_to, 302)
    abort(403)
