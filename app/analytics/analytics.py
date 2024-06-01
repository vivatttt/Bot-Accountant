import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from app.data_of_transaction import Data_trans
import os
from app.utils.names import GRAPH_FOLDER



def generate_pie_chart(inde, type, period):
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

    fig, ax = plt.subplots()

    ax.pie(values, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    filename = f'pie_chart_{period}.png'

    filepath = os.path.join('app/' + GRAPH_FOLDER, filename)
    print(filepath)
    fig.savefig(filepath)
    plt.close(fig)

    return filename


    


