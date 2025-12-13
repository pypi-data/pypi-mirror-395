"""Générateur de structure de package Python selon les best practices."""

import re
from pathlib import Path
from typing import Optional


def _sanitize_package_name(name: str) -> str:
    """
    Nettoie et valide un nom de package Python.

    Args:
        name: Nom du package à nettoyer

    Returns:
        Nom de package valide avec underscores
    """
    # Remplace les tirets et espaces par des underscores
    name = re.sub(r"[- ]+", "_", name.strip())
    # Supprime les caractères non valides
    name = re.sub(r"[^a-zA-Z0-9_]", "", name)
    # S'assure que le nom commence par une lettre ou underscore
    if name and name[0].isdigit():
        name = f"_{name}"
    # S'assure que le nom n'est pas vide
    if not name:
        name = "my_package"
    # Convertit en minuscules
    return name.lower()


def _sanitize_project_name(name: str) -> str:
    """
    Nettoie un nom de projet (peut contenir des tirets).

    Args:
        name: Nom du projet

    Returns:
        Nom de projet nettoyé
    """
    name = name.strip()
    if not name:
        return "my-package"
    # Remplace les espaces par des tirets
    name = re.sub(r"\s+", "-", name)
    # Supprime les caractères invalides
    name = re.sub(r"[^a-zA-Z0-9\-_]", "", name)
    return name.lower()


def _validate_email(email: str) -> str:
    """
    Valide un email basique.

    Args:
        email: Email à valider

    Returns:
        Email validé

    Raises:
        ValueError: Si l'email est invalide
    """
    email = email.strip()
    if not email or "@" not in email:
        raise ValueError("Email invalide. Format attendu: user@example.com")
    return email


def _validate_python_version(version: str) -> str:
    """
    Valide une version Python (ex: 3.8, 3.9).

    Args:
        version: Version Python

    Returns:
        Version validée

    Raises:
        ValueError: Si la version est invalide
    """
    version = version.strip()
    # Format attendu: 3.8, 3.9, 3.10, etc.
    if not re.match(r"^3\.\d+$", version):
        raise ValueError("Version Python invalide. Format attendu: 3.8, 3.9, etc.")
    return version


def generate_package_structure(
    project_name: str,
    package_name: str,
    version: str,
    description: str,
    author_name: str,
    author_email: str,
    python_version: str,
    license_type: str,
    output_dir: str,
    include_makefile: bool = True,
    include_manifest: bool = True,
    include_setup_py: bool = False,
    dependencies: Optional[list] = None,
    dev_dependencies: Optional[list] = None,
    github_username: Optional[str] = None,
    homepage_url: Optional[str] = None,
) -> str:
    """
    Génère une structure complète de package Python selon les best practices.

    Args:
        project_name: Nom du projet (avec tirets, ex: my-package)
        package_name: Nom du package Python (avec underscores, ex: my_package)
        version: Version initiale (ex: 0.1.0)
        description: Description du package
        author_name: Nom de l'auteur
        author_email: Email de l'auteur
        python_version: Version Python minimale (ex: 3.8)
        license_type: Type de licence (MIT, Apache-2.0, etc.)
        output_dir: Dossier de sortie où créer le package
        include_makefile: Inclure un Makefile
        include_manifest: Inclure MANIFEST.in
        include_setup_py: Inclure setup.py (optionnel, pyproject.toml suffit)
        dependencies: Liste des dépendances (optionnel)
        dev_dependencies: Liste des dépendances de développement (optionnel)
        github_username: Nom d'utilisateur GitHub (optionnel)
        homepage_url: URL de la page d'accueil (optionnel)

    Returns:
        Chemin du dossier du package créé

    Raises:
        ValueError: Si les paramètres sont invalides
        OSError: Si les fichiers ne peuvent pas être créés
    """
    # Validation et nettoyage
    project_name = _sanitize_project_name(project_name)
    package_name = _sanitize_package_name(package_name)
    author_email = _validate_email(author_email)
    python_version = _validate_python_version(python_version)

    if not description.strip():
        description = f"A Python package: {package_name}"

    if dependencies is None:
        dependencies = []
    if dev_dependencies is None:
        dev_dependencies = ["pytest>=7.0.0", "black>=23.0.0", "ruff>=0.1.0"]

    # Création du dossier de sortie
    output_path = Path(output_dir)
    package_dir = output_path / project_name

    if package_dir.exists():
        raise FileExistsError(
            f"Le dossier {package_dir} existe déjà. "
            "Supprimez-le ou choisissez un autre nom de projet."
        )

    try:
        package_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise OSError(f"Impossible de créer le dossier {package_dir}: {e}") from e

    # Génération des fichiers
    _generate_pyproject_toml(
        package_dir,
        project_name,
        package_name,
        version,
        description,
        author_name,
        author_email,
        python_version,
        license_type,
        dependencies,
        dev_dependencies,
        github_username,
        homepage_url,
    )

    _generate_readme(package_dir, project_name, package_name, description, author_name)

    _generate_license(package_dir, license_type, author_name)

    _generate_gitignore(package_dir)

    _generate_package_init(package_dir, package_name)

    _generate_tests_structure(package_dir, package_name)

    if include_manifest:
        _generate_manifest_in(package_dir, package_name)

    if include_makefile:
        _generate_makefile(package_dir)

    if include_setup_py:
        _generate_setup_py(
            package_dir,
            project_name,
            package_name,
            version,
            description,
            author_name,
            author_email,
        )

    return str(package_dir)


def _generate_pyproject_toml(
    package_dir: Path,
    project_name: str,
    package_name: str,
    version: str,
    description: str,
    author_name: str,
    author_email: str,
    python_version: str,
    license_type: str,
    dependencies: list,
    dev_dependencies: list,
    github_username: Optional[str],
    homepage_url: Optional[str],
):
    """Génère le fichier pyproject.toml."""
    # URLs GitHub si fourni
    if github_username:
        repo_url = f"https://github.com/{github_username}/{project_name}"
        homepage = homepage_url or repo_url
    else:
        repo_url = homepage_url or ""
        homepage = homepage_url or ""

    # Formatage des dépendances
    if dependencies:
        deps_str = "\n".join([f'    "{dep}",' for dep in dependencies])
        deps_section = f"dependencies = [\n{deps_str}\n]"
    else:
        deps_section = "dependencies = []"

    if dev_dependencies:
        dev_deps_str = "\n".join([f'    "{dep}",' for dep in dev_dependencies])
        dev_deps_section = f"dev = [\n{dev_deps_str}\n]"
    else:
        dev_deps_section = "dev = []"

    # Classifiers Python
    major, minor = python_version.split(".")
    classifiers = f"""    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: {major}.{minor}",
    "License :: OSI Approved :: {license_type} License",
    "Operating System :: OS Independent","""

    content = f"""[build-system]
requires = ["setuptools>=61", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{project_name}"
version = "{version}"
description = "{description}"
readme = "README.md"
requires-python = ">={python_version}"
license = {{text = "{license_type}"}}
authors = [
    {{name = "{author_name}", email = "{author_email}"}}
]
classifiers = [
{classifiers}
]

{deps_section}

keywords = ["python", "package"]

[project.optional-dependencies]
{dev_deps_section}

[project.urls]
"""

    if homepage:
        content += f'Homepage = "{homepage}"\n'
    if github_username:
        content += f'Repository = "{repo_url}"\n'
        content += f'Issues = "{repo_url}/issues"\n'

    content += f"""
[tool.setuptools]
packages = ["{package_name}"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --cov={package_name} --cov-report=term-missing --cov-report=html"

[tool.black]
line-length = 88
target-version = ['py{major}{minor}']
include = '\\.pyi?$'

[tool.ruff]
line-length = 88
target-version = "py{major}{minor}"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
ignore = []

[tool.mypy]
python_version = "{python_version}"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
"""

    (package_dir / "pyproject.toml").write_text(content, encoding="utf-8")


def _generate_readme(
    package_dir: Path,
    project_name: str,
    package_name: str,
    description: str,
    author_name: str,
):
    """Génère le fichier README.md."""
    content = f"""# {project_name}

{description}

## Installation

### Installation depuis PyPI

```bash
pip install {project_name}
```

### Installation depuis le code source

```bash
# Cloner le dépôt
git clone https://github.com/USERNAME/{project_name}.git
cd {project_name}

# Créer un environnement virtuel
python -m venv .venv

# Activer l'environnement
source .venv/bin/activate  # Linux/Mac
# .venv\\Scripts\\activate  # Windows

# Installer en mode développement
pip install -e ".[dev]"
```

## Utilisation

```python
from {package_name} import ...

# Votre code ici
```

## Développement

### Exécuter les tests

```bash
pytest
```

### Formater le code

```bash
black {package_name} tests
```

### Vérifier le code

```bash
ruff check {package_name} tests
```

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## Auteur

{author_name}
"""
    (package_dir / "README.md").write_text(content, encoding="utf-8")


def _generate_license(package_dir: Path, license_type: str, author_name: str):
    """Génère le fichier LICENSE."""
    year = "2025"

    if license_type.upper() == "MIT":
        content = f"""MIT License

Copyright (c) {year} {author_name}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    else:
        # Licence Apache-2.0 ou autre - on met un placeholder
        content = f"""{license_type} License

Copyright (c) {year} {author_name}

See LICENSE file for full license text.
"""

    (package_dir / "LICENSE").write_text(content, encoding="utf-8")


def _generate_gitignore(package_dir: Path):
    """Génère le fichier .gitignore standard pour Python."""
    content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py.cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.envrc
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
.idea/

# VS Code
.vscode/

# Ruff
.ruff_cache/

# PyPI configuration file
.pypirc
"""
    (package_dir / ".gitignore").write_text(content, encoding="utf-8")


def _generate_package_init(package_dir: Path, package_name: str):
    """Génère le fichier __init__.py du package."""
    package_path = package_dir / package_name
    package_path.mkdir(exist_ok=True)

    content = f'''"""
{package_name} - A Python package.
"""

__version__ = "0.1.0"
'''
    (package_path / "__init__.py").write_text(content, encoding="utf-8")


def _generate_tests_structure(package_dir: Path, package_name: str):
    """Génère la structure de tests."""
    tests_dir = package_dir / "tests"
    tests_dir.mkdir(exist_ok=True)

    # __init__.py pour tests
    (tests_dir / "__init__.py").write_text("", encoding="utf-8")

    # test_package.py exemple
    content = f'''"""Tests pour le package {package_name}."""


def test_example():
    """Test d'exemple."""
    assert True
'''
    (tests_dir / f"test_{package_name}.py").write_text(content, encoding="utf-8")


def _generate_manifest_in(package_dir: Path, package_name: str):
    """Génère le fichier MANIFEST.in."""
    content = f"""include README.md
include LICENSE
include pyproject.toml
recursive-include {package_name} *.py
recursive-exclude * __pycache__
recursive-exclude * *.py[co]
"""
    (package_dir / "MANIFEST.in").write_text(content, encoding="utf-8")


def _generate_makefile(package_dir: Path):
    """Génère un Makefile avec des commandes utiles."""
    content = """# Makefile pour le développement Python

.PHONY: help install install-dev test lint format clean build upload

help:
	@echo "Commandes disponibles:"
	@echo "  make install      - Installer le package"
	@echo "  make install-dev  - Installer avec dépendances de développement"
	@echo "  make test         - Exécuter les tests"
	@echo "  make lint         - Vérifier le code avec ruff"
	@echo "  make format       - Formater le code avec black"
	@echo "  make clean        - Nettoyer les fichiers générés"
	@echo "  make build        - Construire les distributions"
	@echo "  make upload       - Uploader sur PyPI (nécessite twine)"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check .

format:
	black .

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

build:
	python -m build

upload:
	twine upload dist/*
"""
    (package_dir / "Makefile").write_text(content, encoding="utf-8")


def _generate_setup_py(
    package_dir: Path,
    project_name: str,
    package_name: str,
    version: str,
    description: str,
    author_name: str,
    author_email: str,
):
    """Génère setup.py (optionnel, pour compatibilité)."""
    content = f'''"""Configuration setup.py pour {project_name}."""
from setuptools import setup

setup()
'''
    (package_dir / "setup.py").write_text(content, encoding="utf-8")
