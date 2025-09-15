# Changelog

Tous les changements notables de ce projet seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Non publié]

### Ajouté
- Documentation complète pour GitHub
- Fichier de contribution (CONTRIBUTING.md)
- Licence MIT
- Fichier requirements.txt complet

## [1.0.0] - 2024-12-19

### Ajouté
- **Interface graphique complète** avec Tkinter
- **Organisation automatique des fichiers** par type
- **Nettoyage des fichiers temporaires** Windows
- **Gestion de la corbeille** (analyse et vidage)
- **Analyse de l'espace disque** avec détails par dossier
- **Nettoyage du cache navigateur** (Chrome, Firefox, Edge)
- **Recherche de fichiers doublons** avec hash MD5
- **Informations système complètes** (CPU, RAM, disques, réseau)
- **Moniteur de performances** en temps réel
- **Gestionnaire de démarrage** Windows
- **Nettoyeur de registre** Windows avec sauvegarde automatique
- **Gestionnaire de services** Windows
- **Analyseur de réseau** avec test de connectivité et vitesse
- **Planificateur de tâches** pour automatiser la maintenance

### Fonctionnalités Détaillées

#### Organisation de Fichiers
- Sélection interactive des fichiers à organiser
- Création automatique des dossiers de destination
- Gestion des conflits de noms de fichiers
- Barre de progression en temps réel
- Statistiques détaillées après organisation
- Support de 50+ types de fichiers

#### Outils de Nettoyage
- Nettoyage sélectif des fichiers temporaires
- Analyse avant suppression
- Calcul de l'espace libéré
- Logs détaillés des opérations

#### Moniteur de Performances
- Graphiques en temps réel (CPU, RAM, disque)
- Historique des performances
- Alertes de performance
- Export des données

#### Gestionnaire de Démarrage
- Liste des programmes de démarrage
- Activation/désactivation des programmes
- Informations détaillées sur chaque programme
- Impact sur le temps de démarrage

#### Nettoyeur de Registre
- Scan complet du registre Windows
- Sauvegarde automatique avant nettoyage
- Catégorisation des erreurs trouvées
- Restauration des sauvegardes

#### Gestionnaire de Services
- Liste complète des services Windows
- Filtrage par statut et type
- Démarrage/arrêt/redémarrage des services
- Informations détaillées sur chaque service

#### Analyseur de Réseau
- Test de connectivité (ping)
- Test de vitesse de connexion
- Informations sur les connexions actives
- Monitoring du trafic réseau

#### Planificateur de Tâches
- Planification de tâches de maintenance
- Tâches prédéfinies (nettoyage, scan, etc.)
- Exécution automatique
- Logs d'exécution

### Sécurité
- Confirmation utilisateur pour les opérations critiques
- Sauvegardes automatiques avant modifications
- Mode simulation pour prévisualiser les changements
- Logs détaillés de toutes les opérations
- Validation des entrées utilisateur

### Interface Utilisateur
- Interface moderne avec onglets
- Barres de progression pour les opérations longues
- Messages d'information et d'erreur clairs
- Tooltips explicatifs
- Responsive design

### Performance
- Opérations multi-threadées pour éviter le gel de l'interface
- Optimisation mémoire pour les gros volumes de données
- Cache intelligent pour les opérations répétitives
- Traitement par lots pour les fichiers multiples

## [0.1.0] - 2024-12-01

### Ajouté
- Version initiale avec organisation de fichiers de base
- Interface graphique simple
- Support des types de fichiers courants

---

## Types de Changements

- **Ajouté** pour les nouvelles fonctionnalités
- **Modifié** pour les changements dans les fonctionnalités existantes
- **Déprécié** pour les fonctionnalités qui seront supprimées dans les versions à venir
- **Supprimé** pour les fonctionnalités supprimées dans cette version
- **Corrigé** pour les corrections de bugs
- **Sécurité** en cas de vulnérabilités