from flask import Blueprint, request, flash, render_template, url_for, redirect

from classes.mysql import Methods

admin = Blueprint('admin', __name__, template_folder='templates')


# Admin panel
@admin.route('/')
def admin_panel():
    # if 'Admin' not in session or session['Admin'] < 7:
    #     flash('У Вас нет доступа к данной странице!')
    return render_template("admin_base.html")


# News
@admin.route('/news', methods=['GET', 'POST'])
def admin_panel_news():
    news = Methods().get_news()
    return render_template("admin_news.html", type_='acn', news=news)


@admin.route('/news/<int:news_id>', methods=['GET', 'POST'])
def admin_panel_edit_news(news_id):
    edit_news = Methods().get_news(news_id)
    if request.method == 'POST':
        if 'delete_news' in request.form:
            Methods().delete_news(news_id)
            flash(f'Новости \'{edit_news["title"]}\' успешно удалена')
        else:
            title = request.form['news_title']
            image = request.form['news_image']
            text = request.form['news_text']
            Methods().edit_news(title, image, text, news_id)
            flash(f'Новости \'{edit_news["title"]}\' успешно изменена')
        return redirect(url_for('admin.admin_panel_news'))
    return render_template("admin_news.html", type_='acn', news_type_='edit', edit_news=edit_news)


@admin.route('/news/create', methods=['GET', 'POST'])
def admin_panel_create_news():
    if request.method == 'POST':
        title = request.form['news_title']
        image = request.form['news_image']
        text = request.form['news_text']
        Methods().create_news(title, image, text)
        flash(f'Новость \'{title}\' успешно создана')
        return redirect(url_for('admin.admin_panel_news'))
    return render_template("admin_news.html", type_='acn', news_type_='create')


# Site settings
@admin.route('/site-settings', methods=['GET', 'POST'])
def admin_panel_site_settings():
    return render_template("site_settings.html", type_='ass')


# Table settings
@admin.route('/table-settings', methods=['GET', 'POST'])
def admin_panel_table_settings():
    return render_template("table_settings.html", type_='ats')


# Accounts
@admin.route('/accounts')
def admin_panel_accounts():
    accounts = Methods().get_users()
    return render_template("accounts.html", type_='aa', accounts=accounts)


@admin.route('/accounts/<int:user_id>', methods=['GET', 'POST'])
def admin_panel_accounts_user(user_id):
    user = Methods().admin_get_user(user_id)
    if request.method == "POST":
        if 'delete_user' in request.form:
            Methods().delete_user(user_id, user["Name"])
            flash(f'Пользователь {user["Name"]}[{user["id"]}] успешно удален')
            return redirect(url_for('admin.admin_panel_accounts'))

    return render_template("accounts.html", type_='aa', accounts_type='edit', user=user)
