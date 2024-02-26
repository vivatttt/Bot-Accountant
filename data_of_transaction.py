import pandas as pd
from datetime import date

class Data_trans:
    def __init__(self):
        super(Data_trans, self).__init__()

        try:
            df = pd.read_csv('trans.csv')

        except Exception as err:
            self.server()


    def server(self):
        df = pd.DataFrame(data=[[0, 0, "0", "0", "0", "0"]],
                          columns=['id_user', "amount", "type", "category", "date", "description"], )
        df.to_csv('trans.csv', index=False)


    def add_transection(self, inde, user_amount, user_type, user_category, user_description):
        df = pd.read_csv('trans.csv')

        if "" in (user_amount, user_type, user_category, user_description):
            return "Не все поля заполнены."

        if user_amount.isdigit():
            if int(user_amount) > 0:
                current_date = date.today()
                df_1 = pd.DataFrame(data=[[inde, user_amount, user_type, user_category, current_date, user_description]],
                                    columns=['id_user', "amount", "type", "category", "date", "description"], )

                df = pd.concat([df, df_1], ignore_index=True)
                df.to_csv('trans.csv', index=False)
                return ""

        return "Неверный ввод суммы транзакции."

    def type_summ(self, inde, user_type):
        df = pd.read_csv('trans.csv')
        search_inde = df[df["id_user"] == inde]

        search_type = search_inde[search_inde["type"] == user_type]
        summa = search_type['amount'].sum()
        return summa

    def my_cash(self, inde):
        plus = self.type_summ(inde, "Доход")
        minus = self.type_summ(inde, "Расход")
        return (plus - minus)

    def count_of_category(self, inde):
        df = pd.read_csv('trans.csv')
        search_inde = df[df['id_user'] == inde]

        counts_values = list(search_inde['category'].value_counts())
        unique_values = list(search_inde['category'].drop_duplicates())

        counts = []
        for i in range(len(unique_values)):
            counts.append([unique_values[i], counts_values[i]])
        return counts

    def category_out(self, inde, user_category):
        df = pd.read_csv('trans.csv')
        search_inde = df[df["id_user"] == inde]

        search_category_out = search_inde[search_inde["category"] == user_category]
        search_category_out = search_category_out[search_category_out["type"] == "Расход"]
        summa = search_category_out['amount'].sum()
        return summa

    def del_transaction(self, inde):
        df = pd.read_csv('trans.csv')
        df = df[df.id_user != inde]
        df.to_csv('trans.csv', index=False)





if __name__ == "__main__":
    window = Data_trans()
    r = window.add_transection(1, '2', 'Доход', "party", "I wanna party")
    r = window.add_transection(1, '16', 'Доход', "school", "I wanna go to school")
    r = window.add_transection(2, '2', 'Доход', "party", "I wanna party")
    r = window.add_transection(1, '2', 'Расход', "party", "I wanna party")
    r = window.add_transection(1, '14', 'Расход', "plane", "I wanna go to school")
    r = window.add_transection(2, '1', 'Расход', "party", "I wanna party")
    w = window.my_cash(2)
    w = window.my_cash(1)
    window.count_of_category(1)
    w = window.category_out(1, "plane")
    window.count_of_category(1)
    window.del_transaction(1)