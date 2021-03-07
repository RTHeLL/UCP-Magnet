import pymysql
import logging

from pymysql import MySQLError

logging.basicConfig(filename='logs/mysql.log', level=logging.DEBUG)


class MySQL:
    try:
        connection = pymysql.connect(host='localhost', user='root', password='root', database='samp',
                                     cursorclass=pymysql.cursors.DictCursor)
    except MySQLError as e:
        logging.log(logging.CRITICAL, e)


class Methods(MySQL):
    def get_news(self, news_id=None):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            if news_id is None:
                sql = "SELECT * FROM news_site"
                cursor.execute(sql)
                result = cursor.fetchall()
            else:
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
            if result is None:
                return False
            try:
                sql = "SELECT * FROM admin WHERE Name = '%s'"
                cursor.execute(sql % username)
                result.update(cursor.fetchone())
            except TypeError:
                logging.log(logging.CRITICAL, "User no admin")
            cursor.close()
            return result

    # def get_settings_db(self):
    #     self.connection.ping()
    #     with self.connection.cursor() as cursor:
    #         sql = "SELECT * FROM site_settings_db"
    #         cursor.execute(sql)
    #         result = cursor.fetchone()
    #         cursor.close()
    #         return result

    def create_news(self, *args):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO news_site (title, image, text) VALUES ('%s', '%s', '%s')"
            cursor.execute(sql % (args[0], args[1], args[2]))
            cursor.close()


if __name__ == '__main__':
    logging.log(logging.ERROR, 'Module "mysql" no worked without main')
