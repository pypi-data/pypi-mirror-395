"""Tests pour le générateur de domaine Django."""

import shutil
import tempfile
from pathlib import Path

import pytest

from pyfastcli.generators.domaine_generator import (
    _sanitize_app_name,
    _sanitize_model_name,
    generate_domaine_structure,
)


class TestSanitizeAppName:
    """Tests pour la fonction _sanitize_app_name."""

    def test_simple_name(self):
        """Test avec un nom simple."""
        assert _sanitize_app_name("pratique") == "pratique"

    def test_name_with_dashes(self):
        """Test avec des tirets."""
        assert _sanitize_app_name("test-app") == "test_app"

    def test_name_with_spaces(self):
        """Test avec des espaces."""
        assert _sanitize_app_name("test app") == "test_app"

    def test_name_starting_with_digit(self):
        """Test avec un nom commençant par un chiffre."""
        assert _sanitize_app_name("123app") == "_123app"

    def test_name_with_special_chars(self):
        """Test avec des caractères spéciaux."""
        assert _sanitize_app_name("test@app#test") == "testapptest"

    def test_empty_name(self):
        """Test avec un nom vide."""
        assert _sanitize_app_name("") == "my_app"

    def test_mixed_case(self):
        """Test avec majuscules/minuscules."""
        assert _sanitize_app_name("TestApp") == "testapp"


class TestSanitizeModelName:
    """Tests pour la fonction _sanitize_model_name."""

    def test_simple_name(self):
        """Test avec un nom simple."""
        assert _sanitize_model_name("Pratique") == "Pratique"

    def test_name_with_underscores(self):
        """Test avec des underscores."""
        assert _sanitize_model_name("test_model") == "TestModel"

    def test_name_with_spaces(self):
        """Test avec des espaces."""
        assert _sanitize_model_name("test model") == "TestModel"

    def test_name_with_dashes(self):
        """Test avec des tirets."""
        assert _sanitize_model_name("test-model") == "TestModel"

    def test_name_with_special_chars(self):
        """Test avec des caractères spéciaux."""
        assert _sanitize_model_name("test@model#test") == "TestModelTest"

    def test_empty_name(self):
        """Test avec un nom vide."""
        assert _sanitize_model_name("") == "Model"

    def test_multiple_words(self):
        """Test avec plusieurs mots."""
        assert _sanitize_model_name("session pratique") == "SessionPratique"


class TestGenerateDomaineStructure:
    """Tests pour la fonction generate_domaine_structure."""

    def setup_method(self):
        """Configuration avant chaque test."""
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir)

    def teardown_method(self):
        """Nettoyage après chaque test."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_generate_basic_structure(self):
        """Test de génération de la structure de base."""
        app_dir = generate_domaine_structure(
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
        assert (Path(app_dir) / "models.py").exists()
        assert (Path(app_dir) / "views.py").exists()
        assert (Path(app_dir) / "urls.py").exists()
        assert (Path(app_dir) / "forms.py").exists()

    def test_generate_with_services(self):
        """Test de génération avec services.py."""
        app_dir = generate_domaine_structure(
            app_name="pratique",
            model_name="Pratique",
            output_dir=str(self.output_dir),
            include_services=True,
        )

        assert (Path(app_dir) / "services.py").exists()

        content = (Path(app_dir) / "services.py").read_text(encoding="utf-8")
        assert "def creer_pratique" in content
        assert "def modifier_pratique" in content
        assert "def supprimer_pratique" in content

    def test_generate_without_services(self):
        """Test de génération sans services.py."""
        app_dir = generate_domaine_structure(
            app_name="pratique",
            model_name="Pratique",
            output_dir=str(self.output_dir),
            include_services=False,
        )

        assert not (Path(app_dir) / "services.py").exists()

    def test_generate_with_selectors(self):
        """Test de génération avec selectors.py."""
        app_dir = generate_domaine_structure(
            app_name="pratique",
            model_name="Pratique",
            output_dir=str(self.output_dir),
            include_selectors=True,
        )

        assert (Path(app_dir) / "selectors.py").exists()

        content = (Path(app_dir) / "selectors.py").read_text(encoding="utf-8")
        assert "def obtenir_pratique_par_id" in content
        assert "def lister_pratiques" in content
        assert "def filtrer_pratiques" in content

    def test_generate_without_selectors(self):
        """Test de génération sans selectors.py."""
        app_dir = generate_domaine_structure(
            app_name="pratique",
            model_name="Pratique",
            output_dir=str(self.output_dir),
            include_selectors=False,
        )

        assert not (Path(app_dir) / "selectors.py").exists()

    def test_generate_templates(self):
        """Test de génération des templates."""
        app_dir = generate_domaine_structure(
            app_name="pratique",
            model_name="Pratique",
            output_dir=str(self.output_dir),
        )

        templates_dir = Path(app_dir) / "templates" / "pratique"
        assert templates_dir.exists()
        assert (templates_dir / "liste.html").exists()
        assert (templates_dir / "detail.html").exists()
        assert (templates_dir / "formulaire.html").exists()

    def test_generate_models_content(self):
        """Test du contenu des modèles générés."""
        app_dir = generate_domaine_structure(
            app_name="pratique",
            model_name="Pratique",
            output_dir=str(self.output_dir),
        )

        models_content = (Path(app_dir) / "models.py").read_text(encoding="utf-8")
        assert "class Pratique" in models_content
        assert "class SessionPratique" in models_content
        assert "created_at" in models_content
        assert "updated_at" in models_content

    def test_generate_views_content(self):
        """Test du contenu des vues générées."""
        app_dir = generate_domaine_structure(
            app_name="pratique",
            model_name="Pratique",
            output_dir=str(self.output_dir),
        )

        views_content = (Path(app_dir) / "views.py").read_text(encoding="utf-8")
        assert "class PratiqueListView" in views_content
        assert "class PratiqueDetailView" in views_content
        assert "class PratiqueCreateView" in views_content
        assert "class PratiqueUpdateView" in views_content
        assert "class PratiqueDeleteView" in views_content
        assert "from django.views.generic" in views_content

    def test_generate_urls_content(self):
        """Test du contenu des URLs générées."""
        app_dir = generate_domaine_structure(
            app_name="pratique",
            model_name="Pratique",
            output_dir=str(self.output_dir),
        )

        urls_content = (Path(app_dir) / "urls.py").read_text(encoding="utf-8")
        assert 'app_name = "pratique"' in urls_content
        assert "PratiqueListView" in urls_content
        assert "PratiqueDetailView" in urls_content
        assert 'name="liste"' in urls_content
        assert 'name="detail"' in urls_content

    def test_generate_forms_content(self):
        """Test du contenu des formulaires générés."""
        app_dir = generate_domaine_structure(
            app_name="pratique",
            model_name="Pratique",
            output_dir=str(self.output_dir),
        )

        forms_content = (Path(app_dir) / "forms.py").read_text(encoding="utf-8")
        assert "class PratiqueForm" in forms_content
        assert "forms.ModelForm" in forms_content
        assert "model = Pratique" in forms_content

    def test_generate_admin_content(self):
        """Test du contenu de admin.py."""
        app_dir = generate_domaine_structure(
            app_name="pratique",
            model_name="Pratique",
            output_dir=str(self.output_dir),
        )

        admin_content = (Path(app_dir) / "admin.py").read_text(encoding="utf-8")
        assert "@admin.register(Pratique)" in admin_content
        assert "class PratiqueAdmin" in admin_content
        assert "from django.contrib import admin" in admin_content

    def test_generate_apps_content(self):
        """Test du contenu de apps.py."""
        app_dir = generate_domaine_structure(
            app_name="pratique",
            model_name="Pratique",
            output_dir=str(self.output_dir),
        )

        apps_content = (Path(app_dir) / "apps.py").read_text(encoding="utf-8")
        assert "class PratiqueConfig" in apps_content
        assert 'name = "pratique"' in apps_content

    def test_generate_file_exists_error(self):
        """Test avec un dossier existant."""
        existing_dir = self.output_dir / "pratique"
        existing_dir.mkdir()

        with pytest.raises(FileExistsError) as exc_info:
            generate_domaine_structure(
                app_name="pratique",
                model_name="Pratique",
                output_dir=str(self.output_dir),
            )

        assert "existe déjà" in str(exc_info.value)

    def test_generate_sanitize_app_name(self):
        """Test de la sanitization du nom d'app."""
        app_dir = generate_domaine_structure(
            app_name="test-app",
            model_name="TestModel",
            output_dir=str(self.output_dir),
        )

        # Le nom devrait être converti en test_app
        assert Path(app_dir).name == "test_app"

    def test_generate_templates_content(self):
        """Test du contenu des templates."""
        app_dir = generate_domaine_structure(
            app_name="pratique",
            model_name="Pratique",
            output_dir=str(self.output_dir),
        )

        liste_content = (
            Path(app_dir) / "templates" / "pratique" / "liste.html"
        ).read_text(encoding="utf-8")
        assert "Liste des Pratiques" in liste_content
        assert "{% url 'pratique:creer' %}" in liste_content

        detail_content = (
            Path(app_dir) / "templates" / "pratique" / "detail.html"
        ).read_text(encoding="utf-8")
        assert "Détails du Pratique" in detail_content
        assert "{{ pratique.id }}" in detail_content

        formulaire_content = (
            Path(app_dir) / "templates" / "pratique" / "formulaire.html"
        ).read_text(encoding="utf-8")
        assert "{% csrf_token %}" in formulaire_content
        assert "{{ form.as_p }}" in formulaire_content

    def test_generate_with_description(self):
        """Test avec une description personnalisée."""
        app_dir = generate_domaine_structure(
            app_name="pratique",
            model_name="Pratique",
            output_dir=str(self.output_dir),
            description="Application de gestion des pratiques",
        )

        assert Path(app_dir).exists()

    def test_generate_services_content(self):
        """Test du contenu de services.py."""
        app_dir = generate_domaine_structure(
            app_name="pratique",
            model_name="Pratique",
            output_dir=str(self.output_dir),
            include_services=True,
        )

        services_content = (Path(app_dir) / "services.py").read_text(encoding="utf-8")
        assert "from django.db import transaction" in services_content
        assert "def creer_pratique" in services_content
        assert "def modifier_pratique" in services_content
        assert "def supprimer_pratique" in services_content

    def test_generate_selectors_content(self):
        """Test du contenu de selectors.py."""
        app_dir = generate_domaine_structure(
            app_name="pratique",
            model_name="Pratique",
            output_dir=str(self.output_dir),
            include_selectors=True,
        )

        selectors_content = (Path(app_dir) / "selectors.py").read_text(encoding="utf-8")
        assert "from typing import Optional, List" in selectors_content
        assert "from django.db.models import QuerySet" in selectors_content
        assert "def obtenir_pratique_par_id" in selectors_content
        assert "def lister_pratiques" in selectors_content
        assert "def filtrer_pratiques" in selectors_content
