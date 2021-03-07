from flask import Blueprint, render_template
from classes.mysql import Methods

news = Blueprint('news', __name__, template_folder='templates')


# News page
@news.route('/')
def news_page_handler(news_id):
    return render_template('news.html', news=Methods().get_news(news_id))
