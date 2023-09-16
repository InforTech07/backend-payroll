# backend-payroll
Payroll management platform API


# Books app
--- 
## descripcion 
El proyecto delslls.,.s

1. docker-compose run api django-admin startproject <nombre-proyecto> .
   docker-compose run --rm api python manage.py startapp apps/<nombre-app>
   crear los directorios primero
   docker-compose run --rm api python manage.py startapp user ./apps/user

2. docker-compose -f docker-compose.yml build startapp

docker-compose up

docker-compose -f .\docker-compose.yml run --rm web python manage.py makemigrations
docker-compose -f .\docker-compose.yml run --rm web python manage.py migrate

docker-compose -f .\docker-compose.yml run --rm web python manage.py createsuperuser

python manage.py migrate admin zero
python manage.py migrate user zero

docker-compose run --rm api python manage.py makemigrations user


djoser:
http://localhost:8000/auth/users/  ver usuarios y crear usuarios


jwt
jwt/create/

"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5NzQyMDYwOCwianRpIjoiN2IyNGY5MWY1NWJmNDljZGIwZWIwMzAyZjAwM2RjZGUiLCJ1c2VyX2lkIjoxfQ.L81QLprvi0ofcpyzV8eh7b-ZcyGWQFEzxIzQMHSPg6A",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk1NDMzNDA4LCJqdGkiOiIxYjE5NTc3ZmIzNTg0Y2VkOTFjMmUwZDMxYTgzOGJkNCIsInVzZXJfaWQiOjF9.p0IdYr92og5MqR20wbSzrauoC07GLhPwG0IWEJ_ncVM"

/users/activation/
uid=MQ
token= bulj71-42e515729577978bb0eeb640c5c40d1b