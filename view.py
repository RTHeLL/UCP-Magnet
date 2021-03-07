from app import app
from flask import render_template
from classes.mysql import Methods
from classes.other import Other


# Main page
@app.route('/')
def main():
    return render_template('index.html', news=Methods().get_news(), server_monitor=Other.get_server_info())
