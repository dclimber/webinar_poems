# Как наcтроить окружение для вебинара
Для сайта со стихами поэтов

## Как запустить:
1. Скачиваете репозиторий по ссылке в Slack.

2. Открываете терминал в папке с репозиторием: `poems_precode`

3. Создаете виртуальное окружение:

```python3 -m venv env```

4. Запускаете его:

Linux/Mac:
```source env/bin/activate ```

Windows:
```env\Scripts\activate```

5. Обновляете pip:

```pip install -U pip```

6. Устанавливаете всё необходимое:

```pip install -r requirements.txt```

7. Создаете супер-пользователя:

```python manage.py createsuperuser```

8. Запускаете сервер:

```python manage.py runserver```


## Как запускать тесты

#### Для приложения `poems`:

```python manage.py test poems --settings=olender.settings.base```

#### Для приложения `search`:

```python manage.py test search --settings=olender.settings.base```
