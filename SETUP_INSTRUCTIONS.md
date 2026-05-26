# Robotic Lab System — Setup Instructions

## Files to copy into your project

Copy all files from this zip into your `robotic_lab_system/` directory,
replacing any existing ones. The structure is:

```
robotic_lab_system/
├── robotic_lab/
│   ├── settings.py       ← REPLACE
│   └── urls.py           ← REPLACE
├── accounts/
│   ├── models.py, views.py, urls.py, forms.py, admin.py, apps.py
├── core/
│   ├── models.py, views.py, urls.py, apps.py
├── inventory/
│   ├── models.py, views.py, urls.py, forms.py, admin.py, apps.py
├── schedules/
│   ├── models.py, views.py, urls.py, forms.py, admin.py, apps.py
├── lab_reports/
│   ├── models.py, views.py, urls.py, forms.py, admin.py, apps.py
├── messaging_app/
│   ├── models.py, views.py, urls.py, forms.py, admin.py, apps.py
└── templates/
    ├── base.html
    ├── accounts/   (login, register, profile, user_list)
    ├── core/       (dashboard)
    ├── inventory/  (equipment_list, detail, form, delete, maintenance_form)
    ├── schedules/  (session_list, detail, form, approve, cancel)
    ├── lab_reports/(report_list, detail, form, review_form)
    └── messaging_app/ (inbox, sent, message_detail, compose, notifications)
```

## Step-by-step setup

### 1. Install Pillow (needed for image uploads)
```powershell
pip install Pillow
```

### 2. Create and apply migrations
```powershell
python manage.py makemigrations accounts
python manage.py makemigrations inventory
python manage.py makemigrations schedules
python manage.py makemigrations lab_reports
python manage.py makemigrations messaging_app
python manage.py migrate
```

### 3. Create superuser (admin)
```powershell
python manage.py createsuperuser
```

### 4. Create static and media directories
```powershell
mkdir static
mkdir media
```

### 5. Run the server
```powershell
python manage.py runserver
```

### 6. Visit the app
- App:       http://127.0.0.1:8000/
- Admin:     http://127.0.0.1:8000/admin/

## First steps after login
1. Log in as superuser at /admin/ and set your role to "Admin"
2. Add Equipment Categories in admin (e.g. Robot Arms, Sensors, Computers)
3. Add Equipment items
4. Register test users with Technician and Researcher roles
5. Try booking a lab session and approving it

## User Roles
| Role | Can Do |
|------|--------|
| Admin | Everything + user management |
| Technician | Manage equipment, approve sessions, review reports |
| Researcher | Book sessions, write reports, message others |
