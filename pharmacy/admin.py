"""
Configuration de l'interface d'administration Django.
======================================================
Enregistre les modèles Utilisateur, Medicament et Vente dans l'admin Django
afin de pouvoir les gérer via l'interface /admin/.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur, Medicament, Vente


# ============================================================
# ADMINISTRATION DU MODÈLE UTILISATEUR
# ============================================================
@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    """
    Configuration de l'affichage du modèle Utilisateur dans l'admin Django.
    Étend UserAdmin pour ajouter le champ 'role' dans les formulaires.
    """
    # Colonnes affichées dans la liste
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active')
    # Filtres latéraux
    list_filter = ('role', 'is_active', 'is_staff')
    # Champs de recherche
    search_fields = ('username', 'email', 'first_name', 'last_name')

    # Ajout du champ 'role' dans le formulaire d'édition
    fieldsets = UserAdmin.fieldsets + (
        ('Rôle dans la pharmacie', {'fields': ('role',)}),
    )
    # Ajout du champ 'role' dans le formulaire de création
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Rôle dans la pharmacie', {'fields': ('role',)}),
    )


# ============================================================
# ADMINISTRATION DU MODÈLE MÉDICAMENT
# ============================================================
@admin.register(Medicament)
class MedicamentAdmin(admin.ModelAdmin):
    """
    Configuration de l'affichage du modèle Medicament dans l'admin Django.
    """
    # Colonnes affichées dans la liste
    list_display = ('nom', 'prix', 'stock', 'date_expiration', 'date_ajout')
    # Filtres latéraux
    list_filter = ('date_expiration',)
    # Champs de recherche
    search_fields = ('nom', 'description')
    # Tri par défaut
    ordering = ('nom',)


# ============================================================
# ADMINISTRATION DU MODÈLE VENTE
# ============================================================
@admin.register(Vente)
class VenteAdmin(admin.ModelAdmin):
    """
    Configuration de l'affichage du modèle Vente dans l'admin Django.
    """
    # Colonnes affichées dans la liste
    list_display = ('medicament', 'quantite', 'prix_unitaire', 'remise',
                    'montant_total', 'vendeur', 'date_vente')
    # Filtres latéraux
    list_filter = ('date_vente', 'vendeur')
    # Champs de recherche
    search_fields = ('medicament__nom', 'vendeur__username')
    # Tri par défaut (plus récent en premier)
    ordering = ('-date_vente',)
    # Champs en lecture seule (calculés automatiquement)
    readonly_fields = ('montant_total',)
