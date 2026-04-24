import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacie_project.settings')
django.setup()

from pharmacy.models import Utilisateur

# Create Admin: Reda Taii
if not Utilisateur.objects.filter(username='reda').exists():
    Utilisateur.objects.create_user(
        username='reda',
        password='reda123',
        first_name='Reda',
        last_name='Taii',
        role='admin',
        is_staff=True,
    )
    print("Created Admin: reda (password: reda123)")
else:
    print("Admin 'reda' already exists.")

# Create Employee: Mounit Rajayi
if not Utilisateur.objects.filter(username='mounit').exists():
    Utilisateur.objects.create_user(
        username='mounit',
        password='mounit123',
        first_name='Mounit',
        last_name='Rajayi',
        role='employe',
        is_staff=False,
    )
    print("Created Employee: mounit (password: mounit123)")
else:
    print("Employee 'mounit' already exists.")
