Make sure you have Django installed. If not, you can install it using pip: pip install django.

Apply migrations to create the necessary database tables: python manage.py migrate.

Start the Django development server: python manage.py runserver.

Dependencies: pip install djangorestframework, pip install djangorestframework-simplejwt, pip install django-rest-framework

You can now access the defined endpoints:
Sign up: http://127.0.0.1:8000/signup
Login: http://127.0.0.1:8000/login
Create a note: http://127.0.0.1:8000/notes/create
Share a note: http://127.0.0.1:8000/notes/share
Get a note by ID: http://127.0.0.1:8000/notes/<note_id>
Update a note by ID: http://127.0.0.1:8000/notes/<note_id>/update
Get note version history: http://127.0.0.1:8000/notes/version-history/<id>
