"""
Formulaires Django pour l'application de gestion de pharmacie.
===============================================================
Ce fichier définit les formulaires utilisés pour :
1. La connexion des utilisateurs (LoginForm)
2. La gestion des médicaments (MedicamentForm)
3. L'enregistrement des ventes (VenteForm)

Tous les formulaires utilisent des widgets Bootstrap 5 pour un rendu moderne.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Medicament, Vente


class LoginForm(AuthenticationForm):
    """
    Formulaire de connexion personnalisé.
    
    Étend AuthenticationForm de Django pour ajouter des classes CSS Bootstrap 5
    aux champs de saisie, améliorant ainsi le rendu visuel.
    """

    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Entrez votre nom d'utilisateur",
            'autofocus': True,
            'id': 'id_username',
        })
    )

    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre mot de passe',
            'id': 'id_password',
        })
    )


class MedicamentForm(forms.ModelForm):
    """
    Formulaire pour l'ajout et la modification d'un médicament.
    
    Basé sur le modèle Medicament, ce formulaire expose les champs :
    nom, description, prix, stock et date d'expiration.
    Chaque champ est stylisé avec des widgets Bootstrap 5.
    """

    class Meta:
        model = Medicament
        # Champs exposés dans le formulaire
        fields = ['nom', 'description', 'prix', 'stock', 'date_expiration']
        # Widgets personnalisés avec classes Bootstrap
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Paracétamol 500mg',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description du médicament (composition, usage, etc.)',
            }),
            'prix': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0',
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'min': '0',
            }),
            'date_expiration': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',  # Affiche un sélecteur de date natif
            }),
        }

    def clean_prix(self):
        """
        Validation personnalisée du prix.
        Vérifie que le prix est strictement positif.
        """
        prix = self.cleaned_data.get('prix')
        if prix is not None and prix < 0:
            raise forms.ValidationError("Le prix ne peut pas être négatif.")
        return prix


class VenteForm(forms.ModelForm):
    """
    Formulaire pour l'enregistrement d'une vente.
    
    Accessible uniquement par les administrateurs.
    Permet de sélectionner un médicament, une quantité et une remise.
    Le prix unitaire est pré-rempli automatiquement via JavaScript.
    
    Note: Le montant total est calculé automatiquement dans le modèle (save()).
    """

    class Meta:
        model = Vente
        # Champs exposés (le vendeur et le montant sont gérés automatiquement)
        fields = ['medicament', 'quantite', 'prix_unitaire', 'remise']
        widgets = {
            'medicament': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_medicament',
            }),
            'quantite': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '1',
                'min': '1',
                'id': 'id_quantite',
            }),
            'prix_unitaire': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'id': 'id_prix_unitaire',
            }),
            'remise': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'id': 'id_remise',
            }),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialisation du formulaire de vente.
        Filtre les médicaments pour n'afficher que ceux qui ont du stock disponible.
        """
        super().__init__(*args, **kwargs)
        # N'afficher que les médicaments ayant du stock (stock > 0)
        self.fields['medicament'].queryset = Medicament.objects.filter(stock__gt=0)

    def clean_quantite(self):
        """
        Validation personnalisée de la quantité.
        Vérifie que la quantité demandée ne dépasse pas le stock disponible.
        """
        quantite = self.cleaned_data.get('quantite')
        medicament = self.cleaned_data.get('medicament')

        if medicament and quantite:
            if quantite > medicament.stock:
                raise forms.ValidationError(
                    f"Stock insuffisant. Seulement {medicament.stock} unité(s) disponible(s)."
                )
        return quantite
