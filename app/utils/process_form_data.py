from typing import Dict

def process_form_data(user : Dict[str, str]) -> Dict[str, str]:
    
    user['username'] = user['username'].strip()
    user['password'] = user['password'].strip()
    user['password_confirmation'] = user['password_confirmation'].strip()

    return user