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

For Railway, the project also supports the plugin connection strings:
- `DATABASE_URL`
- `MYSQL_URL`

If you add a Railway MySQL plugin, Railway will usually provide a connection URL automatically. If it does not, copy the MySQL connection string from the service and set `DATABASE_URL` or `MYSQL_URL`.

Also set these production variables on Railway:
- `SECRET_KEY`
- `DEBUG=false`
- `ALLOWED_HOSTS=admin-member-dashboard-production.up.railway.app`

If you are using a custom Railway domain, replace the value with your domain.

Create a `.env.example` file in the repo with these values to document your environment variables for the project.
