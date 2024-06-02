import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from app.data_of_transaction import Data_trans
import os
from app.utils.names import GRAPH_FOLDER



def get_inf_for_pie_chart(inde, type, period):
    '''
        Круговая диаграмма по категориям

        period : Период за который берутся данные в месяцах (int)
        inde :
        type in ["Expense", "Income"]
    '''

    # здесь получение данных за период period
    transactions = Data_trans()
    transactions.time_ago(inde, period, type)

    values = transactions.category_out(inde, period*30)
    values = [el[0] for el in values]

    return values


    


