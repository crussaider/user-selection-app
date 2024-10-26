# user-selection app

## Функциональность

- **GET /admin**: Админ панель.
- **GET /api/users/{id}**: Получить пользоватея по его ID.

## Запуск приложения

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/crussaider/user-selection-app.git
    cd user-selection-app
    ```

2. Запустите Docker Compose контейнер:
    ```bash
    docker-compose up --build
    ```

3. Выполните миграции и перезапустите Django-приложение:
    ```bash
    docker-compose exec drf-web python manage.py makemigrations
    docker-compose exec drf-web python manage.py migrate
    docker-compose restart drf-web
    ```

## Команды

После запуска приложения можно создать пользователей:
```bash
docker-compose exec drf-web python manage.py create_users
```
Пользователи с ролью "crm_admin" могут использовать админ панель `http://localhost:8000/admin`.
