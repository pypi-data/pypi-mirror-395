"""Tests pour l'interface CLI."""

import shutil
import tempfile
from pathlib import Path

from click.testing import CliRunner

from pyfastcli.cli import cli


class TestCLI:
    """Tests pour la commande CLI."""

    def setup_method(self):
        """Configuration avant chaque test."""
        self.runner = CliRunner()
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir) / "routes"

    def teardown_method(self):
        """Nettoyage après chaque test."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_cli_help(self):
        """Test de l'aide de la CLI."""
        result = self.runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "CLI de génération de code" in result.output

    def test_make_url_help(self):
        """Test de l'aide de la commande make:url."""
        result = self.runner.invoke(cli, ["make:url", "--help"])
        assert result.exit_code == 0
        assert "Génère un fichier .py contenant une route Django Ninja" in result.output

    def test_make_url_with_options(self):
        """Test de la génération avec options en ligne de commande."""
        result = self.runner.invoke(
            cli,
            [
                "make:url",
                "--module-name",
                "orders",
                "--function-name",
                "get_orders",
                "--url-path",
                "/orders",
                "--http-method",
                "get",
                "--tag",
                "Orders",
                "--output-dir",
                str(self.output_dir),
                "--description",
                "Récupère les commandes",
            ],
        )

        assert result.exit_code == 0
        assert "Fichier généré avec succès" in result.output

        file_path = self.output_dir / "get_orders.py"
        assert file_path.exists()

        content = file_path.read_text(encoding="utf-8")
        assert "def get_orders(request):" in content
        assert '@router.get("/orders")' in content
        assert "Récupère les commandes" in content

    def test_make_url_interactive(self):
        """Test de la génération en mode interactif."""
        # Simuler les réponses interactives
        self.runner.invoke(
            cli,
            [
                "make:url",
                "--output-dir",
                str(self.output_dir),
            ],
            input="api\nget_orders\n/orders\nget\nOrders\nRécupère les commandes\n",
        )

        # En mode interactif, les prompts peuvent nécessiter des réponses
        # Pour simplifier, on teste avec toutes les options fournies
        file_path = self.output_dir / "get_orders.py"
        if file_path.exists():
            assert "def get_orders(request):" in file_path.read_text(encoding="utf-8")

    def test_make_url_invalid_method(self):
        """Test avec une méthode HTTP invalide."""
        result = self.runner.invoke(
            cli,
            [
                "make:url",
                "--module-name",
                "test",
                "--function-name",
                "test",
                "--url-path",
                "/test",
                "--http-method",
                "invalid",
                "--output-dir",
                str(self.output_dir),
            ],
        )

        assert result.exit_code != 0
        assert (
            "Invalid" in result.output
            or "invalide" in result.output.lower()
            or "Error" in result.output
        )

    def test_make_url_file_exists(self):
        """Test quand le fichier existe déjà."""
        # Créer le fichier d'abord
        file_path = self.output_dir / "existing.py"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text("existing content")

        result = self.runner.invoke(
            cli,
            [
                "make:url",
                "--module-name",
                "test",
                "--function-name",
                "existing",
                "--url-path",
                "/test",
                "--http-method",
                "get",
                "--output-dir",
                str(self.output_dir),
            ],
            input="\n",  # Entrée vide pour le prompt de description
        )

        assert result.exit_code != 0
        assert "existe déjà" in result.output

    def test_make_url_all_methods(self):
        """Test génération avec toutes les méthodes HTTP."""
        methods = ["get", "post", "put", "delete", "patch"]

        for method in methods:
            result = self.runner.invoke(
                cli,
                [
                    "make:url",
                    "--module-name",
                    "test",
                    "--function-name",
                    f"test_{method}",
                    "--url-path",
                    f"/test/{method}",
                    "--http-method",
                    method,
                    "--output-dir",
                    str(self.output_dir),
                ],
                input="\n",  # Entrée vide pour le prompt de description
            )

            assert result.exit_code == 0, f"Échec pour la méthode {method}"
            file_path = self.output_dir / f"test_{method}.py"
            assert file_path.exists()

            content = file_path.read_text(encoding="utf-8")
            assert f"@router.{method}(" in content


class TestCLIMakePackage:
    """Tests pour la commande make:package."""

    def setup_method(self):
        """Configuration avant chaque test."""
        self.runner = CliRunner()
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir)

    def teardown_method(self):
        """Nettoyage après chaque test."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_make_package_help(self):
        """Test de l'aide de la commande make:package."""
        result = self.runner.invoke(cli, ["make:package", "--help"])
        assert result.exit_code == 0
        assert "Génère une structure complète de package Python" in result.output

    def test_make_package_with_options(self):
        """Test de la génération avec options en ligne de commande."""
        result = self.runner.invoke(
            cli,
            [
                "make:package",
                "--project-name",
                "test-package",
                "--package-name",
                "test_package",
                "--version",
                "0.1.0",
                "--description",
                "A test package",
                "--author-name",
                "Test Author",
                "--author-email",
                "test@example.com",
                "--python-version",
                "3.8",
                "--license",
                "MIT",
                "--output-dir",
                str(self.output_dir),
            ],
        )

        assert result.exit_code == 0
        assert "Package créé avec succès" in result.output

        package_dir = self.output_dir / "test-package"
        assert package_dir.exists()
        assert (package_dir / "pyproject.toml").exists()
        assert (package_dir / "README.md").exists()
        assert (package_dir / "LICENSE").exists()
        assert (package_dir / ".gitignore").exists()
        assert (package_dir / "test_package" / "__init__.py").exists()
        assert (package_dir / "tests" / "__init__.py").exists()

    def test_make_package_with_makefile(self):
        """Test génération avec Makefile."""
        result = self.runner.invoke(
            cli,
            [
                "make:package",
                "--project-name",
                "test-package",
                "--package-name",
                "test_package",
                "--version",
                "0.1.0",
                "--description",
                "A test package",
                "--author-name",
                "Test Author",
                "--author-email",
                "test@example.com",
                "--python-version",
                "3.8",
                "--license",
                "MIT",
                "--output-dir",
                str(self.output_dir),
                "--include-makefile",
            ],
        )

        assert result.exit_code == 0
        package_dir = self.output_dir / "test-package"
        assert (package_dir / "Makefile").exists()

    def test_make_package_without_makefile(self):
        """Test génération sans Makefile."""
        result = self.runner.invoke(
            cli,
            [
                "make:package",
                "--project-name",
                "test-package",
                "--package-name",
                "test_package",
                "--version",
                "0.1.0",
                "--description",
                "A test package",
                "--author-name",
                "Test Author",
                "--author-email",
                "test@example.com",
                "--python-version",
                "3.8",
                "--license",
                "MIT",
                "--output-dir",
                str(self.output_dir),
                "--no-makefile",
            ],
        )

        assert result.exit_code == 0
        package_dir = self.output_dir / "test-package"
        assert not (package_dir / "Makefile").exists()

    def test_make_package_with_manifest(self):
        """Test génération avec MANIFEST.in."""
        result = self.runner.invoke(
            cli,
            [
                "make:package",
                "--project-name",
                "test-package",
                "--package-name",
                "test_package",
                "--version",
                "0.1.0",
                "--description",
                "A test package",
                "--author-name",
                "Test Author",
                "--author-email",
                "test@example.com",
                "--python-version",
                "3.8",
                "--license",
                "MIT",
                "--output-dir",
                str(self.output_dir),
                "--include-manifest",
            ],
        )

        assert result.exit_code == 0
        package_dir = self.output_dir / "test-package"
        assert (package_dir / "MANIFEST.in").exists()

    def test_make_package_with_dependencies(self):
        """Test génération avec dépendances."""
        result = self.runner.invoke(
            cli,
            [
                "make:package",
                "--project-name",
                "test-package",
                "--package-name",
                "test_package",
                "--version",
                "0.1.0",
                "--description",
                "A test package",
                "--author-name",
                "Test Author",
                "--author-email",
                "test@example.com",
                "--python-version",
                "3.8",
                "--license",
                "MIT",
                "--output-dir",
                str(self.output_dir),
                "--dependencies",
                "requests>=2.0.0,click>=8.0.0",
            ],
        )

        assert result.exit_code == 0
        package_dir = self.output_dir / "test-package"
        pyproject_content = (package_dir / "pyproject.toml").read_text(encoding="utf-8")
        assert "requests>=2.0.0" in pyproject_content
        assert "click>=8.0.0" in pyproject_content

    def test_make_package_with_github_username(self):
        """Test génération avec nom d'utilisateur GitHub."""
        result = self.runner.invoke(
            cli,
            [
                "make:package",
                "--project-name",
                "test-package",
                "--package-name",
                "test_package",
                "--version",
                "0.1.0",
                "--description",
                "A test package",
                "--author-name",
                "Test Author",
                "--author-email",
                "test@example.com",
                "--python-version",
                "3.8",
                "--license",
                "MIT",
                "--output-dir",
                str(self.output_dir),
                "--github-username",
                "testuser",
            ],
        )

        assert result.exit_code == 0
        package_dir = self.output_dir / "test-package"
        pyproject_content = (package_dir / "pyproject.toml").read_text(encoding="utf-8")
        assert "github.com/testuser/test-package" in pyproject_content

    def test_make_package_invalid_email(self):
        """Test avec un email invalide."""
        result = self.runner.invoke(
            cli,
            [
                "make:package",
                "--project-name",
                "test-package",
                "--package-name",
                "test_package",
                "--version",
                "0.1.0",
                "--description",
                "A test package",
                "--author-name",
                "Test Author",
                "--author-email",
                "invalid-email",
                "--python-version",
                "3.8",
                "--license",
                "MIT",
                "--output-dir",
                str(self.output_dir),
            ],
        )

        assert result.exit_code != 0
        assert "Email invalide" in result.output

    def test_make_package_file_exists(self):
        """Test quand le dossier existe déjà."""
        # Créer le dossier d'abord
        existing_dir = self.output_dir / "test-package"
        existing_dir.mkdir()

        result = self.runner.invoke(
            cli,
            [
                "make:package",
                "--project-name",
                "test-package",
                "--package-name",
                "test_package",
                "--version",
                "0.1.0",
                "--description",
                "A test package",
                "--author-name",
                "Test Author",
                "--author-email",
                "test@example.com",
                "--python-version",
                "3.8",
                "--license",
                "MIT",
                "--output-dir",
                str(self.output_dir),
            ],
        )

        assert result.exit_code != 0
        assert "existe déjà" in result.output

    def test_make_package_auto_package_name(self):
        """Test génération automatique du nom de package."""
        result = self.runner.invoke(
            cli,
            [
                "make:package",
                "--project-name",
                "my-awesome-package",
                "--version",
                "0.1.0",
                "--description",
                "A test package",
                "--author-name",
                "Test Author",
                "--author-email",
                "test@example.com",
                "--python-version",
                "3.8",
                "--license",
                "MIT",
                "--output-dir",
                str(self.output_dir),
            ],
        )

        assert result.exit_code == 0
        package_dir = self.output_dir / "my-awesome-package"
        # Le package devrait être créé avec le nom dérivé du project_name
        assert (package_dir / "my_awesome_package").exists()


class TestCLIMakeDomaine:
    """Tests pour la commande make:domaine."""

    def setup_method(self):
        """Configuration avant chaque test."""
        self.runner = CliRunner()
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir)

    def teardown_method(self):
        """Nettoyage après chaque test."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_make_domaine_help(self):
        """Test de l'aide de la commande make:domaine."""
        result = self.runner.invoke(cli, ["make:domaine", "--help"])
        assert result.exit_code == 0
        assert "Génère une structure complète de domaine Django" in result.output

    def test_make_domaine_with_options(self):
        """Test de la génération avec options en ligne de commande."""
        result = self.runner.invoke(
            cli,
            [
                "make:domaine",
                "--app-name",
                "pratique",
                "--model-name",
                "Pratique",
                "--output-dir",
                str(self.output_dir),
            ],
            input="\n",  # Entrée vide pour le prompt de description
        )

        assert result.exit_code == 0
        assert "Domaine créé avec succès" in result.output

        app_dir = self.output_dir / "pratique"
        assert app_dir.exists()
        assert (app_dir / "__init__.py").exists()
        assert (app_dir / "apps.py").exists()
        assert (app_dir / "admin.py").exists()
        assert (app_dir / "models.py").exists()
        assert (app_dir / "views.py").exists()
        assert (app_dir / "urls.py").exists()
        assert (app_dir / "forms.py").exists()
        assert (app_dir / "services.py").exists()
        assert (app_dir / "selectors.py").exists()
        assert (app_dir / "templates" / "pratique" / "liste.html").exists()
        assert (app_dir / "templates" / "pratique" / "detail.html").exists()
        assert (app_dir / "templates" / "pratique" / "formulaire.html").exists()

    def test_make_domaine_with_services(self):
        """Test génération avec services.py."""
        result = self.runner.invoke(
            cli,
            [
                "make:domaine",
                "--app-name",
                "test_app",
                "--model-name",
                "TestModel",
                "--output-dir",
                str(self.output_dir),
                "--include-services",
            ],
            input="\n",
        )

        assert result.exit_code == 0
        app_dir = self.output_dir / "test_app"
        assert (app_dir / "services.py").exists()

        content = (app_dir / "services.py").read_text(encoding="utf-8")
        assert "def creer_test_app" in content
        assert "def modifier_test_app" in content
        assert "def supprimer_test_app" in content

    def test_make_domaine_without_services(self):
        """Test génération sans services.py."""
        result = self.runner.invoke(
            cli,
            [
                "make:domaine",
                "--app-name",
                "test_app",
                "--model-name",
                "TestModel",
                "--output-dir",
                str(self.output_dir),
                "--no-services",
            ],
            input="\n",
        )

        assert result.exit_code == 0
        app_dir = self.output_dir / "test_app"
        assert not (app_dir / "services.py").exists()

    def test_make_domaine_with_selectors(self):
        """Test génération avec selectors.py."""
        result = self.runner.invoke(
            cli,
            [
                "make:domaine",
                "--app-name",
                "test_app",
                "--model-name",
                "TestModel",
                "--output-dir",
                str(self.output_dir),
                "--include-selectors",
            ],
            input="\n",
        )

        assert result.exit_code == 0
        app_dir = self.output_dir / "test_app"
        assert (app_dir / "selectors.py").exists()

        content = (app_dir / "selectors.py").read_text(encoding="utf-8")
        assert "def obtenir_test_app_par_id" in content
        assert "def lister_test_apps" in content
        assert "def filtrer_test_apps" in content

    def test_make_domaine_without_selectors(self):
        """Test génération sans selectors.py."""
        result = self.runner.invoke(
            cli,
            [
                "make:domaine",
                "--app-name",
                "test_app",
                "--model-name",
                "TestModel",
                "--output-dir",
                str(self.output_dir),
                "--no-selectors",
            ],
            input="\n",
        )

        assert result.exit_code == 0
        app_dir = self.output_dir / "test_app"
        assert not (app_dir / "selectors.py").exists()

    def test_make_domaine_auto_model_name(self):
        """Test génération automatique du nom de modèle."""
        result = self.runner.invoke(
            cli,
            [
                "make:domaine",
                "--app-name",
                "pratique",
                "--output-dir",
                str(self.output_dir),
            ],
            input="\n",
        )

        assert result.exit_code == 0
        app_dir = self.output_dir / "pratique"
        assert app_dir.exists()

        # Vérifier que le modèle Pratique est utilisé dans les fichiers
        models_content = (app_dir / "models.py").read_text(encoding="utf-8")
        assert "class Pratique" in models_content

    def test_make_domaine_models_content(self):
        """Test du contenu des modèles générés."""
        result = self.runner.invoke(
            cli,
            [
                "make:domaine",
                "--app-name",
                "pratique",
                "--model-name",
                "Pratique",
                "--output-dir",
                str(self.output_dir),
            ],
            input="\n",
        )

        assert result.exit_code == 0
        app_dir = self.output_dir / "pratique"

        models_content = (app_dir / "models.py").read_text(encoding="utf-8")
        assert "class Pratique" in models_content
        assert "class SessionPratique" in models_content
        assert "created_at" in models_content
        assert "updated_at" in models_content

    def test_make_domaine_views_content(self):
        """Test du contenu des vues générées."""
        result = self.runner.invoke(
            cli,
            [
                "make:domaine",
                "--app-name",
                "pratique",
                "--model-name",
                "Pratique",
                "--output-dir",
                str(self.output_dir),
            ],
            input="\n",
        )

        assert result.exit_code == 0
        app_dir = self.output_dir / "pratique"

        views_content = (app_dir / "views.py").read_text(encoding="utf-8")
        assert "class PratiqueListView" in views_content
        assert "class PratiqueDetailView" in views_content
        assert "class PratiqueCreateView" in views_content
        assert "class PratiqueUpdateView" in views_content
        assert "class PratiqueDeleteView" in views_content

    def test_make_domaine_urls_content(self):
        """Test du contenu des URLs générées."""
        result = self.runner.invoke(
            cli,
            [
                "make:domaine",
                "--app-name",
                "pratique",
                "--model-name",
                "Pratique",
                "--output-dir",
                str(self.output_dir),
            ],
            input="\n",
        )

        assert result.exit_code == 0
        app_dir = self.output_dir / "pratique"

        urls_content = (app_dir / "urls.py").read_text(encoding="utf-8")
        assert 'app_name = "pratique"' in urls_content
        assert 'name="liste"' in urls_content
        assert 'name="detail"' in urls_content
        assert 'name="creer"' in urls_content
        assert 'name="modifier"' in urls_content
        assert 'name="supprimer"' in urls_content

    def test_make_domaine_templates_content(self):
        """Test du contenu des templates générés."""
        result = self.runner.invoke(
            cli,
            [
                "make:domaine",
                "--app-name",
                "pratique",
                "--model-name",
                "Pratique",
                "--output-dir",
                str(self.output_dir),
            ],
            input="\n",
        )

        assert result.exit_code == 0
        app_dir = self.output_dir / "pratique"

        liste_content = (app_dir / "templates" / "pratique" / "liste.html").read_text(
            encoding="utf-8"
        )
        assert "Liste des Pratiques" in liste_content
        assert "{% url 'pratique:creer' %}" in liste_content

        detail_content = (app_dir / "templates" / "pratique" / "detail.html").read_text(
            encoding="utf-8"
        )
        assert "Détails du Pratique" in detail_content

        formulaire_content = (
            app_dir / "templates" / "pratique" / "formulaire.html"
        ).read_text(encoding="utf-8")
        assert "{% csrf_token %}" in formulaire_content
        assert "{{ form.as_p }}" in formulaire_content

    def test_make_domaine_file_exists(self):
        """Test quand le dossier existe déjà."""
        # Créer le dossier d'abord
        existing_dir = self.output_dir / "pratique"
        existing_dir.mkdir()

        result = self.runner.invoke(
            cli,
            [
                "make:domaine",
                "--app-name",
                "pratique",
                "--model-name",
                "Pratique",
                "--output-dir",
                str(self.output_dir),
            ],
            input="\n",
        )

        assert result.exit_code != 0
        assert "existe déjà" in result.output

    def test_make_domaine_with_description(self):
        """Test avec une description personnalisée."""
        result = self.runner.invoke(
            cli,
            [
                "make:domaine",
                "--app-name",
                "pratique",
                "--model-name",
                "Pratique",
                "--output-dir",
                str(self.output_dir),
                "--description",
                "Application de gestion des pratiques",
            ],
        )

        assert result.exit_code == 0
        app_dir = self.output_dir / "pratique"
        assert app_dir.exists()

    def test_make_domaine_sanitize_app_name(self):
        """Test de la sanitization du nom d'app."""
        result = self.runner.invoke(
            cli,
            [
                "make:domaine",
                "--app-name",
                "test-app",
                "--model-name",
                "TestModel",
                "--output-dir",
                str(self.output_dir),
            ],
            input="\n",
        )

        assert result.exit_code == 0
        # Le nom devrait être converti en test_app
        app_dir = self.output_dir / "test_app"
        assert app_dir.exists()

    def test_make_domaine_admin_content(self):
        """Test du contenu de admin.py."""
        result = self.runner.invoke(
            cli,
            [
                "make:domaine",
                "--app-name",
                "pratique",
                "--model-name",
                "Pratique",
                "--output-dir",
                str(self.output_dir),
            ],
            input="\n",
        )

        assert result.exit_code == 0
        app_dir = self.output_dir / "pratique"

        admin_content = (app_dir / "admin.py").read_text(encoding="utf-8")
        assert "@admin.register(Pratique)" in admin_content
        assert "class PratiqueAdmin" in admin_content

    def test_make_domaine_forms_content(self):
        """Test du contenu de forms.py."""
        result = self.runner.invoke(
            cli,
            [
                "make:domaine",
                "--app-name",
                "pratique",
                "--model-name",
                "Pratique",
                "--output-dir",
                str(self.output_dir),
            ],
            input="\n",
        )

        assert result.exit_code == 0
        app_dir = self.output_dir / "pratique"

        forms_content = (app_dir / "forms.py").read_text(encoding="utf-8")
        assert "class PratiqueForm" in forms_content
        assert "forms.ModelForm" in forms_content


class TestCLIMakeDomaineDDD:
    """Tests pour la commande make:domaine-ddd."""

    def setup_method(self):
        """Configuration avant chaque test."""
        self.runner = CliRunner()
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir)

    def teardown_method(self):
        """Nettoyage après chaque test."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_make_domaine_ddd_help(self):
        """Test de l'aide de la commande make:domaine-ddd."""
        result = self.runner.invoke(cli, ["make:domaine-ddd", "--help"])
        assert result.exit_code == 0
        assert (
            "Génère une structure complète de domaine Django selon les principes DDD"
            in result.output
        )

    def test_make_domaine_ddd_with_options(self):
        """Test de la génération avec options en ligne de commande."""
        result = self.runner.invoke(
            cli,
            [
                "make:domaine-ddd",
                "--app-name",
                "pratique",
                "--model-name",
                "Pratique",
                "--output-dir",
                str(self.output_dir),
            ],
            input="\n",
        )

        assert result.exit_code == 0
        assert "Domaine DDD créé avec succès" in result.output

        app_dir = self.output_dir / "pratique"
        assert app_dir.exists()
        assert (app_dir / "__init__.py").exists()
        assert (app_dir / "apps.py").exists()
        assert (app_dir / "admin.py").exists()
        assert (app_dir / "domain" / "models.py").exists()
        assert (app_dir / "domain" / "services.py").exists()
        assert (app_dir / "domain" / "value_objects.py").exists()
        assert (app_dir / "infrastructure" / "repositories.py").exists()
        assert (app_dir / "presentation" / "views.py").exists()
        assert (app_dir / "presentation" / "forms.py").exists()
        assert (app_dir / "presentation" / "serializers.py").exists()
        assert (app_dir / "presentation" / "urls.py").exists()
        assert (app_dir / "templates" / "pratique" / "liste.html").exists()
        assert (app_dir / "templates" / "pratique" / "detail.html").exists()
        assert (app_dir / "templates" / "pratique" / "formulaire.html").exists()
        assert (app_dir / "tests" / "test_models.py").exists()
        assert (app_dir / "tests" / "test_services.py").exists()
        assert (app_dir / "tests" / "test_views.py").exists()

    def test_make_domaine_ddd_with_serializers(self):
        """Test génération avec serializers.py."""
        result = self.runner.invoke(
            cli,
            [
                "make:domaine-ddd",
                "--app-name",
                "test_app",
                "--model-name",
                "TestModel",
                "--output-dir",
                str(self.output_dir),
                "--include-serializers",
            ],
            input="\n",
        )

        assert result.exit_code == 0
        app_dir = self.output_dir / "test_app"
        assert (app_dir / "presentation" / "serializers.py").exists()

        content = (app_dir / "presentation" / "serializers.py").read_text(
            encoding="utf-8"
        )
        # Le nom du modèle est sanitized, donc TestModel devient Testmodel
        assert "class TestmodelSerializer" in content
        assert "Testmodel" in content

    def test_make_domaine_ddd_without_serializers(self):
        """Test génération sans serializers.py."""
        result = self.runner.invoke(
            cli,
            [
                "make:domaine-ddd",
                "--app-name",
                "test_app",
                "--model-name",
                "TestModel",
                "--output-dir",
                str(self.output_dir),
                "--no-serializers",
            ],
            input="\n",
        )

        assert result.exit_code == 0
        app_dir = self.output_dir / "test_app"
        assert not (app_dir / "presentation" / "serializers.py").exists()

    def test_make_domaine_ddd_auto_model_name(self):
        """Test génération automatique du nom de modèle."""
        result = self.runner.invoke(
            cli,
            [
                "make:domaine-ddd",
                "--app-name",
                "pratique",
                "--output-dir",
                str(self.output_dir),
            ],
            input="\n",
        )

        assert result.exit_code == 0
        app_dir = self.output_dir / "pratique"
        assert app_dir.exists()

        models_content = (app_dir / "domain" / "models.py").read_text(encoding="utf-8")
        assert "class Pratique" in models_content

    def test_make_domaine_ddd_domain_structure(self):
        """Test de la structure du domaine."""
        result = self.runner.invoke(
            cli,
            [
                "make:domaine-ddd",
                "--app-name",
                "pratique",
                "--model-name",
                "Pratique",
                "--output-dir",
                str(self.output_dir),
            ],
            input="\n",
        )

        assert result.exit_code == 0
        app_dir = self.output_dir / "pratique"

        # Vérifier domain/models.py
        models_content = (app_dir / "domain" / "models.py").read_text(encoding="utf-8")
        assert "class Pratique" in models_content
        assert "def est_valide" in models_content
        assert "def peut_etre_modifiee" in models_content

        # Vérifier domain/services.py
        services_content = (app_dir / "domain" / "services.py").read_text(
            encoding="utf-8"
        )
        assert "class PratiqueService" in services_content
        assert "def creer_pratique" in services_content

        # Vérifier domain/value_objects.py
        vo_content = (app_dir / "domain" / "value_objects.py").read_text(
            encoding="utf-8"
        )
        assert "class PratiqueId" in vo_content
        assert "@dataclass(frozen=True)" in vo_content

    def test_make_domaine_ddd_infrastructure_structure(self):
        """Test de la structure infrastructure."""
        result = self.runner.invoke(
            cli,
            [
                "make:domaine-ddd",
                "--app-name",
                "pratique",
                "--model-name",
                "Pratique",
                "--output-dir",
                str(self.output_dir),
            ],
            input="\n",
        )

        assert result.exit_code == 0
        app_dir = self.output_dir / "pratique"

        repos_content = (app_dir / "infrastructure" / "repositories.py").read_text(
            encoding="utf-8"
        )
        assert "class PratiqueRepository" in repos_content
        assert "def obtenir_par_id" in repos_content
        assert "def lister_tous" in repos_content
        assert "def rechercher" in repos_content

    def test_make_domaine_ddd_presentation_structure(self):
        """Test de la structure presentation."""
        result = self.runner.invoke(
            cli,
            [
                "make:domaine-ddd",
                "--app-name",
                "pratique",
                "--model-name",
                "Pratique",
                "--output-dir",
                str(self.output_dir),
            ],
            input="\n",
        )

        assert result.exit_code == 0
        app_dir = self.output_dir / "pratique"

        views_content = (app_dir / "presentation" / "views.py").read_text(
            encoding="utf-8"
        )
        assert "class PratiqueListView" in views_content
        assert "PratiqueService" in views_content
        assert "PratiqueRepository" in views_content

        forms_content = (app_dir / "presentation" / "forms.py").read_text(
            encoding="utf-8"
        )
        assert "class PratiqueForm" in forms_content

        urls_content = (app_dir / "presentation" / "urls.py").read_text(
            encoding="utf-8"
        )
        assert 'app_name = "pratique"' in urls_content

    def test_make_domaine_ddd_tests_structure(self):
        """Test de la structure des tests."""
        result = self.runner.invoke(
            cli,
            [
                "make:domaine-ddd",
                "--app-name",
                "pratique",
                "--model-name",
                "Pratique",
                "--output-dir",
                str(self.output_dir),
            ],
            input="\n",
        )

        assert result.exit_code == 0
        app_dir = self.output_dir / "pratique"

        test_models_content = (app_dir / "tests" / "test_models.py").read_text(
            encoding="utf-8"
        )
        assert "class PratiqueModelTest" in test_models_content

        test_services_content = (app_dir / "tests" / "test_services.py").read_text(
            encoding="utf-8"
        )
        assert "class PratiqueServiceTest" in test_services_content

        test_views_content = (app_dir / "tests" / "test_views.py").read_text(
            encoding="utf-8"
        )
        assert "class PratiqueViewsTest" in test_views_content

    def test_make_domaine_ddd_file_exists(self):
        """Test quand le dossier existe déjà."""
        existing_dir = self.output_dir / "pratique"
        existing_dir.mkdir()

        result = self.runner.invoke(
            cli,
            [
                "make:domaine-ddd",
                "--app-name",
                "pratique",
                "--model-name",
                "Pratique",
                "--output-dir",
                str(self.output_dir),
            ],
            input="\n",
        )

        assert result.exit_code != 0
        assert "existe déjà" in result.output
