import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
from app.utils.names import categories, types
class Data_trans:
    def __init__(self):
        super(Data_trans, self).__init__()

        try:
            self.df = pd.read_csv('app/csvy/trans.csv')

        except Exception as err:
            self.server()


    def server(self):
        df = pd.DataFrame(columns=['id_user', "amount", "type", "category", "date", "description"], )

        df.to_csv('app/csvy/trans.csv', index=False)


    def add_transection(self, inde, user_amount, user_type, user_category, user_description, user_date=False):
        df = pd.read_csv('app/csvy/trans.csv')

        if "" in (user_amount, user_type, user_category, user_description):
            return "Not all fields are filled in."

        if user_amount.isdigit():
            if int(user_amount) > 0:
                if user_date == False:
                    current_date = date.today()
                else:
                    current_date = user_date

                df_1 = pd.DataFrame(
                    data=[[inde, user_amount, user_type, user_category, current_date, user_description]],
                    columns=['id_user', "amount", "type", "category", "date", "description"], )

                df = pd.concat([df, df_1], ignore_index=True)
                df.to_csv('app/csvy/trans.csv', index=False)
                return ""


        return "Incorrect entry of the transaction amount."

    def type_summ(self, inde, user_type):
        df = pd.read_csv('app/csvy/trans.csv')
        search_inde = df[df["id_user"] == inde]

        search_type = search_inde[search_inde["type"] == user_type]
        summa = search_type['amount'].sum()
        return summa

    def my_cash(self, inde):
        plus = self.type_summ(inde, "Income")
        minus = self.type_summ(inde, "Expense")

        return (plus - minus)

    def count_of_category(self, inde):
        df = pd.read_csv('app/csvy/trans.csv')
        search_inde = df[df['id_user'] == inde]

        counts_values = list(search_inde['category'].value_counts())
        unique_values = list(search_inde['category'].drop_duplicates())

        counts = []
        for i in range(len(unique_values)):
            counts.append([unique_values[i], counts_values[i]])
        return counts

    def category_out(self, inde, days_1):
        df = pd.read_csv('app/csvy/trans.csv')
        search_inde = df[df["id_user"] == inde]

        current_date = date.today()
        current_date = current_date - relativedelta(days=days_1)

        search_inde = search_inde.loc[:, :]
        search_inde['date'] = (pd.to_datetime(search_inde['date']).dt.date)
        search_inde = search_inde.loc[search_inde['date'] >= current_date]

        cater = []

        for i in categories:
            search_category_out = search_inde[search_inde[i] == user_category]
            search_category_out = search_category_out[search_category_out["type"] == "Expense"]
            summa = search_category_out['amount'].sum()
            cater.append([i, summa])
        return cater

    def time_ago(self, inde, days_1, type_trans, categories=[]):
        df = pd.read_csv('app/csvy/trans.csv')
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
        df = pd.read_csv('app/csvy/trans.csv')
        df = df[df.id_user != inde]
        df.to_csv('app/csvy/trans.csv', index=False)

#
# if __name__ == "__main__":
#     window = Data_trans()
#     # w = window.add_transection(1, '1', '1', '1', '1')