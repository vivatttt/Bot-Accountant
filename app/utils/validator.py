from typing import Dict
import re
import pandas as pd
from app.data_of_entering import Data_enter

def validate(user : Dict[str, str]) -> str:

    '''
    user :
        Args: "username", "password", "password_confirmation"
    '''

    username, password, password_confirmartion = user['username'], user['password'], user['password_confirmation']

    if not username or not password or not password_confirmartion:
        return "Fields cannot be empty"
    
    # Логин должен содержать только буквы, цифры и нижнее подчеркивание
    username_pattern = r'^\w+$'
    # Пароль должен быть длиной от 6 до 16 символов и содержать как минимум одну цифру, одну букву в верхнем регистре и одну букву в нижнем регистре
    password_pattern = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,16}$'

    if not re.match(username_pattern, username):
        return "Login can only contain letters, numbers and underscores."
    if not re.match(password_pattern, password):
        return "The password must be between 6 and 10 characters long and contain at least one number, one uppercase letter and one lowercase letter."
    if password != password_confirmartion:
        return "Password mismatch."

    frame = Data_enter()

    try:
        df = pd.read_csv('app/csvy/akks.csv')

    except Exception:
        frame.server()
        df = pd.read_csv('app/csvy/akks.csv')

    if (df['login'] == username).any():
        return "This login already exists."

    return ''