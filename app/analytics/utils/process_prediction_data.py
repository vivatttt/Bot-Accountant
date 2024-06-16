from datetime import datetime

def process_goal_prediction(date_str):
    if not date_str:
        return 'The goal is not expected to be achieved in the near future'
    date = datetime.strptime(date_str, '%Y-%m')
    return f'The goal is expected to be achieved around {date.strftime("%B %Y")}'