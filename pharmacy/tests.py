"""
Tests unitaires et d'intégration — Application de Gestion de Pharmacie
========================================================================
Ce fichier contient l'ensemble des tests automatisés pour vérifier la conformité
de l'application aux exigences du cahier des charges.

Organisation des tests :
1. AUTHENTIFICATION          — Connexion, déconnexion, protection des pages
2. CONTRÔLE D'ACCÈS (RBAC)  — Permissions Admin vs Employé
3. CRUD MÉDICAMENTS          — Ajout, consultation, modification, suppression
4. GESTION DES VENTES        — Enregistrement, historique, remises (Admin only)
5. RESTRICTIONS              — Absence de module Client, données masquées
6. MODÈLES                   — Propriétés calculées, sauvegarde automatique

Exécution : python manage.py test pharmacy -v 2
"""

from decimal import Decimal
from datetime import timedelta

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from .models import Utilisateur, Medicament, Vente


# ============================================================
# HELPERS — Création rapide d'objets de test
# ============================================================

class TestDataMixin:
    """
    Mixin fournissant des méthodes utilitaires pour créer
    rapidement des données de test réutilisables.
    """

    def create_admin(self, username='admin', password='admin123'):
        """Crée et retourne un utilisateur Admin."""
        return Utilisateur.objects.create_user(
            username=username,
            password=password,
            role='admin',
            first_name='Ahmed',
            last_name='Benali',
            email='admin@pharmagest.ma',
        )

    def create_employe(self, username='employe', password='employe123'):
        """Crée et retourne un utilisateur Employé."""
        return Utilisateur.objects.create_user(
            username=username,
            password=password,
            role='employe',
            first_name='Sara',
            last_name='Moussaoui',
            email='employe@pharmagest.ma',
        )

    def create_medicament(self, **kwargs):
        """Crée et retourne un médicament avec des valeurs par défaut."""
        defaults = {
            'nom': 'Paracétamol 500mg',
            'description': 'Antalgique et antipyrétique.',
            'prix': Decimal('12.50'),
            'stock': 100,
            'date_expiration': timezone.now().date() + timedelta(days=365),
        }
        defaults.update(kwargs)
        return Medicament.objects.create(**defaults)

    def create_medicament_expire(self, **kwargs):
        """Crée et retourne un médicament expiré."""
        defaults = {
            'nom': 'Aspirine 500mg (expiré)',
            'prix': Decimal('8.00'),
            'stock': 25,
            'date_expiration': timezone.now().date() - timedelta(days=30),
        }
        defaults.update(kwargs)
        return Medicament.objects.create(**defaults)

    def create_medicament_stock_faible(self, **kwargs):
        """Crée et retourne un médicament avec un stock faible (< 10)."""
        defaults = {
            'nom': 'Ciprofloxacine 500mg',
            'prix': Decimal('45.00'),
            'stock': 5,
            'date_expiration': timezone.now().date() + timedelta(days=180),
        }
        defaults.update(kwargs)
        return Medicament.objects.create(**defaults)

    def create_vente(self, medicament=None, vendeur=None, **kwargs):
        """Crée et retourne une vente."""
        if medicament is None:
            medicament = self.create_medicament()
        if vendeur is None:
            vendeur = self.create_admin(username='vendeur_test')
        defaults = {
            'medicament': medicament,
            'vendeur': vendeur,
            'quantite': 5,
            'prix_unitaire': medicament.prix,
            'remise': Decimal('0'),
        }
        defaults.update(kwargs)
        return Vente.objects.create(**defaults)


# ============================================================
# 1. TESTS D'AUTHENTIFICATION
# ============================================================

class AuthenticationTests(TestDataMixin, TestCase):
    """
    Vérifie le système de connexion sécurisé.
    Exigence : Authentification avec identifiants valides,
    redirection après connexion/déconnexion.
    """

    def setUp(self):
        self.client = Client()
        self.admin = self.create_admin()
        self.employe = self.create_employe()

    # --- Tests de la page de connexion ---

    def test_login_page_accessible(self):
        """La page de connexion est accessible sans authentification."""
        response = self.client.get(reverse('pharmacy:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_connexion_url(self):
        """La page /connexion/ est accessible."""
        response = self.client.get(reverse('pharmacy:login_page'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_contains_form(self):
        """La page de connexion contient un formulaire avec champ username et password."""
        response = self.client.get(reverse('pharmacy:login'))
        self.assertContains(response, 'id_username')
        self.assertContains(response, 'id_password')
        self.assertContains(response, 'csrf')

    # --- Tests de connexion réussie ---

    def test_admin_login_success(self):
        """Un admin peut se connecter avec des identifiants valides."""
        response = self.client.post(reverse('pharmacy:login'), {
            'username': 'admin',
            'password': 'admin123',
        })
        self.assertRedirects(response, reverse('pharmacy:dashboard'))

    def test_employe_login_success(self):
        """Un employé peut se connecter avec des identifiants valides."""
        response = self.client.post(reverse('pharmacy:login'), {
            'username': 'employe',
            'password': 'employe123',
        })
        self.assertRedirects(response, reverse('pharmacy:dashboard'))

    def test_login_creates_session(self):
        """La connexion crée une session utilisateur active."""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('pharmacy:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    # --- Tests de connexion échouée ---

    def test_login_invalid_password(self):
        """Connexion refusée avec un mot de passe incorrect."""
        response = self.client.post(reverse('pharmacy:login'), {
            'username': 'admin',
            'password': 'wrong_password',
        })
        self.assertEqual(response.status_code, 200)  # Reste sur la page
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_invalid_username(self):
        """Connexion refusée avec un nom d'utilisateur inexistant."""
        response = self.client.post(reverse('pharmacy:login'), {
            'username': 'utilisateur_inexistant',
            'password': 'admin123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_empty_fields(self):
        """Connexion refusée avec des champs vides."""
        response = self.client.post(reverse('pharmacy:login'), {
            'username': '',
            'password': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    # --- Tests de déconnexion ---

    def test_logout_redirects_to_login(self):
        """La déconnexion redirige vers la page de connexion."""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('pharmacy:logout'))
        self.assertRedirects(response, reverse('pharmacy:login'))

    def test_logout_destroys_session(self):
        """Après déconnexion, l'utilisateur n'est plus authentifié."""
        self.client.login(username='admin', password='admin123')
        self.client.get(reverse('pharmacy:logout'))
        response = self.client.get(reverse('pharmacy:dashboard'))
        # Devrait rediriger vers login car non authentifié
        self.assertNotEqual(response.status_code, 200)

    # --- Tests de redirection ---

    def test_authenticated_user_redirected_from_login(self):
        """Un utilisateur déjà connecté est redirigé vers le dashboard."""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('pharmacy:login'))
        self.assertRedirects(response, reverse('pharmacy:dashboard'))

    def test_unauthenticated_user_redirected_to_login(self):
        """Un utilisateur non connecté est redirigé vers la page de connexion."""
        response = self.client.get(reverse('pharmacy:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/connexion/', response.url)


# ============================================================
# 2. TESTS DE CONTRÔLE D'ACCÈS (RBAC)
# ============================================================

class RoleBasedAccessTests(TestDataMixin, TestCase):
    """
    Vérifie que les permissions sont correctement appliquées
    selon le rôle de l'utilisateur (Admin vs Employé).
    Exigence : Séparation stricte des droits d'accès.
    """

    def setUp(self):
        self.client = Client()
        self.admin = self.create_admin()
        self.employe = self.create_employe()
        self.medicament = self.create_medicament()

    # --- Tests d'accès Admin ---

    def test_admin_can_access_dashboard(self):
        """L'admin peut accéder au tableau de bord."""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('pharmacy:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_admin_can_access_medicament_list(self):
        """L'admin peut accéder à la liste des médicaments."""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('pharmacy:medicament_list'))
        self.assertEqual(response.status_code, 200)

    def test_admin_can_access_vente_list(self):
        """L'admin peut accéder à l'historique des ventes."""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('pharmacy:vente_list'))
        self.assertEqual(response.status_code, 200)

    def test_admin_can_access_vente_create(self):
        """L'admin peut accéder au formulaire de vente."""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('pharmacy:vente_create'))
        self.assertEqual(response.status_code, 200)

    def test_admin_can_access_medicament_delete(self):
        """L'admin peut accéder à la page de suppression d'un médicament."""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(
            reverse('pharmacy:medicament_delete', args=[self.medicament.pk])
        )
        self.assertEqual(response.status_code, 200)

    # --- Tests d'accès Employé ---

    def test_employe_can_access_dashboard(self):
        """L'employé peut accéder au tableau de bord."""
        self.client.login(username='employe', password='employe123')
        response = self.client.get(reverse('pharmacy:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_employe_can_access_medicament_list(self):
        """L'employé peut accéder à la liste des médicaments."""
        self.client.login(username='employe', password='employe123')
        response = self.client.get(reverse('pharmacy:medicament_list'))
        self.assertEqual(response.status_code, 200)

    def test_employe_can_access_medicament_create(self):
        """L'employé peut accéder au formulaire d'ajout de médicament."""
        self.client.login(username='employe', password='employe123')
        response = self.client.get(reverse('pharmacy:medicament_create'))
        self.assertEqual(response.status_code, 200)

    def test_employe_can_access_medicament_detail(self):
        """L'employé peut voir le détail d'un médicament."""
        self.client.login(username='employe', password='employe123')
        response = self.client.get(
            reverse('pharmacy:medicament_detail', args=[self.medicament.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_employe_can_access_medicament_update(self):
        """L'employé peut accéder au formulaire de modification d'un médicament."""
        self.client.login(username='employe', password='employe123')
        response = self.client.get(
            reverse('pharmacy:medicament_update', args=[self.medicament.pk])
        )
        self.assertEqual(response.status_code, 200)

    # --- Tests de RESTRICTION Employé ---

    def test_employe_cannot_access_vente_list(self):
        """L'employé est redirigé s'il tente d'accéder aux ventes."""
        self.client.login(username='employe', password='employe123')
        response = self.client.get(reverse('pharmacy:vente_list'))
        self.assertRedirects(response, reverse('pharmacy:dashboard'))

    def test_employe_cannot_access_vente_create(self):
        """L'employé ne peut pas créer de vente."""
        self.client.login(username='employe', password='employe123')
        response = self.client.get(reverse('pharmacy:vente_create'))
        self.assertRedirects(response, reverse('pharmacy:dashboard'))

    def test_employe_cannot_access_vente_detail(self):
        """L'employé ne peut pas voir le détail d'une vente."""
        vente = self.create_vente(medicament=self.medicament, vendeur=self.admin)
        self.client.login(username='employe', password='employe123')
        response = self.client.get(
            reverse('pharmacy:vente_detail', args=[vente.pk])
        )
        self.assertRedirects(response, reverse('pharmacy:dashboard'))

    def test_employe_cannot_delete_medicament(self):
        """L'employé ne peut pas supprimer de médicament."""
        self.client.login(username='employe', password='employe123')
        response = self.client.get(
            reverse('pharmacy:medicament_delete', args=[self.medicament.pk])
        )
        self.assertRedirects(response, reverse('pharmacy:dashboard'))

    def test_employe_cannot_post_delete_medicament(self):
        """L'employé ne peut pas envoyer un POST de suppression."""
        self.client.login(username='employe', password='employe123')
        response = self.client.post(
            reverse('pharmacy:medicament_delete', args=[self.medicament.pk])
        )
        self.assertRedirects(response, reverse('pharmacy:dashboard'))
        # Le médicament doit toujours exister
        self.assertTrue(Medicament.objects.filter(pk=self.medicament.pk).exists())

    def test_employe_cannot_access_api_prix(self):
        """L'employé ne peut pas accéder à l'API de prix."""
        self.client.login(username='employe', password='employe123')
        response = self.client.get(
            reverse('pharmacy:api_medicament_prix', args=[self.medicament.pk])
        )
        self.assertRedirects(response, reverse('pharmacy:dashboard'))

    # --- Tests du contenu affiché selon le rôle ---

    def test_admin_dashboard_shows_sales_stats(self):
        """Le dashboard admin affiche les statistiques de ventes."""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('pharmacy:dashboard'))
        self.assertContains(response, "Ventes aujourd")
        self.assertContains(response, 'CA total')

    def test_employe_dashboard_hides_sales_stats(self):
        """Le dashboard employé ne montre PAS les statistiques de ventes."""
        self.client.login(username='employe', password='employe123')
        response = self.client.get(reverse('pharmacy:dashboard'))
        self.assertNotContains(response, 'CA total')
        self.assertNotContains(response, 'Total ventes')

    def test_admin_sees_ventes_in_sidebar(self):
        """L'admin voit le lien 'Ventes' dans le menu."""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('pharmacy:dashboard'))
        self.assertContains(response, 'Ventes')

    def test_admin_sees_delete_button(self):
        """L'admin voit le bouton 'Supprimer' sur le détail d'un médicament."""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(
            reverse('pharmacy:medicament_detail', args=[self.medicament.pk])
        )
        self.assertContains(response, 'Supprimer')

    def test_employe_does_not_see_delete_button(self):
        """L'employé ne voit PAS le bouton 'Supprimer'."""
        self.client.login(username='employe', password='employe123')
        response = self.client.get(
            reverse('pharmacy:medicament_detail', args=[self.medicament.pk])
        )
        self.assertNotContains(response, 'Supprimer')


# ============================================================
# 3. TESTS CRUD MÉDICAMENTS
# ============================================================

class MedicamentCRUDTests(TestDataMixin, TestCase):
    """
    Vérifie les opérations CRUD sur les médicaments.
    Exigence : Admin et Employé peuvent Ajouter/Voir/Modifier.
    Seul l'Admin peut Supprimer.
    """

    def setUp(self):
        self.client = Client()
        self.admin = self.create_admin()
        self.employe = self.create_employe()

    # --- CREATE ---

    def test_admin_create_medicament(self):
        """L'admin peut ajouter un nouveau médicament."""
        self.client.login(username='admin', password='admin123')
        response = self.client.post(reverse('pharmacy:medicament_create'), {
            'nom': 'Ibuprofène 400mg',
            'description': 'Anti-inflammatoire.',
            'prix': '15.00',
            'stock': '50',
            'date_expiration': (timezone.now().date() + timedelta(days=365)).isoformat(),
        })
        self.assertRedirects(response, reverse('pharmacy:medicament_list'))
        self.assertTrue(Medicament.objects.filter(nom='Ibuprofène 400mg').exists())

    def test_employe_create_medicament(self):
        """L'employé peut ajouter un nouveau médicament."""
        self.client.login(username='employe', password='employe123')
        response = self.client.post(reverse('pharmacy:medicament_create'), {
            'nom': 'Amoxicilline 500mg',
            'description': 'Antibiotique.',
            'prix': '35.00',
            'stock': '80',
            'date_expiration': (timezone.now().date() + timedelta(days=365)).isoformat(),
        })
        self.assertRedirects(response, reverse('pharmacy:medicament_list'))
        self.assertTrue(Medicament.objects.filter(nom='Amoxicilline 500mg').exists())

    def test_create_medicament_required_fields(self):
        """La création échoue si les champs obligatoires sont manquants."""
        self.client.login(username='admin', password='admin123')
        response = self.client.post(reverse('pharmacy:medicament_create'), {
            'nom': '',
            'prix': '',
            'stock': '',
            'date_expiration': '',
        })
        self.assertEqual(response.status_code, 200)  # Reste sur le formulaire
        self.assertEqual(Medicament.objects.count(), 0)

    def test_create_medicament_negative_price_rejected(self):
        """Un prix négatif est refusé par la validation du formulaire."""
        self.client.login(username='admin', password='admin123')
        response = self.client.post(reverse('pharmacy:medicament_create'), {
            'nom': 'Médicament invalide',
            'prix': '-10.00',
            'stock': '50',
            'date_expiration': (timezone.now().date() + timedelta(days=365)).isoformat(),
        })
        self.assertEqual(response.status_code, 200)  # Formulaire ré-affiché
        self.assertFalse(Medicament.objects.filter(nom='Médicament invalide').exists())

    # --- READ ---

    def test_medicament_list_displays_all(self):
        """La liste affiche tous les médicaments enregistrés."""
        self.create_medicament(nom='Médicament A')
        self.create_medicament(nom='Médicament B')
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('pharmacy:medicament_list'))
        self.assertContains(response, 'Médicament A')
        self.assertContains(response, 'Médicament B')

    def test_medicament_detail_shows_all_fields(self):
        """Le détail affiche tous les champs requis."""
        med = self.create_medicament()
        self.client.login(username='admin', password='admin123')
        response = self.client.get(
            reverse('pharmacy:medicament_detail', args=[med.pk])
        )
        self.assertContains(response, med.nom)
        self.assertContains(response, '12,50')  # prix formaté
        self.assertContains(response, 'Stock disponible')

    def test_medicament_search_filter(self):
        """La recherche filtre par nom de médicament."""
        self.create_medicament(nom='Paracétamol 500mg')
        self.create_medicament(nom='Ibuprofène 400mg')
        self.client.login(username='admin', password='admin123')
        response = self.client.get(
            reverse('pharmacy:medicament_list') + '?q=Paracétamol'
        )
        self.assertContains(response, 'Paracétamol')
        self.assertNotContains(response, 'Ibuprofène')

    def test_medicament_filter_expires(self):
        """Le filtre 'expires' affiche uniquement les médicaments expirés."""
        self.create_medicament(nom='Valide')
        self.create_medicament_expire(nom='Expiré Test')
        self.client.login(username='admin', password='admin123')
        response = self.client.get(
            reverse('pharmacy:medicament_list') + '?filtre=expires'
        )
        self.assertContains(response, 'Expiré Test')
        self.assertNotContains(response, 'Valide')

    def test_medicament_filter_stock_faible(self):
        """Le filtre 'stock_faible' affiche les médicaments en stock faible."""
        self.create_medicament(nom='Stock OK', stock=100)
        self.create_medicament_stock_faible(nom='Stock Faible Test')
        self.client.login(username='admin', password='admin123')
        response = self.client.get(
            reverse('pharmacy:medicament_list') + '?filtre=stock_faible'
        )
        self.assertContains(response, 'Stock Faible Test')
        self.assertNotContains(response, 'Stock OK')

    # --- UPDATE ---

    def test_admin_update_medicament(self):
        """L'admin peut modifier un médicament."""
        med = self.create_medicament()
        self.client.login(username='admin', password='admin123')
        response = self.client.post(
            reverse('pharmacy:medicament_update', args=[med.pk]),
            {
                'nom': 'Paracétamol 1000mg',
                'description': 'Antalgique dosage fort.',
                'prix': '18.00',
                'stock': '200',
                'date_expiration': med.date_expiration.isoformat(),
            }
        )
        self.assertRedirects(
            response,
            reverse('pharmacy:medicament_detail', args=[med.pk])
        )
        med.refresh_from_db()
        self.assertEqual(med.nom, 'Paracétamol 1000mg')
        self.assertEqual(med.prix, Decimal('18.00'))
        self.assertEqual(med.stock, 200)

    def test_employe_update_medicament(self):
        """L'employé peut modifier un médicament."""
        med = self.create_medicament()
        self.client.login(username='employe', password='employe123')
        response = self.client.post(
            reverse('pharmacy:medicament_update', args=[med.pk]),
            {
                'nom': med.nom,
                'description': med.description,
                'prix': str(med.prix),
                'stock': '150',
                'date_expiration': med.date_expiration.isoformat(),
            }
        )
        self.assertRedirects(
            response,
            reverse('pharmacy:medicament_detail', args=[med.pk])
        )
        med.refresh_from_db()
        self.assertEqual(med.stock, 150)

    # --- DELETE ---

    def test_admin_delete_medicament(self):
        """L'admin peut supprimer un médicament."""
        med = self.create_medicament()
        pk = med.pk
        self.client.login(username='admin', password='admin123')
        response = self.client.post(
            reverse('pharmacy:medicament_delete', args=[pk])
        )
        self.assertRedirects(response, reverse('pharmacy:medicament_list'))
        self.assertFalse(Medicament.objects.filter(pk=pk).exists())

    def test_employe_cannot_delete_medicament(self):
        """L'employé ne peut PAS supprimer un médicament (serveur refuse)."""
        med = self.create_medicament()
        self.client.login(username='employe', password='employe123')
        response = self.client.post(
            reverse('pharmacy:medicament_delete', args=[med.pk])
        )
        self.assertRedirects(response, reverse('pharmacy:dashboard'))
        # Le médicament doit toujours exister
        self.assertTrue(Medicament.objects.filter(pk=med.pk).exists())

    def test_delete_medicament_with_ventes_fails(self):
        """Un médicament lié à des ventes ne peut pas être supprimé (PROTECT)."""
        med = self.create_medicament()
        self.create_vente(medicament=med, vendeur=self.admin)
        self.client.login(username='admin', password='admin123')
        response = self.client.post(
            reverse('pharmacy:medicament_delete', args=[med.pk])
        )
        # Le médicament doit toujours exister car PROTECT empêche la suppression
        self.assertTrue(Medicament.objects.filter(pk=med.pk).exists())


# ============================================================
# 4. TESTS GESTION DES VENTES (Admin uniquement)
# ============================================================

class VenteManagementTests(TestDataMixin, TestCase):
    """
    Vérifie les fonctionnalités de gestion des ventes.
    Exigence : Module exclusivement accessible aux administrateurs.
    """

    def setUp(self):
        self.client = Client()
        self.admin = self.create_admin()
        self.employe = self.create_employe()
        self.medicament = self.create_medicament(stock=100)

    # --- Création de ventes ---

    def test_admin_create_vente(self):
        """L'admin peut enregistrer une vente."""
        self.client.login(username='admin', password='admin123')
        response = self.client.post(reverse('pharmacy:vente_create'), {
            'medicament': self.medicament.pk,
            'quantite': 10,
            'prix_unitaire': '12.50',
            'remise': '0',
        })
        self.assertRedirects(response, reverse('pharmacy:vente_list'))
        self.assertEqual(Vente.objects.count(), 1)

    def test_vente_decrements_stock(self):
        """L'enregistrement d'une vente décrémente le stock du médicament."""
        self.client.login(username='admin', password='admin123')
        initial_stock = self.medicament.stock
        self.client.post(reverse('pharmacy:vente_create'), {
            'medicament': self.medicament.pk,
            'quantite': 10,
            'prix_unitaire': '12.50',
            'remise': '0',
        })
        self.medicament.refresh_from_db()
        self.assertEqual(self.medicament.stock, initial_stock - 10)

    def test_vente_sets_vendeur_automatically(self):
        """Le vendeur est automatiquement défini comme l'utilisateur connecté."""
        self.client.login(username='admin', password='admin123')
        self.client.post(reverse('pharmacy:vente_create'), {
            'medicament': self.medicament.pk,
            'quantite': 5,
            'prix_unitaire': '12.50',
            'remise': '0',
        })
        vente = Vente.objects.first()
        self.assertEqual(vente.vendeur, self.admin)

    def test_vente_with_discount(self):
        """Une vente avec remise calcule correctement le montant total."""
        self.client.login(username='admin', password='admin123')
        self.client.post(reverse('pharmacy:vente_create'), {
            'medicament': self.medicament.pk,
            'quantite': 10,
            'prix_unitaire': '10.00',
            'remise': '20',
        })
        vente = Vente.objects.first()
        # 10 × 10.00 = 100.00, remise 20% → 80.00
        self.assertEqual(vente.montant_total, Decimal('80.00'))

    def test_vente_quantity_exceeds_stock_rejected(self):
        """Une vente avec une quantité supérieure au stock est refusée."""
        self.client.login(username='admin', password='admin123')
        response = self.client.post(reverse('pharmacy:vente_create'), {
            'medicament': self.medicament.pk,
            'quantite': 999,
            'prix_unitaire': '12.50',
            'remise': '0',
        })
        self.assertEqual(response.status_code, 200)  # Formulaire ré-affiché
        self.assertEqual(Vente.objects.count(), 0)

    # --- Historique des ventes ---

    def test_vente_list_displays_all(self):
        """L'historique affiche toutes les ventes."""
        self.create_vente(medicament=self.medicament, vendeur=self.admin)
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('pharmacy:vente_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.medicament.nom)

    def test_vente_detail_shows_info(self):
        """Le détail d'une vente affiche les bonnes informations."""
        vente = self.create_vente(medicament=self.medicament, vendeur=self.admin)
        self.client.login(username='admin', password='admin123')
        response = self.client.get(
            reverse('pharmacy:vente_detail', args=[vente.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.medicament.nom)
        self.assertContains(response, 'Montant total')

    def test_vente_search_by_medicament_name(self):
        """La recherche de ventes filtre par nom de médicament."""
        med_a = self.create_medicament(nom='Doliprane')
        med_b = self.create_medicament(nom='Vitamines')
        self.create_vente(medicament=med_a, vendeur=self.admin)
        self.create_vente(
            medicament=med_b,
            vendeur=self.create_admin(username='admin2')
        )
        self.client.login(username='admin', password='admin123')
        response = self.client.get(
            reverse('pharmacy:vente_list') + '?q=Doliprane'
        )
        self.assertContains(response, 'Doliprane')
        self.assertNotContains(response, 'Vitamines')

    # --- Employé bloqué ---

    def test_employe_cannot_create_vente(self):
        """L'employé ne peut PAS enregistrer une vente (POST)."""
        self.client.login(username='employe', password='employe123')
        response = self.client.post(reverse('pharmacy:vente_create'), {
            'medicament': self.medicament.pk,
            'quantite': 5,
            'prix_unitaire': '12.50',
            'remise': '0',
        })
        self.assertRedirects(response, reverse('pharmacy:dashboard'))
        self.assertEqual(Vente.objects.count(), 0)

    def test_employe_cannot_view_vente_list(self):
        """L'employé ne peut PAS accéder à l'historique des ventes."""
        self.client.login(username='employe', password='employe123')
        response = self.client.get(reverse('pharmacy:vente_list'))
        self.assertRedirects(response, reverse('pharmacy:dashboard'))


# ============================================================
# 5. TESTS DES RESTRICTIONS
# ============================================================

class RestrictionTests(TestDataMixin, TestCase):
    """
    Vérifie les restrictions spécifiées dans le cahier des charges :
    - Pas de module Client
    - Employé ne voit pas les données de ventes
    - Seul l'Admin gère les remises
    """

    def setUp(self):
        self.client = Client()
        self.admin = self.create_admin()
        self.employe = self.create_employe()

    def test_no_client_model(self):
        """Aucun modèle 'Client' n'existe dans l'application."""
        from pharmacy import models
        model_names = [
            cls.__name__.lower()
            for cls in models.__dict__.values()
            if isinstance(cls, type) and issubclass(cls, models.models.Model)
        ]
        self.assertNotIn('client', model_names)

    def test_no_client_url(self):
        """Aucune URL contenant 'client' n'est définie."""
        from pharmacy.urls import urlpatterns
        for pattern in urlpatterns:
            self.assertNotIn('client', str(pattern.pattern))

    def test_employe_dashboard_no_sales_data(self):
        """Le dashboard de l'employé ne contient aucune donnée de vente."""
        # Créer quelques ventes
        med = self.create_medicament()
        self.create_vente(medicament=med, vendeur=self.admin)

        self.client.login(username='employe', password='employe123')
        response = self.client.get(reverse('pharmacy:dashboard'))
        content = response.content.decode()

        # Ne doit pas contenir les éléments liés aux ventes
        self.assertNotIn('CA total', content)
        self.assertNotIn('chiffre_affaires', content)

    def test_employe_medicament_detail_no_ventes(self):
        """Le détail d'un médicament vu par un employé ne montre pas l'historique de ventes."""
        med = self.create_medicament()
        self.create_vente(medicament=med, vendeur=self.admin)

        self.client.login(username='employe', password='employe123')
        response = self.client.get(
            reverse('pharmacy:medicament_detail', args=[med.pk])
        )
        # Ne doit pas afficher la section "Dernières ventes"
        self.assertNotContains(response, 'Dernières ventes')


# ============================================================
# 6. TESTS DES MODÈLES
# ============================================================

class UtilisateurModelTests(TestDataMixin, TestCase):
    """Vérifie le modèle Utilisateur et ses méthodes."""

    def test_admin_role(self):
        """Un utilisateur avec role='admin' est identifié comme admin."""
        admin = self.create_admin()
        self.assertTrue(admin.is_admin())
        self.assertFalse(admin.is_employe())

    def test_employe_role(self):
        """Un utilisateur avec role='employe' est identifié comme employé."""
        employe = self.create_employe()
        self.assertTrue(employe.is_employe())
        self.assertFalse(employe.is_admin())

    def test_default_role_is_employe(self):
        """Le rôle par défaut d'un nouvel utilisateur est 'employe'."""
        user = Utilisateur.objects.create_user(
            username='nouveau', password='test123'
        )
        self.assertEqual(user.role, 'employe')

    def test_str_representation(self):
        """La représentation textuelle contient le nom d'utilisateur et le rôle."""
        admin = self.create_admin()
        self.assertIn('admin', str(admin))
        self.assertIn('Administrateur', str(admin))


class MedicamentModelTests(TestDataMixin, TestCase):
    """Vérifie le modèle Medicament et ses propriétés calculées."""

    def test_est_expire_true(self):
        """Un médicament avec une date passée est marqué comme expiré."""
        med = self.create_medicament_expire()
        self.assertTrue(med.est_expire)

    def test_est_expire_false(self):
        """Un médicament avec une date future n'est pas expiré."""
        med = self.create_medicament()
        self.assertFalse(med.est_expire)

    def test_expire_bientot(self):
        """Un médicament expirant dans 15 jours est marqué 'expire bientôt'."""
        med = self.create_medicament(
            date_expiration=timezone.now().date() + timedelta(days=15)
        )
        self.assertTrue(med.expire_bientot)

    def test_expire_bientot_false(self):
        """Un médicament expirant dans 60 jours n'est PAS 'expire bientôt'."""
        med = self.create_medicament(
            date_expiration=timezone.now().date() + timedelta(days=60)
        )
        self.assertFalse(med.expire_bientot)

    def test_stock_faible_true(self):
        """Un stock de 5 est considéré comme faible."""
        med = self.create_medicament(stock=5)
        self.assertTrue(med.stock_faible)

    def test_stock_faible_false(self):
        """Un stock de 100 n'est PAS considéré comme faible."""
        med = self.create_medicament(stock=100)
        self.assertFalse(med.stock_faible)

    def test_stock_faible_boundary(self):
        """Un stock de 10 n'est PAS faible (seuil strict < 10)."""
        med = self.create_medicament(stock=10)
        self.assertFalse(med.stock_faible)

    def test_str_representation(self):
        """La représentation textuelle est le nom du médicament."""
        med = self.create_medicament(nom='Doliprane 1000mg')
        self.assertEqual(str(med), 'Doliprane 1000mg')


class VenteModelTests(TestDataMixin, TestCase):
    """Vérifie le modèle Vente et le calcul automatique du montant."""

    def test_montant_total_auto_calculated(self):
        """Le montant total est calculé automatiquement lors de la sauvegarde."""
        med = self.create_medicament(prix=Decimal('10.00'))
        admin = self.create_admin()
        vente = Vente(
            medicament=med,
            vendeur=admin,
            quantite=5,
            prix_unitaire=Decimal('10.00'),
            remise=Decimal('0'),
        )
        vente.save()
        self.assertEqual(vente.montant_total, Decimal('50.00'))

    def test_montant_total_with_discount(self):
        """Le montant total avec remise est correctement calculé."""
        med = self.create_medicament(prix=Decimal('20.00'))
        admin = self.create_admin()
        vente = Vente(
            medicament=med,
            vendeur=admin,
            quantite=10,
            prix_unitaire=Decimal('20.00'),
            remise=Decimal('10'),
        )
        vente.save()
        # 20 × 10 = 200, remise 10% → 180
        self.assertEqual(vente.montant_total, Decimal('180.00'))

    def test_montant_total_full_discount(self):
        """Une remise de 100% donne un montant total de 0."""
        med = self.create_medicament()
        admin = self.create_admin()
        vente = Vente(
            medicament=med,
            vendeur=admin,
            quantite=5,
            prix_unitaire=Decimal('10.00'),
            remise=Decimal('100'),
        )
        vente.save()
        self.assertEqual(vente.montant_total, Decimal('0.00'))

    def test_str_representation(self):
        """La représentation textuelle contient le nom du médicament et la quantité."""
        med = self.create_medicament(nom='Ibuprofène')
        admin = self.create_admin()
        vente = self.create_vente(medicament=med, vendeur=admin)
        self.assertIn('Ibuprofène', str(vente))
        self.assertIn('x5', str(vente))

    def test_vente_ordering(self):
        """Les ventes sont triées par date décroissante (plus récente d'abord)."""
        med = self.create_medicament()
        admin = self.create_admin()
        vente1 = self.create_vente(medicament=med, vendeur=admin)
        vente2 = self.create_vente(medicament=med, vendeur=admin)
        ventes = list(Vente.objects.all())
        self.assertEqual(ventes[0], vente2)  # Plus récente en premier


# ============================================================
# 7. TESTS DES FORMULAIRES
# ============================================================

class FormValidationTests(TestDataMixin, TestCase):
    """Vérifie la validation des formulaires."""

    def test_vente_form_filters_out_of_stock(self):
        """Le formulaire de vente n'affiche pas les médicaments sans stock."""
        from .forms import VenteForm
        med_with_stock = self.create_medicament(nom='Avec stock', stock=50)
        med_no_stock = self.create_medicament(nom='Sans stock', stock=0)

        form = VenteForm()
        queryset = form.fields['medicament'].queryset
        self.assertIn(med_with_stock, queryset)
        self.assertNotIn(med_no_stock, queryset)

    def test_medicament_form_all_required_fields(self):
        """Le formulaire de médicament inclut tous les champs obligatoires."""
        from .forms import MedicamentForm
        form = MedicamentForm()
        self.assertIn('nom', form.fields)
        self.assertIn('prix', form.fields)
        self.assertIn('stock', form.fields)
        self.assertIn('date_expiration', form.fields)


# ============================================================
# 8. TESTS DE SÉCURITÉ
# ============================================================

class SecurityTests(TestDataMixin, TestCase):
    """Vérifie la sécurité générale de l'application."""

    def setUp(self):
        self.client = Client()

    def test_all_views_require_auth_dashboard(self):
        """Le dashboard requiert une authentification."""
        response = self.client.get(reverse('pharmacy:dashboard'))
        self.assertNotEqual(response.status_code, 200)

    def test_all_views_require_auth_medicaments(self):
        """La liste des médicaments requiert une authentification."""
        response = self.client.get(reverse('pharmacy:medicament_list'))
        self.assertNotEqual(response.status_code, 200)

    def test_all_views_require_auth_ventes(self):
        """La liste des ventes requiert une authentification."""
        response = self.client.get(reverse('pharmacy:vente_list'))
        self.assertNotEqual(response.status_code, 200)

    def test_csrf_protection_on_login(self):
        """Le formulaire de connexion contient un token CSRF."""
        response = self.client.get(reverse('pharmacy:login'))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_csrf_protection_on_medicament_form(self):
        """Le formulaire de médicament contient un token CSRF."""
        admin = self.create_admin()
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('pharmacy:medicament_create'))
        self.assertContains(response, 'csrfmiddlewaretoken')
