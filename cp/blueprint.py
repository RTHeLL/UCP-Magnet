import hashlib

from flask import Blueprint, request, render_template, session, flash, redirect, url_for

from classes.mysql import Methods
from classes.other import Other

cp = Blueprint('cp', __name__, template_folder='templates')


# Main CP
@cp.route('/')
def user_panel_cp():
    # if KeyError:
    #     return render_template("index.html", news=Methods().get_news(), server_monitor=get_server_info())
    try:
        user = Methods().get_user(session['name'])
        return render_template("cp.html", user=user)
    except KeyError:
        return render_template("cp.html", user=None)
    # return render_template("index.html", news=Methods().get_news(), server_monitor=Other().get_server_info())


# Login CP
@cp.route('/login', methods=['GET', 'POST'])
def user_panel_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if len(username) < 1 or len(password) < 1:
            flash('Введите данные для входа')
            return render_template('login.html')
        user = Methods().get_user(username)

        if user is not False:
            user_password = user["pKey"]
            # user_password_encode = hashlib.md5(user_password.encode())
            if hashlib.md5(password.encode()).hexdigest() == user_password:
                session['name'] = user['Name']
                if 'level' in user:
                    session['Admin'] = user['level']
                return redirect(url_for('cp.user_panel_cp'))
            else:
                flash('Проверьте правильность введенных данных')
                return render_template('login.html')
        else:
            flash('Такого пользователя не существует')
    return render_template('login.html')


# Logout CP
@cp.route('/logout', methods=['GET', 'POST'])
def user_panel_logout():
    session.clear()
    return redirect(url_for('main'))
    # return render_template("index.html", news=Methods().get_news(), server_monitor=Other().get_server_info())
