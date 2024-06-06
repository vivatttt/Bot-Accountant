import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from app.data_of_transaction import Data_trans
from datetime import datetime


def get_inf_for_pie_chart(inde, type, period):
    '''
        Круговая диаграмма по категориям

        period : Период за который берутся данные в месяцах (int)
        inde :
        type in ["expense", "income"]
    '''
    inde = int(inde)
    # здесь получение данных за период period
    transactions = Data_trans()

    values = transactions.category_out(inde, period * 30, type)

    labels = [el[0] for el in values]
    values = [el[1] for el in values]

    return labels, values


def get_inf_for_bar_chart(inde):

    '''
        Столбчатая диаграмма по месяцам
        
    '''
 
    inde = int(inde)
    cur_month = int(datetime.now().month)
    cur_year = int(datetime.now().year)
    
    income_arr = []
    expense_arr = []
    date_arr =  []

    transactions = Data_trans()

    for _ in range(6):
        cur_month -= 1
        if cur_month == 0:
            cur_month = 12
            cur_year -= 1
        
        if cur_month > 9:
            cur_date = f'{cur_year}-{cur_month}'
        else:
            cur_date = f'{cur_year}-0{cur_month}'
       
        date_arr.append(cur_date)
        income_arr.append(transactions.sum_for_month(inde, cur_date, 'income'))
        expense_arr.append(transactions.sum_for_month(inde, cur_date, 'expense'))

    return income_arr, expense_arr, date_arr


