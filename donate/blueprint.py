from flask import Blueprint, request, flash, render_template

from classes.mysql import Methods

donate = Blueprint('donate', __name__, template_folder='templates')


# Donate
@donate.route('/', methods=['GET', 'POST'])
def donate_handler():
    if request.method == 'POST':
        nickname = request.form['nickname']
        amount = request.form['sum']
        user = Methods().get_user(nickname)
        print(user)
        if not nickname:
            flash('Не введено имя!')
        elif not amount or isinstance(amount, int) is None:
            flash('Не введена или некоректно введена сумма')
        elif user is False:
            flash('Такого пользователя не существует!')
        else:
            flash('Система находится в разработке....')
    return render_template("donate.html")