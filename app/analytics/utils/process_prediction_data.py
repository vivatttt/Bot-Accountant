from datetime import datetime, date

def process_goal_prediction(date_str : str) -> str:
    if not date_str:
        return 'The goal is not expected to be achieved in the near future'
    
    now = datetime.now()
    now = now.strftime('%Y-%m')
    if date_str == now:
        return 'The goal is reached! Congratulations!'
    cur_date = datetime.strptime(date_str, '%Y-%m')    
    return f'The goal is expected to be achieved around {cur_date.strftime("%B %Y")}'