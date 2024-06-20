# Иерархия файлов

```txt
MONAI
├── app
│   ├── analytics
│   │   ├── analytics.py
│   │   ├── model.py
│   │   └── utils
│   │       ├── check_enough_data_for_analytics.py
│   │       ├── __init__.py
│   │       └──process_prediction_data.py
│   ├── csvy
│   │   ├── akks.csv
│   │   ├── end.csv
│   │   ├── goal.csv
│   │   ├── test.csv
│   │   └── trans.csv
│   ├── data_of_entering.py
│   ├── data_of_goal.py
│   ├── data_of_transaction.py
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── static
│   │   ├── imgs
│   │   │   ├── analytics.svg
│   │   │   ├── buget.svg
│   │   │   ├── celendar.svg
│   │   │   ├── Group.svg
│   │   │   ├── logo.svg
│   │   │   └── tommy.png
│   │   └── styles
│   │       └── main.css
│   ├── templates
│   │   ├── analytics_page.html
│   │   ├── auth_page.html
│   │   ├── error.html
│   │   ├── goal_page.html
│   │   ├── layout.html
│   │   ├── main_page.html
│   │   ├── not_enough_data_for_anaytics.html
│   │   └── transactions_page.html
│   ├── test
│   │   ├── test_1.py
│   │   └── test.py
│   └── utils
│       ├── hash_password.py
│       ├── names.py
│       ├── process_form_data.py
│       └── validator.py
├── env
├── Makefile
├── README.md
├── requirements.txt
└── run.py
```

# Документация разработчика

- Диаграмма активности приложения

![Диаграмма активности](/report/data/activity_chart.png)

- Диаграмма устройства баз данных

![Диаграмма активности](/report/data/database_structure.png)
- Описание функций

## `app/routes.py`
```python
"""
    app/routes.py
    Декораторы описывают эндпоинты (и опционально методы), к которым привязаны функции
    Глобально в этом файле есть доступ к сущности session.

    В случае, если в данных пользователя нет в session, выполняе редирект на страница входа/регистрации.
    При попытке открыть страницу регистрации/входа, иначе, выполняем редирект на главную страницу.
"""

```
<br>

#### `main()`
```python
@app.route('/')
def main() -> Union[Response, str]:
    """
    Если пользователь не вошел в сессию, перенаправляем на функцию входа/регистрации
    Иначе получаем индекс пользователя из сессии и отдаем  main_page.html с данными пользователя
    """
    pass
```

### `show_aut()`
```python
@app.get('/auth')
def show_auth() -> Union[Response, str]:
    """
    Отдача шаблона показа формы регистрации auth_page.html
    """
    pass
```

### `do_auth()`
```python
@app.post('/auth')
def do_auth() -> Union[Response, str]:
    """
    Обработка данных из форм.
    Если в пользовательских данных есть поле password_confirmation, то находимся на этапе регистрации.
    Тогда проверяем данные регистрации на валидность. Если данные валидны, добавляем пользователя в БД.
    Далее шаги одинаковые и для регистрации и для входа - добавляем в сессию данные пользователя.
    Если на этапе валидации или входа возвращаемся на страницу входа, отображая ошибку
    """
    pass
```

### `analytics()`
```python
@app.route('/analytics')
def analytics() -> Union[Response, str]:
    """
    Если данных пользователя достаточно для построения аналитики - отрисовываем их и отдаем вместе с шаблоном analytics_page.html
    Иначе возвращаем параметр, которого не хвататет для построения в ошибке, вместе с шаблоном not_enough_data_for_analytics.html
    """
    pass
```

### `show_transactions()`
```python
@app.get('/transactions')
def show_transaction() -> Union[Response, str]:
    """
    Страница отображения формы с добавлением транзакции шаблона transactions_page.html 
    """
    pass
```

### `make_transaction()`
```python
@app.post('/transactions')
def make_transaction() -> Union[Response, str]:
    """
    Обработка данных из форм.
    Если данные валидны, добавляем в бд, иначе, возвращаем выполняем редирект на show_transaction() с соответствующей ошибкой
    """
    pass
```

### `show_goal()`
```python
@app.get('/goal')
def show_goal() -> Union[Response, str]:
    """
    Страница отображения формы с добавлением/обновлением цели из шаблона goal_page.html
    """
    pass
```

### `add_to_goal()`

```python
@app.post('/goal')
def add_to_goal() -> Union[Response, str]:
    """
    Совершние перевода между основным аккаунтом и копилкой, если нет противоречия (недостаточно средств на основном аккаунте или в копилке)
    """
    pass
```

### `new_goal()`

```python
@app.post('/goal-new')
def new_goal() -> Union[Response, str]:
    """
    Обновление цель
    """
    pass
```

### `exit()`

```python
@app.get('/exit')
def exitt():
    """
    Очистка данных сессии
    """
    pass
```

## `app/utils`

### `.../hash_password.py`
### `hash_password()`
```python
def hash_password(password : str) -> str:
    """
    Функция возвращает хэшированный пароль
    """
    pass
```
<br>

### `.../process_form_data.py`
### `process_form_data()`
```python
def process_form_data(user : Dict[str, str]) -> Dict[str, str]:
    """
    Функция возвращает очищенные от символов пустого пространства данные полей
    """
    pass
```
<br>

### `.../validate.py`
### `validate()`
```python
def validate(user : Dict[str, str]) -> str:
    """
    Функция валидирует поля usrname, password, password_confirmation, в случае несоответствия ожидаемым значениям возвращает соответствующую ошибку
    """
    pass
```

## `app/analytics`

### `.../model.py`
### `predict()`
```python
def predict(inde : UUID, type : Enum) -> str:
    """
    Функция предсказания расходов/доходов.
    Строит диаграмму на основе данных пользователя из датафрейма, а так же предсказанных данных. 
    Возвращает html-представление строки диаграммы, встраиваемой в шаблон.
    """
    pass
```
### `predict_cumulative()`
```python
def predict_cumulative(inde : UUID, type : Enum) -> str:
    """
    Функция предсказания кумулятивных единиц - бюджета/копилки.
    Строит диаграмму на основе данных пользователя из датафрейма, а так же предсказанных данных. 
    Возвращает html-представление строки диаграммы, встраиваемой в шаблон.
    """
    pass
```

### `utils/check_enough_data.py`
### `check_enough_data_for_analytics.py`
```python
def check_enough_data_for_analytics(inde : UUID) -> tuple(bool, str):
    """
    Функция для проверки достаточности данных для аналитики.
    В случае, если одно из необходимых условий не выполняется, возвращается соответствующее сообщение о том, чего не хватает.
    """
    pass
```
### `utils/process_prediciton_data`
### `process_prediction_data.py`
```python
def process_goal_prediction(date_str : str) -> str:
    """
    На основе ожидаемой даты достижения цели формируется соотвующее сообщение 
    Если динамика роста отрицательная или не ожидается, что цель будет достигнута в ближайший год, возвращается соответствующее сообщение.
    """
    pass
```
- Описание классов

## `app/data_of_entering.py`
```python
"""
    В файле идет обращение к базе данных app/csvy/akks.csv и ее обработка.
"""

```
<br>

#### `class Data_enter`
```python
class Data_enter:
    def server():
        """
        Создание базы данных с пользователями.
        """
        pass

    def done_registration(login_acc : str, password_acc : str):
        """
        Добавление новой записи, нового пользователя.
        """
        pass

    def enter_acc(login_acc : str, password_acc : str) -> str:
        """
        Проверка совпадения данных при входе с базой данных.
        """
        pass

    def change_data(inde : int, what_change : str, for_change : str, flag : int) -> str:
        """
        изменение данных в определенной ячейке.
        """
        pass

    def del_akk(inde : int):
        """
        Удаление строки в базе данных, информацию о пользоввателе.
        """
        pass

    def info_user(inde : int) -> list[str, int, int]:
        """
        Получение значений из базы данных, информации о пользователе.
        """
        pass
```


## `app/data_of_goal.py`
```python
"""
    В файле идет обращение к базе данных app/csvy/goal.csv и ее обработка.
"""

```
<br>


#### `class Data_goal`
```python
class Data_goal:
    def server():
        """
        Создание базы данных с информацией о транзакциях цели.
        """
        pass

    def add_goal(inde : int, user_amount : int, user_type : str) -> str:
        """
        Добавление новой записи, транзакции цели.
        """
        pass
        
    def type_information(inde : int) -> tuple(int, list):
        """
        Получение остатка на счете пользоваетля в пределенную дату.
        """
        pass

    def my_cash(inde : int) -> int:
        """
        Получение остатка на счете пользоваетля сейчас.
        """
        pass

    def del_transaction(inde : int):
        """
        Удаление строки в базе данных, информацию о транзакциях пользоввателя.
        """
        pass

    def time_ago(inde : int, days_1 : datatime, type_trans : str, categories : list[str]) -> int:
        """
        Получение суммы расоходов или доходов за определенное время.
        """
        pass

```

## `app/data_of_transaction.py`
```python
"""
    В файле идет обращение к базе данных app/csvy/trans.csv и ее обработка.
"""

```
<br>


#### `class Data_trans`
```python
class Data_trans:
    def server():
        """
        Создание базы данных с информацией о транзакциях пользователя.
        """
        pass

    def add_transaction(inde : int, user_amount : int, user_type : str, user_category : str, user_description : str, user_date : datetime) -> str:
        """
        Добавление новой записи транзакции.
        """
        pass
        
    def type_summ(inde : int, user_type : str) -> int:
        """
        Получение суммы расходов или доходов пользователя.
        """
        pass

    def my_cash(inde : int) -> int:
        """
        Получение остатка на счете пользоваетля сейчас.
        """
        pass

    def count_of_category(inde : int):
        """
        Получение количества транзакций, связанных с определенной категорией, 
        """
        pass

    def category_out(inde : int, days_1 : datatime, type : str) -> list[list[str, int]]:
        """
        Получение расходов или доходов пользователя на категории.
        """
        pass

    def sum_for_month(inde : int, month : int, type : str) -> int:
        """
        Получение суммы расходы или дохода за определенное количество месяцев..
        """
        pass

    def del_transaction(inde : int):
        """
        Удаление строки в базе данных, информацию о транзакциях пользоввателя.
        """
        pass

    def time_ago(inde : int, days_1 : datatime, type_trans : str, categories : list[str]) -> int:
        """
        Получение суммы расоходов или доходов на определенные категории.
        """
        pass
```