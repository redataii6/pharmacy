"""
Configuration des URLs principales du projet.
==============================================
Ce fichier regroupe toutes les routes de l'application.
Les URLs de l'application pharmacy sont incluses via include().
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Interface d'administration Django (accessible via /admin/)
    path('admin/', admin.site.urls),

    # Toutes les URLs de notre application de pharmacie
    # Inclut les routes définies dans pharmacy/urls.py
    path('', include('pharmacy.urls')),
]
