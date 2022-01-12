# django_blog
Blog written with Djnago with book Django2 by Example by Antonio Mele

## How to run
- Pull repository and move to project dir
- Create virtualenv
```python
python -m venv env
```
- Install requirements
```python
pip install -r requirements.txt
```
- Create .env file in root project dir with next variables
    - DJANGO_SECRET_KEY (str) secret key for your project
    - DJANGO_DEBUG (int 0|1) 1 if you need to start project with debug mode else 0
    - EMAIL_HOST (str) smpt host. For example smtp.gmail.com
    - EMAIL_HOST_USER (str) username for smpt
    - EMAIL_HOST_PASSWORD (str) password for smpt
    - EMAIL_USE_TLS (int 0|1) if 1 TLS protocol will be enabled
    - EMAIL_PORT (int) default 587
- Run project with
```python
python manage.py runserver
```
- Go to localhost:8000
