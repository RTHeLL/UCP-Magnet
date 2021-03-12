import pymysql
import logging
import configparser

from pymysql import MySQLError

config = configparser.ConfigParser()
logger = logging.getLogger(__name__)
if __name__ == '__main__':
    log_handler = logging.FileHandler('../logs/mysql.log')
    config.read('../config.ini')
else:
    log_handler = logging.FileHandler('logs/mysql.log')
    config.read('config.ini')
log_handler.setLevel(logging.DEBUG)
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
log_handler.setFormatter(log_format)
logger.addHandler(log_handler)


class MySQL:
    try:
        connection = pymysql.connect(host=config['MySQL']['HOST'],
                                     user=config['MySQL']['USER'],
                                     password=config['MySQL']['PASS'],
                                     database=config['MySQL']['DB'],
                                     cursorclass=pymysql.cursors.DictCursor)
    except MySQLError as e:
        logger.log(logging.CRITICAL, e)


class Methods(MySQL):
    def get_news(self, news_id=None):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            if news_id is None:
                sql = "SELECT * FROM news_site ORDER BY date DESC"
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
                logger.log(logging.INFO, "User no admin")
            cursor.close()
            return result

    def admin_get_user(self, user_id):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM accounts WHERE id = '%s'"
            cursor.execute(sql % user_id)
            result = cursor.fetchone()
            if result is None:
                return False
            try:
                sql = "SELECT * FROM admin WHERE Name = '%s'"
                cursor.execute(sql % result['Name'])
                result.update(cursor.fetchone())
            except TypeError:
                logger.log(logging.INFO, "User no admin")
            cursor.close()
            return result

    def get_users(self):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM accounts"
            cursor.execute(sql)
            result = cursor.fetchall()
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

    def edit_news(self, *args):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            sql = "UPDATE news_site SET title='%s', image='%s', text='%s' WHERE id = %d"
            cursor.execute(sql % (args[0], args[1], args[2], args[3]))
            cursor.close()

    def delete_news(self, *args):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            sql = "DELETE FROM news_site WHERE id = %d"
            cursor.execute(sql % args[0])
            cursor.close()

    def delete_user(self, *args):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            sql = "DELETE FROM accounts WHERE id = %d"
            cursor.execute(sql % args[0])
            try:
                sql = "DELETE FROM admin WHERE Name = '%s'"
                cursor.execute(sql % args[1])
            except TypeError:
                logger.log(logging.INFO, "User no admin")
            cursor.close()


if __name__ == '__main__':
    logger.log(logging.ERROR, 'Module "mysql" no worked without main')
