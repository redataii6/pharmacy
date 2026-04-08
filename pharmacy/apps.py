"""
Configuration de l'application Pharmacy.
=========================================
Définit le nom de l'application et son affichage dans l'admin Django.
"""

from django.apps import AppConfig


class PharmacyConfig(AppConfig):
    """Configuration de l'application de gestion de pharmacie."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pharmacy'
    # Nom affiché dans l'interface d'administration Django
    verbose_name = 'Gestion de Pharmacie'
