import pandas as pd

class Data_enter:
    def __init__(self):
        super(Data_enter, self).__init__()

        try:
            df = pd.read_csv('csvy/akks.csv')

        except Exception as err:
            self.server()


    def server(self):
        df = pd.DataFrame(columns=["login", "password"], )
        df.to_csv('csvy/akks.csv', index=False)


    def done_registration(self, login_acc, password_acc, sec_password_acc):
        df = pd.read_csv('csvy/akks.csv')

        if " " in (login_acc + password_acc + sec_password_acc):
            return "Пароль и логин не могут содержать пробелы."
        if (df['login'] == login_acc).any():
            return "Данный логин уже существует."
        if password_acc != sec_password_acc:
            return "Пароли не совпадают."


        df_1 = pd.DataFrame(data=[[login_acc, password_acc]],
                            columns=["login", "password"], )

        df = pd.concat([df, df_1], ignore_index=True)
        df.to_csv('csvy/akks.csv', index=False)
        return ""

    def enter_acc(self, login_acc, password_acc):
        df = pd.read_csv('csvy/akks.csv')

        search_log = df[df["login"] == login_acc]
        try:
            inde = search_log.index[0]
            password_list = df.loc[inde, 'password']

            if password_acc != password_list:
                return "Неверный логин или пароль."
            return str(inde)

        except Exception as err:
            return "Неверный логин или пароль."

    def change_data(self, inde, what_change, for_change):
        df = pd.read_csv('csvy/akks.csv')
        df.at[inde, what_change] = for_change
        df.to_csv('csvy/akks.csv', index=False)

    def del_akk(self, inde):
        df = pd.read_csv('csvy/akks.csv')
        df = df.drop(index=inde)
        df.to_csv('csvy/akks.csv', index=False)


if __name__ == "__main__":
    window = Data_enter()