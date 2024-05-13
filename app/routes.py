from app import app
from flask import Blueprint, redirect, render_template, request, session
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
            'main_page_after_signup.html'
        )
    # если пользователь еще не зашел в свой аккунт / не зарегистрировался
    return render_template(
        'main_page_before_signup.html'
    )

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

# страница с бюджетом
@app.route('/login')
def login():
    return render_template(
        'login_page.html'
    )

@app.post('/users')
def users_post():
    user = process_form_data(request.form.to_dict())

    error = validate(user)

    if error:
        return render_template(
            'register_page.html',
            user=user,
            error=error
        ), 422
    
    # ТУТ ОБРАБОТКА И ДОБАВЛЕНИЕ В БАЗУ ДАННЫХ

    username = user['username']
    password = hash_password(user['password'])
    
    # Здесь вход в аккаунт

    return redirect('/users/succesfully_created', code=302)

@app.route('/users/succesfully_created')
def users_sucesfully():
    return render_template(
        'registration_completed.html'
    )

@app.route('/users/new')
def user_new():
    user = {
        'username' : '',
        'password' : '',
        'password_confirmation' : ''
    }
    error = ''

    return render_template(
        'register_page.html',
        user=user,
        error=error
    )


