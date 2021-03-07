from flask import Blueprint, request, flash, render_template, session

from classes.mysql import Methods

admin = Blueprint('admin', __name__, template_folder='templates')


# Admin panel
@admin.route('/', methods=['GET', 'POST'])
def admin_panel():
    if 'Admin' not in session or session['Admin'] < 7:
        flash('У Вас нет доступа к данной странице!')
    return render_template("admin.html")


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
            return render_template("admin.html")
        # item = request.form.get('admin_select')
        # settings = Methods().get_settings_db()
        # if str(item) == 'db_setting':
        #     return render_template("admin.html", item=item, settings=settings)
        # else:
        #     return render_template("admin.html")
