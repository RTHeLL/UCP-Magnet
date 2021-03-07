from flask import Blueprint, request, flash, render_template, session

from classes.mysql import Methods

admin = Blueprint('admin', __name__, template_folder='templates')


# Admin panel
@admin.route('/')
def admin_panel():
    # if 'Admin' not in session or session['Admin'] < 7:
    #     flash('У Вас нет доступа к данной странице!')
    return render_template("admin_base.html")


# Create news
@admin.route('/create-news', methods=['GET', 'POST'])
def admin_panel_create_news():
    if request.method == 'POST':
        title = request.form['news_title']
        image = request.form['news_image']
        text = request.form['news_text']
        if not title:
            flash('Не введен заголовок!')
        elif not image:
            flash('Не введена ссылка на изображение!')
        elif not text:
            flash('Не введен текст!')
        else:
            Methods().create_news(title, image, text)
            return render_template("admin_base.html")
    return render_template("admin_base.html")


# Site settings
@admin.route('/site-settings', methods=['GET', 'POST'])
def admin_panel_site_settings():
    return render_template("admin_base.html")


# Table settings
@admin.route('/table-settings', methods=['GET', 'POST'])
def admin_panel_table_settings():
    return render_template("admin_base.html")


# Accounts
@admin.route('/accounts', methods=['GET', 'POST'])
def admin_panel_accounts():
    accounts = Methods().get_users()
    return render_template("admin_base.html", accounts=accounts)
