from app import app
from flask import Blueprint, redirect, render_template, request, session, flash
from datetime import date, datetime
from app.utils.validator import validate
from app.utils.hash_password import hash_password
from app.utils.process_form_data import process_form_data


routes = Blueprint('routes', __name__)

# главная страница
@app.route('/')
def main():
    if 'username' in session:

        # если пользователь уже зашел в свой аккаунт
        return render_template(
            'main_page.html'
        )
    # если пользователь еще не зашел в свой аккунт / не зарегистрировался
    return render_template(
        'main_page.html'
    )

# login - GET, POST
# register - GET, POST

# страница отображения регистрации 
@app.get('/register')
def show_register():
    user = user = {
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
    # Добавление в базу данных

    # Здесь вход в аккаунт
    session['username'] = username # добавление имени пользователя в куки 
    flash('User succesfully created', 'success')
    return redirect('/users/succesfully_created', code=302)


# страница отображения регистрации 
@app.get('/login')
def show_login():
    user = user = {
        'username' : '',
        'password' : '',
        'password_confirmation' : ''
    }
    error = ''

    return render_template(
        'login_page.html',
        user=user,
        error=error
    )

# страница обработки регистрации
@app.post('/login')
def do_login():
    user = process_form_data(request.form.to_dict())
    error = '' # здесь проверка валидности пользователя

    '''

    user {
        username : ...
        password : ... !!! Не забываем, что сравниваем не пароль пользователя, а хеш пароля (функция hash_password)
    }

    error - строка
    
    '''

    if error:
        return render_template(
            'login_page.html',
            user=user,
            error=error
        ), 422
    
    username = user['username']
    session['username'] = username # добавление имени пользователя в куки 

    return redirect('/users/succesfully_created', code=302)



# страница аналитики
@app.route('/analytics')
def analytics():
    return render_template(
        'analytics_page.html'
    )

# страница добавлением / удалением транизакций
@app.route('/transactions')
def transactions():
    return render_template(
        'transactions_page.html'
    )

# страница с бюджетом
@app.route('/budget')
def budget():
    return render_template(
        'budget_page.html'
    )



