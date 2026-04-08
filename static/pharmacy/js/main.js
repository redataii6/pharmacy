/**
 * ============================================================
 * JavaScript personnalisé — Application PharmaGest
 * ============================================================
 * Ce fichier contient le code JavaScript pour :
 * 1. Calcul dynamique du montant total dans le formulaire de vente
 * 2. Pré-remplissage du prix unitaire lors de la sélection d'un médicament
 * 3. Auto-dismiss des messages flash après 5 secondes
 * ============================================================
 */

document.addEventListener('DOMContentLoaded', function () {

    // ============================================================
    // 1. CALCUL DYNAMIQUE DU MONTANT TOTAL (Formulaire de vente)
    // ============================================================

    /**
     * Calcule et affiche le montant total estimé dans le formulaire de vente.
     * 
     * Formule : montant = (prix_unitaire × quantité) × (1 - remise / 100)
     * 
     * Cette fonction est appelée chaque fois qu'un des champs
     * (prix, quantité, remise) est modifié.
     */
    function calculerMontantTotal() {
        const prixInput = document.getElementById('id_prix_unitaire');
        const quantiteInput = document.getElementById('id_quantite');
        const remiseInput = document.getElementById('id_remise');
        const montantDisplay = document.getElementById('montant_total_display');

        // Vérifier que tous les éléments existent (page de vente uniquement)
        if (!prixInput || !quantiteInput || !remiseInput || !montantDisplay) return;

        // Récupérer les valeurs numériques des champs
        const prix = parseFloat(prixInput.value) || 0;
        const quantite = parseInt(quantiteInput.value) || 0;
        const remise = parseFloat(remiseInput.value) || 0;

        // Calculer le montant total avec remise
        const sousTotal = prix * quantite;
        const montantTotal = sousTotal * (1 - remise / 100);

        // Afficher le montant formaté avec 2 décimales
        montantDisplay.textContent = montantTotal.toFixed(2) + ' DH';

        // Changer la couleur selon le montant
        if (montantTotal > 0) {
            montantDisplay.classList.remove('text-muted');
            montantDisplay.classList.add('text-primary');
        } else {
            montantDisplay.classList.remove('text-primary');
            montantDisplay.classList.add('text-muted');
        }
    }

    // Attacher les écouteurs d'événements aux champs du formulaire de vente
    const champsVente = ['id_prix_unitaire', 'id_quantite', 'id_remise'];
    champsVente.forEach(function (champId) {
        const element = document.getElementById(champId);
        if (element) {
            element.addEventListener('input', calculerMontantTotal);
            element.addEventListener('change', calculerMontantTotal);
        }
    });

    // ============================================================
    // 2. PRÉ-REMPLISSAGE DU PRIX LORS DE LA SÉLECTION D'UN MÉDICAMENT
    // ============================================================

    /**
     * Lorsqu'un médicament est sélectionné dans le formulaire de vente,
     * son prix est automatiquement injecté dans le champ "Prix unitaire"
     * et l'information de stock est affichée.
     * 
     * Les données des prix sont injectées dans le template via un objet
     * JavaScript `medicamentPrices` généré côté serveur.
     */
    const selectMedicament = document.getElementById('id_medicament');
    if (selectMedicament) {
        selectMedicament.addEventListener('change', function () {
            const medicamentId = this.value;
            const prixInput = document.getElementById('id_prix_unitaire');
            const stockInfo = document.getElementById('stock_info');

            // Vérifier que l'objet medicamentPrices existe (défini dans le template)
            if (typeof medicamentPrices !== 'undefined' && medicamentId && medicamentPrices[medicamentId]) {
                const data = medicamentPrices[medicamentId];

                // Pré-remplir le prix unitaire
                if (prixInput) {
                    prixInput.value = data.prix.toFixed(2);
                }

                // Afficher l'information de stock
                if (stockInfo) {
                    stockInfo.innerHTML = '<i class="bi bi-box-seam me-1"></i>Stock disponible : <strong>' + data.stock + '</strong> unités';
                    stockInfo.classList.remove('text-danger');
                    stockInfo.classList.add('text-muted');
                    if (data.stock < 10) {
                        stockInfo.classList.remove('text-muted');
                        stockInfo.classList.add('text-danger');
                    }
                }

                // Recalculer le montant total
                calculerMontantTotal();
            } else {
                // Réinitialiser si aucun médicament sélectionné
                if (prixInput) prixInput.value = '';
                if (stockInfo) stockInfo.innerHTML = '';
            }
        });
    }

    // ============================================================
    // 3. AUTO-DISMISS DES MESSAGES FLASH
    // ============================================================

    /**
     * Ferme automatiquement les messages flash (alerts Bootstrap)
     * après 5 secondes avec une animation de fondu.
     */
    const alertElements = document.querySelectorAll('.alert');
    alertElements.forEach(function (alert) {
        setTimeout(function () {
            // Utiliser l'API Bootstrap pour fermer l'alerte proprement
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000); // 5 secondes
    });

    // Calcul initial si on est sur la page de vente
    calculerMontantTotal();
});
