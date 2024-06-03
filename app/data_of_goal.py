import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

class Data_goal:
    def __init__(self):
        super(Data_goal, self).__init__()

        try:
            self.df = pd.read_csv('app/csvy/goal.csv')

        except Exception as err:
            self.server()


    def server(self):
        df = pd.DataFrame(columns=['id_user', "amount", "type", "date"], )
        df.to_csv('app/csvy/goal.csv', index=False)


    def add_goal(self, inde, user_amount, user_type):
        df = pd.read_csv('app/csvy/goal.csv')

        if "" in (user_amount, user_type):
            return "Not all fields are filled in."

        if user_amount.isdigit():
            if int(user_amount) > 0:
                current_date = date.today()

                df_1 = pd.DataFrame(
                    data=[[inde, user_amount, user_type, current_date]],
                    columns=['id_user', "amount", "type", "date"], )

                df = pd.concat([df, df_1], ignore_index=True)
                df.to_csv('app/csvy/goal.csv', index=False)
                return ""


        return "Incorrect entry of the transaction amount."

    def type_summ(self, inde, user_type):
        df = pd.read_csv('app/csvy/goal.csv')
        search_inde = df[df["id_user"] == inde]

        search_type = search_inde[search_inde["type"] == user_type]
        summa = search_type['amount'].sum()
        return summa

    def my_cash(self, inde):
        plus = self.type_summ(inde, "Доход")
        minus = self.type_summ(inde, "Расход")

        return (plus - minus)

    def time_ago(self, inde, days_1, type_trans, categories=[]):
        df = pd.read_csv('app/csvy/goal.csv')
        search_inde = df[df["id_user"] == inde]
        search = search_inde[search_inde["type"] == type_trans]

        current_date = date.today()
        current_date = current_date - relativedelta(days=days_1)

        search = search.loc[:, :]
        search['date'] = (pd.to_datetime(search['date']).dt.date)
        search = search.loc[search['date'] >= current_date]

        endy = pd.DataFrame(columns=['id_user', "amount", "type", "category", "date", "description"], )

        for i in categories:
            new = search[search["category"] == i]
            endy = endy._append(new)

        summa = endy['amount'].sum()

        endy.to_csv('app/csvy/end.csv', index=False)
        return summa

    def del_transaction(self, inde):
        df = pd.read_csv('app/csvy/goal.csv')
        df = df[df.id_user != inde]
        df.to_csv('app/csvy/goal.csv', index=False)

#
# if __name__ == "__main__":
#     window = Data_trans()
#     # w = window.add_transection(1, '1', '1', '1', '1')