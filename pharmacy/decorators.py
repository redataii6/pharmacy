"""
Décorateurs personnalisés pour le contrôle d'accès.
====================================================
Ce fichier contient les décorateurs utilisés pour restreindre
l'accès aux vues en fonction du rôle de l'utilisateur.
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def admin_required(view_func):
    """
    Décorateur qui restreint l'accès à une vue aux administrateurs uniquement.
    
    Combine deux vérifications :
    1. L'utilisateur doit être connecté (sinon redirection vers la page de connexion)
    2. L'utilisateur doit avoir le rôle 'admin' (sinon redirection vers le dashboard)
    
    Usage:
        @admin_required
        def ma_vue_admin(request):
            ...
    
    Args:
        view_func: La fonction de vue à protéger.
    
    Returns:
        function: La vue protégée par le décorateur.
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        # Vérifier si l'utilisateur a le rôle admin
        if not request.user.is_admin():
            # Afficher un message d'erreur et rediriger vers le dashboard
            messages.error(
                request,
                "⛔ Accès refusé. Cette fonctionnalité est réservée aux administrateurs."
            )
            return redirect('pharmacy:dashboard')
        # Si l'utilisateur est admin, exécuter la vue normalement
        return view_func(request, *args, **kwargs)
    return wrapper
