"""
Tags de template personnalisés pour l'application de pharmacie.
================================================================
Fournit des filtres et tags utilisables dans les templates HTML
pour simplifier la logique d'affichage.
"""

from django import template

register = template.Library()


@register.filter(name='is_admin')
def is_admin(user):
    """
    Filtre de template pour vérifier si un utilisateur est administrateur.
    
    Usage dans un template :
        {% load pharmacy_tags %}
        {% if user|is_admin %}
            ... contenu réservé à l'admin ...
        {% endif %}
    
    Args:
        user: L'objet utilisateur à vérifier.
    
    Returns:
        bool: True si l'utilisateur a le rôle 'admin', False sinon.
    """
    if hasattr(user, 'is_admin'):
        return user.is_admin()
    return False


@register.filter(name='is_employe')
def is_employe(user):
    """
    Filtre de template pour vérifier si un utilisateur est employé.
    
    Usage dans un template :
        {% load pharmacy_tags %}
        {% if user|is_employe %}
            ... contenu réservé à l'employé ...
        {% endif %}
    
    Args:
        user: L'objet utilisateur à vérifier.
    
    Returns:
        bool: True si l'utilisateur a le rôle 'employe', False sinon.
    """
    if hasattr(user, 'is_employe'):
        return user.is_employe()
    return False
