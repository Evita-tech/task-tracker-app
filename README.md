# Task Tracker

A secure, web-based Task Tracking application built with Django as part of an internship assignment. It supports role-based project and task management, with Managers able to create projects/tasks and assign them, and Team Members able to update the status of tasks assigned to them.

## Features

- **User authentication** — registration, login, and logout
- **Role-based access control** — two roles (Manager and Team Member) with different permissions, enforced using Django Groups
- **Project management** — Managers can create and view projects
- **Task management** — Managers can create tasks, assign them to users, and set their status (To Do, In Progress, Done)
- **Dashboard** — live counts of projects and tasks by status
- **Search, filter, and sort** — on the task list, by keyword, status, and column
- **Responsive UI** — styled with Bootstrap
- **Automated tests** — covering authentication, permissions, and core workflows

## Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite (default Django database)
- **Frontend:** Django templates, Bootstrap
- **Version control:** Git, GitHub
- **API testing:** Postman

## Setup / Installation

1. Clone the repository:

git clone https://github.com/Evita-tech/task-tracker-app.git
cd task-tracker-app

2. Create and activate a virtual environment:
 ```
 python -m venv .venv
.venv\Scripts\activate
```


3. Install dependencies:
```
pip install -r requirements.txt
```


4. Apply database migrations:
```
python manage.py migrate
```


5. Create a superuser (for admin access):
```
python manage.py createsuperuser
```


6. Run the development server:
```
python manage.py runserver
```

7. Open your browser and go to http://127.0.0.1:8000/


## Project Structure

- `tasktracker/` — main Django project settings and URL configuration
- `tasks/` — the core app containing models, views, forms, templates, and tests
- `templates/registration/` — login template
- `requirements.txt` — Python package dependencies
- `db.sqlite3` — the SQLite database file

## Role-Based Access Control

Two Django Groups control permissions:

- **Manager** — can create and view projects, create and assign tasks
- **Team Member** — can only update the status of tasks assigned to them

Access checks are enforced in the view functions, and unauthorized users are redirected to the dashboard.

## Running Tests

Automated tests cover authentication, permissions, and core workflows. Run them with:

```
python manage.py test
```