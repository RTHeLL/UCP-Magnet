import view

from admin.blueprint import admin
from app import app
from cp.blueprint import cp
from donate.blueprint import donate
from news.blueprint import news

app.register_blueprint(cp, url_prefix='/cp')
app.register_blueprint(news, url_prefix='/news-<int:news_id>')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(donate, url_prefix='/donate')


# Init module
if __name__ == '__main__':
    app.run(debug=True)
