"""
Configuration WSGI pour le projet pharmacie.
Point d'entrée pour les serveurs web compatibles WSGI (ex: Gunicorn).
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacie_project.settings')
application = get_wsgi_application()
