"""
Configuration des URLs de l'application pharmacy.
===================================================
Ce fichier définit toutes les routes (URLs) de l'application.
Chaque URL est associée à une vue et possède un nom unique
pour faciliter les références dans les templates ({% url 'pharmacy:nom' %}).
"""

from django.urls import path
from . import views

# Namespace de l'application pour éviter les conflits de noms
app_name = 'pharmacy'

urlpatterns = [
    # ===========================================================
    # AUTHENTIFICATION
    # ===========================================================
    # Page de connexion (page d'accueil par défaut)
    path('', views.login_view, name='login'),
    path('connexion/', views.login_view, name='login_page'),
    # Déconnexion
    path('deconnexion/', views.logout_view, name='logout'),

    # ===========================================================
    # TABLEAU DE BORD
    # ===========================================================
    path('dashboard/', views.dashboard, name='dashboard'),

    # ===========================================================
    # CRUD MÉDICAMENTS
    # ===========================================================
    # Liste de tous les médicaments
    path('medicaments/', views.medicament_list, name='medicament_list'),
    # Ajouter un nouveau médicament
    path('medicaments/ajouter/', views.medicament_create, name='medicament_create'),
    # Détail d'un médicament spécifique
    path('medicaments/<int:pk>/', views.medicament_detail, name='medicament_detail'),
    # Modifier un médicament existant
    path('medicaments/<int:pk>/modifier/', views.medicament_update, name='medicament_update'),
    # Supprimer un médicament (Admin uniquement)
    path('medicaments/<int:pk>/supprimer/', views.medicament_delete, name='medicament_delete'),

    # ===========================================================
    # CRUD VENTES (Admin uniquement)
    # ===========================================================
    # Historique des ventes
    path('ventes/', views.vente_list, name='vente_list'),
    # Enregistrer une nouvelle vente
    path('ventes/ajouter/', views.vente_create, name='vente_create'),
    # Détail d'une vente
    path('ventes/<int:pk>/', views.vente_detail, name='vente_detail'),

    # ===========================================================
    # API INTERNE
    # ===========================================================
    # Récupérer le prix d'un médicament (utilisé par JavaScript)
    path('api/medicament/<int:pk>/prix/', views.api_medicament_prix, name='api_medicament_prix'),
]
