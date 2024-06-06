from statsmodels.tsa.statespace.sarimax import SARIMAX 
import pandas as pd
import warnings 
import plotly.graph_objs as go
warnings.filterwarnings("ignore") 


def predict(inde):

    inde = int(inde)

    df = pd.read_csv('app/csvy/trans.csv') 
    search = df[df['id_user'] == inde]
    search = df[df['type'] == 'expense']
    search['date'] = pd.to_datetime(search['date'])

    search['month'] = search['date'].dt.to_period('M')
    sum_by_month = search.groupby('month')['amount'].sum().reset_index()


    model = SARIMAX(sum_by_month['amount'],  
                    order = (0, 1, 1),  
                    seasonal_order = (2, 1, 1, 12)) 

    result = model.fit(disp=False) 
    
    forecast = result.predict(
        start = len(search),  
        end = (len(search)-1) + 4,  
        typ = 'levels'
            ).rename('amount') 
    last_month = sum_by_month['month'].iloc[-1]
    sum_by_month['month'] = sum_by_month['month'].dt.strftime('%Y-%m')
    new_months = [(last_month + i).strftime('%Y-%m') for i in range(1, len(forecast) + 1)]

    forecast = pd.DataFrame({'month': new_months, 'amount': forecast})
    
    trace1 = go.Scatter(x=sum_by_month['month'], y=sum_by_month['amount'], mode='lines', name='Past expenses', line=dict(color='rgb(247, 247, 247)'))

    trace2 = go.Scatter(x=forecast['month'], y=forecast['amount'], mode='lines', name='Prediction expenses', line=dict(color='rgb(248,181,0)'))

    data = [trace1, trace2]
 
    layout = go.Layout(title='Expenses predictions', xaxis=dict(title='Month'), yaxis=dict(title='Amount'))

    fig = go.Figure(data=data, layout=layout)
    
    fig.update_layout(
        barmode='group',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgb(57, 62, 70)',
        font=dict(color='white'),
        title=dict(
            font=dict(color='white', size=30)
        ),
        legend=dict(font=dict(size=20, color='white'))
    )

    return fig.to_html(full_html=False)

    
