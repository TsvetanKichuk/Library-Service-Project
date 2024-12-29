# Library Service Project

## Project Description

This is a service designed to manage borrowing and returning books within a library system.
The project is built using Django, Django REST Framework, and follows RESTful API standards.
The library service enables users to borrow books, return them, track overdue borrowing records,
and manage basic library operations such as book and user management.

## Technology Stack

- **Backend:** Python 3.12.7, Django 5.x, Django REST Framework, Celery
- **Database:** PostgreSQL
- **Testing:** Django Test Framework
- **Others:** Click, Pillow, PyYAML, psycopg2, pyflakes, pytz

## Installation

### System Requirements

- Python 3.12.7
- PostgreSQL
- pip (Python package installer)

### Installation Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/TsvetanKichuk/Library-Service-Project
    cd library_service_project
    ```

2. Set up a virtual environment:
    ```in to the terminal
    python -m venv venv
    source venv/bin/activate  # For Windows: venv\Scripts\activate
    ```

3. Install the dependencies:
    ```in to the terminal
    pip install -r requirements.txt
    ```
4. Create .env file:
   set DB_HOST=<your db hostname>
   set DB_NAME=<your db name>
   set DB_USER=<your db username>
   set DB_PASSWORD=<your db user password>
   set SECRET_KEY=<your secret key>

5. Configure your database settings in `settings.py`:
    ```python
     DATABASES = {
     "default": {
         "ENGINE": "django.db.backends.postgresql",
         "NAME": os.environ["POSTGRES_DB"],
         "USER": os.environ["POSTGRES_USER"],
         "PASSWORD": os.environ["POSTGRES_PASSWORD"],
         "HOST": os.environ["POSTGRES_HOST"],
         "PORT": os.environ["POSTGRES_PORT"],
     }
 }
      ```

6. Apply migrations:
    ```in to the terminal
    python manage.py migrate
    ```

7. Run the development server:
    ```in to the terminal
    python manage.py runserver
    ```

8. Create a superuser to access the admin panel:
    ```in to the terminal
    python manage.py createsuperuser
    ```
   # Getting access

<ul>
  <li>Create user via /api/user/register/</li>
  <li>Get access token via /api/user/token/</li>
</ul>

## Run with docker

## Docker should be installed

```shell
    docker build -t <your login name/name of image> .
    docker-compose up
```

## Usage

After starting the server, the interface is available at: `http://127.0.0.1:8000`.

### API Endpoints

Major endpoints for interacting with the application:

- `/api/user/register/` - Register a new user
- `/api/user/token/` - Get token of user
- `/api/user/me/` - Retrieve details of the logged-in user
- `/api/books/` - List all books
- `/api/books/<id>/` - Get details of a book 
- `/api/borrowings/` - List borrowings
- `/api/borrowings/<id>/` - Get details of a borrowing
- `/api/borrowings/return/<id>/` - Return a borrowed book with the actual return date
- `/api/payments/` - List of payments


### Swagger API
- `/api/doc/swagger/`

### Interface Screenshots

![Снимок экрана 2024-12-29 152526](https://github.com/user-attachments/assets/20b12da3-9d61-4731-8a3c-357fdca0d360)
![Снимок экрана 2024-12-29 152440](https://github.com/user-attachments/assets/47857cad-1d2f-4829-8e39-58e731fc14c6)
![Снимок экрана 2024-12-29 152401](https://github.com/user-attachments/assets/18ee3f28-70de-4058-93b4-6f1585063d54)
![Снимок экрана 2024-12-29 152342](https://github.com/user-attachments/assets/1108b9af-cb88-400f-ac44-0367a6d554cd)
![Снимок экрана 2024-12-29 152319](https://github.com/user-attachments/assets/5d96ce06-b87c-4043-aefb-9d59e7b329dd)
![Снимок экрана 2024-12-29 152606](https://github.com/user-attachments/assets/37a4261d-2e39-4c14-ac97-5cd3865b2475)

## Testing

To run tests, execute:

```in to the terminal
python manage.py test
```
