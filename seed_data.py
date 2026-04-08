#!/usr/bin/env python
"""
Script de données de test — Application PharmaGest
====================================================
Ce script crée des données de démonstration dans la base de données :
- 2 utilisateurs (1 Admin + 1 Employé)
- 15 médicaments variés (certains expirés, certains en stock faible)
- 8 ventes de démonstration

Usage :
    python manage.py shell < seed_data.py
    ou
    python seed_data.py  (si DJANGO_SETTINGS_MODULE est configuré)

ATTENTION : Ce script supprime les données existantes avant de les recréer.
"""

import os
import sys
import django
from datetime import date, timedelta
from decimal import Decimal

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacie_project.settings')

# Ajouter le répertoire du projet au path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Initialiser Django
django.setup()

# Importer les modèles après l'initialisation de Django
from pharmacy.models import Utilisateur, Medicament, Vente


def seed_utilisateurs():
    """
    Crée les utilisateurs de démonstration.
    
    Utilisateurs créés :
    - admin / admin123   → Rôle Administrateur
    - employe / employe123 → Rôle Employé
    """
    print("=" * 60)
    print("📌 Création des utilisateurs...")
    print("=" * 60)

    # Supprimer les utilisateurs existants (sauf superuser Django)
    Utilisateur.objects.filter(is_superuser=False).delete()

    # Créer l'administrateur
    admin = Utilisateur.objects.create_user(
        username='admin',
        password='admin123',
        email='admin@pharmagest.ma',
        first_name='Ahmed',
        last_name='Benali',
        role='admin',
        is_staff=True,  # Accès à l'interface admin Django
    )
    print(f"  ✅ Admin créé : {admin.username} (mot de passe : admin123)")

    # Créer l'employé
    employe = Utilisateur.objects.create_user(
        username='employe',
        password='employe123',
        email='employe@pharmagest.ma',
        first_name='Fatima',
        last_name='Zahra',
        role='employe',
        is_staff=False,
    )
    print(f"  ✅ Employé créé : {employe.username} (mot de passe : employe123)")

    return admin, employe


def seed_medicaments():
    """
    Crée 15 médicaments de démonstration avec des statuts variés :
    - Médicaments valides avec stock normal
    - Médicaments avec stock faible (< 10)
    - Médicaments expirés
    - Médicaments expirant bientôt (dans les 30 jours)
    """
    print("\n" + "=" * 60)
    print("💊 Création des médicaments...")
    print("=" * 60)

    # Supprimer les médicaments existants
    Vente.objects.all().delete()
    Medicament.objects.all().delete()

    aujourd_hui = date.today()

    # Liste des médicaments à créer
    medicaments_data = [
        # --- Médicaments valides avec stock normal ---
        {
            'nom': 'Paracétamol 500mg',
            'description': 'Analgésique et antipyrétique. Utilisé pour soulager la douleur et réduire la fièvre.',
            'prix': Decimal('12.50'),
            'stock': 150,
            'date_expiration': aujourd_hui + timedelta(days=365),
        },
        {
            'nom': 'Amoxicilline 500mg',
            'description': 'Antibiotique de la famille des pénicillines. Traitement des infections bactériennes.',
            'prix': Decimal('35.00'),
            'stock': 80,
            'date_expiration': aujourd_hui + timedelta(days=540),
        },
        {
            'nom': 'Ibuprofène 400mg',
            'description': 'Anti-inflammatoire non stéroïdien (AINS). Soulage la douleur et l\'inflammation.',
            'prix': Decimal('18.00'),
            'stock': 120,
            'date_expiration': aujourd_hui + timedelta(days=450),
        },
        {
            'nom': 'Oméprazole 20mg',
            'description': 'Inhibiteur de la pompe à protons. Traitement du reflux gastro-œsophagien.',
            'prix': Decimal('42.00'),
            'stock': 60,
            'date_expiration': aujourd_hui + timedelta(days=300),
        },
        {
            'nom': 'Metformine 850mg',
            'description': 'Antidiabétique oral. Traitement du diabète de type 2.',
            'prix': Decimal('28.50'),
            'stock': 200,
            'date_expiration': aujourd_hui + timedelta(days=720),
        },
        {
            'nom': 'Amlodipine 5mg',
            'description': 'Antihypertenseur. Traitement de l\'hypertension artérielle.',
            'prix': Decimal('55.00'),
            'stock': 45,
            'date_expiration': aujourd_hui + timedelta(days=400),
        },
        {
            'nom': 'Vitamine C 1000mg',
            'description': 'Complément alimentaire. Renforce le système immunitaire.',
            'prix': Decimal('22.00'),
            'stock': 300,
            'date_expiration': aujourd_hui + timedelta(days=600),
        },

        # --- Médicaments avec stock faible (< 10) ---
        {
            'nom': 'Ciprofloxacine 500mg',
            'description': 'Antibiotique fluoroquinolone. Traitement des infections urinaires.',
            'prix': Decimal('65.00'),
            'stock': 5,
            'date_expiration': aujourd_hui + timedelta(days=180),
        },
        {
            'nom': 'Doliprane 1000mg',
            'description': 'Paracétamol dosé à 1000mg. Analgésique et antipyrétique forte dose.',
            'prix': Decimal('15.00'),
            'stock': 3,
            'date_expiration': aujourd_hui + timedelta(days=200),
        },
        {
            'nom': 'Loratadine 10mg',
            'description': 'Antihistaminique. Traitement des allergies et rhinite allergique.',
            'prix': Decimal('30.00'),
            'stock': 8,
            'date_expiration': aujourd_hui + timedelta(days=250),
        },

        # --- Médicaments expirés ---
        {
            'nom': 'Aspirine 500mg',
            'description': 'Acide acétylsalicylique. Analgésique, anti-inflammatoire et antiagrégant plaquettaire.',
            'prix': Decimal('10.00'),
            'stock': 25,
            'date_expiration': aujourd_hui - timedelta(days=30),
        },
        {
            'nom': 'Cétirizine 10mg',
            'description': 'Antihistaminique de 2ème génération. Traitement des réactions allergiques.',
            'prix': Decimal('20.00'),
            'stock': 15,
            'date_expiration': aujourd_hui - timedelta(days=60),
        },

        # --- Médicaments expirant bientôt (dans les 30 jours) ---
        {
            'nom': 'Diclofénac 50mg',
            'description': 'AINS puissant. Traitement des douleurs articulaires et musculaires.',
            'prix': Decimal('25.00'),
            'stock': 40,
            'date_expiration': aujourd_hui + timedelta(days=15),
        },
        {
            'nom': 'Pantoprazole 40mg',
            'description': 'Inhibiteur de la pompe à protons. Traitement de l\'ulcère gastrique.',
            'prix': Decimal('48.00'),
            'stock': 20,
            'date_expiration': aujourd_hui + timedelta(days=10),
        },
        {
            'nom': 'Azithromycine 250mg',
            'description': 'Antibiotique macrolide. Traitement des infections respiratoires.',
            'prix': Decimal('72.00'),
            'stock': 12,
            'date_expiration': aujourd_hui + timedelta(days=25),
        },
    ]

    medicaments = []
    for data in medicaments_data:
        med = Medicament.objects.create(**data)
        status = ""
        if med.est_expire:
            status = "❌ EXPIRÉ"
        elif med.expire_bientot:
            status = "⚠️ EXPIRE BIENTÔT"
        elif med.stock_faible:
            status = "📦 STOCK FAIBLE"
        else:
            status = "✅ OK"

        print(f"  {status} — {med.nom} | Stock: {med.stock} | Exp: {med.date_expiration}")
        medicaments.append(med)

    return medicaments


def seed_ventes(admin, medicaments):
    """
    Crée 8 ventes de démonstration effectuées par l'administrateur.
    Chaque vente décrémente automatiquement le stock du médicament.
    """
    print("\n" + "=" * 60)
    print("🛒 Création des ventes...")
    print("=" * 60)

    # Liste des ventes à créer (index du médicament, quantité, remise)
    ventes_data = [
        {'med_index': 0, 'quantite': 10, 'remise': Decimal('0')},     # Paracétamol
        {'med_index': 1, 'quantite': 5, 'remise': Decimal('10')},      # Amoxicilline
        {'med_index': 2, 'quantite': 8, 'remise': Decimal('5')},       # Ibuprofène
        {'med_index': 3, 'quantite': 3, 'remise': Decimal('0')},       # Oméprazole
        {'med_index': 0, 'quantite': 20, 'remise': Decimal('15')},     # Paracétamol (2ème vente)
        {'med_index': 4, 'quantite': 12, 'remise': Decimal('0')},      # Metformine
        {'med_index': 6, 'quantite': 25, 'remise': Decimal('20')},     # Vitamine C
        {'med_index': 5, 'quantite': 2, 'remise': Decimal('0')},       # Amlodipine
    ]

    for data in ventes_data:
        med = medicaments[data['med_index']]
        vente = Vente(
            medicament=med,
            quantite=data['quantite'],
            prix_unitaire=med.prix,
            remise=data['remise'],
            vendeur=admin,
        )
        vente.save()  # Le montant total est calculé dans save()

        # Décrémenter le stock
        med.stock -= data['quantite']
        med.save()

        print(
            f"  ✅ Vente : {data['quantite']}x {med.nom} "
            f"| Remise: {data['remise']}% "
            f"| Total: {vente.montant_total} DH"
        )

    return Vente.objects.all()


def main():
    """Fonction principale — Exécute la création des données de test."""
    print("\n" + "🌱" * 30)
    print("  SCRIPT DE DONNÉES DE TEST — PharmaGest")
    print("🌱" * 30 + "\n")

    # Étape 1 : Créer les utilisateurs
    admin, employe = seed_utilisateurs()

    # Étape 2 : Créer les médicaments
    medicaments = seed_medicaments()

    # Étape 3 : Créer les ventes
    ventes = seed_ventes(admin, medicaments)

    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES DONNÉES CRÉÉES")
    print("=" * 60)
    print(f"  👤 Utilisateurs : {Utilisateur.objects.filter(is_superuser=False).count()}")
    print(f"  💊 Médicaments  : {Medicament.objects.count()}")
    print(f"  🛒 Ventes       : {Vente.objects.count()}")
    print("\n" + "=" * 60)
    print("  🔑 IDENTIFIANTS DE CONNEXION")
    print("=" * 60)
    print("  Admin   → Utilisateur: admin    | Mot de passe: admin123")
    print("  Employé → Utilisateur: employe  | Mot de passe: employe123")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
