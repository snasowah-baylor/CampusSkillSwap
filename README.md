# Campus SkillSwap

A beginner-friendly Django project for a student marketplace where users can post skills or services they offer to others.

## Features
- Create, edit, and view skill posts
- User signup, login, and logout
- Dashboard for managing personal listings
- Simple Bootstrap-based UI

## Setup
1. Activate your existing virtual environment.
2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Notes
- The app uses SQLite by default.
- Use the admin site at `/admin/` to inspect `SkillPost` records.
