from app import app
from flask import (Blueprint, 
                   redirect, 
                   render_template, 
                   request, 
                   session, 
                   flash, 
                   url_for,
                   get_flashed_messages)

from datetime import date, datetime
from app.utils.validator import validate
from app.utils.hash_password import hash_password
from app.utils.process_form_data import process_form_data
from app.data_of_entering import Data_enter
from app.data_of_transaction import Data_trans



routes = Blueprint('routes', __name__)
app.secret_key = 'daria_dusheiko'
# главная страница
@app.route('/')
def main():
    if 'username' in session:

        # если пользователь уже зашел в свой аккаунт
        return render_template(
            'main_page.html'
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
    return render_template(
        'analytics_page.html'
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
    user_transaction = Data_trans()

    inde = session.get('inde', '')
    print(inde)
    if not inde:
        # тут обработка ошибки
        print('ERROR INDE')
    error = user_transaction.add_transection(inde, transaction.get('amount'), transaction.get('type'), transaction.get('category'), transaction.get('description'), transaction.get('date'))

    if error:
        
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


# страница с бюджетом
@app.route('/goal')
def budget():
    return render_template(
        'goal_page.html'
    )


