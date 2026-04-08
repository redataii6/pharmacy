#!/usr/bin/env python
"""
Script de gestion Django pour l'application de gestion de pharmacie.
Permet d'exécuter les commandes administratives (migrations, runserver, etc.).
"""
import os
import sys


def main():
    """Point d'entrée principal pour les commandes de gestion Django."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacie_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Impossible d'importer Django. Vérifiez que Django est installé "
            "et disponible dans votre variable d'environnement PYTHONPATH. "
            "Avez-vous oublié d'activer votre environnement virtuel ?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
