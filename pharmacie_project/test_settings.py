"""
Configuration Django pour l'exécution des tests.
=================================================
Utilise SQLite en mémoire pour des tests rapides,
sans dépendance à MySQL.

Usage : python manage.py test pharmacy --settings=pharmacie_project.test_settings -v 2
"""

from .settings import *  # noqa: F401, F403

# Utiliser SQLite en mémoire pour les tests (rapide, pas de MySQL requis)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Accélérer le hachage des mots de passe pendant les tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
