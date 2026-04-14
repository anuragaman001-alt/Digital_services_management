# Digital Services Management — Setup Guide

## Requirements
- Python 3.10+
- pip

## Setup Steps

### 1. Create and activate virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run migrations
```bash
python manage.py migrate
```

### 4. Seed sample data (optional)
```bash
python manage.py shell < seed_data.py
```

### 5. Run the server
```bash
python manage.py runserver
```

### 6. Open in browser
Go to: http://127.0.0.1:8000/accounts/login/

## Default Accounts (after seeding)
- Admin: `admin` / `admin123`
- User: `user1` / `user123`

## Project Structure
```
digital_services/
├── accounts/       # User auth, registration, profile
├── services/       # Plans management
├── subscriptions/  # Subscription management
├── reports/        # Sales report (admin only)
├── templates/      # HTML templates
├── core/           # Django settings and URL config
└── manage.py
```

## Features
- User registration and login (no OTP)
- Admin and user roles
- WiFi, SIM, OTT plan management
- Subscription management (Active / Inactive)
- Invoice download
- Sales report with CSV export (admin only)
