# Local Masters Platform

Клиент-серверное веб-приложение «Платформа для локальных мастеров».

Проект представляет собой онлайн-площадку, где пользователи могут размещать изделия ручной работы, просматривать товары других мастеров, добавлять товары в корзину и оформлять заказы.

## Функциональность

- регистрация и вход пользователя;
- просмотр каталога товаров;
- просмотр страницы отдельного товара;
- профиль пользователя;
- добавление товара мастером;
- загрузка изображения товара;
- добавление товаров в корзину;
- изменение количества товаров в корзине;
- оформление заказа;
- просмотр списка заказов;
- запрет добавления собственного товара в корзину;
- административная панель Django.

## Технологический стек

- Python
- Django
- Django Templates
- Bootstrap 5
- PostgreSQL
- Redis
- Gunicorn
- WhiteNoise
- Docker
- Docker Compose
- GitHub Actions
- Render

## Структура проекта

```text
local_masters_platform/
├── core/                 # настройки проекта Django
├── pages/                # главная страница
├── products/             # товары и каталог
├── profiles/             # профили пользователей
├── orders/               # корзина и заказы
├── users/                # регистрация и авторизация
├── templates/            # HTML-шаблоны
├── static/               # статические файлы
├── media/                # пользовательские изображения
├── Dockerfile            # сборка Docker-образа
├── docker-compose.yml    # запуск приложения и сервисов
├── requirements.txt      # зависимости Python
├── build.sh              # скрипт сборки для Render
└── manage.py
```

## Локальный запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/badabumb/local_masters_platform.git
cd local_masters_platform
```

### 2. Создать виртуальное окружение

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Выполнить миграции

```bash
python manage.py migrate
```

### 5. Создать администратора

```bash
python manage.py createsuperuser
```

### 6. Запустить приложение

```bash
python manage.py runserver
```

После запуска приложение будет доступно по адресу:

```text
http://127.0.0.1:8000/
```

## Запуск через Docker Compose

```bash
docker compose up --build
```

После запуска приложение будет доступно по адресу:

```text
http://localhost:8080/
```

## Административная панель

Административная панель Django доступна по адресу:

```text
http://localhost:8080/admin/
```

В ней можно управлять пользователями, профилями, товарами, корзиной и заказами.

## Переменные окружения

Приложение использует переменные окружения для настройки разных сред запуска.

Пример:

```text
SECRET_KEY=secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=postgres
POSTGRES_DB=masters_db
POSTGRES_USER=masters_user
POSTGRES_PASSWORD=masters_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
REDIS_HOST=redis
REDIS_PORT=6379
APP_VERSION=1.0.0
APP_ENV=development
```

## Облачное развёртывание

Приложение развёрнуто на платформе Render.

Публичный адрес:

```text
https://local-masters-platform.onrender.com
```

В качестве базы данных используется PostgreSQL, размещённая в облачной инфраструктуре Render.

## Назначение проекта

Проект разработан в рамках курсовой работы по дисциплине «Проектирование и разработка клиент-серверных приложений».

Тема курсовой работы: «Платформа для локальных мастеров».