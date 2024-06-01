from app import app
from flask import (
                    Blueprint, 
                   redirect, 
                   render_template, 
                   request, 
                   session, 
                   flash, 
                   url_for,
                   get_flashed_messages
                   )
import os
from datetime import date, datetime
from app.utils.validator import validate
from app.utils.hash_password import hash_password
from app.utils.process_form_data import process_form_data
from app.data_of_entering import Data_enter
from app.data_of_transaction import Data_trans
from app.data_of_goal import Data_goal
import pandas as pd
from app.analytics.analytics import generate_pie_chart
from app.utils.names import GRAPH_FOLDER


routes = Blueprint('routes', __name__)
app.secret_key = 'daria_dusheiko'
# главная страница
@app.route('/')
def main():
    if 'username' in session:
        inde = session.get('inde')
        
        # если пользователь уже зашел в свой аккаунт
        user_info = Data_enter()
        data_info = user_info.info_user(int(inde))

        return render_template(
            'main_page.html',
            cur_goal=data_info[0],
            moneybox=data_info[1],
            budget=data_info[2]
        )
    
    # если пользователь еще не зашел в свой аккунт / не зарегистрировался

    return redirect(
        url_for('show_register'),
        code=302
    )

# login - GET, POST
# register - GET, POST

# страница отображения регистрации 
@app.get('/register')
def show_register():

    if 'username' in session:
        return redirect(
            url_for('main'), 
            code=302
            )
    
    user = {
        'username' : '',
        'password' : '',
        'password_confirmation' : ''
    }
    error = ""

    return render_template(
        'register_page.html',
        user=user,
        error=error
    )

# страница обработки регистрации
@app.post('/register')
def do_register():
    user = process_form_data(request.form.to_dict())

    error = validate(user)


    if error:
        return render_template(
            'register_page.html',
            user=user,
            error=error
        ), 422

    username = user['username']
    password = hash_password(user['password'])

    # Поменять структуру done_registration()

    # Добавление в базу данных
    add_user = Data_enter()
    add_user.done_registration(username, password)
    inde = add_user.enter_acc(username, password)['inde']

    # Здесь вход в аккаунт

    session['inde'] = inde # добавление имени пользователя в куки
    session['username'] = username
    flash('User succesfully created', 'success')

    return redirect('/', code=302)


# страница отображения входа
@app.get('/login')
def show_login():
    if 'username' in session:
        return redirect('/', code=302)
    user = user = {
        'username' : '',
        'password' : '',
    }
    error = ''

    return render_template(
        'login_page.html',
        user=user,
        error=error
    )

# страница обработки входа
@app.post('/login')
def do_login():
    user = process_form_data(request.form.to_dict())

    add_user = Data_enter()

    login_result = add_user.enter_acc(user['username'], hash_password(user['password']))

    '''
    user {
        username : ...
        password : ... !!! Не забываем, что сравниваем не пароль пользователя, а хеш пароля (функция hash_password)
    }

    error - строка
    '''

    if login_result['error']:
        return render_template(
            'login_page.html',
            user=user,
            error=login_result['error']
        ), 422

    session['username'] = user['username'] # добавление имени пользователя в куки
    session['inde'] = login_result['inde']

    return redirect(
        url_for('main'),
        code=302
        )


# страница аналитики
@app.route('/analytics')
def analytics():


    inde = session.get('inde')

    # генерируем круговую диаграмму
    pie_chart_1_month_filename = generate_pie_chart(inde=inde, period=1, type="Expense")
    pie_chart_1_month_filepath = os.path.join(GRAPH_FOLDER, pie_chart_1_month_filename)

    pie_chart_3_month_filename = generate_pie_chart(inde=inde, period=3, type="Expense")
    pie_chart_3_month_filepath = os.path.join(GRAPH_FOLDER, pie_chart_3_month_filename)

    pie_chart_6_month_filename = generate_pie_chart(inde=inde, period=6, type="Expense")
    pie_chart_6_month_filepath = os.path.join(GRAPH_FOLDER, pie_chart_6_month_filename)

    print(pie_chart_1_month_filepath)

    return render_template(
        'analytics_page.html',
        pie_chart_1=pie_chart_1_month_filepath,
        pie_chart_3=pie_chart_3_month_filepath,
        pie_chart_6=pie_chart_6_month_filepath
    )

# страница добавлением / удалением транизакций
@app.get('/transactions')
def show_transaction():
    return render_template(
        'transactions_page.html',
        transaction={},
        error=''
    )


@app.post('/transactions')
def make_transaction():
    transaction = request.form.to_dict()
    '''
    transaction = {
        amount :
        type :
        category :
        date :
        description : 

    }
    '''

    inde = int(session.get('inde', ''))
    signed_amount = int(transaction['amount'])

    add_info = Data_enter()
    
    if transaction['type'] == 'expense':
        signed_amount = -signed_amount

    error = add_info.change_data(inde, "budget", signed_amount, 1)

    if error:

        return render_template(
            'transactions_page.html',
            transaction=transaction,
            error=error
        ), 422
    
    user_transaction = Data_trans()
    error = user_transaction.add_transection(inde, transaction.get('amount'), transaction.get('type'), transaction.get('category'), transaction.get('description'), transaction.get('date'))
    
    if error:
        # если выходим по этой ошибке, то нужно вернуть измененную ранее сумму бюджета
        add_info.change_data(inde, "budget", -signed_amount, 1)
        return render_template(
            'transactions_page.html',
            transaction=transaction,
            error=error
        ), 422

    flash('Transaction succesfully added', 'success')
    return render_template(
        'transactions_page.html',
        transaction={},
        error=''
    )


# страница с целью
@app.get('/goal')
def show_goal():
    return render_template(
        'goal_page.html',
        goal={},
        error=''
    )
# добавление транзакции в цели
@app.post('/goal')
def add_to_goal():
    '''
    goal = {
        amount :
        type :

    }
    '''

    goal = request.form.to_dict()
    inde = int(session.get('inde'))
 
    signed_amount = int(goal['amount'])
    if goal['type'] == 'expense':
        signed_amount = -signed_amount

    add_info = Data_enter()
    
    error = add_info.change_data(inde, "moneybox", signed_amount, 1)
    if error:
        return render_template(
            'goal_page.html',
            goal=goal,
            error=error
        ), 422

    # тут добавление транзакции в бд
    goal_tran = Data_goal()
    error = goal_tran.add_goal(inde, goal['amount'], goal['type'])
    
    if error:
        # если выходим по этой ошибке, то нужно вернуть измененную ранее сумму в копилке
        add_info.change_data(inde, "moneybox", -signed_amount, 1)
        return render_template(
            'goal_page.html',
            goal=goal,
            error=error
        ), 422
    
    flash('You became closer to the goal!', 'success')
    return render_template(
        'goal_page.html',
        goal={},
        error=''
    )

# изменение цели
@app.post('/goal-new')
def new_goal():
    '''
    goal = {
        new_amount :
    }
    '''

    inde = int(session.get('inde'))
    new_amount = int(request.form.get('new_amount'))
    # тут обновление цели пользователя
    del_cha = Data_enter()
    del_cha.change_data(inde, "goal", new_amount, 1)

    del_goal = Data_goal()
    del_goal.del_transaction(inde)

    flash('Goal succesfully updated', 'success')

    return redirect(
        url_for('add_to_goal'),
        code=302
    )

