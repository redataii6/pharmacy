"""
Modèles de données pour l'application de gestion de pharmacie.
===============================================================
Ce fichier définit les trois modèles principaux :
1. Utilisateur — Modèle d'authentification personnalisé avec gestion des rôles
2. Medicament — Représente un médicament en stock
3. Vente — Représente une vente de médicament (accessible uniquement par l'Admin)

CONTRAINTE : Pas de modèle Client dans cette version.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


# ============================================================
# MODÈLE UTILISATEUR PERSONNALISÉ
# ============================================================
class Utilisateur(AbstractUser):
    """
    Modèle utilisateur personnalisé étendant AbstractUser.
    
    Ajoute un champ 'role' pour distinguer les administrateurs des employés.
    Les droits d'accès sont déterminés par ce rôle :
    - Admin : accès complet (CRUD médicaments + ventes + suppression)
    - Employé : accès limité (consultation, ajout, modification de médicaments uniquement)
    """

    # Choix possibles pour le rôle de l'utilisateur
    ROLE_CHOICES = (
        ('admin', 'Administrateur'),
        ('employe', 'Employé'),
    )

    # Champ rôle — détermine les permissions de l'utilisateur
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='employe',
        verbose_name='Rôle',
        help_text="Détermine le niveau d'accès de l'utilisateur."
    )

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        ordering = ['username']  # Tri alphabétique par nom d'utilisateur

    def __str__(self):
        """Représentation textuelle : nom d'utilisateur (rôle)."""
        return f"{self.username} ({self.get_role_display()})"

    def is_admin(self):
        """
        Vérifie si l'utilisateur a le rôle Administrateur.
        
        Returns:
            bool: True si l'utilisateur est administrateur, False sinon.
        """
        return self.role == 'admin'

    def is_employe(self):
        """
        Vérifie si l'utilisateur a le rôle Employé.
        
        Returns:
            bool: True si l'utilisateur est employé, False sinon.
        """
        return self.role == 'employe'


# ============================================================
# MODÈLE MÉDICAMENT
# ============================================================
class Medicament(models.Model):
    """
    Représente un médicament dans le stock de la pharmacie.
    
    Contient les informations essentielles : nom, description, prix,
    quantité en stock et date d'expiration. Fournit des propriétés
    calculées pour détecter les médicaments expirés ou en stock faible.
    """

    # Nom commercial du médicament
    nom = models.CharField(
        max_length=200,
        verbose_name='Nom du médicament',
        help_text="Nom commercial du médicament."
    )

    # Description détaillée (optionnelle)
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Description',
        help_text="Description détaillée du médicament (composition, usage, etc.)."
    )

    # Prix unitaire en dirhams (ou autre devise)
    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Prix unitaire (DH)',
        help_text="Prix de vente unitaire du médicament."
    )

    # Quantité disponible en stock
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name='Quantité en stock',
        help_text="Nombre d'unités disponibles en stock."
    )

    # Date d'expiration du médicament
    date_expiration = models.DateField(
        verbose_name="Date d'expiration",
        help_text="Date limite d'utilisation du médicament."
    )

    # Date d'ajout automatique au système
    date_ajout = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'ajout",
        help_text="Date et heure d'enregistrement dans le système."
    )

    class Meta:
        verbose_name = 'Médicament'
        verbose_name_plural = 'Médicaments'
        ordering = ['nom']  # Tri alphabétique par nom

    def __str__(self):
        """Représentation textuelle : nom du médicament."""
        return self.nom

    @property
    def est_expire(self):
        """
        Vérifie si le médicament est expiré.
        
        Compare la date d'expiration avec la date actuelle.
        
        Returns:
            bool: True si la date d'expiration est dépassée, False sinon.
        """
        return self.date_expiration < timezone.now().date()

    @property
    def expire_bientot(self):
        """
        Vérifie si le médicament expire dans les 30 prochains jours.
        
        Returns:
            bool: True si le médicament expire dans moins de 30 jours
                  (mais n'est pas encore expiré), False sinon.
        """
        aujourd_hui = timezone.now().date()
        delta = self.date_expiration - aujourd_hui
        return 0 <= delta.days <= 30

    @property
    def stock_faible(self):
        """
        Vérifie si le stock est faible (moins de 10 unités).
        
        Returns:
            bool: True si le stock est inférieur à 10, False sinon.
        """
        return self.stock < 10


# ============================================================
# MODÈLE VENTE (Accessible uniquement par l'Admin)
# ============================================================
class Vente(models.Model):
    """
    Représente une vente de médicament effectuée par un administrateur.
    
    Ce modèle est strictement réservé aux utilisateurs avec le rôle Admin.
    Les employés n'ont aucun accès à ce module (ni en lecture, ni en écriture).
    
    Le montant total est calculé automatiquement en tenant compte de la remise :
    montant_total = (prix_unitaire × quantité) × (1 - remise/100)
    """

    # Lien vers le médicament vendu
    medicament = models.ForeignKey(
        Medicament,
        on_delete=models.PROTECT,  # Empêche la suppression d'un médicament qui a des ventes
        related_name='ventes',
        verbose_name='Médicament',
        help_text="Médicament concerné par cette vente."
    )

    # Quantité vendue
    quantite = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Quantité vendue',
        help_text="Nombre d'unités vendues."
    )

    # Prix unitaire au moment de la vente (peut différer du prix actuel)
    prix_unitaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Prix unitaire (DH)',
        help_text="Prix unitaire au moment de la vente."
    )

    # Pourcentage de remise appliquée (entre 0 et 100)
    remise = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Remise (%)',
        help_text="Pourcentage de remise appliquée (0 à 100)."
    )

    # Montant total après remise (calculé automatiquement)
    montant_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Montant total (DH)',
        help_text="Montant total de la vente après application de la remise.",
        editable=False  # Calculé automatiquement, non modifiable manuellement
    )

    # Date et heure de la vente (enregistrée automatiquement)
    date_vente = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de vente',
        help_text="Date et heure de la transaction."
    )

    # Lien vers l'utilisateur ayant effectué la vente
    vendeur = models.ForeignKey(
        Utilisateur,
        on_delete=models.PROTECT,  # Empêche la suppression d'un utilisateur ayant des ventes
        related_name='ventes',
        verbose_name='Vendeur',
        help_text="Administrateur ayant enregistré la vente."
    )

    class Meta:
        verbose_name = 'Vente'
        verbose_name_plural = 'Ventes'
        ordering = ['-date_vente']  # Tri par date de vente décroissante (plus récente en premier)

    def __str__(self):
        """Représentation textuelle : nom du médicament - quantité - date."""
        return f"Vente de {self.medicament.nom} (x{self.quantite}) — {self.date_vente.strftime('%d/%m/%Y')}"

    def save(self, *args, **kwargs):
        """
        Surcharge de la méthode save pour calculer automatiquement le montant total.
        
        Formule : montant_total = (prix_unitaire × quantité) × (1 - remise / 100)
        
        La méthode appelle ensuite la méthode save() parente pour sauvegarder
        l'objet en base de données.
        """
        # Calcul du sous-total avant remise
        sous_total = self.prix_unitaire * self.quantite
        # Application de la remise
        self.montant_total = sous_total * (1 - self.remise / 100)
        # Appel de la méthode save() du parent
        super().save(*args, **kwargs)
