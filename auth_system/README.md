# Auth System (DRF) — Test Task

Backend: регистрация/логин/логаут/профиль/soft-delete + RBAC (User → Role → Permission).  
Ошибки: **401** если нет токена, **403** если токен есть, но прав нет.

## Запуск (локально)

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate

pip install -r requirements.txt

python manage.py makemigrations users access
python manage.py migrate
python manage.py seed
python manage.py runserver