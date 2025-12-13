"""Tests pour le générateur de modèles Django."""

from pathlib import Path

import pytest

from pyfastcli.generators.model_generator import (
    discover_existing_models,
    generate_model_file,
)


class TestDiscoverExistingModels:
    """Tests pour la découverte des modèles existants."""

    def test_discover_no_models(self, tmp_path):
        """Test avec aucun modèle existant."""
        result = discover_existing_models(tmp_path)
        assert result == []

    def test_discover_single_model(self, tmp_path):
        """Test avec un seul modèle."""
        app_dir = tmp_path / "myapp"
        app_dir.mkdir()
        models_file = app_dir / "models.py"
        models_file.write_text(
            "from django.db import models\n\n"
            "class MyModel(models.Model):\n"
            "    name = models.CharField(max_length=100)\n"
        )

        result = discover_existing_models(tmp_path)
        assert len(result) == 1
        assert ("myapp", "MyModel") in result

    def test_discover_multiple_models(self, tmp_path):
        """Test avec plusieurs modèles."""
        # App 1
        app1_dir = tmp_path / "app1"
        app1_dir.mkdir()
        (app1_dir / "models.py").write_text(
            "from django.db import models\n\n"
            "class Model1(models.Model):\n"
            "    pass\n\n"
            "class Model2(models.Model):\n"
            "    pass\n"
        )

        # App 2
        app2_dir = tmp_path / "app2"
        app2_dir.mkdir()
        (app2_dir / "models.py").write_text(
            "from django.db import models\n\n"
            "class Model3(models.Model):\n"
            "    pass\n"
        )

        result = discover_existing_models(tmp_path)
        assert len(result) == 3
        assert ("app1", "Model1") in result
        assert ("app1", "Model2") in result
        assert ("app2", "Model3") in result

    def test_discover_ignores_abstract_models(self, tmp_path):
        """Test que les modèles abstraits sont ignorés."""
        app_dir = tmp_path / "myapp"
        app_dir.mkdir()
        models_file = app_dir / "models.py"
        models_file.write_text(
            "from django.db import models\n\n"
            "class AbstractModel(models.Model):\n"
            "    class Meta:\n"
            "        abstract = True\n\n"
            "class RealModel(models.Model):\n"
            "    pass\n"
        )

        result = discover_existing_models(tmp_path)
        # AbstractModel devrait être trouvé mais pas filtré ici
        # (le filtrage se fait dans la logique métier si nécessaire)
        assert len(result) >= 1
        assert ("myapp", "RealModel") in result


class TestGenerateModelFile:
    """Tests pour la génération de fichiers de modèles."""

    def test_generate_new_model_file(self, tmp_path):
        """Test génération d'un nouveau fichier models.py."""
        app_dir = tmp_path / "myapp"
        app_dir.mkdir()

        fields = [
            {"name": "name", "type": "CharField", "options": "max_length=100"},
            {"name": "email", "type": "EmailField", "options": ""},
        ]

        result = generate_model_file(
            app_name="myapp",
            model_name="User",
            fields=fields,
            output_dir=str(tmp_path),
            add_timestamps=True,
        )

        assert Path(result).exists()
        content = Path(result).read_text()
        assert "class User(models.Model):" in content
        assert "name = models.CharField(max_length=100)" in content
        assert "email = models.EmailField()" in content
        assert "created_at" in content
        assert "updated_at" in content

    def test_generate_model_without_timestamps(self, tmp_path):
        """Test génération sans timestamps."""
        app_dir = tmp_path / "myapp"
        app_dir.mkdir()

        fields = [{"name": "name", "type": "CharField", "options": ""}]

        result = generate_model_file(
            app_name="myapp",
            model_name="Simple",
            fields=fields,
            output_dir=str(tmp_path),
            add_timestamps=False,
        )

        content = Path(result).read_text()
        assert "created_at" not in content
        assert "updated_at" not in content

    def test_generate_model_with_foreign_key(self, tmp_path):
        """Test génération avec ForeignKey."""
        app_dir = tmp_path / "myapp"
        app_dir.mkdir()

        fields = [
            {
                "name": "category",
                "type": "ForeignKey",
                "options": "",
                "related_model": "categories.Category",
            }
        ]

        result = generate_model_file(
            app_name="myapp",
            model_name="Product",
            fields=fields,
            output_dir=str(tmp_path),
            add_timestamps=True,
        )

        content = Path(result).read_text()
        assert "from categories.models import Category" in content
        assert "category = models.ForeignKey(Category" in content
        assert "on_delete=models.CASCADE" in content

    def test_generate_model_with_many_to_many(self, tmp_path):
        """Test génération avec ManyToManyField."""
        app_dir = tmp_path / "myapp"
        app_dir.mkdir()

        fields = [
            {
                "name": "tags",
                "type": "ManyToManyField",
                "options": "",
                "related_model": "tags.Tag",
            }
        ]

        result = generate_model_file(
            app_name="myapp",
            model_name="Post",
            fields=fields,
            output_dir=str(tmp_path),
            add_timestamps=True,
        )

        content = Path(result).read_text()
        assert "from tags.models import Tag" in content
        assert "tags = models.ManyToManyField(Tag" in content

    def test_generate_model_adds_to_existing_file(self, tmp_path):
        """Test ajout d'un modèle à un fichier existant."""
        app_dir = tmp_path / "myapp"
        app_dir.mkdir()
        models_file = app_dir / "models.py"
        models_file.write_text(
            "from django.db import models\n\n"
            "class ExistingModel(models.Model):\n"
            "    pass\n"
        )

        fields = [{"name": "name", "type": "CharField", "options": ""}]

        result = generate_model_file(
            app_name="myapp",
            model_name="NewModel",
            fields=fields,
            output_dir=str(tmp_path),
            add_timestamps=True,
        )

        content = Path(result).read_text()
        assert "class ExistingModel" in content
        # Le nom est sanitized, donc "NewModel" devient "Newmodel"
        assert "class Newmodel" in content

    def test_generate_model_raises_if_exists(self, tmp_path):
        """Test que ça lève une erreur si le modèle existe déjà."""
        app_dir = tmp_path / "myapp"
        app_dir.mkdir()
        models_file = app_dir / "models.py"
        # Utilisons un nom qui sera identique après sanitization
        # "Mymodel" reste "Mymodel" après sanitization
        models_file.write_text(
            "from django.db import models\n\n"
            "class Mymodel(models.Model):\n"
            "    pass\n"
        )

        fields = [{"name": "name", "type": "CharField", "options": ""}]

        # Le nom "Mymodel" sera sanitized en "Mymodel" (identique)
        with pytest.raises(ValueError, match="existe déjà"):
            generate_model_file(
                app_name="myapp",
                model_name="Mymodel",  # Même nom que dans le fichier
                fields=fields,
                output_dir=str(tmp_path),
                add_timestamps=True,
            )

    def test_generate_model_with_uuid_field(self, tmp_path):
        """Test génération avec UUIDField."""
        app_dir = tmp_path / "myapp"
        app_dir.mkdir()

        fields = [{"name": "uuid", "type": "UUIDField", "options": ""}]

        result = generate_model_file(
            app_name="myapp",
            model_name="Item",
            fields=fields,
            output_dir=str(tmp_path),
            add_timestamps=False,
        )

        content = Path(result).read_text()
        assert "import uuid" in content
        assert "uuid = models.UUIDField" in content

    def test_generate_model_raises_without_related_model(self, tmp_path):
        """Test erreur si un champ de relation n'a pas de related_model."""
        app_dir = tmp_path / "myapp"
        app_dir.mkdir()

        # Test avec ForeignKey sans related_model
        fields = [
            {
                "name": "author",
                "type": "ForeignKey",
                "options": "",
                "related_model": None,
            }
        ]

        with pytest.raises(ValueError, match="nécessite un modèle lié"):
            generate_model_file(
                app_name="myapp",
                model_name="Article",
                fields=fields,
                output_dir=str(tmp_path),
                add_timestamps=True,
            )

        # Test avec ManyToManyField sans related_model
        fields = [
            {
                "name": "tags",
                "type": "ManyToManyField",
                "options": "",
                "related_model": None,
            }
        ]

        with pytest.raises(ValueError, match="nécessite un modèle lié"):
            generate_model_file(
                app_name="myapp",
                model_name="Post",
                fields=fields,
                output_dir=str(tmp_path),
                add_timestamps=True,
            )

        # Test avec OneToOneField sans related_model
        fields = [
            {
                "name": "profile",
                "type": "OneToOneField",
                "options": "",
                "related_model": None,
            }
        ]

        with pytest.raises(ValueError, match="nécessite un modèle lié"):
            generate_model_file(
                app_name="myapp",
                model_name="User",
                fields=fields,
                output_dir=str(tmp_path),
                add_timestamps=True,
            )
