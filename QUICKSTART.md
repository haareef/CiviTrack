# CiviTrack 360 - Quick Start Guide

## What's Been Created

Your Django project is now fully set up with all 9 pages from the React prototype converted to Django templates with Tailwind CSS styling.

## Project Status

✅ **All 9 Pages Implemented:**
1. ✅ Login Page - Email & DOB authentication
2. ✅ Register Page - User registration
3. ✅ Welcome Page - Welcome screen
4. ✅ Project List - View all projects
5. ✅ New Project - Create projects
6. ✅ Project Details - Manage projects and branches
7. ✅ New Branch - Create branches
8. ✅ Branch History - Track sub-branches and expenses
9. ✅ Released History - View fund release transactions

## Running the Application

### 1. Start the Development Server

```bash
cd "c:\Users\haare\OneDrive\Desktop\CiviTrack_project"
python manage.py runserver
```

The server will be available at: **http://localhost:8000**

### 2. Create a New User Account

- Go to http://localhost:8000/register/
- Fill in the form:
  - **Username**: Your username
  - **Email**: Your email address
  - **DOB (Password)**: 8 digits (e.g., 25042004)
  - **Confirm Password**: Re-enter the 8 digits
- Click "REGISTER"

### 3. Login

- Go to http://localhost:8000/ (or http://localhost:8000/login/)
- Enter your email and DOB
- Click "LOG IN"

### 4. Create a Project

- Click "New Project"
- Fill in:
  - Project Name
  - Project Amount (₹)
  - Starting Date
  - Finishing Date (removed)
- Click "ADD PROJECT"

### 5. Manage Branches

- Click on a project
- Click "New Branch"
- Enter branch name
- Add sub-branches to track expenses
- Monitor total spent amount

### 6. Release Funds

- In project details, enter amount and date in "Released Amount" section
- Click "Submit"
- View release history anytime

## Admin Panel

Access the admin panel at: **http://localhost:8000/admin**

**Default Admin Credentials:**
- Username: `admin`
- Password: You can set this by running: `python manage.py changepassword admin`

## Project Structure

```
📁 CiviTrack_project/
├── 📁 civitrack/              # Main Django project
├── 📁 projects/               # Main app
├── 📁 templates/              # 9 HTML templates
├── manage.py                  # Django management
├── requirements.txt           # Dependencies
├── README.md                  # Full documentation
└── db.sqlite3                 # Database (auto-created)
```

## Database Models

- **Project**: Budget, dates, total released amount
- **Branch**: Organized expenses under projects
- **SubBranch**: Individual expense tracker
- **ReleasedHistory**: Fund release transactions

## Key Features

✨ **Authentication**
- User registration and login
- Secure password handling
- User-specific projects

🏗️ **Project Management**
- Create multiple projects
- Track budgets and timelines
- Monitor fund releases

💼 **Branch Organization**
- Organize expenses into branches
- Track sub-branch expenses
- Calculate totals automatically

📊 **Reporting**
- Released amount history
- Branch expense tracking
- Project budget overview

## Technology Stack

- **Backend**: Django 5.0, Python 3.10+
- **Database**: SQLite (file-based)
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Authentication**: Django built-in

## Deployment

To deploy, see README.md for hosting options:
- Railway
- Render
- PythonAnywhere

## Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8080
```

### Database Issues
```bash
python manage.py migrate
```

### Create New Superuser
```bash
python manage.py createsuperuser
```

### Collect Static Files (for production)
```bash
python manage.py collectstatic
```

## Next Steps

1. ✅ Start the development server
2. ✅ Create a test user account
3. ✅ Create a test project
4. ✅ Add branches and track expenses
5. ✅ Explore all features
6. 📝 Customize to your needs (colors, branding, etc.)

## Need Help?

- Check README.md for detailed documentation
- Django docs: https://docs.djangoproject.com
- Tailwind CSS: https://tailwindcss.com/docs

---

**Happy Building! 🚀**
