# Admin Dashboard

A Django-based admin dashboard with role-based access control for Admin and Member roles.

## Features
- Authentication (signup/login)
- Role-based access control
- Project and task management
- Dashboard summary with task status and overdue counts
- REST API endpoints for frontend integration

## Setup
1. Activate the Python virtual environment:
   ```powershell
   .venv\Scripts\Activate
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```powershell
   .venv\Scripts\python.exe manage.py migrate
   ```
4. Start the development server:
   ```powershell
   .venv\Scripts\python.exe manage.py runserver
   ```

## Database
By default, the app uses SQLite for local development. To use MySQL, set these environment variables before running the app:
- `MYSQL_DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_HOST`
- `MYSQL_PORT`
