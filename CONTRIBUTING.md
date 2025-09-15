# Guide de Contribution - XTri PC Optimizer Suite

Merci de votre intérêt pour contribuer à XTri ! Ce guide vous aidera à comprendre comment participer au développement du projet.

## 🚀 Comment Contribuer

### 1. Fork et Clone

```bash
# Fork le repository sur GitHub, puis clonez votre fork
git clone https://github.com/Zxldrok/XTri.git
cd XTri

# Ajoutez le repository original comme remote
git remote add upstream https://github.com/Zxldrok/XTri.git
```

### 2. Configuration de l'Environnement

```bash
# Créez un environnement virtuel
python -m venv .venv

# Activez l'environnement
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Installez les dépendances
pip install -r requirements.txt
```

### 3. Développement

```bash
# Créez une nouvelle branche pour votre fonctionnalité
git checkout -b feature/nom-de-votre-fonctionnalite

# Effectuez vos modifications
# ...

# Testez votre code
python pc_optimizer_suite.py
```

### 4. Commit et Push

```bash
# Ajoutez vos fichiers
git add .

# Committez avec un message descriptif
git commit -m "feat: ajouter nouvelle fonctionnalité X"

# Poussez vers votre fork
git push origin feature/nom-de-votre-fonctionnalite
```

### 5. Pull Request

1. Allez sur GitHub et créez une Pull Request
2. Décrivez clairement vos changements
3. Référencez les issues liées si applicable

## 📋 Standards de Code

### Style de Code

- **PEP 8** : Suivez les conventions Python
- **Noms de variables** : Utilisez des noms descriptifs en français ou anglais
- **Commentaires** : Commentez le code complexe en français
- **Docstrings** : Documentez les fonctions importantes

### Structure des Commits

Utilisez le format de commit conventionnel :

```
type(scope): description

Corps du message (optionnel)

Footer (optionnel)
```

**Types de commits :**
- `feat`: nouvelle fonctionnalité
- `fix`: correction de bug
- `docs`: documentation
- `style`: formatage, pas de changement de code
- `refactor`: refactorisation du code
- `test`: ajout de tests
- `chore`: tâches de maintenance

**Exemples :**
```
feat(ui): ajouter onglet gestionnaire de services
fix(cleanup): corriger erreur lors du nettoyage des fichiers temp
docs(readme): mettre à jour les instructions d'installation
```

## 🧪 Tests

### Tests Manuels

1. Testez toutes les fonctionnalités modifiées
2. Vérifiez que l'interface reste responsive
3. Testez sur différentes versions de Windows si possible

### Tests Automatisés (À venir)

```bash
# Lancer les tests (quand disponibles)
pytest tests/
```

## 🐛 Signaler des Bugs

### Avant de Signaler

1. Vérifiez que le bug n'a pas déjà été signalé
2. Testez avec la dernière version
3. Reproduisez le bug de manière consistante

### Template de Bug Report

```markdown
**Description du Bug**
Description claire et concise du problème.

**Étapes pour Reproduire**
1. Allez à '...'
2. Cliquez sur '....'
3. Faites défiler jusqu'à '....'
4. Voir l'erreur

**Comportement Attendu**
Description de ce qui devrait se passer.

**Captures d'Écran**
Si applicable, ajoutez des captures d'écran.

**Environnement**
- OS: [ex. Windows 11]
- Version Python: [ex. 3.11.0]
- Version XTri: [ex. 1.0.0]
```

## 💡 Proposer des Fonctionnalités

### Template de Feature Request

```markdown
**Problème à Résoudre**
Description claire du problème que cette fonctionnalité résoudrait.

**Solution Proposée**
Description claire de ce que vous voulez qui se passe.

**Alternatives Considérées**
Description des solutions alternatives que vous avez considérées.

**Contexte Additionnel**
Ajoutez tout autre contexte ou captures d'écran sur la demande de fonctionnalité ici.
```

## 📁 Structure du Projet

```
XTri/
├── pc_optimizer_suite.py    # Application principale
├── file_organizer_gui.py    # Module d'organisation de fichiers
├── requirements.txt         # Dépendances Python
├── start.bat               # Script de lancement Windows
├── README.md               # Documentation principale
├── CONTRIBUTING.md         # Ce fichier
├── LICENSE                 # Licence MIT
├── .gitignore             # Fichiers à ignorer par Git
└── .venv/                 # Environnement virtuel (local)
```

## 🎯 Domaines de Contribution

### Priorités Actuelles

1. **Tests automatisés** - Ajouter une suite de tests
2. **Optimisation des performances** - Améliorer la vitesse
3. **Interface utilisateur** - Améliorer l'UX/UI
4. **Documentation** - Améliorer la documentation
5. **Nouvelles fonctionnalités** - Ajouter de nouveaux outils

### Idées de Fonctionnalités

- **Thèmes sombres/clairs** pour l'interface
- **Planification automatique** des tâches de maintenance
- **Rapports détaillés** en PDF/HTML
- **Support multilingue** (anglais, espagnol, etc.)
- **Mode portable** sans installation
- **Intégration cloud** pour les sauvegardes

## 🤝 Code de Conduite

### Notre Engagement

Nous nous engageons à faire de la participation à notre projet une expérience sans harcèlement pour tous, quel que soit l'âge, la taille corporelle, le handicap visible ou invisible, l'ethnicité, les caractéristiques sexuelles, l'identité et l'expression de genre, le niveau d'expérience, l'éducation, le statut socio-économique, la nationalité, l'apparence personnelle, la race, la religion ou l'identité et l'orientation sexuelles.

### Standards

**Comportements encouragés :**
- Utiliser un langage accueillant et inclusif
- Respecter les différents points de vue et expériences
- Accepter gracieusement les critiques constructives
- Se concentrer sur ce qui est le mieux pour la communauté
- Faire preuve d'empathie envers les autres membres de la communauté

**Comportements inacceptables :**
- Langage ou imagerie sexualisés et attention sexuelle non désirée
- Trolling, commentaires insultants/désobligeants, et attaques personnelles ou politiques
- Harcèlement public ou privé
- Publication d'informations privées d'autrui sans permission explicite
- Autres conduites qui pourraient raisonnablement être considérées comme inappropriées dans un cadre professionnel

## 📞 Contact

Si vous avez des questions sur ce guide de contribution :

- Ouvrez une issue sur GitHub
- Contactez les mainteneurs du projet

---

**Merci de contribuer à XTri ! 🚀**
