import matplotlib.pyplot as plt
from app.data_of_transaction import Data_trans
import os


GRAPH_FOLDER = 'app/data'

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
    fig, ax = plt.subplot()

    ax.pie(values, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    filename = 'pie_chart.png'
    filepath = os.path.join(GRAPH_FOLDER, filename)
    fig.savefig(filepath)
    plt.close(fig)


    


