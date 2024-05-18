import pandas as pd

class Data_enter:
    def __init__(self):
        super(Data_enter, self).__init__()

        try:
            df = pd.read_csv('app/csvy/akks.csv')

        except Exception as err:
            self.server()


    def server(self):
        df = pd.DataFrame(columns=["login", "password", "goal"], )
        df.to_csv('app/csvy/akks.csv', index=False)


    def done_registration(self, login_acc, password_acc):
        df = pd.read_csv('app/csvy/akks.csv')

        df_1 = pd.DataFrame(data=[[login_acc, password_acc, "0/0"]],
                            columns=["login", "password", "goal"])

        df = pd.concat([df, df_1], ignore_index=True)
        df.to_csv('app/csvy/akks.csv', index=False)
        return ""

    # def change_goal(self, log, amountic, flag=0):
    #     df = pd.read_csv('app/csvy/akks.csv')
    #     search_inde = df[df["login"] == log]
    #     what_change = search_inde["goal"]
    #     k = what_change.index('/')
    #
    #     if flag == 1:
    #         df.at[inde, "goal"] = what_change[:k] + str(amountic)
    #     else:
    #         df.at[inde, "goal"] = str(amountic) + what_change[k + 1:]
    #     df.to_csv('app/csvy/akks.csv', index=False)


    def enter_acc(self, login_acc, password_acc):
        df = pd.read_csv('app/csvy/akks.csv')

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
        df = pd.read_csv('app/csvy/akks.csv')
        df.at[inde, what_change] = for_change
        df.to_csv('app/csvy/akks.csv', index=False)

    def del_akk(self, inde):
        df = pd.read_csv('app/csvy/akks.csv')
        df = df.drop(index=inde)
        df.to_csv('app/csvy/akks.csv', index=False)


# if __name__ == "__main__":
#     window = Data_enter()