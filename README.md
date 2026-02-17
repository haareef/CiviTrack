<<<<<<< HEAD
# CiviTrack 360 - Site Management System

A comprehensive Django-based site management system for tracking projects, branches, expenses, and fund releases.

## Features

- **User Authentication**: Register and login with email and DOB
- **Project Management**: Create and manage multiple projects with budgets and timelines
- **Branch Management**: Organize projects into branches for better expense tracking
- **Expense Tracking**: Track sub-branches and individual expenses
- **Fund Release History**: Monitor all fund releases with dates
- **Responsive Design**: Mobile-friendly interface with Tailwind CSS

## Tech Stack

- **Backend**: Python 3.10+, Django 5.0
- **Database**: SQLite
- **Frontend**: HTML, CSS (Tailwind CSS), JavaScript
- **Authentication**: Django's built-in auth system

## Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or extract the project**
   ```bash
   cd CiviTrack_project
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser** (admin account)
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

## Project Structure

```
CiviTrack_project/
├── civitrack/              # Main Django project
│   ├── settings.py        # Project settings
│   ├── urls.py            # Main URL configuration
│   ├── wsgi.py            # WSGI application
│   └── asgi.py            # ASGI application
├── projects/              # Django app
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # App URL configuration
│   ├── forms.py           # Form definitions
│   ├── admin.py           # Admin configuration
│   └── migrations/        # Database migrations
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── welcome.html       # Welcome page
│   ├── project_list.html  # Project list page
│   ├── new_project.html   # Create project page
│   ├── project_details.html
│   ├── new_branch.html    # Create branch page
│   ├── branch_history.html
│   ├── edit_subbranch.html
│   └── released_history.html
├── static/                # Static files (CSS, JS, images)
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── db.sqlite3             # SQLite database (created after migration)
```

## Pages Overview

1. **Login Page** - User authentication with email and DOB
2. **Register Page** - Create new user account
3. **Welcome Page** - Welcome screen after login
4. **Project List** - View all projects
5. **New Project** - Create a new project
6. **Project Details** - View project details, manage branches, and release funds
7. **New Branch** - Create a new branch under a project
8. **Branch History** - Manage sub-branches and track expenses
9. **Released History** - View all fund release transactions

## Key Models

### Project
- name
- amount (total budget)
- start_date
- end_date (removed)
- total_released
- user (ForeignKey to User)

### Branch
- project (ForeignKey)
- name
- total_spent

### SubBranch
- branch (ForeignKey)
- name
- amount
- date

### ReleasedHistory
- project (ForeignKey)
- amount
- date

## Usage

### Create a Project
1. Login with your account
2. Click "New Project"
3. Fill in project details and save

### Add Branches
1. Go to project details
2. Click "New Branch"
3. Enter branch name

### Track Expenses
1. Go to branch details
2. Add sub-branches with amounts and dates
3. Track total spent

### Release Funds
1. Go to project details
2. Enter amount and date in "Released Amount" section
3. Click "Submit"
4. View history anytime

## Admin Panel

Access the admin panel at `/admin` to:
- Manage users
- View and edit projects
- Manage branches and sub-branches
- View released history

## Future Enhancements

- Export reports to PDF/Excel
- Role-based access control
- Project completion tracking
- Budget analysis and forecasting
- Mobile app
- Email notifications

## Support & Documentation

For more information about Django, visit: https://docs.djangoproject.com

## License

This project is open source and available for educational purposes.

---

**Developed by**: Haareef M A
=======
# CiviTrack
>>>>>>> b4385c522fb00dee1d1e01fbe67ea5c223ec556f
