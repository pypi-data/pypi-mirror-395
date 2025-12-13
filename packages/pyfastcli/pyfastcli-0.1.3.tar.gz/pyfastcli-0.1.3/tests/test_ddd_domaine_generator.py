"""Tests pour le générateur de domaine Django DDD."""

import shutil
import tempfile
from pathlib import Path

import pytest

from pyfastcli.generators.ddd_domaine_generator import (
    generate_ddd_domaine_structure,
)


class TestGenerateDDDDomaineStructure:
    """Tests pour la fonction generate_ddd_domaine_structure."""

    def setup_method(self):
        """Configuration avant chaque test."""
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir)

    def teardown_method(self):
        """Nettoyage après chaque test."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_generate_basic_structure(self):
        """Test de génération de la structure de base."""
        app_dir = generate_ddd_domaine_structure(
            app_name="pratique",
            model_name="Pratique",
            output_dir=str(self.output_dir),
        )

        assert Path(app_dir).exists()
        assert Path(app_dir).name == "pratique"

        # Vérifier les fichiers de base
        assert (Path(app_dir) / "__init__.py").exists()
        assert (Path(app_dir) / "apps.py").exists()
        assert (Path(app_dir) / "admin.py").exists()

    def test_generate_domain_layer(self):
        """Test de génération de la couche domain."""
        app_dir = generate_ddd_domaine_structure(
            app_name="pratique",
            model_name="Pratique",
            output_dir=str(self.output_dir),
        )

        assert (Path(app_dir) / "domain" / "__init__.py").exists()
        assert (Path(app_dir) / "domain" / "models.py").exists()
        assert (Path(app_dir) / "domain" / "services.py").exists()
        assert (Path(app_dir) / "domain" / "value_objects.py").exists()

        models_content = (Path(app_dir) / "domain" / "models.py").read_text(
            encoding="utf-8"
        )
        assert "class Pratique" in models_content
        assert "def est_valide" in models_content

        services_content = (Path(app_dir) / "domain" / "services.py").read_text(
            encoding="utf-8"
        )
        assert "class PratiqueService" in services_content

        vo_content = (Path(app_dir) / "domain" / "value_objects.py").read_text(
            encoding="utf-8"
        )
        assert "class PratiqueId" in vo_content

    def test_generate_infrastructure_layer(self):
        """Test de génération de la couche infrastructure."""
        app_dir = generate_ddd_domaine_structure(
            app_name="pratique",
            model_name="Pratique",
            output_dir=str(self.output_dir),
        )

        assert (Path(app_dir) / "infrastructure" / "__init__.py").exists()
        assert (Path(app_dir) / "infrastructure" / "repositories.py").exists()

        repos_content = (
            Path(app_dir) / "infrastructure" / "repositories.py"
        ).read_text(encoding="utf-8")
        assert "class PratiqueRepository" in repos_content
        assert "def obtenir_par_id" in repos_content

    def test_generate_presentation_layer(self):
        """Test de génération de la couche presentation."""
        app_dir = generate_ddd_domaine_structure(
            app_name="pratique",
            model_name="Pratique",
            output_dir=str(self.output_dir),
        )

        assert (Path(app_dir) / "presentation" / "__init__.py").exists()
        assert (Path(app_dir) / "presentation" / "views.py").exists()
        assert (Path(app_dir) / "presentation" / "forms.py").exists()
        assert (Path(app_dir) / "presentation" / "urls.py").exists()

        views_content = (Path(app_dir) / "presentation" / "views.py").read_text(
            encoding="utf-8"
        )
        assert "class PratiqueListView" in views_content
        assert "PratiqueService" in views_content

    def test_generate_with_serializers(self):
        """Test de génération avec serializers."""
        app_dir = generate_ddd_domaine_structure(
            app_name="pratique",
            model_name="Pratique",
            output_dir=str(self.output_dir),
            include_serializers=True,
        )

        assert (Path(app_dir) / "presentation" / "serializers.py").exists()

        serializers_content = (
            Path(app_dir) / "presentation" / "serializers.py"
        ).read_text(encoding="utf-8")
        assert "class PratiqueSerializer" in serializers_content
        assert "rest_framework" in serializers_content

    def test_generate_without_serializers(self):
        """Test de génération sans serializers."""
        app_dir = generate_ddd_domaine_structure(
            app_name="pratique",
            model_name="Pratique",
            output_dir=str(self.output_dir),
            include_serializers=False,
        )

        assert not (Path(app_dir) / "presentation" / "serializers.py").exists()

    def test_generate_templates(self):
        """Test de génération des templates."""
        app_dir = generate_ddd_domaine_structure(
            app_name="pratique",
            model_name="Pratique",
            output_dir=str(self.output_dir),
        )

        templates_dir = Path(app_dir) / "templates" / "pratique"
        assert templates_dir.exists()
        assert (templates_dir / "liste.html").exists()
        assert (templates_dir / "detail.html").exists()
        assert (templates_dir / "formulaire.html").exists()

    def test_generate_tests(self):
        """Test de génération des tests."""
        app_dir = generate_ddd_domaine_structure(
            app_name="pratique",
            model_name="Pratique",
            output_dir=str(self.output_dir),
        )

        assert (Path(app_dir) / "tests" / "__init__.py").exists()
        assert (Path(app_dir) / "tests" / "test_models.py").exists()
        assert (Path(app_dir) / "tests" / "test_services.py").exists()
        assert (Path(app_dir) / "tests" / "test_views.py").exists()

    def test_generate_file_exists_error(self):
        """Test avec un dossier existant."""
        existing_dir = self.output_dir / "pratique"
        existing_dir.mkdir()

        with pytest.raises(FileExistsError) as exc_info:
            generate_ddd_domaine_structure(
                app_name="pratique",
                model_name="Pratique",
                output_dir=str(self.output_dir),
            )

        assert "existe déjà" in str(exc_info.value)

    def test_generate_views_use_services(self):
        """Test que les vues utilisent les services."""
        app_dir = generate_ddd_domaine_structure(
            app_name="pratique",
            model_name="Pratique",
            output_dir=str(self.output_dir),
        )

        views_content = (Path(app_dir) / "presentation" / "views.py").read_text(
            encoding="utf-8"
        )
        assert "from pratique.domain.services import PratiqueService" in views_content
        assert (
            "from pratique.infrastructure.repositories import PratiqueRepository"
            in views_content
        )
        assert "PratiqueService.creer_pratique" in views_content

    def test_generate_admin_imports(self):
        """Test que admin.py importe depuis domain."""
        app_dir = generate_ddd_domaine_structure(
            app_name="pratique",
            model_name="Pratique",
            output_dir=str(self.output_dir),
        )

        admin_content = (Path(app_dir) / "admin.py").read_text(encoding="utf-8")
        assert "from pratique.domain.models import Pratique" in admin_content
