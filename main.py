import pymysql
from pymysql import MySQLError
import logging
from flask import Flask, render_template
from samp_client.client import SampClient
from samp_client.exceptions import ConnectionError

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


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


@app.route('/')
def main():
    news = Methods().get_news()
    server = SampClient(address='46.174.50.46', port=7844).connect()
    try:
        server_info = server.get_server_info()
    except ConnectionError:
        server_info = None
    return render_template('index.html', news=news, server_monitor=server_info)


@app.route('/news-<int:news_id>')
def news_page(news_id):
    news = Methods().get_news_id(news_id)
    return render_template('news.html', news=news)


# @app.route('/cp', methods=['GET', 'POST'])
# @oid.loginhandler
# def user_panel():
#     return render_template('cp.html')
