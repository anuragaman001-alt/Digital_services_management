"""
Run with: python manage.py shell < seed_data.py
Seeds the database with sample data.
"""
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import CustomUser
from services.models import Plan
from subscriptions.models import Subscription, Invoice
from django.utils import timezone
from datetime import timedelta

print("Seeding data...")

# Create admin
if not CustomUser.objects.filter(username='admin').exists():
    admin = CustomUser.objects.create_superuser(
        username='admin', email='admin@example.com',
        password='admin123', first_name='Admin', last_name='User'
    )
    admin.role = 'admin'
    admin.save()
    print("Admin created: admin / admin123")

# Create test users
for i in range(1, 4):
    if not CustomUser.objects.filter(username=f'user{i}').exists():
        u = CustomUser.objects.create_user(
            username=f'user{i}', email=f'user{i}@example.com',
            password='user123', first_name=f'User{i}', last_name='Test',
            role='user'
        )
        print(f"User created: user{i} / user123")

# Create plans
plans_data = [
    dict(plan_type='wifi', name='Basic WiFi', price=299, validity_days=30, speed_mbps=10, data_limit_gb=100),
    dict(plan_type='wifi', name='Standard WiFi', price=599, validity_days=30, speed_mbps=50, data_limit_gb=None),
    dict(plan_type='wifi', name='Premium WiFi', price=999, validity_days=30, speed_mbps=200, data_limit_gb=None),
    dict(plan_type='sim', name='Basic SIM', price=199, validity_days=28, mobile_data_gb=1, calls='100 mins', sms='100 SMS'),
    dict(plan_type='sim', name='Standard SIM', price=399, validity_days=28, mobile_data_gb=2, calls='Unlimited', sms='Unlimited'),
    dict(plan_type='ott', name='Basic OTT', price=149, validity_days=30, streams=1, resolution='HD'),
    dict(plan_type='ott', name='Premium OTT', price=349, validity_days=30, streams=4, resolution='4K'),
]
for pd in plans_data:
    plan, created = Plan.objects.get_or_create(name=pd['name'], defaults=pd)
    if created:
        print(f"Plan created: {plan.name}")

print("Done! Database seeded.")
