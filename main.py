import os

import pymysql
from pymysql import MySQLError
import logging
from flask import Flask, render_template, request, redirect, url_for, session
import hashlib
from samp_client.client import SampClient
from samp_client.exceptions import ConnectionError
from wtforms import ValidationError

app = Flask(__name__)
app.secret_key = os.urandom(24)
logging.basicConfig(level=logging.DEBUG)


# Get server info
def get_server_info():
    server = SampClient(address='46.174.50.46', port=7844).connect()
    try:
        server_info = server.get_server_info()
    except ConnectionError:
        server_info = None
    return server_info


class MySQL:
    try:
        connection = pymysql.connect(host='localhost', user='root', password='root', database='samp',
                                     cursorclass=pymysql.cursors.DictCursor)
    except MySQLError as e:
        logging.log(logging.CRITICAL, e)


class Methods(MySQL):
    def get_news(self):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM news_site"
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            return result

    def get_news_id(self, news_id):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM news_site WHERE id = %d"
            cursor.execute(sql % news_id)
            result = cursor.fetchone()
            cursor.close()
            return result

    def get_user(self, username):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM accounts WHERE Name = '%s'"
            cursor.execute(sql % username)
            result = cursor.fetchone()
            cursor.close()
            return result


# Main page
@app.route('/')
def main():
    return render_template('index.html', news=Methods().get_news(), server_monitor=get_server_info())


# News page
@app.route('/news-<int:news_id>')
def news_page(news_id):
    news = Methods().get_news_id(news_id)
    return render_template('news.html', news=news)


# User panel
@app.route('/cp/login', methods=['GET', 'POST'])
def user_panel_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if len(username) < 1 or len(password) < 1:
            return render_template("login.html", error=ValidationError('Введите данные для входа'))
        user = Methods().get_user(username)

        if len(user) > 0:
            user_password = user["pKey"]
            # user_password_encode = hashlib.md5(user_password.encode())
            if hashlib.md5(password.encode()).hexdigest() == user_password:
                session['name'] = user['Name']
                return render_template("index.html", news=Methods().get_news(), server_monitor=get_server_info())
            else:
                return "Проверьте правильность введенных данных"
    else:
        return render_template('login.html')


@app.route('/cp/logout', methods=['GET', 'POST'])
def user_panel_logout():
    session.clear()
    return render_template("index.html", news=Methods().get_news(), server_monitor=get_server_info())


@app.route('/cp')
def user_panel_cp():
    # if KeyError:
    #     return render_template("index.html", news=Methods().get_news(), server_monitor=get_server_info())
    user = Methods().get_user(session['name'])
    return render_template("cp.html", user=user)


# Init module
if __name__ == '__main__':
    app.run(debug=True)
