# Учебный проект для первого вебинара
Сайт со стихами поэтов

# Как запустить:
Клонируете репозиторий:

```git clone https://github.com/dclimber/webinar_poems.git```

Создаете виртуальное окружение:

```python3 -m venv env```

Запускаете его:

Linux/Mac:
```source env/bin/activate ```

Windows:
```env\Scripts\activate```

Обновляете pip:

```pip install -U pip```

Устанавливаете всё необходимое:

```pip install -r requirements.txt```

Делаете миграции:

```python manage.py migrate```

Создаете супер-пользователя:

```python manage.py createsuperuser```

Запускаете сервер:

```python manage.py runserver```


# Как работать:
В админке:
1) Добавьте поэтов из poets.txt
2) Загрузите .html файлы через parser:
akhmatova.html
esenin.html
vladimir.html
bella.html
marina.html
3) «тыкайте и наслаждайтесь»
