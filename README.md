# 💊 PharmaGest — Application de Gestion de Pharmacie

> Projet universitaire EMSI — Application web de gestion de pharmacie développée avec Django et MySQL.

---

## 📋 Table des matières

1. [Présentation du projet](#-présentation-du-projet)
2. [Fonctionnalités](#-fonctionnalités)
3. [Prérequis techniques](#-prérequis-techniques)
4. [Installation et configuration](#-installation-et-configuration)
5. [Lancer l'application](#-lancer-lapplication)
6. [Exécution des tests](#-exécution-des-tests)
7. [Rôles et permissions](#-rôles-et-permissions)
8. [Structure du projet](#-structure-du-projet)
9. [Stack technique](#-stack-technique)
10. [Conformité au cahier des charges](#-conformité-au-cahier-des-charges)

---

## 🎯 Présentation du projet

**PharmaGest** est une application web de gestion de pharmacie permettant de :
- Gérer l'inventaire des médicaments (ajout, modification, consultation, suppression)
- Suivre les dates d'expiration et les niveaux de stock
- Enregistrer les ventes avec application de remises
- Contrôler l'accès selon le rôle de l'utilisateur (Admin / Employé)

L'application respecte les contraintes du cahier des charges universitaire :
- **Pas de module Client** — conformément aux spécifications
- **Séparation stricte des rôles** — Admin vs Employé
- **Interface en français** — tous les libellés et messages sont en français

---

## ✨ Fonctionnalités

### Authentification sécurisée
- Connexion par identifiant et mot de passe
- Protection CSRF sur tous les formulaires
- Validation des mots de passe (longueur, complexité)
- Redirection automatique après connexion/déconnexion

### Gestion des médicaments (Admin + Employé)
- **Ajouter** un médicament (nom, description, prix, stock, date d'expiration)
- **Consulter** la liste avec filtres (expirés, stock faible, expirant bientôt)
- **Rechercher** par nom de médicament
- **Modifier** les informations d'un médicament
- **Supprimer** un médicament (**Admin uniquement**)

### Gestion des ventes (Admin uniquement)
- Enregistrer une vente avec sélection du médicament
- Appliquer une remise (0% à 100%)
- Calcul automatique du montant total
- Décrémentation automatique du stock
- Historique des ventes avec recherche

### Tableau de bord
- Statistiques des médicaments (total, stock faible, expirés, expirant bientôt)
- Statistiques des ventes — **visibles uniquement par l'Admin**
- Tableau des médicaments à surveiller

---

## ⚙️ Prérequis techniques

| Outil | Version minimale |
|-------|-----------------|
| Python | 3.10+ |
| MySQL | 5.7+ (via XAMPP ou installation native) |
| pip | 21+ |
| Navigateur | Chrome, Firefox, Safari ou Edge |

---

## 🚀 Installation et configuration

### 1. Cloner le projet

```bash
git clone <url-du-dépôt>
cd project_rech
```

### 2. Installer les dépendances Python

```bash
pip install django==4.2.17 mysqlclient==2.2.8
```

### 3. Configurer la base de données MySQL

**Option A — Avec MySQL (XAMPP recommandé)**

1. Démarrer MySQL via XAMPP Control Panel
2. Créer la base de données :

```sql
mysql -u root

CREATE DATABASE pharmagest_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

3. Vérifier la configuration dans `pharmacie_project/settings.py` :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pharmagest_db',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

**Option B — Avec SQLite (sans MySQL)**

Modifier `pharmacie_project/settings.py` :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### 4. Appliquer les migrations

```bash
python manage.py migrate
```

### 5. Charger les données de test

```bash
python seed_data.py
```

Ce script crée :
- 2 utilisateurs (admin et employé)
- 15 médicaments (avec différents statuts de stock et d'expiration)
- 8 ventes de test

---

## ▶️ Lancer l'application

```bash
python manage.py runserver
```

Ouvrir dans le navigateur : **http://127.0.0.1:8000**

### Identifiants de connexion

| Rôle | Utilisateur | Mot de passe |
|------|------------|-------------|
| Administrateur | `admin` | `admin123` |
| Employé | `employe` | `employe123` |

---

## 🧪 Exécution des tests

### Lancer tous les tests

```bash
python manage.py test pharmacy -v 2
```

### Lancer un groupe de tests spécifique

```bash
# Tests d'authentification
python manage.py test pharmacy.tests.AuthenticationTests -v 2

# Tests de contrôle d'accès (RBAC)
python manage.py test pharmacy.tests.RoleBasedAccessTests -v 2

# Tests CRUD médicaments
python manage.py test pharmacy.tests.MedicamentCRUDTests -v 2

# Tests gestion des ventes
python manage.py test pharmacy.tests.VenteManagementTests -v 2

# Tests des restrictions
python manage.py test pharmacy.tests.RestrictionTests -v 2

# Tests des modèles
python manage.py test pharmacy.tests.UtilisateurModelTests -v 2
python manage.py test pharmacy.tests.MedicamentModelTests -v 2
python manage.py test pharmacy.tests.VenteModelTests -v 2

# Tests des formulaires
python manage.py test pharmacy.tests.FormValidationTests -v 2

# Tests de sécurité
python manage.py test pharmacy.tests.SecurityTests -v 2
```

### Couverture des tests

Les tests vérifient les exigences suivantes du cahier des charges :

| Catégorie | Nombre de tests | Exigence couverte |
|-----------|:--------------:|-------------------|
| Authentification | 13 | Connexion sécurisée, sessions, redirections |
| Contrôle d'accès (RBAC) | 17 | Permissions Admin vs Employé |
| CRUD Médicaments | 13 | Ajout, lecture, modification, suppression |
| Gestion des ventes | 11 | Création, historique, remises, stock |
| Restrictions | 4 | Pas de module Client, données masquées |
| Modèles (Utilisateur) | 4 | Rôles, représentation textuelle |
| Modèles (Médicament) | 8 | Propriétés calculées (expiré, stock faible) |
| Modèles (Vente) | 5 | Calcul montant, tri par date |
| Formulaires | 2 | Validation, filtrage stock |
| Sécurité | 5 | Auth requise, CSRF |
| **Total** | **82** | |

---

## 👥 Rôles et permissions

### Administrateur (`admin`)

| Fonctionnalité | Accès |
|---------------|:-----:|
| Tableau de bord (avec stats ventes) | ✅ |
| Voir la liste des médicaments | ✅ |
| Ajouter un médicament | ✅ |
| Modifier un médicament | ✅ |
| Supprimer un médicament | ✅ |
| Voir les ventes | ✅ |
| Enregistrer une vente | ✅ |
| Appliquer des remises | ✅ |
| Voir le détail d'une vente | ✅ |

### Employé (`employe`)

| Fonctionnalité | Accès |
|---------------|:-----:|
| Tableau de bord (sans stats ventes) | ✅ |
| Voir la liste des médicaments | ✅ |
| Ajouter un médicament | ✅ |
| Modifier un médicament | ✅ |
| Supprimer un médicament | ❌ |
| Voir les ventes | ❌ |
| Enregistrer une vente | ❌ |
| Appliquer des remises | ❌ |
| Voir le détail d'une vente | ❌ |

### Mécanisme de contrôle d'accès

Le contrôle d'accès est appliqué à **deux niveaux** :

1. **Côté serveur (Backend)** — Décorateur `@admin_required` qui vérifie le rôle avant d'exécuter la vue. Si l'utilisateur n'est pas admin, il est redirigé vers le tableau de bord avec un message d'erreur.

2. **Côté client (Frontend)** — Filtre de template `{% if user|is_admin %}` qui masque les éléments d'interface (boutons, menus, sections) non autorisés pour l'employé.

---

## 📁 Structure du projet

```
project_rech/
├── manage.py                          # Script de gestion Django
├── seed_data.py                       # Script de chargement des données de test
├── requirements.txt                   # Dépendances Python
├── README.md                          # Ce fichier
├── db.sqlite3                         # Base SQLite (alternative à MySQL)
│
├── pharmacie_project/                 # Configuration du projet Django
│   ├── __init__.py
│   ├── settings.py                    # Paramètres (DB, apps, auth, i18n)
│   ├── urls.py                        # Routes principales
│   ├── wsgi.py                        # Point d'entrée WSGI
│   └── asgi.py                        # Point d'entrée ASGI
│
├── pharmacy/                          # Application principale
│   ├── __init__.py
│   ├── admin.py                       # Configuration admin Django
│   ├── apps.py                        # Configuration de l'application
│   ├── decorators.py                  # @admin_required
│   ├── forms.py                       # LoginForm, MedicamentForm, VenteForm
│   ├── models.py                      # Utilisateur, Medicament, Vente
│   ├── tests.py                       # Tests unitaires et d'intégration (82 tests)
│   ├── urls.py                        # Routes de l'application
│   ├── views.py                       # Vues (authentification, CRUD, API)
│   │
│   ├── templatetags/                  # Filtres de template personnalisés
│   │   ├── __init__.py
│   │   └── pharmacy_tags.py           # is_admin, is_employe
│   │
│   ├── templates/pharmacy/            # Templates HTML
│   │   ├── base.html                  # Template de base (navbar, sidebar)
│   │   ├── login.html                 # Page de connexion
│   │   ├── dashboard.html             # Tableau de bord
│   │   ├── medicament_list.html       # Liste des médicaments
│   │   ├── medicament_detail.html     # Détail d'un médicament
│   │   ├── medicament_form.html       # Formulaire ajout/modification
│   │   ├── medicament_confirm_delete.html  # Confirmation de suppression
│   │   ├── vente_list.html            # Historique des ventes
│   │   ├── vente_detail.html          # Détail d'une vente
│   │   └── vente_form.html            # Formulaire de vente
│   │
│   └── migrations/                    # Migrations de base de données
│
└── static/pharmacy/                   # Fichiers statiques
    ├── css/
    │   └── style.css                  # Styles CSS personnalisés
    └── js/
        └── main.js                    # JavaScript (calculs dynamiques)
```

---

## 🛠️ Stack technique

| Couche | Technologie | Version |
|--------|------------|---------|
| **Backend** | Python / Django | 4.2.17 (LTS) |
| **Base de données** | MySQL (mysqlclient) | 2.2.8 |
| **Frontend** | HTML5 / CSS3 / JavaScript | — |
| **Framework CSS** | Bootstrap | 5.3.3 |
| **Icônes** | Bootstrap Icons | 1.11.3 |
| **Typographie** | Google Fonts (Inter) | — |
| **Serveur web** | Django Development Server | — |

---

## ✅ Conformité au cahier des charges

| # | Exigence | Statut | Implémentation |
|---|----------|:------:|----------------|
| 1 | Système de connexion sécurisé | ✅ | `LoginForm` + Django Auth + CSRF |
| 2 | Deux rôles : Admin et Employé | ✅ | Champ `role` dans le modèle `Utilisateur` |
| 3 | Admin : tous les droits | ✅ | Accès complet à médicaments + ventes + suppression |
| 4 | Employé : accès limité | ✅ | Voir/Ajouter/Modifier médicaments uniquement |
| 5 | CRUD Médicaments | ✅ | 4 vues + 4 templates |
| 6 | Champs requis : Nom, Expiration, Prix, Stock | ✅ | Modèle `Medicament` avec validateurs |
| 7 | Suppression Admin uniquement | ✅ | `@admin_required` sur `medicament_delete` |
| 8 | Module ventes (Admin only) | ✅ | `@admin_required` sur toutes les vues vente |
| 9 | Enregistrement des ventes avec remises | ✅ | `VenteForm` + calcul auto du montant |
| 10 | Historique des ventes | ✅ | `vente_list` avec recherche |
| 11 | Pas de module Client | ✅ | Aucun modèle, URL ou template Client |
| 12 | Employé ne voit pas les ventes | ✅ | Backend (`@admin_required`) + Frontend (`is_admin`) |
| 13 | Django + MySQL | ✅ | Django 4.2.17 + mysqlclient 2.2.8 |
| 14 | HTML5 / CSS3 / JavaScript | ✅ | Bootstrap 5.3 + CSS custom + JS custom |
| 15 | Interfaces séparées Admin/Employé | ✅ | Dashboard et menus adaptés au rôle |
| 16 | Documentation technique | ✅ | Ce fichier README.md |
| 17 | Tests de validation | ✅ | 82 tests automatisés dans `pharmacy/tests.py` |

---

## 📄 Licence

Projet universitaire — EMSI © 2026. Usage académique uniquement.

# pharmacy