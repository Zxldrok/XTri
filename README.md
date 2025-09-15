# 🚀 Suite d'Optimisation PC - XTri

Une suite complète d'outils d'optimisation PC avec interface graphique moderne, incluant l'organisation de fichiers et de nombreux outils de maintenance système avancés.

## ✨ Fonctionnalités Principales

### 📁 Organisation de Fichiers
- **Interface graphique moderne** avec Tkinter
- **Organisation automatique** par type de fichier
- **Sélection interactive** des fichiers à organiser
- **Création automatique** des dossiers de destination
- **Gestion des conflits** de noms de fichiers
- **Barre de progression** en temps réel
- **Statistiques détaillées** après organisation
<img width="994" height="775" alt="image" src="https://github.com/user-attachments/assets/acda8514-fc18-4954-b4b1-43a8d40c18ab" />


### 🧹 Outils d'Optimisation PC

- **Nettoyage des fichiers temporaires** Windows
- **Gestion de la corbeille** (analyse et vidage)
- **Analyse de l'espace disque** avec détails par dossier
- **Nettoyage du cache navigateur** (Chrome, Firefox, Edge)
- **Recherche de fichiers doublons** avec hash MD5
- **Informations système complètes** (CPU, RAM, disques, réseau)

### 📊 Outils Avancés
- **Moniteur de performances** en temps réel (CPU, RAM, disque)
- **Gestionnaire de démarrage** Windows
- **Nettoyeur de registre** Windows avec sauvegarde
- **Gestionnaire de services** Windows
- **Analyseur de réseau** avec test de connectivité
- **Planificateur de tâches** pour automatiser la maintenance

## 📋 Types de fichiers supportés (Organisation)

- **Images** : .jpg, .jpeg, .png, .gif, .bmp, .svg, .webp, .tiff
- **Vidéos** : .mp4, .mkv, .avi, .mov, .wmv, .flv, .webm, .m4v
- **Documents** : .pdf, .docx, .doc, .txt, .pptx, .xlsx, .csv, .rtf, .odt
- **Musique** : .mp3, .wav, .flac, .aac, .ogg, .m4a, .wma
- **Archives** : .zip, .rar, .7z, .tar, .gz, .bz2, .xz
- **Autres** : Tous les autres types de fichiers

## 🛠️ Outils d'Optimisation Disponibles

### 🧹 Nettoyage Temporaire
- Fichiers temporaires Windows
- Cache utilisateur
- Fichiers de logs (optionnel)

### 🗑️ Gestion Corbeille
- Analyse du contenu
- Affichage des tailles et dates
- Vidage sécurisé

### 💾 Analyse Disque
- Utilisation de l'espace par disque
- Top 10 des dossiers les plus volumineux
- Statistiques détaillées

### 🌐 Cache Navigateur
- Support Chrome, Firefox, Edge
- Nettoyage sélectif par navigateur
- Calcul de l'espace libéré

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- Windows 10/11 (recommandé)

### Installation des dépendances

```bash
# Cloner le repository
git clone https://github.com/Zxldrok/XTri.git
cd XTri

# Créer un environnement virtuel
python -m venv .venv

# Activer l'environnement virtuel
# Sur Windows:
.venv\Scripts\activate
# Sur Linux/Mac:
source .venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

## 🎯 Utilisation

### Lancement de l'application

```bash
# Méthode 1: Script Python
python pc_optimizer_suite.py

# Méthode 2: Script batch (Windows)
start.bat
```

### Interface utilisateur

1. **Onglet Organisation** : Sélectionnez un dossier et organisez vos fichiers automatiquement
2. **Onglet Nettoyage** : Analysez et nettoyez les fichiers temporaires
3. **Onglet Corbeille** : Gérez le contenu de votre corbeille
4. **Onglet Disque** : Analysez l'utilisation de l'espace disque
5. **Onglet Navigateur** : Nettoyez le cache de vos navigateurs
6. **Onglet Doublons** : Trouvez et supprimez les fichiers en double
7. **Onglet Système** : Consultez les informations système
8. **Onglet Performances** : Surveillez les performances en temps réel
9. **Onglet Démarrage** : Gérez les programmes de démarrage
10. **Onglet Registre** : Nettoyez le registre Windows
11. **Onglet Services** : Gérez les services Windows
12. **Onglet Réseau** : Analysez votre connexion réseau
13. **Onglet Planificateur** : Automatisez vos tâches de maintenance

## 📦 Dépendances

- `tkinter` : Interface graphique (inclus avec Python)
- `psutil` : Informations système et processus
- `matplotlib` : Graphiques de performance
- `pathlib` : Manipulation des chemins de fichiers
- `hashlib` : Calcul des hash pour la détection de doublons

## 🛡️ Sécurité

- **Sauvegarde automatique** du registre avant nettoyage
- **Confirmation utilisateur** pour les opérations critiques
- **Mode simulation** pour prévisualiser les changements
- **Logs détaillés** de toutes les opérations

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Poussez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## ⚠️ Avertissement

Cet outil modifie des fichiers système et le registre Windows. Utilisez-le avec précaution et créez toujours des sauvegardes avant d'effectuer des opérations critiques.

## 📞 Support

Si vous rencontrez des problèmes ou avez des questions :
- Ouvrez une issue sur GitHub
- Consultez la documentation
- Vérifiez les logs d'erreur dans l'application

## 🔄 Changelog

### Version 1.0.0
- Interface graphique complète
- Organisation automatique des fichiers
- Outils de nettoyage système
- Moniteur de performances
- Gestionnaire de démarrage
- Nettoyeur de registre
- Gestionnaire de services
- Analyseur de réseau
- Planificateur de tâches

---

**Développé avec ❤️ pour optimiser votre PC Windows**

### 🔍 Recherche Doublons
- Détection par hash MD5
- Analyse récursive des dossiers
- Groupement des fichiers identiques

### ℹ️ Informations Système
- CPU (cœurs, utilisation)
- Mémoire RAM (totale, utilisée, disponible)
- Disques (espace, utilisation)
- Réseau (statistiques I/O)

## Prérequis

- Python 3.6 ou plus récent
- Tkinter (inclus par défaut avec Python)
- Modules standard : `os`, `shutil`, `pathlib`

## Installation

1. Clonez ou téléchargez le script `file_organizer.py`
2. Aucune installation de dépendances supplémentaires requise

## 🚀 Utilisation

### Lancement de la Suite Complète

1. Lancez la suite d'optimisation :
   ```bash
   python pc_optimizer_suite.py
   ```

2. **Naviguez entre les onglets** pour accéder aux différents outils

### 📁 Onglet Organisation de Fichiers

1. **Sélectionnez le dossier** à organiser
2. **Scannez** le dossier pour voir tous les fichiers
3. **Sélectionnez** les fichiers à organiser
4. **Organisez** les fichiers sélectionnés

### 🧹 Onglet Nettoyage Temporaire

1. **Sélectionnez** les types de fichiers à nettoyer
2. **Analysez** pour voir l'espace utilisé
3. **Nettoyez** les fichiers temporaires

### 🗑️ Onglet Corbeille

1. **Analysez** le contenu de la corbeille
2. **Consultez** la liste des fichiers
3. **Videz** la corbeille si nécessaire

### 💾 Onglet Analyse Disque

1. **Sélectionnez** le disque à analyser
2. **Lancez l'analyse** pour voir l'utilisation
3. **Consultez** les dossiers les plus volumineux

### 🌐 Onglet Cache Navigateur

1. **Sélectionnez** les navigateurs à nettoyer
2. **Choisissez** les types de données (cache, cookies, historique)
3. **Analysez** puis **nettoyez** si souhaité

### 🔍 Onglet Recherche Doublons

1. **Sélectionnez** le dossier à analyser
2. **Lancez la recherche** de doublons
3. **Consultez** les groupes de fichiers identiques

### ℹ️ Onglet Informations Système

1. **Consultez** les informations en temps réel
2. **Actualisez** pour mettre à jour les données

## 🔧 Fonctionnement

### Architecture de l'Application

L'application utilise une **interface à onglets** pour séparer les différents outils :

- **Threading** pour les opérations longues sans bloquer l'interface
- **Gestion d'erreurs** robuste pour chaque opération
- **Interface responsive** qui s'adapte à la taille de la fenêtre
- **Confirmations utilisateur** pour les opérations critiques

### Sécurité et Précautions

- **Confirmations** avant toute suppression
- **Sauvegarde automatique** des paramètres
- **Gestion des permissions** Windows
- **Vérification d'existence** des fichiers avant traitement
- **Messages d'avertissement** pour les opérations sensibles

## 📊 Exemples d'utilisation

### Organisation de Fichiers

Avant :
```
Téléchargements/
├── photo1.jpg
├── document.pdf
├── musique.mp3
└── video.mp4
```

Après :
```
Téléchargements/
├── Images/
│   └── photo1.jpg
├── Documents/
│   └── document.pdf
├── Musique/
│   └── musique.mp3
└── Vidéos/
    └── video.mp4
```

### Nettoyage Système

- **Fichiers temporaires** : Libération de 2.5 GB d'espace
- **Cache navigateur** : Suppression de 800 MB de cache Chrome
- **Corbeille** : Vidage de 1.2 GB de fichiers supprimés
- **Doublons** : Détection de 15 fichiers dupliqués (450 MB)

## ⚠️ Sécurité et Avertissements

### Organisation de Fichiers
- Le script **déplace** les fichiers (ne les copie pas)
- **Aucune suppression** n'est effectuée
- **Gestion des conflits** : renommage automatique si nécessaire

### Outils d'Optimisation
- **Confirmations obligatoires** avant suppression
- **Fermeture des navigateurs** requise avant nettoyage cache
- **Sauvegarde recommandée** avant nettoyage système
- **Permissions administrateur** parfois nécessaires
- **Test sur petit échantillon** recommandé avant usage intensif

### Précautions Importantes
- ⚠️ **Fermez tous les navigateurs** avant nettoyage cache
- ⚠️ **Sauvegardez vos données** importantes
- ⚠️ **Testez d'abord** sur un petit dossier
- ⚠️ **Vérifiez les permissions** si erreurs d'accès

## 🛠️ Personnalisation

### Catégories de Fichiers

Modifiez le dictionnaire `categories` dans `pc_optimizer_suite.py` :

```python
categories = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    'Documents': ['.pdf', '.docx', '.doc', '.txt'],
    'Musique': ['.mp3', '.wav', '.flac'],
    # Ajoutez vos propres catégories
    'MesVideos': ['.mp4', '.avi'],
    'MonTravail': ['.xlsx', '.pptx']
}
```

### Chemins de Cache Navigateur

Personnalisez les chemins dans `_get_browser_cache_paths()` pour d'autres navigateurs ou configurations spécifiques.

### Interface Utilisateur

- **Thèmes** : Modifiez `self.style.theme_use('clam')`
- **Couleurs** : Personnalisez les couleurs dans les styles TTK
- **Taille fenêtre** : Ajustez `self.root.geometry("1000x750")`

## 🐛 Dépannage

### Problèmes courants

1. **Erreur de permissions** :
   - Lancez en tant qu'administrateur
   - Vérifiez les droits d'accès aux dossiers système

2. **Module psutil non trouvé** :
   ```bash
   pip install psutil
   ```

3. **Erreur de nettoyage navigateur** :
   - Fermez complètement tous les navigateurs
   - Vérifiez les permissions sur les dossiers AppData

4. **Interface qui ne répond pas** :
   - Les opérations longues utilisent des threads
   - Patientez pendant les analyses de disque

5. **Erreur d'accès corbeille** :
   - Nécessite des permissions administrateur
   - Utilisez PowerShell en tant qu'administrateur

### Installation des Dépendances

```bash
pip install -r requirements.txt
```

### Support

En cas de problème :
- Vérifiez les permissions système
- Consultez les logs d'erreur dans l'interface
- Testez d'abord sur de petits échantillons
- Sauvegardez vos données importantes

## Licence

Ce script est fourni tel quel, sans garantie. Utilisez-le à vos propres risques.

## Auteur

Script créé par Zx.
