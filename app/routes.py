from app import app
from flask import redirect, render_template, request, session
from datetime import date, datetime


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

# страница регистрации
@app.route('/register')
def register():
    return render_template(
        'register_page.html'
    )

# страница с бюджетом
@app.route('/login')
def login():
    return render_template(
        'login_page.html'
    )


