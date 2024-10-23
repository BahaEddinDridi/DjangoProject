python -m venv env
env\Scripts\activate
python manage.py runserver
pip install -r requirements.txt
python manage.py migrate
