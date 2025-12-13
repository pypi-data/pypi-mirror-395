# pyfastcli

CLI pour générer des fichiers Python, routes Django Ninja, packages Python et domaines Django de manière interactive.

## Description

`pyfastcli` est un outil en ligne de commande qui facilite la génération de code Python. Il propose plusieurs commandes pour générer :
- Des routes Django Ninja
- Des packages Python complets
- Des domaines Django (structure classique)
- Des domaines Django avec architecture DDD (Domain-Driven Design)

Il pose des questions interactives et génère automatiquement tous les fichiers nécessaires avec du code initialisé.

## Configuration de l'environnement virtuel

Avant d'installer `pyfastcli`, il est recommandé de créer et d'activer un environnement virtuel Python pour isoler les dépendances du projet.

### Création avec venv (méthode standard)

```bash
# Créer un environnement virtuel
python -m venv .venv

# Activer l'environnement virtuel
# Sur Linux/Mac :
source .venv/bin/activate

# Sur Windows :
# .venv\Scripts\activate
```

### Création avec uv (recommandé)

```bash
# Créer un environnement virtuel
uv venv

# Activer l'environnement virtuel
# Sur Linux/Mac :
source .venv/bin/activate

# Sur Windows :
# .venv\Scripts\activate
```

### Vérification

Une fois l'environnement activé, vous devriez voir `(.venv)` au début de votre ligne de commande :

```bash
(.venv) user@machine:~/projet$
```

### Désactivation

Pour désactiver l'environnement virtuel :

```bash
deactivate
```

##  Installation

### Dépendances

**Pour utiliser pyfastcli :**
- `click>=8.0.0` (installé automatiquement)

**Pour utiliser le code généré :**
- **`make:url`** : Nécessite `django-ninja` dans votre projet Django
- **`make:domaine`** : Nécessite `django` dans votre projet Django
- **`make:domaine-ddd`** : Nécessite `django` dans votre projet Django
  - Si vous utilisez les serializers : Nécessite aussi `djangorestframework`
- **`make:model`** : Nécessite `django` dans votre projet Django

> **Note importante** : Le générateur lui-même n'a pas besoin de Django ou DRF pour fonctionner. Ces dépendances sont nécessaires uniquement pour **utiliser** le code généré dans votre projet Django.

### Installation avec dépendances optionnelles

Si vous voulez installer pyfastcli avec les dépendances nécessaires pour tester/utiliser le code généré :

```bash
# Installation avec Django uniquement
pip install "pyfastcli[django]"

# Installation avec Django Ninja
pip install "pyfastcli[django-ninja]"

# Installation avec Django REST Framework
pip install "pyfastcli[django-drf]"

# Installation avec toutes les dépendances Django
pip install "pyfastcli[django-all]"

# Installation avec dépendances de développement
pip install "pyfastcli[dev]"

# Installation complète (dev + django-all)
pip install "pyfastcli[dev,django-all]"
```

**Avec uv :**
```bash
# Installation avec toutes les dépendances Django
uv pip install "pyfastcli[django-all]"
```

### Installation depuis le code source

#### Avec uv (recommandé)

```bash
# Cloner le dépôt
git clone https://github.com/hedi/pyfastcli.git
cd pyfastcli

# Créer un environnement virtuel (si pas déjà fait)
uv venv

# Activer l'environnement virtuel
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

# Synchroniser toutes les dépendances (y compris dev)
uv sync

# Ou installer en mode développement avec uv pip
uv pip install -e ".[dev]"
```

**⚠️ Important avec uv :**
-  **Ne pas utiliser** : `uv run pip install` (cela provoque une erreur "externally-managed-environment")
-  **Utiliser** : `uv sync` ou `uv pip install` directement

#### Avec pip standard

```bash
# Créer un environnement virtuel
python -m venv .venv

# Activer l'environnement
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

# Installer en mode développement
pip install -e .

# Ou installer avec les dépendances de développement
pip install -e ".[dev]"
```

### Installation depuis PyPI (quand disponible)

```bash
pip install pyfastcli
```

## Utilisation

`pyfastcli` propose plusieurs commandes pour différents cas d'usage :

### Vue d'ensemble des commandes

| Commande | Description | Cas d'usage |
|----------|-------------|-------------|
| `make:url` | Génère une route Django Ninja | API REST avec Django Ninja |
| `make:package` | Génère un package Python complet | Création de bibliothèques Python |
| `make:domaine` | Génère un domaine Django classique | Applications Django traditionnelles |
| `make:domaine-ddd` | Génère un domaine Django DDD | Applications Django avec architecture DDD |
| `make:model` | Génère un modèle Django interactivement | Création de modèles avec champs personnalisés |

### Commandes disponibles

- **`make:url`** - Génère une route Django Ninja
- **`make:package`** - Génère une structure complète de package Python
- **`make:domaine`** - Génère une structure de domaine Django classique
- **`make:domaine-ddd`** - Génère une structure de domaine Django avec architecture DDD
- **`make:model`** - Génère un modèle Django avec champs interactifs

---

## 1. make:url - Génération de routes Django Ninja

Génère un fichier Python contenant une route Django Ninja.

### Génération interactive

```bash
pyfastcli make:url
```

Le CLI vous posera des questions sur :
- Le nom du module/app
- Le nom de la fonction
- Le chemin d'URL
- La méthode HTTP (get, post, put, delete, etc.)
- Le tag Ninja
- Le dossier de sortie
- La description de l'endpoint (optionnel)

### Génération avec options

```bash
pyfastcli make:url \
  --function-name get_orders \
  --url-path /orders \
  --http-method get \
  --tag Orders \
  --output-dir app/api/routes \
  --description "Récupère la liste des commandes"
```

### Options disponibles

| Option | Raccourci | Description | Défaut |
|--------|-----------|-------------|--------|
| `--module-name` | `-m` | Nom du module/app | `api` |
| `--function-name` | `-f` | Nom de la fonction | `hello` |
| `--url-path` | `-u` | Chemin d'URL | `/hello` |
| `--http-method` | `-M` | Méthode HTTP | `get` |
| `--tag` | `-t` | Tag Ninja | `Default` |
| `--output-dir` | `-o` | Dossier de sortie | `app/api/routes` |
| `--description` | `-d` | Description de l'endpoint | Optionnel |

### Exemple de fichier généré

Pour la commande `pyfastcli make:url --function-name get_orders --url-path /orders --http-method get --tag Orders`, le fichier `get_orders.py` sera créé :

```python
from ninja import Router

router = Router(tags=["Orders"])


@router.get("/orders")
def get_orders(request):
    """
    Endpoint get_orders
    """
    return {"message": "Hello from get_orders!"}
```

### Intégration dans votre projet Django

Après la génération, n'oubliez pas d'inclure le router dans votre fichier `urls.py` :

```python
from django.urls import path
from ninja import NinjaAPI
from app.api.routes.get_orders import router as orders_router

api = NinjaAPI()

api.add_router(orders_router, prefix="/api")

urlpatterns = [
    path("api/", api.urls),
]
```

---

## 2. make:package - Génération de package Python

Génère une structure complète de package Python selon les best practices modernes.

### Génération interactive

```bash
pyfastcli make:package
```

### Génération avec options

```bash
pyfastcli make:package \
  --project-name my-awesome-package \
  --package-name my_awesome_package \
  --version 0.1.0 \
  --description "Un package Python génial" \
  --author-name "Votre Nom" \
  --author-email "votre@email.com" \
  --python-version 3.8 \
  --license MIT \
  --output-dir .
```

### Structure générée

```
my-awesome-package/
├── pyproject.toml          # Configuration moderne du package
├── README.md               # Documentation
├── LICENSE                 # Licence (MIT, Apache-2.0, etc.)
├── .gitignore             # Fichiers à ignorer
├── MANIFEST.in            # Fichiers à inclure dans la distribution
├── Makefile               # Commandes utiles (optionnel)
├── my_awesome_package/    # Code source
│   └── __init__.py
└── tests/                 # Tests
    ├── __init__.py
    └── test_my_awesome_package.py
```

### Options principales

| Option | Raccourci | Description | Défaut |
|--------|-----------|-------------|--------|
| `--project-name` | `-p` | Nom du projet (avec tirets) | Requis |
| `--package-name` | `-n` | Nom du package Python | Auto |
| `--version` | `-v` | Version initiale | `0.1.0` |
| `--description` | `-d` | Description | Requis |
| `--author-name` | `-a` | Nom de l'auteur | Requis |
| `--author-email` | `-e` | Email de l'auteur | Requis |
| `--python-version` | | Version Python minimale | `3.8` |
| `--license` | `-l` | Type de licence | `MIT` |
| `--output-dir` | `-o` | Dossier de sortie | `.` |
| `--include-makefile/--no-makefile` | | Inclure Makefile | `True` |
| `--include-manifest/--no-manifest` | | Inclure MANIFEST.in | `True` |

---

## 3. make:domaine - Génération de domaine Django classique

Génère une structure complète de domaine Django avec tous les fichiers nécessaires.

### Génération interactive

```bash
pyfastcli make:domaine
```

### Génération avec options

```bash
pyfastcli make:domaine \
  --app-name pratique \
  --model-name Pratique \
  --output-dir .
```

### Structure générée

```
pratique/
├── __init__.py
├── apps.py
├── admin.py
├── models.py              # Modèles Pratique, SessionPratique
├── views.py               # Vues génériques Django
├── urls.py                # Routes de l'app
├── forms.py               # Formulaires
├── services.py            # Logique métier (optionnel)
├── selectors.py           # Requêtes complexes (optionnel)
└── templates/
    └── pratique/
        ├── liste.html
        ├── detail.html
        └── formulaire.html
```

### Options principales

| Option | Raccourci | Description | Défaut |
|--------|-----------|-------------|--------|
| `--app-name` | `-a` | Nom de l'app Django | Requis |
| `--model-name` | `-m` | Nom du modèle principal | Auto |
| `--output-dir` | `-o` | Dossier de sortie | `.` |
| `--include-services/--no-services` | | Inclure services.py | `True` |
| `--include-selectors/--no-selectors` | | Inclure selectors.py | `True` |
| `--description` | `-d` | Description du domaine | Optionnel |

### Prochaines étapes après génération

1. Ajoutez `'pratique'` à `INSTALLED_APPS` dans `settings.py`
2. Incluez les URLs dans votre `urls.py` principal :
   ```python
   from django.urls import include, path
   path('pratique/', include('pratique.urls')),
   ```
3. Exécutez les migrations :
   ```bash
   python manage.py makemigrations pratique
   python manage.py migrate
   ```

---

## 4. make:domaine-ddd - Génération de domaine Django avec architecture DDD

Génère une structure de domaine Django organisée selon les principes DDD (Domain-Driven Design) light.

### Génération interactive

```bash
pyfastcli make:domaine-ddd
```

### Génération avec options

```bash
pyfastcli make:domaine-ddd \
  --app-name pratique \
  --model-name Pratique \
  --output-dir . \
  --include-serializers
```

### Structure générée

```
pratique/
├── __init__.py
├── apps.py
├── admin.py
├── domain/                      # Couche domaine
│   ├── models.py               # Entités métier avec logique métier pure
│   ├── services.py             # Règles métier complexes
│   └── value_objects.py        # Objets de valeur immutables
├── infrastructure/             # Couche infrastructure
│   └── repositories.py         # Accès DB, querysets personnalisés
├── presentation/               # Couche présentation
│   ├── views.py               # Django views (utilisent services et repositories)
│   ├── forms.py              # Formulaires
│   ├── serializers.py        # DRF serializers (optionnel)
│   └── urls.py               # Routes
├── templates/
│   └── pratique/
│       ├── liste.html
│       ├── detail.html
│       └── formulaire.html
└── tests/
    ├── test_models.py
    ├── test_services.py
    └── test_views.py
```

### Avantages de l'architecture DDD

- **Séparation des responsabilités** : Domain, Infrastructure, Presentation
- **Logique métier isolée** : Les règles métier sont dans le domaine
- **Testabilité** : Chaque couche peut être testée indépendamment
- **Maintenabilité** : Code organisé et facile à comprendre
- **Évolutivité** : Facile d'ajouter de nouvelles fonctionnalités

### Options principales

| Option | Raccourci | Description | Défaut |
|--------|-----------|-------------|--------|
| `--app-name` | `-a` | Nom de l'app Django | Requis |
| `--model-name` | `-m` | Nom du modèle principal | Auto |
| `--output-dir` | `-o` | Dossier de sortie | `.` |
| `--include-serializers/--no-serializers` | | Inclure serializers.py pour DRF | `True` |
| `--description` | `-d` | Description du domaine | Optionnel |

### Prochaines étapes après génération

1. Ajoutez `'pratique'` à `INSTALLED_APPS` dans `settings.py`
2. Incluez les URLs dans votre `urls.py` principal :
   ```python
   from django.urls import include, path
   path('pratique/', include('pratique.presentation.urls')),
   ```
3. Exécutez les migrations :
   ```bash
   python manage.py makemigrations pratique
   python manage.py migrate
   ```
4. Si vous utilisez les serializers, assurez-vous d'avoir `'rest_framework'` dans `INSTALLED_APPS`

## 🔧 Dépannage : Erreur "externally-managed-environment"

### Pourquoi cette erreur se produit ?

Si vous obtenez l'erreur `externally-managed-environment` avec `uv run pip install`, c'est parce que :

1. **`uv run pip install` n'est pas la bonne commande** : `uv run` exécute une commande dans l'environnement virtuel, mais `pip` essaie d'installer dans l'environnement système Python (protégé par PEP 668).

2. **Solution avec uv** : Utilisez directement les commandes `uv` :
   ```bash
   # CORRECT - Synchroniser depuis pyproject.toml
   uv sync
   
   # CORRECT - Installer avec uv pip (sans "run")
   uv pip install -e ".[dev]"
   
   # INCORRECT - Ne pas utiliser cette commande
   uv run pip install ...
   ```

3. **Alternative** : Si vous voulez utiliser `pip` directement, activez d'abord l'environnement virtuel :
   ```bash
   # Activer l'environnement virtuel
   source .venv/bin/activate  # Linux/Mac
   # .venv\Scripts\activate  # Windows
   
   # Puis utiliser pip normalement
   pip install -e ".[dev]"
   ```

## 🔧 Dépannage : Erreur "ModuleNotFoundError: No module named 'pyfastcli.commands'"

### Pourquoi cette erreur se produit ?

Si vous obtenez l'erreur `ModuleNotFoundError: No module named 'pyfastcli.commands'` lors de l'exécution de `pyfastcli make:url` ou d'autres commandes, cela signifie que le package a été installé depuis PyPI avec une version incomplète, ou que les modules n'ont pas été correctement inclus lors de l'installation.

### Solution

**Réinstaller le package depuis le code source local :**

```bash
# Désinstaller la version actuelle
pip uninstall pyfastcli -y

# Réinstaller depuis le répertoire local en mode développement (recommandé)
pip install -e /chemin/vers/py-cli-maker

# Ou installer depuis le répertoire local (installation normale)
pip install /chemin/vers/py-cli-maker
```

**Exemple concret :**

```bash
# Si le projet est dans /home/hedi/projects/Python-TP/py-cli-maker
cd /home/hedi/projects/test2
source .venv/bin/activate
pip uninstall pyfastcli -y
pip install -e /home/hedi/projects/Python-TP/py-cli-maker
```

**Vérification :**

Après la réinstallation, vérifiez que le module `commands` est présent :

```bash
# Vérifier le contenu du package installé
ls -la .venv/lib/python3.12/site-packages/pyfastcli/

# Vous devriez voir les dossiers : commands/, generators/, __init__.py, cli.py
```

**Note :** L'option `-e` (editable) permet de tester les modifications du code source sans réinstaller à chaque fois. C'est particulièrement utile pour le développement.

##  Outils de qualité de code pour développeurs

Ce projet utilise plusieurs outils pour maintenir un code de qualité. Voici comment les utiliser :

### Installation des outils

#### Avec uv (recommandé)

```bash
# Synchroniser toutes les dépendances de développement depuis pyproject.toml
uv sync

# Ou installer en mode développement
uv pip install -e ".[dev]"

# Ou utiliser les dependency-groups de uv
uv sync --group dev
```

#### Avec pip standard

```bash
# Installer tous les outils de développement
pip install -e ".[dev]"

# Ou installer individuellement
pip install black ruff mypy pytest pytest-cov ipdb
```

** Erreur courante avec uv :**
Si vous obtenez l'erreur `externally-managed-environment` :
-  **Ne pas utiliser** : `uv run pip install ...`
-  **Utiliser** : `uv sync` ou `uv pip install ...` directement

### 1. Black - Formatage automatique

**Black** formate automatiquement votre code selon le style PEP 8.

#### Utilisation

**Avec uv :**
```bash
# Vérifier ce qui sera changé (sans modifier)
uv run black --check pyfastcli/

# Formater tous les fichiers Python
uv run black pyfastcli/ tests/

# Formater un fichier spécifique
uv run black pyfastcli/cli.py
```

**Avec pip standard :**
```bash
# Vérifier ce qui sera changé (sans modifier)
black --check pyfastcli/

# Formater tous les fichiers Python
black pyfastcli/ tests/

# Formater un fichier spécifique
black pyfastcli/cli.py
```

#### Configuration

La configuration de Black est dans `pyproject.toml` :

```toml
[tool.black]
line-length = 88
target-version = ['py38', 'py39', 'py310', 'py311', 'py312']
include = '\.pyi?$'
```

#### Intégration dans l'éditeur

Pour un formatage automatique à la sauvegarde, configurez votre éditeur (VS Code, PyCharm, etc.) pour utiliser Black.

### 2. Ruff - Linting ultra-rapide

**Ruff** est un linter ultra-rapide qui remplace Flake8, isort et d'autres outils.

#### Utilisation

**Avec uv :**
```bash
# Vérifier les erreurs
uv run ruff check pyfastcli/ tests/

# Corriger automatiquement ce qui peut l'être
uv run ruff check --fix pyfastcli/ tests/

# Vérifier un fichier spécifique
uv run ruff check pyfastcli/cli.py

# Formater les imports (remplace isort)
uv run ruff format pyfastcli/
```

**Avec pip standard :**
```bash
# Vérifier les erreurs
ruff check pyfastcli/ tests/

# Corriger automatiquement ce qui peut l'être
ruff check --fix pyfastcli/ tests/

# Vérifier un fichier spécifique
ruff check pyfastcli/cli.py

# Formater les imports (remplace isort)
ruff format pyfastcli/
```

#### Configuration

La configuration de Ruff est dans `pyproject.toml` :

```toml
[tool.ruff]
line-length = 88
target-version = "py38"
select = ["E", "F", "I", "N", "W", "UP"]
ignore = []
```

#### Codes d'erreur

Consultez la [documentation des règles Ruff](https://docs.astral.sh/ruff/rules/) pour comprendre les codes d'erreur.

### 3. Mypy - Vérification de types statique

**Mypy** vérifie que vous utilisez correctement les annotations de types.

#### Utilisation

**Avec uv :**
```bash
# Vérifier les types dans tout le projet
uv run mypy pyfastcli/

# Vérifier un fichier spécifique
uv run mypy pyfastcli/cli.py

# Mode strict (recommandé pour les nouveaux projets)
uv run mypy --strict pyfastcli/
```

**Avec pip standard :**
```bash
# Vérifier les types dans tout le projet
mypy pyfastcli/

# Vérifier un fichier spécifique
mypy pyfastcli/cli.py

# Mode strict (recommandé pour les nouveaux projets)
mypy --strict pyfastcli/
```

#### Configuration

La configuration de Mypy est dans `pyproject.toml` :

```toml
[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
```

#### Exemple d'annotation de types

```python
def generate_ninja_route_file(
    module_name: str,
    function_name: str,
    url_path: str,
    http_method: str,
    tag: str,
    output_dir: str,
    description: str | None = None,
) -> str:
    """Génère un fichier Python contenant une route Django Ninja."""
    # ...
```

### 4. Pytest - Framework de tests

**Pytest** est utilisé pour exécuter les tests automatisés.

#### Utilisation

**Avec uv :**
```bash
# Exécuter tous les tests
uv run pytest

# Mode verbose (affiche plus de détails)
uv run pytest -v

# Mode très verbose
uv run pytest -vv

# Exécuter un fichier de test spécifique
uv run pytest tests/test_ninja_routes.py

# Exécuter une classe de test spécifique
uv run pytest tests/test_ninja_routes.py::TestSanitizeFuncName

# Exécuter un test spécifique
uv run pytest tests/test_ninja_routes.py::TestSanitizeFuncName::test_simple_name

# Exécuter avec couverture de code
uv run pytest --cov=pyfastcli --cov-report=term-missing

# Générer un rapport HTML de couverture
uv run pytest --cov=pyfastcli --cov-report=html
# Ouvrir htmlcov/index.html dans votre navigateur
```

**Avec pip standard :**
```bash
# Exécuter tous les tests
pytest

# Mode verbose (affiche plus de détails)
pytest -v

# Mode très verbose
pytest -vv

# Exécuter un fichier de test spécifique
pytest tests/test_ninja_routes.py

# Exécuter une classe de test spécifique
pytest tests/test_ninja_routes.py::TestSanitizeFuncName

# Exécuter un test spécifique
pytest tests/test_ninja_routes.py::TestSanitizeFuncName::test_simple_name

# Exécuter avec couverture de code
pytest --cov=pyfastcli --cov-report=term-missing

# Générer un rapport HTML de couverture
pytest --cov=pyfastcli --cov-report=html
# Ouvrir htmlcov/index.html dans votre navigateur
```

#### Structure des tests

Les tests sont organisés dans le dossier `tests/` :

```
tests/
├── __init__.py
├── test_ninja_routes.py  # Tests pour le générateur
└── test_cli.py           # Tests pour l'interface CLI
```

#### Exemple de test

```python
def test_sanitize_func_name():
    """Test avec un nom simple."""
    assert _sanitize_func_name("get_orders") == "get_orders"
    assert _sanitize_func_name("get orders") == "get_orders"
```

### 5. ipdb - Débogueur interactif

**ipdb** est un débogueur interactif amélioré pour Python.

#### Configuration

```bash
# Configurer ipdb comme débogueur par défaut
export PYTHONBREAKPOINT=ipdb.set_trace

# Ou dans votre shell (bash/zsh)
echo 'export PYTHONBREAKPOINT=ipdb.set_trace' >> ~/.bashrc
```

#### Utilisation dans le code

```python
def generate_ninja_route_file(...):
    # Votre code
    breakpoint()  # Le débogueur s'arrête ici
    # Suite du code
```

#### Commandes principales

Une fois dans le débogueur :

| Commande | Description |
|----------|-------------|
| `n` (next) | Exécute la ligne suivante |
| `s` (step) | Entre dans une fonction |
| `c` (continue) | Continue jusqu'au prochain point d'arrêt |
| `l` (list) | Affiche le code autour de la ligne actuelle |
| `p variable` | Affiche la valeur d'une variable |
| `pp variable` | Affiche joliment la valeur d'une variable |
| `u` (up) | Remonte dans la pile d'appels |
| `d` (down) | Descend dans la pile d'appels |
| `q` (quit) | Quitte le débogueur |

#### Exemple d'utilisation

```python
def test_function():
    a = 10
    b = 5
    breakpoint()  # Arrêt ici
    result = a + b
    return result
```

Exécutez avec : `python -m pytest tests/test_file.py::test_function`

#### Analyse post-mortem

Pour inspecter l'état du programme après une erreur :

```python
def test_with_error():
    try:
        result = division(10, 0)
    except Exception as e:
        import ipdb; ipdb.post_mortem()
        raise
```

##  Workflow de développement recommandé

### Avec uv

1. **Installer les dépendances**
   ```bash
   uv sync
   ```

2. **Écrire le code**
   ```bash
   # Créer/modifier vos fichiers
   ```

3. **Formater avec Black**
   ```bash
   uv run black pyfastcli/ tests/
   ```

4. **Vérifier avec Ruff**
   ```bash
   uv run ruff check --fix pyfastcli/ tests/
   ```

5. **Vérifier les types avec Mypy**
   ```bash
   uv run mypy pyfastcli/
   ```

6. **Exécuter les tests**
   ```bash
   uv run pytest -v
   ```

7. **Vérifier la couverture**
   ```bash
   uv run pytest --cov=pyfastcli --cov-report=term-missing
   ```

### Avec pip standard

1. **Écrire le code**
   ```bash
   # Créer/modifier vos fichiers
   ```

2. **Formater avec Black**
   ```bash
   black pyfastcli/ tests/
   ```

3. **Vérifier avec Ruff**
   ```bash
   ruff check --fix pyfastcli/ tests/
   ```

4. **Vérifier les types avec Mypy**
   ```bash
   mypy pyfastcli/
   ```

5. **Exécuter les tests**
   ```bash
   pytest -v
   ```

6. **Vérifier la couverture**
   ```bash
   pytest --cov=pyfastcli --cov-report=term-missing
   ```

##  Utilisation du Makefile

Le projet inclut un `Makefile` qui automatise toutes les tâches de développement. Le Makefile détecte automatiquement si vous utilisez `uv` ou `pip` standard.

### Afficher l'aide

Pour voir toutes les commandes disponibles :

```bash
make help
```

Ou simplement :

```bash
make
```

### Commandes disponibles

#### Installation

```bash
# Installer les dépendances de développement
make install-dev
```

Cette commande :
- Essaie d'abord d'utiliser `uv sync` (si `uv` est installé)
- Sinon, utilise `pip install -e ".[dev]"`

#### Formatage et qualité de code

```bash
# Formater le code avec Black
make format

# Vérifier et corriger le code avec Ruff
make lint

# Vérifier les types avec Mypy
make type
```

#### Tests

```bash
# Exécuter tous les tests
make test

# Exécuter les tests avec couverture de code
make coverage
```

La commande `coverage` génère :
- Un rapport dans le terminal
- Un rapport HTML dans `htmlcov/index.html` (ouvrez-le dans votre navigateur)

#### Pipeline complet

```bash
# Exécuter tous les outils de qualité en une seule commande
make quality
```

Cette commande exécute dans l'ordre :
1. `make format` - Formate le code
2. `make lint` - Vérifie et corrige le code
3. `make type` - Vérifie les types
4. `make test` - Exécute les tests

C'est la commande recommandée avant de committer votre code !

#### Nettoyage

```bash
# Nettoyer tous les fichiers temporaires
make clean
```

Cette commande supprime :
- Les dossiers `__pycache__`
- Les fichiers `.pyc` et `.pyo`
- Les dossiers `.egg-info`
- Les caches de pytest, mypy, ruff
- Les rapports de couverture

### Exemples d'utilisation

#### Workflow quotidien

```bash
# 1. Installer les dépendances (une seule fois)
make install-dev

# 2. Travailler sur votre code...

# 3. Avant de committer, exécuter le pipeline complet
make quality

# 4. Si tout passe, committer
git add .
git commit -m "Ma nouvelle fonctionnalité"
```

#### Vérification rapide

```bash
# Juste formater le code
make format

# Juste vérifier les erreurs
make lint

# Juste exécuter les tests
make test
```

#### Après les tests

```bash
# Générer un rapport de couverture détaillé
make coverage

# Ouvrir le rapport HTML
# Linux/Mac
open htmlcov/index.html
# Windows
start htmlcov/index.html
```

### Avantages du Makefile

1. **Détection automatique** : Détecte si vous utilisez `uv` ou `pip` et utilise la bonne commande
2. **Commandes simples** : `make quality` au lieu de taper plusieurs commandes
3. **Cohérence** : Tous les développeurs utilisent les mêmes commandes
4. **Documentation** : `make help` montre toutes les commandes disponibles

### Commandes équivalentes

Si vous préférez utiliser les commandes directement :

| Makefile | Commande équivalente (avec uv) | Commande équivalente (avec pip) |
|----------|--------------------------------|----------------------------------|
| `make format` | `uv run black pyfastcli/ tests/` | `black pyfastcli/ tests/` |
| `make lint` | `uv run ruff check --fix pyfastcli/ tests/` | `ruff check --fix pyfastcli/ tests/` |
| `make type` | `uv run mypy pyfastcli/` | `mypy pyfastcli/` |
| `make test` | `uv run pytest -v` | `pytest -v` |
| `make coverage` | `uv run pytest --cov=pyfastcli --cov-report=html` | `pytest --cov=pyfastcli --cov-report=html` |
| `make quality` | `uv run black ... && uv run ruff ... && uv run mypy ... && uv run pytest` | `black ... && ruff ... && mypy ... && pytest` |

## 5. make:model - Génération interactive de modèles Django

Génère un modèle Django avec des champs définis interactivement, similaire à `make:entity` de Symfony.

### Fonctionnalités

- **Interface interactive** : Pose des questions pour chaque champ
- **Types de champs** : Propose tous les types de champs Django disponibles
- **Détection automatique** : Détecte les modèles existants pour les relations
- **Relations** : Supporte ForeignKey, ManyToManyField et OneToOneField
- **Options avancées** : Permet de configurer max_length, blank, null, verbose_name, etc.

### Génération interactive

```bash
pyfastcli make:model
```

Le CLI vous posera des questions sur :
- Le nom de l'app Django
- Le nom du modèle
- Le dossier de sortie
- Pour chaque champ :
  - Le nom du champ
  - Le type de champ (avec liste de suggestions)
  - Si c'est une relation, le modèle lié (avec liste des modèles existants)
  - Les options supplémentaires (max_length, blank, null, verbose_name, etc.)

### Génération avec options

```bash
pyfastcli make:model \
  --app-name pratique \
  --model-name Pratique \
  --output-dir . \
  --no-timestamps  # Pour ne pas ajouter created_at/updated_at
```

### Options disponibles

| Option | Raccourci | Description | Défaut |
|--------|-----------|-------------|--------|
| `--app-name` | `-a` | Nom de l'app Django | Demande interactivement |
| `--model-name` | `-m` | Nom du modèle | Demande interactivement |
| `--output-dir` | `-o` | Dossier de sortie (chemin du projet Django) | `.` |
| `--no-timestamps` | | Ne pas ajouter created_at et updated_at | `False` |

### Types de champs disponibles

La commande propose tous les types de champs Django standards :

- **Champs texte** : `CharField`, `TextField`, `EmailField`, `URLField`, `SlugField`
- **Champs numériques** : `IntegerField`, `BigIntegerField`, `DecimalField`, `FloatField`, `PositiveIntegerField`
- **Champs date/heure** : `DateField`, `DateTimeField`, `TimeField`, `DurationField`
- **Champs booléens** : `BooleanField`
- **Champs fichiers** : `FileField`, `ImageField`
- **Champs spéciaux** : `UUIDField`, `JSONField`, `IPAddressField`, `BinaryField`
- **Relations** : `ForeignKey`, `ManyToManyField`, `OneToOneField`

### Détection des modèles existants

La commande scanne automatiquement votre projet Django pour trouver les modèles existants et vous les propose lors de la création de relations :

```
🔍 Recherche des modèles existants...
✅ 3 modèle(s) trouvé(s)

Modèles existants disponibles :
  1. categories.Category
  2. tags.Tag
  3. users.User

Choisissez le modèle lié (numéro ou app.Model): 1
```

### Exemple d'utilisation interactive

```bash
$ pyfastcli make:model --app-name blog --model-name Article

🔍 Recherche des modèles existants...
✅ 2 modèle(s) trouvé(s)

📝 Définition des champs du modèle

--- Champ 1 ---
Nom du champ (ou 'fin' pour terminer): title
Est-ce une relation vers un autre modèle ? [y/N]: n

Types de champs disponibles :
  1. CharField
  2. TextField
  ...
Choisissez le type de champ (numéro ou nom): 1

Options disponibles (laissez vide pour terminer) :
Ajouter max_length ? [y/N]: y
max_length [255]: 200
Le champ peut être vide (blank=True) ? [y/N]: n
Le champ peut être null (null=True) ? [y/N]: n
Ajouter un verbose_name ? [y/N]: y
verbose_name: Titre de l'article

--- Champ 2 ---
Nom du champ (ou 'fin' pour terminer): author
Est-ce une relation vers un autre modèle ? [y/N]: y

Types de relations disponibles :
  1. ForeignKey
  2. ManyToManyField
  3. OneToOneField
Choisissez le type de relation (numéro ou nom): 1

Modèles existants disponibles :
  1. users.User
Choisissez le modèle lié (numéro ou app.Model): 1

Ajouter related_name ? [y/N]: y
related_name: articles

--- Champ 3 ---
Nom du champ (ou 'fin' pour terminer): fin

⚙️  Génération du modèle...
✅ Modèle généré avec succès : /path/to/blog/models.py

💡 Prochaines étapes :
  1. Vérifiez le modèle dans /path/to/blog/models.py
  2. Exécutez: python manage.py makemigrations blog
  3. Appliquez: python manage.py migrate
```

### Exemple de modèle généré

Pour l'exemple ci-dessus, le modèle généré sera :

```python
from django.db import models
from users.models import User


class Article(models.Model):
    """Modèle Article."""

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name="Titre de l'article")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Date de modification"
    )

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Article #{self.id}"
```

### Ajout à un fichier existant

Si le fichier `models.py` existe déjà, le nouveau modèle sera ajouté au fichier existant. Si le modèle existe déjà, une erreur sera levée.

### Prochaines étapes

Après la génération :

1. Vérifiez le modèle généré dans `{app_name}/models.py`
2. Exécutez les migrations : `python manage.py makemigrations {app_name}`
3. Appliquez les migrations : `python manage.py migrate`
4. (Optionnel) Ajoutez le modèle à `admin.py` pour l'interface d'administration

---

##  Structure du projet

```
pyfastcli/
├── pyfastcli/          # Code source du package
│   ├── __init__.py
│   ├── cli.py             # Interface CLI
│   └── generators/        # Générateurs
│       ├── __init__.py
│       ├── ninja_routes.py          # Générateur de routes Django Ninja
│       ├── package_generator.py     # Générateur de packages Python
│       ├── domaine_generator.py     # Générateur de domaines Django classiques
│       ├── ddd_domaine_generator.py # Générateur de domaines Django DDD
│       └── model_generator.py       # Générateur de modèles Django
├── tests/                 # Tests
│   ├── __init__.py
│   ├── test_ninja_routes.py
│   ├── test_package_generator.py
│   ├── test_domaine_generator.py
│   ├── test_ddd_domaine_generator.py
│   ├── test_model_generator.py
│   └── test_cli.py
├── pyproject.toml         # Configuration du projet
└── README.md             # Ce fichier
```

## Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Poussez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

**N'oubliez pas** d'exécuter les outils de qualité avant de soumettre :
```bash
make quality  # ou exécutez les commandes individuellement
```

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Liens utiles

- [Documentation Django Ninja](https://django-ninja.rest-framework.com/)
- [Documentation Click](https://click.palletsprojects.com/)
- [Documentation Black](https://black.readthedocs.io/)
- [Documentation Ruff](https://docs.astral.sh/ruff/)
- [Documentation Mypy](https://mypy.readthedocs.io/)
- [Documentation Pytest](https://docs.pytest.org/)

## 👤 Auteur

**Hedi DHIB** - hedi.dhib@gmail.com

## Remerciements

- Django Ninja pour le framework de routes
- Click pour l'interface CLI
- La communauté Python pour les outils de qualité

