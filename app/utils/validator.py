from typing import Dict
import re

def validate(user : Dict[str, str]) -> str:

    '''
    user :
        Args: "username", "password", "password_confirmation"
    '''
    
    username, password, password_confirmartion = user['username'], user['password'], user['password_confirmation']

    if not username or not password or not password_confirmartion:
        return "Поля не могут быть пустыми"
    
    # Логин должен содержать только буквы, цифры и нижнее подчеркивание
    username_pattern = r'^\w+$'
    # Пароль должен быть длиной от 6 до 16 символов и содержать как минимум одну цифру, одну букву в верхнем регистре и одну букву в нижнем регистре
    password_pattern = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,16}$'

    if not re.match(username_pattern, username):
        return "Логин может содержать только буквы, цифры и нижнее подчеркивание"
    if not re.match(password_pattern, password):
        return "Пароль должен быть длиной от 8 до 16 символов и содержать как минимум одну цифру, одну букву в верхнем регистре и одну букву в нижнем регистре"
    if password != password_confirmartion:
        return "Пароли не совпадают"
    return ''