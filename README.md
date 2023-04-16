# hw05_final

## Описание проекта
Yatube - социальная сеть для публикации дневников.
Используется классическая MVT архитектура, присутствует пагинация постов и кеширование
страниц. Реализована регистрация с верификацией данных, сменой и восстановление пароля
через e-mail. Подготовлены тесты, проверяющие работу сервиса.

## Инструкции по запуску
Клонировать репозиторий и перейти в него в командной строке:

```bash
@git clone https://github.com/KiselevD92/hw05_final.git
@cd hw05_final
```

Cоздать и активировать виртуальное окружение:

```bash
@python3 -m venv env
@source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```bash
@python3 -m pip install --upgrade pip
@pip install -r requirements.txt
```
Выполнить миграции:

```bash
@python3 manage.py migrate
```

Запустить проект:

```bash
@python3 manage.py runserver
```

## Использованные технологии
Python 3.7
Django 3
Django REST Framework
PostgreSQL
Simple-JWT
pytest

## Автор
Киселев Дмитрий
