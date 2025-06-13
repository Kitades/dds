Клонируйте репозиторий:
git clone https://github.com/git@github.com:Kitades/dds.git


Зайти в репозиторий:
cd dds


Установить интерпритатор:
python -m venv venv


Активировать:
source venv/bin/activate


Установить зависимости:
pip install -r requirements.txt


Примените миграции:
python manage.py migrate


Создайте суперпользователя:
python manage.py createsuperuser


Запустите сервер:
python manage.py runserver


Главная страница: http://localhost:8000/


Админ-панель: http://localhost:8000/admin/