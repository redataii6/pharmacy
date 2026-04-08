"""
Vues (Views) pour l'application de gestion de pharmacie.
=========================================================
Ce fichier contient toutes les vues de l'application :

1. AUTHENTIFICATION
   - login_view    : Connexion de l'utilisateur
   - logout_view   : Déconnexion de l'utilisateur

2. TABLEAU DE BORD
   - dashboard     : Page d'accueil avec statistiques

3. CRUD MÉDICAMENTS (Tous les utilisateurs connectés)
   - medicament_list   : Liste des médicaments avec filtres
   - medicament_create : Ajout d'un nouveau médicament
   - medicament_detail : Détail d'un médicament
   - medicament_update : Modification d'un médicament
   - medicament_delete : Suppression (Admin uniquement)

4. CRUD VENTES (Admin uniquement)
   - vente_list    : Historique des ventes
   - vente_create  : Enregistrement d'une nouvelle vente
   - vente_detail  : Détail d'une vente

SÉCURITÉ : Les décorateurs @login_required et @admin_required 
garantissent le contrôle d'accès selon le rôle de l'utilisateur.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from django.http import JsonResponse

from .models import Utilisateur, Medicament, Vente
from .forms import LoginForm, MedicamentForm, VenteForm
from .decorators import admin_required


# ============================================================
# VUES D'AUTHENTIFICATION
# ============================================================

def login_view(request):
    """
    Vue de connexion des utilisateurs.
    
    - GET  : Affiche le formulaire de connexion.
    - POST : Valide les identifiants et redirige vers le tableau de bord.
    
    Si l'utilisateur est déjà connecté, il est redirigé automatiquement
    vers le tableau de bord.
    """
    # Si l'utilisateur est déjà connecté, rediriger vers le dashboard
    if request.user.is_authenticated:
        return redirect('pharmacy:dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            # Récupérer les données validées du formulaire
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Authentifier l'utilisateur
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Connecter l'utilisateur et créer une session
                login(request, user)
                messages.success(
                    request,
                    f"👋 Bienvenue, {user.get_full_name() or user.username} ! "
                    f"Vous êtes connecté en tant que {user.get_role_display()}."
                )
                return redirect('pharmacy:dashboard')
        else:
            messages.error(request, "❌ Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = LoginForm()

    return render(request, 'pharmacy/login.html', {'form': form})


def logout_view(request):
    """
    Vue de déconnexion de l'utilisateur.
    
    Détruit la session active et redirige vers la page de connexion.
    Fonctionne avec les méthodes GET et POST pour plus de flexibilité.
    """
    logout(request)
    messages.info(request, "👋 Vous avez été déconnecté avec succès.")
    return redirect('pharmacy:login')


# ============================================================
# TABLEAU DE BORD
# ============================================================

@login_required
def dashboard(request):
    """
    Vue du tableau de bord principal.
    
    Affiche des statistiques générales sur l'état de la pharmacie :
    - Nombre total de médicaments
    - Médicaments en stock faible (< 10 unités)
    - Médicaments expirés ou expirant bientôt
    - Statistiques de ventes (Admin uniquement)
    
    Le contenu affiché varie selon le rôle de l'utilisateur.
    """
    aujourd_hui = timezone.now().date()
    dans_30_jours = aujourd_hui + timezone.timedelta(days=30)

    # --- Statistiques sur les médicaments (visibles par tous) ---
    total_medicaments = Medicament.objects.count()

    # Médicaments dont le stock est inférieur à 10
    stock_faible = Medicament.objects.filter(stock__lt=10).count()

    # Médicaments dont la date d'expiration est dépassée
    medicaments_expires = Medicament.objects.filter(
        date_expiration__lt=aujourd_hui
    ).count()

    # Médicaments expirant dans les 30 prochains jours (mais pas encore expirés)
    expire_bientot = Medicament.objects.filter(
        date_expiration__gte=aujourd_hui,
        date_expiration__lte=dans_30_jours
    ).count()

    # Liste des médicaments à surveiller (expirés ou expirant bientôt)
    medicaments_alertes = Medicament.objects.filter(
        date_expiration__lte=dans_30_jours
    ).order_by('date_expiration')[:10]

    # --- Statistiques de ventes (Admin uniquement) ---
    ventes_aujourd_hui = 0
    chiffre_affaires_jour = 0
    total_ventes = 0
    chiffre_affaires_total = 0

    if request.user.is_admin():
        # Ventes effectuées aujourd'hui
        ventes_du_jour = Vente.objects.filter(date_vente__date=aujourd_hui)
        ventes_aujourd_hui = ventes_du_jour.count()
        chiffre_affaires_jour = ventes_du_jour.aggregate(
            total=Sum('montant_total')
        )['total'] or 0

        # Total des ventes (toutes périodes confondues)
        total_ventes = Vente.objects.count()
        chiffre_affaires_total = Vente.objects.aggregate(
            total=Sum('montant_total')
        )['total'] or 0

    # --- Préparer le contexte pour le template ---
    context = {
        'total_medicaments': total_medicaments,
        'stock_faible': stock_faible,
        'medicaments_expires': medicaments_expires,
        'expire_bientot': expire_bientot,
        'medicaments_alertes': medicaments_alertes,
        'ventes_aujourd_hui': ventes_aujourd_hui,
        'chiffre_affaires_jour': chiffre_affaires_jour,
        'total_ventes': total_ventes,
        'chiffre_affaires_total': chiffre_affaires_total,
    }

    return render(request, 'pharmacy/dashboard.html', context)


# ============================================================
# VUES CRUD — MÉDICAMENTS
# ============================================================

@login_required
def medicament_list(request):
    """
    Vue affichant la liste de tous les médicaments.
    
    Supporte les filtres via paramètres GET :
    - ?filtre=expires     : Médicaments expirés uniquement
    - ?filtre=stock_faible : Médicaments en stock faible uniquement
    - ?filtre=expire_bientot : Médicaments expirant dans les 30 jours
    - ?q=recherche        : Recherche par nom de médicament
    
    Accessible par tous les utilisateurs connectés (Admin et Employé).
    """
    aujourd_hui = timezone.now().date()
    dans_30_jours = aujourd_hui + timezone.timedelta(days=30)

    # Récupérer tous les médicaments par défaut
    medicaments = Medicament.objects.all()

    # --- Appliquer les filtres si présents dans l'URL ---
    filtre = request.GET.get('filtre', '')
    recherche = request.GET.get('q', '')

    if filtre == 'expires':
        # Filtrer les médicaments expirés
        medicaments = medicaments.filter(date_expiration__lt=aujourd_hui)
    elif filtre == 'stock_faible':
        # Filtrer les médicaments en stock faible
        medicaments = medicaments.filter(stock__lt=10)
    elif filtre == 'expire_bientot':
        # Filtrer les médicaments expirant dans les 30 jours
        medicaments = medicaments.filter(
            date_expiration__gte=aujourd_hui,
            date_expiration__lte=dans_30_jours
        )

    if recherche:
        # Recherche par nom (insensible à la casse)
        medicaments = medicaments.filter(nom__icontains=recherche)

    context = {
        'medicaments': medicaments,
        'filtre_actif': filtre,
        'recherche': recherche,
    }

    return render(request, 'pharmacy/medicament_list.html', context)


@login_required
def medicament_create(request):
    """
    Vue pour ajouter un nouveau médicament.
    
    - GET  : Affiche le formulaire vide.
    - POST : Valide et enregistre le nouveau médicament.
    
    Accessible par tous les utilisateurs connectés (Admin et Employé).
    """
    if request.method == 'POST':
        form = MedicamentForm(request.POST)
        if form.is_valid():
            # Sauvegarder le médicament en base de données
            medicament = form.save()
            messages.success(
                request,
                f"✅ Le médicament « {medicament.nom} » a été ajouté avec succès."
            )
            return redirect('pharmacy:medicament_list')
    else:
        form = MedicamentForm()

    context = {
        'form': form,
        'titre': 'Ajouter un médicament',
        'bouton': 'Ajouter',
    }
    return render(request, 'pharmacy/medicament_form.html', context)


@login_required
def medicament_detail(request, pk):
    """
    Vue affichant le détail d'un médicament spécifique.
    
    Affiche toutes les informations du médicament identifié par sa clé primaire.
    Affiche également l'historique des ventes associées (Admin uniquement).
    
    Args:
        pk (int): Clé primaire du médicament.
    
    Accessible par tous les utilisateurs connectés.
    """
    medicament = get_object_or_404(Medicament, pk=pk)

    # Récupérer les ventes associées si l'utilisateur est admin
    ventes = []
    if request.user.is_admin():
        ventes = medicament.ventes.all()[:10]

    context = {
        'medicament': medicament,
        'ventes': ventes,
    }
    return render(request, 'pharmacy/medicament_detail.html', context)


@login_required
def medicament_update(request, pk):
    """
    Vue pour modifier un médicament existant.
    
    - GET  : Affiche le formulaire pré-rempli avec les données actuelles.
    - POST : Valide et enregistre les modifications.
    
    Args:
        pk (int): Clé primaire du médicament à modifier.
    
    Accessible par tous les utilisateurs connectés (Admin et Employé).
    """
    medicament = get_object_or_404(Medicament, pk=pk)

    if request.method == 'POST':
        form = MedicamentForm(request.POST, instance=medicament)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f"✅ Le médicament « {medicament.nom} » a été modifié avec succès."
            )
            return redirect('pharmacy:medicament_detail', pk=medicament.pk)
    else:
        form = MedicamentForm(instance=medicament)

    context = {
        'form': form,
        'medicament': medicament,
        'titre': f'Modifier : {medicament.nom}',
        'bouton': 'Enregistrer les modifications',
    }
    return render(request, 'pharmacy/medicament_form.html', context)


@admin_required
def medicament_delete(request, pk):
    """
    Vue pour supprimer un médicament.
    
    ⚠️ ACCÈS RESTREINT : Administrateurs uniquement.
    Les employés n'ont pas le droit de supprimer des médicaments.
    
    - GET  : Affiche la page de confirmation de suppression.
    - POST : Supprime le médicament de la base de données.
    
    Args:
        pk (int): Clé primaire du médicament à supprimer.
    """
    medicament = get_object_or_404(Medicament, pk=pk)

    if request.method == 'POST':
        nom = medicament.nom
        try:
            medicament.delete()
            messages.success(
                request,
                f"🗑️ Le médicament « {nom} » a été supprimé avec succès."
            )
        except Exception:
            messages.error(
                request,
                f"❌ Impossible de supprimer « {nom} ». "
                "Ce médicament est lié à des ventes existantes."
            )
        return redirect('pharmacy:medicament_list')

    context = {
        'medicament': medicament,
    }
    return render(request, 'pharmacy/medicament_confirm_delete.html', context)


# ============================================================
# VUES CRUD — VENTES (Admin uniquement)
# ============================================================

@admin_required
def vente_list(request):
    """
    Vue affichant l'historique des ventes.
    
    ⚠️ ACCÈS RESTREINT : Administrateurs uniquement.
    
    Affiche la liste de toutes les ventes triées par date décroissante.
    Supporte la recherche par nom de médicament.
    """
    ventes = Vente.objects.select_related('medicament', 'vendeur').all()

    # Recherche par nom de médicament
    recherche = request.GET.get('q', '')
    if recherche:
        ventes = ventes.filter(medicament__nom__icontains=recherche)

    context = {
        'ventes': ventes,
        'recherche': recherche,
    }
    return render(request, 'pharmacy/vente_list.html', context)


@admin_required
def vente_create(request):
    """
    Vue pour enregistrer une nouvelle vente.
    
    ⚠️ ACCÈS RESTREINT : Administrateurs uniquement.
    
    Lors de l'enregistrement d'une vente :
    1. Le stock du médicament est automatiquement décrémenté.
    2. Le montant total est calculé automatiquement (dans le modèle).
    3. Le vendeur est automatiquement défini comme l'utilisateur connecté.
    
    - GET  : Affiche le formulaire de vente.
    - POST : Valide et enregistre la vente.
    """
    if request.method == 'POST':
        form = VenteForm(request.POST)
        if form.is_valid():
            # Créer l'objet vente sans le sauvegarder (commit=False)
            vente = form.save(commit=False)
            # Définir le vendeur comme l'utilisateur connecté
            vente.vendeur = request.user
            # Sauvegarder la vente (le montant total est calculé dans le modèle)
            vente.save()

            # Décrémenter le stock du médicament
            medicament = vente.medicament
            medicament.stock -= vente.quantite
            medicament.save()

            messages.success(
                request,
                f"✅ Vente enregistrée : {vente.quantite}x {medicament.nom} "
                f"pour {vente.montant_total} DH."
            )
            return redirect('pharmacy:vente_list')
    else:
        form = VenteForm()

    context = {
        'form': form,
    }
    return render(request, 'pharmacy/vente_form.html', context)


@admin_required
def vente_detail(request, pk):
    """
    Vue affichant le détail d'une vente spécifique.
    
    ⚠️ ACCÈS RESTREINT : Administrateurs uniquement.
    
    Args:
        pk (int): Clé primaire de la vente.
    """
    vente = get_object_or_404(
        Vente.objects.select_related('medicament', 'vendeur'),
        pk=pk
    )
    context = {
        'vente': vente,
    }
    return render(request, 'pharmacy/vente_detail.html', context)


# ============================================================
# API INTERNE — Prix du médicament (pour le JavaScript)
# ============================================================

@admin_required
def api_medicament_prix(request, pk):
    """
    Point d'accès API pour récupérer le prix d'un médicament.
    
    Utilisé par le JavaScript du formulaire de vente pour pré-remplir
    automatiquement le champ prix_unitaire lorsqu'un médicament est sélectionné.
    
    Args:
        pk (int): Clé primaire du médicament.
    
    Returns:
        JsonResponse: {"prix": <prix>, "stock": <stock>}
    """
    medicament = get_object_or_404(Medicament, pk=pk)
    return JsonResponse({
        'prix': float(medicament.prix),
        'stock': medicament.stock,
        'nom': medicament.nom,
    })
