import pandas as pd
from datetime import datetime, timedelta


def check_enough_data_for_analytics(inde):
    
    df_accs = pd.read_csv('app/csvy/akks.csv')
    goal = df_accs.loc[inde, 'goal']
    moneybox = df_accs.loc[inde, 'moneybox']

    if goal <= 0:
        return False, 'Set a goal'
    if moneybox <= 0:
        return False, 'Top up your moneybox'
    
    df_trans = pd.read_csv('app/csvy/trans.csv')
    user_trans = df_trans[df_trans['id_user'] == inde]

    if user_trans.size < 5:
        return False, 'You must add at least 5 transactions'
    df_trans['date'] = pd.to_datetime(df_trans['date'])
    oldest_date = df_trans['date'].min()
    current_date = datetime.now()

    if current_date - oldest_date < timedelta(days=120):
        return False, 'It must take at least 3 month since the first transaction'

    df_goal = pd.read_csv('app/csvy/goal.csv')
    user_goal_trans = df_goal[df_goal['id_user'] == inde]

    if user_goal_trans.size < 5:
        return False, 'You must add at least 5 transactions to goal'

    df_goal['date'] = pd.to_datetime(df_goal['date'])
    oldest_date = df_goal['date'].min()
    current_date = datetime.now()

    if current_date - oldest_date < timedelta(days=120):
        return False, 'It must take at least 3 month since the first goal transaction'

    return True, ''


