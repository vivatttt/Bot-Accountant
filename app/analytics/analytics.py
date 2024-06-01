import matplotlib.pyplot as plt
import os


GRAPH_FOLDER = 'app/data'

def generate_pie_chart(period):
    '''
        Круговая диаграмма по категориям

        period : Период за который берутся данные в месяцах

    '''



    # здесь получение данных за период period

    values = 
    fig, ax = plt.subplot()

    ax.pie(values, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    filename = 'pie_chart.png'
    filepath = os.path.join(GRAPH_FOLDER, filename)
    fig.savefig(filepath)
    plt.close(fig)


    


