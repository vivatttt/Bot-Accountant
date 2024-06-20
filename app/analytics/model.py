from statsmodels.tsa.statespace.sarimax import SARIMAX 
import pandas as pd
import warnings 
from datetime import datetime
import plotly.graph_objs as go
from app.utils.names import COLOR
warnings.filterwarnings("ignore") 


def predict(inde, type):

    inde = int(inde)

    df = pd.read_csv('app/csvy/trans.csv') 
    search = df[df['id_user'] == inde]
    search = df[df['type'] == type]
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
    title = {
        'trace_1' : f'Past {type}s',
        'trace_2' : f'Prediction {type}s',
        'head' : f'{type.capitalize()} predictions'
    }
    trace1 = go.Scatter(x=sum_by_month['month'], y=sum_by_month['amount'], mode='lines', name=title['trace_1'], line=dict(color='rgb(247, 247, 247)'))
    trace2 = go.Scatter(x=forecast['month'], y=forecast['amount'], mode='lines', name=title['trace_2'], line=dict(color='rgb(248,181,0)'))

    data = [trace1, trace2]
    
    layout = go.Layout(title=title['head'], xaxis=dict(title='Month'), yaxis=dict(title='Amount'))

    fig = go.Figure(data=data, layout=layout)
    
    fig.update_layout(
        barmode='group',
        plot_bgcolor=COLOR,
        paper_bgcolor=COLOR,
        font=dict(color='white'),
        title=dict(
            font=dict(color='white', size=30)
        ),
        legend=dict(font=dict(size=20, color='white'))
    )

    return fig.to_html(full_html=False)

    
def predict_cumulative(inde, type):
    inde = int(inde)
    match type:
        case 'goal':
            path_to_df = 'app/csvy/goal.csv'
        case _:
            path_to_df = 'app/csvy/trans.csv'

    df = pd.read_csv(path_to_df)
    user_data = df[df['id_user'] == inde]

    user_data['date'] = pd.to_datetime(user_data['date'])
    user_data['month'] = user_data['date'].dt.to_period('M')

    income_data = user_data[user_data['type'] == 'income'].groupby('month')['amount'].sum().reset_index()
    expense_data = user_data[user_data['type'] == 'expense'].groupby('month')['amount'].sum().reset_index()

    budget_data = pd.merge(income_data, expense_data, on='month', how='outer', suffixes=('_income', '_expense')).fillna(0)

    budget_data['net_income'] = budget_data['amount_income'] - budget_data['amount_expense']
    budget_data[type] = budget_data['net_income'].cumsum()

    model = SARIMAX(budget_data[type],  
                    order = (0, 1, 1),  
                    seasonal_order = (2, 1, 1, 12)) 

    result = model.fit(disp=False) 
    
    forecast = result.predict(
        start = len(user_data),  
        end = (len(user_data)-1) + 10,  
        typ = 'levels'
            ).rename(type) 
    last_month = budget_data['month'].iloc[-1]
    budget_data['month'] = budget_data['month'].dt.strftime('%Y-%m')
    new_months = [(last_month + i).strftime('%Y-%m') for i in range(1, len(forecast) + 1)]

    forecast = pd.DataFrame({'month': new_months, type: forecast})

    title = {
        'trace_1' : f'Past {type}',
        'trace_2' : f'Prediction {type}',
        'head' : f'{type.capitalize()} predictions'
    }

    trace1 = go.Scatter(x=budget_data['month'], y=budget_data[type], mode='lines', name=title['trace_1'], line=dict(color='rgb(247, 247, 247)'))
    trace2 = go.Scatter(x=forecast['month'], y=forecast[type], mode='lines', name=title['trace_2'], line=dict(color='rgb(248,181,0)'))

    data = [trace1, trace2]
    
    layout = go.Layout(title=title['head'], xaxis=dict(title='Month'), yaxis=dict(title='Amount'))

    fig = go.Figure(data=data, layout=layout)
    
    fig.update_layout(
        barmode='group',
        plot_bgcolor=COLOR,
        paper_bgcolor=COLOR,
        font=dict(color='white'),
        title=dict(
            font=dict(color='white', size=30)
        ),
        legend=dict(font=dict(size=20, color='white'))
    )

    goal_reached_at = ""
    
    
    if type == 'goal':
        df_accs = pd.read_csv('app/csvy/akks.csv')
     
        target_goal = df_accs.loc[inde, 'goal']
        moneybox = df_accs.loc[inde, 'moneybox']
        # Если цель уже достигнута, выставляем сегодняшнюю дату
        if target_goal <= moneybox:
            now = datetime.now()
            goal_reached_at = now.strftime('%Y-%m')

        else:
            for _, row in forecast.iterrows():
                if row['goal'] >= target_goal:
                    goal_reached_at = row['month']
                    break

    return fig.to_html(full_html=False), goal_reached_at
