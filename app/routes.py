from app import app
import plotly.graph_objs as go
import plotly.express as px
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
from app.analytics.analytics import get_inf_for_pie_chart, get_inf_for_bar_chart
from app.analytics.model import predict
from app.utils.names import GRAPH_FOLDER, CATEGORIES, TYPES


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
        url_for('show_auth'),
        code=302
    )

@app.get('/auth')
def show_auth():

    if 'username' in session:
        return redirect(
            url_for('main'), 
            code=302
            )
    
    user = user = {
        'username' : '',
        'password' : '',
    }
    error = ''

    return render_template(
        'auth_page.html',
        user=user,
        error=error
    )

@app.post('/auth')
def do_auth():
    user = process_form_data(request.form.to_dict())
    
    username = user['username']
    password = hash_password(user['password'])


    if 'password_confirmation' in user.keys():
        error = validate(user)
    
        if error:
            return render_template(
                'auth_page.html',
                user=user,
                error=error
            ), 422
        # Добавление в базу данных
        add_user = Data_enter()
        add_user.done_registration(username, password)
        inde = add_user.enter_acc(username, password)['inde']

        # Здесь вход в аккаунт
        session['inde'] = inde
        session['username'] = username
        flash('User succesfully created', 'success')

        return redirect('/', code=302)

    add_user = Data_enter()
    login_result = add_user.enter_acc(username, password)

    '''
    user {
        username : ...
        password : ... !!! Не забываем, что сравниваем не пароль пользователя, а хеш пароля (функция hash_password)
    }

    error - строка
    '''

    if login_result['error']:
        return render_template(
            'auth_page.html',
            user=user,
            error=login_result['error']
        ), 422

    session['username'] = user['username']
    session['inde'] = login_result['inde']

    return redirect(
        url_for('main'),
        code=302
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

    if 'username' not in session:
        return redirect(
            url_for('show_register'),
            code=302
        )

    inde = session.get('inde')
    diagrams = {
        'pie_chart' : {
            'income' : [],
            'expense' : []
        },
        'line': [],
        'circle': [],
    }

    '''
    diagrams = {
        'pie_chart' : {
            'income' : [1, 3, 6month]
            'expense' : [1, 3, 6month]
        }
    }
    '''

    colors = ['rgb(248, 181, 0)', 'rgb(92, 99, 110)', 'rgb(57, 62, 70)', 'rgb(247, 247, 247)', 'rgb(150, 143, 135)']
    # генерируем круговые диаграммы
    for type in TYPES:
        for month in [1, 3, 6]:
            labels, values = get_inf_for_pie_chart(inde, type, month)

            fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=colors), hole=0.3)])
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
            fig.update_layout(
                title={
                "text": type + " for " + str(month) + " month:",
                "y":0.96,
                "x":0.5,

                "xanchor":"center",
                "yanchor":"top",
                'font': {'size': 30, 'color': 'white'},
                }, legend=dict(font=dict(size=15, color='white')))
            html_code = fig.to_html(full_html=False)
            diagrams['pie_chart'][type].append(html_code)

    goal_tran = Data_goal()
    summ, date = goal_tran.type_information(int(inde))
    if summ != []:
        fig = px.line(y=summ, x=date, title='Life of goal')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        fig.update_layout(
            title={
                "text": "Life of goal:",
                "y": 0.96,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
                'font': {'size': 30, 'color': 'white'},
            })
        fig.update_layout(
            font=dict(color='white'),
            title=dict(
                font=dict(color='white', size=30)
            ),
            legend=dict(font=dict(size=20, color='white'))
        )
        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgb(57, 62, 70)',

            font=dict(color='white'),
            title=dict(
                font=dict(color='white', size=30)
            ),
            legend=dict(font=dict(size=20, color='white')),
        )
        fig.update_traces(line=dict(color='rgb(248, 181, 0)'))
        html_code = fig.to_html(full_html=False)
        diagrams["line"].append(html_code)


    # генерируем столбчатые диаграммы расходов и доходов
    # за последние 6 месяцев

    fig = go.Figure()

    incomes, expenses, days = get_inf_for_bar_chart(inde)

    fig.add_trace(go.Bar(
        x=days,
        y=incomes,
        name='Incomes',
        marker=dict(color='rgb(92,99,110)')
    ))
    
    fig.add_trace(go.Bar(
        x=days,
        y=expenses,
        name='Expenses',
        marker=dict(color='rgb(248,181,0)')
    ))
    
    fig.update_layout(
        barmode='group',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgb(57, 62, 70)',

        font=dict(color='white'),
        title=dict(
            font=dict(color='white', size=30)
        ),
        legend=dict(font=dict(size=20, color='white'))
    )

    html_code = fig.to_html(full_html=False)
    diagrams['bar_chart'] = html_code

    diagrams['predict_expenses'] = predict(inde)


    labels, values = get_inf_for_pie_chart(inde, type, month)


    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=colors), hole=0.7)])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(
        title={
            "text": type + " for " + str(month) + " month:",
            "y": 0.96,
            "x": 0.5,

            "xanchor": "center",
            "yanchor": "top",
            'font': {'size': 30, 'color': 'white'},
        }, legend=dict(font=dict(size=15, color='white')))
    html_code = fig.to_html(full_html=False)
    diagrams['pie_chart'][type].append(html_code)


    return render_template(
        'analytics_page.html',
        diagrams=diagrams
    )

# страница добавлением / удалением транизакций
@app.get('/transactions')
def show_transaction():
    
    if 'username' not in session:
        return redirect(
            url_for('show_register'),
            code=302
        )

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

    if 'username' not in session:
        return redirect(
            url_for('show_register'),
            code=302
        )

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

# выход из аккаунта
@app.get('/exit')
def exit():
    session.clear()

    return redirect(
        url_for('main'),
        code=302
    )
