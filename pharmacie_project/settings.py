"""
Configuration Django pour le projet de gestion de pharmacie.
============================================================
Ce fichier contient tous les paramètres du projet :
- Connexion à la base de données MySQL
- Applications installées
- Configuration de l'authentification
- Paramètres de localisation (français)
"""

import os
from pathlib import Path

# ============================================================
# CHEMINS DE BASE
# ============================================================
# Répertoire racine du projet (deux niveaux au-dessus de ce fichier)
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# SÉCURITÉ
# ============================================================
# Clé secrète pour le chiffrement — À CHANGER en production !
SECRET_KEY = 'django-insecure-pharma-projet-universitaire-clef-a-changer-2024'

# Mode débogage activé pour le développement
DEBUG = True

# Hôtes autorisés à accéder à l'application
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# ============================================================
# APPLICATIONS INSTALLÉES
# ============================================================
INSTALLED_APPS = [
    # Applications Django par défaut
    'django.contrib.admin',          # Interface d'administration Django
    'django.contrib.auth',           # Système d'authentification
    'django.contrib.contenttypes',   # Types de contenu
    'django.contrib.sessions',       # Gestion des sessions
    'django.contrib.messages',       # Système de messages flash
    'django.contrib.staticfiles',    # Fichiers statiques (CSS, JS, images)
    'django.contrib.humanize',       # Filtres d'affichage (nombres, dates)

    # Notre application de pharmacie
    'pharmacy.apps.PharmacyConfig',
]

# ============================================================
# MIDDLEWARE (Couches de traitement des requêtes)
# ============================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',          # Sécurité HTTP
    'django.contrib.sessions.middleware.SessionMiddleware',   # Sessions
    'django.middleware.common.CommonMiddleware',              # Traitement commun
    'django.middleware.csrf.CsrfViewMiddleware',              # Protection CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Authentification
    'django.contrib.messages.middleware.MessageMiddleware',   # Messages flash
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Protection clickjacking
]

# ============================================================
# CONFIGURATION DES URLs
# ============================================================
ROOT_URLCONF = 'pharmacie_project.urls'

# ============================================================
# CONFIGURATION DES TEMPLATES (HTML)
# ============================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Répertoires supplémentaires de templates (vide car on utilise app_directories)
        'DIRS': [],
        # Recherche automatique des templates dans chaque application
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',    # Accès à 'request' dans les templates
                'django.contrib.auth.context_processors.auth',   # Accès à 'user' dans les templates
                'django.contrib.messages.context_processors.messages',  # Messages flash
            ],
        },
    },
]

# ============================================================
# WSGI - Point d'entrée du serveur web
# ============================================================
WSGI_APPLICATION = 'pharmacie_project.wsgi.application'

# ============================================================
# BASE DE DONNÉES — MySQL
# ============================================================
# Configuration de la connexion à MySQL
# Assurez-vous que la base de données et l'utilisateur existent :
#   CREATE DATABASE pharmagest_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
#   CREATE USER 'pharmagest_user'@'localhost' IDENTIFIED BY 'votre_mot_de_passe';
#   GRANT ALL PRIVILEGES ON pharmagest_db.* TO 'pharmagest_user'@'localhost';
#   FLUSH PRIVILEGES;
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pharmagest_db',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# ============================================================
# MODÈLE UTILISATEUR PERSONNALISÉ
# ============================================================
# On utilise notre propre modèle Utilisateur au lieu du modèle par défaut
AUTH_USER_MODEL = 'pharmacy.Utilisateur'

# ============================================================
# VALIDATION DES MOTS DE PASSE
# ============================================================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ============================================================
# LOCALISATION — Français
# ============================================================
LANGUAGE_CODE = 'fr-fr'          # Langue de l'interface
TIME_ZONE = 'Europe/Paris'       # Fuseau horaire
USE_I18N = True                   # Internationalisation activée
USE_TZ = True                     # Gestion des fuseaux horaires activée

# ============================================================
# FICHIERS STATIQUES (CSS, JavaScript, Images)
# ============================================================
STATIC_URL = '/static/'
# Répertoires supplémentaires contenant des fichiers statiques
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
# Répertoire de collecte des fichiers statiques en production
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ============================================================
# CONFIGURATION DE L'AUTHENTIFICATION
# ============================================================
# URL de redirection après connexion réussie
LOGIN_REDIRECT_URL = '/dashboard/'
# URL de la page de connexion
LOGIN_URL = '/connexion/'
# URL de redirection après déconnexion
LOGOUT_REDIRECT_URL = '/connexion/'

# ============================================================
# CLÉ PRIMAIRE PAR DÉFAUT
# ============================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
