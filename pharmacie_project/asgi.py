"""
Configuration ASGI pour le projet pharmacie.
Point d'entrée pour les serveurs web asynchrones compatibles ASGI.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacie_project.settings')
application = get_asgi_application()
