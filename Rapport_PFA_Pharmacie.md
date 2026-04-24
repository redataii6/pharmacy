<div align="center">

[Insérer Logo EMSI ici]

**École Marocaine des Sciences de l'Ingénieur**
Filière : Ingénierie Informatique et Réseaux (4IIR)

**RAPPORT DE PROJET DE FIN D'ANNÉE**

***

# Conception et développement d'une application web pour la gestion de pharmacie

***

**Réalisé par :**
[Votre Nom complet]

**Encadré par :**
[Nom(s) de votre/vos encadrant(s)]

**Année Universitaire :** 2025/2026

</div>

<div style="page-break-after: always"></div>

# Dédicaces

À mes chers parents,
Pour votre amour inconditionnel, vos sacrifices, et votre soutien indéfectible tout au long de mes études. Vous avez toujours été ma source de motivation et d'inspiration. Que ce travail soit le témoignage de ma profonde gratitude.

À mes frères, mes sœurs et ma famille,
Pour votre présence constante et vos encouragements dans les moments de doute.

À mes amis et collègues de promotion,
Pour les moments de partage, la solidarité et l'entraide durant ces années passées à l'EMSI. 

À tous ceux qui ont contribué de près ou de loin à l'accomplissement de ce projet.

Je vous dédie ce travail.

<div style="page-break-after: always"></div>

# Remerciements

Avant d'entamer la présentation de ce rapport, je tiens à exprimer mes plus sincères remerciements à toutes les personnes qui m'ont accompagné et soutenu durant la réalisation de ce Projet de Fin d'Année.

Mes remerciements s'adressent tout particulièrement à mon encadrant, [Nom de l'encadrant], pour ses conseils avisés, sa disponibilité, et ses directives précieuses qui ont grandement enrichi ce travail. Ses encouragements et son expertise technique m'ont guidé tout au long de la conception et du développement de ce projet.

Je tiens également à remercier chaleureusement la direction et tout le corps professoral de l'École Marocaine des Sciences de l'Ingénieur (EMSI) pour la qualité de l'enseignement dispensé, leur pédagogie et leur dévouement envers notre réussite professionnelle.

Enfin, j'adresse ma reconnaissance à tous ceux qui, de près ou de loin, ont apporté leur pierre à l'édifice pour l'aboutissement de ce travail, que ce soit par un conseil, une aide technique ou un soutien moral.

<div style="page-break-after: always"></div>

# Résumé / Abstract

**Résumé**
La gestion efficace d'une pharmacie est un défi majeur qui nécessite précision, rapidité et fiabilité, notamment pour le suivi des stocks et des dates de péremption. Ce Projet de Fin d'Année présente la conception et le développement d'une application web dédiée à la gestion automatisée d'une pharmacie. L'objectif principal est d'informatiser les processus critiques, incluant la gestion des médicaments, le suivi des ventes et le contrôle des accès selon un modèle RBAC (Role-Based Access Control). L'application a été développée en utilisant des technologies modernes : le framework Django (Python) pour le backend, MySQL pour la base de données, et HTML5/CSS3/JavaScript (Bootstrap) pour des interfaces utilisateur ergonomiques et réactives. Notre solution garantit une traçabilité optimale et une sécurité accrue pour ses utilisateurs (Administrateurs et Employés).
**Mots-clés :** Web, Gestion de Pharmacie, Django, Python, MySQL, RBAC.

**Abstract**
Efficient pharmacy management is a major challenge that requires precision, speed, and reliability, especially for inventory tracking and expiration dates. This End-of-Year Project presents the design and development of a web application dedicated to the automated management of a pharmacy. The main objective is to computerize critical processes, including medication management, sales tracking, and access control according to an RBAC (Role-Based Access Control) model. The application was developed using modern technologies: the Django framework (Python) for the backend, MySQL for the database, and HTML5/CSS3/JavaScript (Bootstrap) for ergonomic and responsive user interfaces. Our solution ensures optimal traceability and increased security for its users (Administrators and Employees).
**Keywords:** Web, Pharmacy Management, Django, Python, MySQL, RBAC.

<div style="page-break-after: always"></div>

# Introduction Générale

Le secteur de la santé, et plus particulièrement celui de la pharmacie, est un domaine où la marge d'erreur tolérée est quasi nulle. La gestion des médicaments impose des règles strictes en matière de suivi de stock et de traçabilité des ventes. L'apparition de risques tels que la rupture de stock de produits vitaux ou la vente de médicaments périmés peut avoir des conséquences graves tant sur le plan sanitaire que légal.

Aujourd'hui, la numérisation des processus de gestion est devenue incontournable pour optimiser les performances des officines. C'est dans ce contexte que s'inscrit notre Projet de Fin d'Année, dont la problématique s'articule autour de la question suivante : *Comment concevoir une plateforme centralisée permettant de sécuriser la gestion des médicaments tout en offrant une interface intuitive et adaptée aux différents profils d'une pharmacie ?*

L'objectif de ce projet est donc de concevoir et développer une application web de gestion de pharmacie robuste. Notre solution se concentre sur l'automatisation du suivi des stocks, la détection proactive des dates de péremption, et la sécurisation des opérations grâce à un système de contrôle d'accès basé sur les rôles (RBAC).

Afin d'exposer clairement notre démarche, ce rapport est structuré en quatre chapitres principaux :
1. Le premier chapitre présente le contexte général et la méthodologie adoptée pour la réalisation du projet.
2. Le deuxième chapitre est consacré à l'analyse et à la spécification des besoins fonctionnels et non fonctionnels.
3. Le troisième chapitre détaille la phase de conception, incluant l'architecture logicielle et la modélisation des données.
4. Enfin, le dernier chapitre illustre l'implémentation de la solution, les outils utilisés et les interfaces développées, avant de conclure par un bilan général et des perspectives.

<div style="page-break-after: always"></div>

# Chapitre 1 : Contexte Général du Projet

## 1.1 Introduction
La transition numérique constitue un levier de performance stratégique pour les établissements pharmaceutiques. Avant de plonger dans les spécifications techniques de notre application, il convient de comprendre l'environnement global dans lequel s'insère ce projet, d'identifier les limites des systèmes actuels et de définir la méthode de travail adoptée.

## 1.2 Problématique
Une pharmacie mal gérée ou gérée de manière traditionnelle (support papier ou tableurs rudimentaires) fait face à plusieurs défis :
* **Erreurs d'inventaire :** Le comptage manuel des milliers de références est sujet aux erreurs humaines, conduisant à des ruptures de stock inattendues.
* **Risques sanitaires liés aux péremptions :** L'absence d'alertes automatisées augmente le risque de conserver en rayon des médicaments périmés, un danger majeur pour la santé publique.
* **Sécurité des données et des finances :** L'absence de différenciation des profils utilisateurs expose l'officine à des erreurs de manipulation ou des actes de malveillance lors des encaissements ou de la suppression de données critiques.

## 1.3 Solution proposée
Pour répondre à ces problématiques, nous proposons une application web centralisée construite autour des piliers suivants :
* **Une gestion de stock intelligente :** Automatisation du maintien des quantités après chaque transaction.
* **Un système d'alerte :** Mise en évidence immédiate des lots s'approchant de leur date limite d'utilisation.
* **Une sécurité par les rôles (RBAC) :** Séparation stricte des privilèges entre l'administrateur (gestion globale et accès financier) et les employés (gestion logistique du rayon).

## 1.4 Méthodologie de travail
Pour mener à bien ce projet de développement, nous avons adopté la méthodologie **Agile Scrum**. Cette approche itérative et incrémentale permet de :
* Diviser le projet en plusieurs "sprints" (cycles de développement courts).
* S'adapter rapidement aux imprévus et ajuster les fonctionnalités en cours de route.
* Assurer des livraisons fonctionnelles continues (d'abord l'authentification, ensuite le CRUD des médicaments, puis le système de vente).

## 1.5 Conclusion du chapitre
Ce premier chapitre a permis de délimiter le cadre de notre projet en identifiant clairement les problématiques métiers de la pharmacie et la méthodologie de gestion choisie pour y pallier. Le chapitre suivant traitera de l'analyse détaillée des fonctionnalités attendues par notre système.

<div style="page-break-after: always"></div>

# Chapitre 2 : Analyse et Spécification des Besoins

## 2.1 Introduction
L'analyse des besoins est la phase fondatrice du cycle de vie du développement logiciel. Elle consiste à répertorier et à décrire rigoureusement ce que le système doit faire (besoins fonctionnels) et comment il doit se comporter (besoins non-fonctionnels), tout en identifiant ses utilisateurs.

## 2.2 Identification des acteurs
Le système interagit avec deux types d'acteurs principaux, dotés de responsabilités clairement distinctes :
* **L'Administrateur (Pharmacien titulaire) :** Il dispose d'un contrôle total sur l'application. Il supervise les ventes, peut supprimer ou appliquer des remises sur les médicaments, et dispose de la vue sur le tableau de bord global.
* **L'Employé (Préparateur en pharmacie) :** Son rôle est purement logistique. Il peut consulter l'inventaire, ajouter de nouveaux arrivages (médicaments) ou modifier les quantités en stock. Il n'a aucun accès aux transactions de vente ni aux fonctions de suppression.

## 2.3 Besoins Fonctionnels
Les fonctionnalités principales du système incluent :
* **Authentification et Autorisation :** Connexion sécurisée de l'utilisateur avec redirection selon son rôle (Admin VS Employé).
* **Gestion des Médicaments (CRUD) :**
    * Création, Lecture, Mise à jour pour les employés.
    * Suppression exclusive pour l'administrateur.
* **Suivi des Ventes :** Interface de facturation générant une diminution automatique du stock (réservée à l'administrateur).
* **Gestion des Péremptions :** Modules ou alertes visuelles identifiant les produits expirés ou proches de l'expiration.

## 2.4 Besoins Non-Fonctionnels
Afin de garantir une exploitation optimale, l'application doit respecter plusieurs critères de qualité :
* **Sécurité :** Les mots de passe codés dans la base de données doivent être hachés. L'accès aux vues sensibles de l'application doit être protégé bloquant les accès non autorisés.
* **Performance :** Le temps de réponse des requêtes à la base de données (notamment lors du chargement de l'inventaire) doit être minimal pour garantir une fluidité d'utilisation en officine.
* **Ergonomie (UI/UX) :** L'interface doit être "Responsive", utilisable aussi bien sur un moniteur de bureau que sur une tablette, avec une palette de couleurs professionnelle et claire.

## 2.5 Diagrammes des Cas d'Utilisation
Le diagramme des cas d'utilisation modélise les interactions globales entre les utilisateurs et le système.

`[Insérer Diagramme de Cas d'Utilisation global ici]`
*Au centre de ce diagramme figurent les processus clés de l'application, entourés des acteurs Administrateur et Employé. L'Administrateur est relié à l'ensemble des cas d'utilisation, tandis que l'Employé est strictement restreint à la gestion de l'inventaire.*

**Détail des cas d'utilisation majeurs :**
1. **Cas "S'authentifier" :** L'acteur saisit ses identifiants. Le système interroge la table des utilisateurs. Si les informations sont correctes, le système vérifie le rôle de l'utilisateur et gère la session courante (redirection vers le Dashboard pour l'Admin, ou vers le Stock pour l'Employé).
2. **Cas "Gérer une vente" :** Cas exclusif à l'Administrateur. Il sélectionne un médicament disponible dans le système, indique la quantité vendue et valide. Le système met à jour la base de données, décrémente le stock, et clôture la transaction générant l'historique de vente. Ce cas inclut directement la mise à jour conditionnelle des quantités.

## 2.6 Conclusion du chapitre
À l'issue de cette phase, nous avons formulé avec exactitude le comportement attendu de l'application pour qu'elle réponde parfaitement aux attentes de la pharmacie. L'étape suivante porte sur la conception technique de la solution.

<div style="page-break-after: always"></div>

# Chapitre 3 : Conception

## 3.1 Introduction
Après avoir ciblé ce que le système doit offrir, la phase de conception définit la manière dont nous allons concevoir la solution. Ce chapitre aborde l'architecture logicielle retenue et les modèles de données qui soutiendront l'application.

## 3.2 Architecture du système
Le système a été structuré en s'appuyant sur le framework web Django, qui utilise une architecture appelée **MVT (Model-View-Template)**.
* **Model (Modèle) :** Représente la structure des données. Les modèles interagissent directement avec la base de données MySQL via l'ORM (Object-Relational Mapping) de Django. Cela permet d'écrire des interactions complexes avec les données sans manipulation directe de syntaxe SQL classique.
* **View (Vue) :** Il s'agit du contrôleur principal de l'application. Les vues reçoivent les requêtes HTTP, interrogent les modèles pour obtenir les données nécessaires, appliquent la logique métier (par exemple, la vérification des permissions), et renvoient une réponse HTTP adaptée.
* **Template (Gabarit) :** Représente la couche d'affichage (HTML/CSS/JS). Les templates reçoivent les données calculées par les vues et les affichent à l'utilisateur final.

Cette séparation stricte rend le code maintenable et hautement modulaire.

## 3.3 Modélisation des données
La base de données relationnelle est un composant vital. Les entités principales de notre application sont :
* **Utilisateur (User) :** Le modèle utilisateur gérant l'authentification inclut un attribut de rôle permettant de distinguer avec précision l'Administrateur de l'Employé.
* **Médicament (Medication) :** Comporte des attributs métiers essentiels tels que le nom du produit, le prix unitaire, la quantité en stock, et la date limite de péremption, élément central pour le système d'alerte.
* **Vente (Sale) :** Relie un utilisateur et un médicament. Cette table sauvegarde la quantité vendue, la date exacte de la transaction et le montant calculé, garantissant l'historique de toutes les activités monétaires.

`[Insérer Diagramme de Classes ou MCD ici]`

## 3.4 Modélisation dynamique
Afin de bien comprendre les interactions synchrones réelles, nous présentons le séquencement pour la vente d'un produit.

**Processus de "Vente d'un médicament" :**
`[Insérer Diagramme de Séquence : Vente d'un médicament ici]`
1. L'Administrateur accède à l'interface de vente et envoie un ordre de transaction depuis le formulaire.
2. Le système (La Vue) relai depuis la base de données l'état ponctuel du médicament.
3. Le processus contrôle que la quantité en stock soit supérieure ou égale à la quantité requise.
4. Si cela est avéré, l'ORM exécute une fonction transactionnelle en base de données pour décrémenter le stock dans la table des médicaments, et enregistre son historique en tant que Vente validée.
5. Une fois terminé, le système clôt l'action par une notification visuelle adressée à l'Administrateur sur l'interface graphique.

## 3.5 Conclusion du chapitre
L'implémentation du standard MVT et la modélisation de nos données ont permis de poser d'excellentes fondations fonctionnelles aux logiques du système. Ces garanties techniques nous engagent à attaquer la phase d'implémentation pure abordée dans le dernier chapitre.

<div style="page-break-after: always"></div>

# Chapitre 4 : Réalisation (Implémentation)

## 4.1 Introduction
Ce dernier chapitre concrétise l'ensemble des études préparatoires documentées précédemment par du code. Nous allons y décrire les différents composants constituant le noyau de développement, ainsi que des captures réelles de l'application aboutie.

## 4.2 Environnement matériel et logiciel
Le projet exploite des outils reconnus de l'industrie technologique :
* **Langage de programmation principal :** Python, réputé pour sa flexibilité et la pureté de sa syntaxe.
* **Framework Backend :** Django. Il a grandement renforcé la sécurité locale et native des formulaires web développés, en optimisant les temps de production.
* **Serveur de Bases de données :** MySQL associé au connecteur Python `mysqlclient`.
* **Technologies Frontend :** Les interfaces répondent au HTML5 et ont été mis en page avec CSS3 pour utiliser et s'orienter vers Bootstrap afin d'offrir une grande clarté.
* **Outil de développement (IDE) :** Visual Studio Code.

## 4.3 Présentation des interfaces

Cette section décrit les visuels concrets de la proposition.

### 4.3.1 Interface d'Authentification (Login)
`[Insérer Capture d'écran : Page de Login]`
La porte d'accès au logiciel a été rendue volontairement minimaliste pour ne conserver que l'essentiel. L'accès refuse systématiquement les tentatives frauduleuses et affiche rapidement le statut des erreurs potentielles rencontrées.

### 4.3.2 Tableau de Bord (Dashboard Admin)
`[Insérer Capture d'écran : Dashboard Admin]`
Accessible exclusivement à partir des droits de l'Administrateur, cette section de supervision est le centre de pilotage. On y retrouve l'activité de l'application triée selon le chiffre des ventes et la centralisation critique des avertissements des médicaments péremptables.

### 4.3.3 Interface de Gestion des Médicaments (Liste)
`[Insérer Capture d'écran : Liste des Médicaments]`
Voici la partie dévolue à l'accomplissement des activités des préparateurs d'officine, listant dynamiquement le tableau total du grand inventaire.
* **Action Employé :** Outils simples pour rajouter et rafraichir un stock fraîchement réceptionné.
* **Action Administrateur :** Outil exclusif étendu qui ajoute l'icône supprimant intégralement un item de la base logicielle.
Pour ces deux profils, une déformation colorielle instantanée permet de détecter tout médicament dont la date de validité à été dépassée pour un signalement optimal.

### 4.3.4 Interface de Vente
`[Insérer Capture d'écran : Interface de Vente]`
Dédié au seul pôle Administratif de la pharmacie. Le tableau assure la validation instantanée de tout produit délivré. Sitôt l'entier validé, un événement retire la valeur numérique dans la pile de la base de données. 

## 4.4 Conclusion du chapitre
La réalisation complète du projet a abouti à un outil fonctionnel qui s’adosse très convenablement  aux requêtes exprimées dès sa phase préliminaire. L’usage de la combinaison Python Django et MySQL correspond totalement aux directives pour l'élaboration sécurisée d’un tel produit.

<div style="page-break-after: always"></div>

# Conclusion Générale et Perspectives

L'élaboration de ce Projet de Fin d'Année nous a permis de franchir avec succès toutes les étapes essentielles du cycle de vie logiciel pour déboucher sur une application web robuste et entièrement vouée à la numérisation des rouages d'une pharmacie.

En reprenant la problématique initiale, nous constatons que l'utilisation de méthodes traditionnelles laissait place à des marges d'erreur inacceptables en contexte médical. Notre solution est parvenue à répondre à ces défis cruciaux grâce à un contrôle automatisé et à un historique des stocks intègre. Grâce à l'architecture RBAC, nous avons solidement différencié l’administratif du logistique, assurant à la fois fluidité d'utilisation pour l'employé et sécurisation complète pour l'administrateur. Le suivi réactif et ciblé des dates de péremption concrétise l'aspect de santé publique en annulant virtuellement le risque de vente d'articles périmés.

Cette aventure technique a représenté une riche opportunité de mettre en œuvre techniquement les savoir-faire acquis à l'EMSI : la gestion d'un standard puissant tel que Django, la maîtrise de sa base MySQL au format interactif et la production d'interfaces d'usagers pensées en format Bootstrap.

Bien que l'application actuelle respecte le périmètre du cahier des charges avec stabilité et performance, notre produit reste parfaitement évolutif et ouvert à de nombreuses perspectives d'avenir :
* **Module d’intégration Fournisseur :** Permettant d'installer un principe d'alerte ou d'email automatisé vers divers laboratoires pharmaceutiques si des zones minimales de stock venaient à être franchies.
* **Création d'une API mobile :** Connecter la structure Backend à `Django REST Framework` serait un passage essentiel en prévision d'une numérisation des inventaires physiques grâce à une tablette, incluant le support Scanner-Code Barre en Wi-Fi.
* **Amélioration du système par un principe IA :** Découverte des corrélations des grandes dates de vente ou saisons de maux selon des calculs de pointe, favorisant la préparation et l'ajustement local du gérant en direct en prévente de saisons épidémiologiques.

Les travaux établis snt d'ores et déjà un fond de réalisation excellent qui permettra d’évoluer, fort de l'acquisition des expériences fondatrices de technicien ingénieur de demain en développement informatique.
