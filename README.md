# 🧠 CSS Error Detector

Une application **Python/Tkinter** qui scanne les fichiers **CSS** d'un projet pour détecter automatiquement des erreurs courantes et problématiques.

## 🎯 Objectif

Cet outil détecte les erreurs CSS fréquentes qui peuvent casser le rendu ou poser des problèmes de maintenance :
- ✅ Commentaires CSS non fermés (`/* ... `)
- ✅ Propriétés `content:` mal formatées 
- ✅ Fonctions `url()` incomplètes
- ✅ Autres motifs suspects configurables

## 🚀 Fonctionnalités

- 📂 **Sélection de dossier** - Choisir facilement votre projet
- 🔍 **Scan automatique** - Analyse récursive de tous les fichiers `.css`
- ⚠️ **Détection d'erreurs** - Motifs regex précompilés pour de meilleures performances
- 📋 **Export facile** - Clic droit pour copier chemin + ligne d'erreur
- 🚫 **Dossiers ignorés** - Exclut automatiquement `node_modules`, `.git`, etc.
- 📊 **Interface claire** - TableView avec colonnes triées

## 🛠️ Installation

### Prérequis
- Python 3.6+
- Tkinter (inclus par défaut avec Python)

### Installation
```bash
git clone https://github.com/votre-username/css-error-detector.git
cd css-error-detector
```

Aucune dépendance externe requise ! Le script utilise uniquement les modules Python standard.

## ▶️ Utilisation

```bash
python css_checker.py
```

### Mode d'emploi
1. **📁 Choisir un dossier** - Sélectionnez la racine de votre projet
2. **📂 Scanner le dossier** - Lancez l'analyse
3. **Consulter les résultats** - Tableau avec fichier/ligne/erreur
4. **Copier les erreurs** - Clic droit → "Copier chemin complet"

## 🔍 Types d'erreurs détectées

| Motif | Description |
|-------|-------------|
| `/*[^*]*$` | Commentaire CSS non fermé |
| `content:\s*/` | Propriété content avec `/` sans guillemets |
| `content:\s*[^\";\']+$` | content sans guillemets appropriés |
| `url\([^\'\")]*$` | Fonction url() incomplète |
| `^/\*.*$` | Début de commentaire potentiellement problématique |

## 📁 Structure du projet

```
css-error-detector/
├── css_checker.py      # Application principale
├── README.md          # Cette documentation
└── .gitignore         # Fichiers à ignorer
```

## 🎨 Aperçu de l'interface

L'application affiche :
- **Table des erreurs** avec colonnes Fichier/Ligne/Erreur
- **Barre de statut** indiquant le nombre de fichiers scannés
- **Boutons d'action** pour naviguer et scanner
- **Menu contextuel** pour copier rapidement les chemins

## ⚙️ Personnalisation

### Ajouter des motifs d'erreur

Modifiez la liste `SUSPICIOUS_PATTERNS` dans le code :

```python
SUSPICIOUS_PATTERNS = [
    (re.compile(r'votre-regex'), "Description de l'erreur"),
    # ... autres motifs
]
```

### Modifier les dossiers ignorés

Ajustez la variable `IGNORED_DIRS` :

```python
IGNORED_DIRS = {"node_modules", "build", ".git", "__pycache__", "dist"}
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. **Fork** le projet
2. **Créer** une branche feature (`git checkout -b feature/nouvelle-detection`)
3. **Commit** vos changements (`git commit -m 'Ajout détection erreur X'`)
4. **Push** sur la branche (`git push origin feature/nouvelle-detection`)
5. **Ouvrir** une Pull Request

### Idées d'améliorations
- 🔄 Export des résultats (JSON/CSV)
- 🎯 Détection de motifs CSS spécifiques à des frameworks
- 📈 Statistiques détaillées par type d'erreur
- 🔧 Interface de configuration des règles
- 📝 Suggestions de correction automatique

## 🐛 Limitations connues

- **Faux positifs possibles** sur du CSS très spécialisé ou commenté
- **Pas de correction automatique** - outil de détection uniquement  
- **Regex basiques** - ne comprend pas la syntaxe CSS complexe
- **Encodage** - gestion UTF-8 par défaut avec fallback

## 📜 Licence

Ce projet est sous licence **MIT**. Voir le fichier `LICENSE` pour plus de détails.

## 🔗 Liens utiles

- [Documentation CSS - MDN](https://developer.mozilla.org/fr/docs/Web/CSS)
- [Validation CSS W3C](https://jigsaw.w3.org/css-validator/)
- [Python Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)

---

> 💡 **Astuce** : Utilisez cet outil dans votre workflow CI/CD pour détecter automatiquement les erreurs CSS avant déploiement !
