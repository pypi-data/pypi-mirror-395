"""Tests pour le générateur de package Python."""

import shutil
import tempfile
from pathlib import Path

import pytest

from pyfastcli.generators.package_generator import (
    _sanitize_package_name,
    _sanitize_project_name,
    _validate_email,
    _validate_python_version,
    generate_package_structure,
)


class TestSanitizePackageName:
    """Tests pour la fonction _sanitize_package_name."""

    def test_simple_name(self):
        """Test avec un nom simple."""
        assert _sanitize_package_name("my_package") == "my_package"

    def test_name_with_dashes(self):
        """Test avec des tirets."""
        assert _sanitize_package_name("my-package") == "my_package"

    def test_name_with_spaces(self):
        """Test avec des espaces."""
        assert _sanitize_package_name("my package") == "my_package"

    def test_name_starting_with_digit(self):
        """Test avec un nom commençant par un chiffre."""
        assert _sanitize_package_name("123package") == "_123package"

    def test_name_with_special_chars(self):
        """Test avec des caractères spéciaux."""
        assert _sanitize_package_name("my@package#test") == "mypackagetest"

    def test_empty_name(self):
        """Test avec un nom vide."""
        assert _sanitize_package_name("") == "my_package"

    def test_mixed_case(self):
        """Test avec majuscules/minuscules."""
        assert _sanitize_package_name("MyPackage") == "mypackage"


class TestSanitizeProjectName:
    """Tests pour la fonction _sanitize_project_name."""

    def test_simple_name(self):
        """Test avec un nom simple."""
        assert _sanitize_project_name("my-package") == "my-package"

    def test_name_with_spaces(self):
        """Test avec des espaces."""
        assert _sanitize_project_name("my package") == "my-package"

    def test_name_with_underscores(self):
        """Test avec des underscores."""
        assert _sanitize_project_name("my_package") == "my_package"

    def test_empty_name(self):
        """Test avec un nom vide."""
        assert _sanitize_project_name("") == "my-package"

    def test_mixed_case(self):
        """Test avec majuscules/minuscules."""
        assert _sanitize_project_name("MyPackage") == "mypackage"


class TestValidateEmail:
    """Tests pour la fonction _validate_email."""

    def test_valid_email(self):
        """Test avec un email valide."""
        assert _validate_email("user@example.com") == "user@example.com"

    def test_email_with_spaces(self):
        """Test avec des espaces."""
        assert _validate_email("  user@example.com  ") == "user@example.com"

    def test_invalid_email_no_at(self):
        """Test avec un email sans @."""
        with pytest.raises(ValueError, match="Email invalide"):
            _validate_email("userexample.com")

    def test_invalid_email_empty(self):
        """Test avec un email vide."""
        with pytest.raises(ValueError, match="Email invalide"):
            _validate_email("")


class TestValidatePythonVersion:
    """Tests pour la fonction _validate_python_version."""

    def test_valid_version(self):
        """Test avec une version valide."""
        assert _validate_python_version("3.8") == "3.8"
        assert _validate_python_version("3.9") == "3.9"
        assert _validate_python_version("3.12") == "3.12"

    def test_version_with_spaces(self):
        """Test avec des espaces."""
        assert _validate_python_version("  3.8  ") == "3.8"

    def test_invalid_version_format(self):
        """Test avec un format invalide."""
        with pytest.raises(ValueError, match="Version Python invalide"):
            _validate_python_version("3")
        with pytest.raises(ValueError, match="Version Python invalide"):
            _validate_python_version("3.8.0")
        with pytest.raises(ValueError, match="Version Python invalide"):
            _validate_python_version("python3.8")


class TestGeneratePackageStructure:
    """Tests pour la fonction generate_package_structure."""

    def setup_method(self):
        """Configuration avant chaque test."""
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir)

    def teardown_method(self):
        """Nettoyage après chaque test."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_generate_basic_package(self):
        """Test génération d'un package de base."""
        package_dir = generate_package_structure(
            project_name="test-package",
            package_name="test_package",
            version="0.1.0",
            description="A test package",
            author_name="Test Author",
            author_email="test@example.com",
            python_version="3.8",
            license_type="MIT",
            output_dir=str(self.output_dir),
        )

        package_path = Path(package_dir)
        assert package_path.exists()
        assert package_path.name == "test-package"

        # Vérifier les fichiers essentiels
        assert (package_path / "pyproject.toml").exists()
        assert (package_path / "README.md").exists()
        assert (package_path / "LICENSE").exists()
        assert (package_path / ".gitignore").exists()
        assert (package_path / "test_package" / "__init__.py").exists()
        assert (package_path / "tests" / "__init__.py").exists()
        assert (package_path / "tests" / "test_test_package.py").exists()

    def test_generate_package_with_makefile(self):
        """Test génération avec Makefile."""
        package_dir = generate_package_structure(
            project_name="test-package",
            package_name="test_package",
            version="0.1.0",
            description="A test package",
            author_name="Test Author",
            author_email="test@example.com",
            python_version="3.8",
            license_type="MIT",
            output_dir=str(self.output_dir),
            include_makefile=True,
        )

        package_path = Path(package_dir)
        assert (package_path / "Makefile").exists()

    def test_generate_package_without_makefile(self):
        """Test génération sans Makefile."""
        package_dir = generate_package_structure(
            project_name="test-package",
            package_name="test_package",
            version="0.1.0",
            description="A test package",
            author_name="Test Author",
            author_email="test@example.com",
            python_version="3.8",
            license_type="MIT",
            output_dir=str(self.output_dir),
            include_makefile=False,
        )

        package_path = Path(package_dir)
        assert not (package_path / "Makefile").exists()

    def test_generate_package_with_manifest(self):
        """Test génération avec MANIFEST.in."""
        package_dir = generate_package_structure(
            project_name="test-package",
            package_name="test_package",
            version="0.1.0",
            description="A test package",
            author_name="Test Author",
            author_email="test@example.com",
            python_version="3.8",
            license_type="MIT",
            output_dir=str(self.output_dir),
            include_manifest=True,
        )

        package_path = Path(package_dir)
        assert (package_path / "MANIFEST.in").exists()

    def test_generate_package_with_setup_py(self):
        """Test génération avec setup.py."""
        package_dir = generate_package_structure(
            project_name="test-package",
            package_name="test_package",
            version="0.1.0",
            description="A test package",
            author_name="Test Author",
            author_email="test@example.com",
            python_version="3.8",
            license_type="MIT",
            output_dir=str(self.output_dir),
            include_setup_py=True,
        )

        package_path = Path(package_dir)
        assert (package_path / "setup.py").exists()

    def test_generate_package_with_dependencies(self):
        """Test génération avec dépendances."""
        package_dir = generate_package_structure(
            project_name="test-package",
            package_name="test_package",
            version="0.1.0",
            description="A test package",
            author_name="Test Author",
            author_email="test@example.com",
            python_version="3.8",
            license_type="MIT",
            output_dir=str(self.output_dir),
            dependencies=["requests>=2.0.0", "click>=8.0.0"],
        )

        package_path = Path(package_dir)
        pyproject_content = (package_path / "pyproject.toml").read_text(
            encoding="utf-8"
        )
        assert "requests>=2.0.0" in pyproject_content
        assert "click>=8.0.0" in pyproject_content

    def test_generate_package_with_dev_dependencies(self):
        """Test génération avec dépendances de développement."""
        package_dir = generate_package_structure(
            project_name="test-package",
            package_name="test_package",
            version="0.1.0",
            description="A test package",
            author_name="Test Author",
            author_email="test@example.com",
            python_version="3.8",
            license_type="MIT",
            output_dir=str(self.output_dir),
            dev_dependencies=["pytest>=7.0.0", "black>=23.0.0"],
        )

        package_path = Path(package_dir)
        pyproject_content = (package_path / "pyproject.toml").read_text(
            encoding="utf-8"
        )
        assert "pytest>=7.0.0" in pyproject_content
        assert "black>=23.0.0" in pyproject_content

    def test_generate_package_with_github_username(self):
        """Test génération avec nom d'utilisateur GitHub."""
        package_dir = generate_package_structure(
            project_name="test-package",
            package_name="test_package",
            version="0.1.0",
            description="A test package",
            author_name="Test Author",
            author_email="test@example.com",
            python_version="3.8",
            license_type="MIT",
            output_dir=str(self.output_dir),
            github_username="testuser",
        )

        package_path = Path(package_dir)
        pyproject_content = (package_path / "pyproject.toml").read_text(
            encoding="utf-8"
        )
        assert "github.com/testuser/test-package" in pyproject_content

    def test_generate_package_file_exists_error(self):
        """Test que FileExistsError est levée si le dossier existe."""
        # Créer le dossier d'abord
        existing_dir = self.output_dir / "test-package"
        existing_dir.mkdir()

        with pytest.raises(FileExistsError, match="existe déjà"):
            generate_package_structure(
                project_name="test-package",
                package_name="test_package",
                version="0.1.0",
                description="A test package",
                author_name="Test Author",
                author_email="test@example.com",
                python_version="3.8",
                license_type="MIT",
                output_dir=str(self.output_dir),
            )

    def test_generate_package_invalid_email(self):
        """Test avec un email invalide."""
        with pytest.raises(ValueError, match="Email invalide"):
            generate_package_structure(
                project_name="test-package",
                package_name="test_package",
                version="0.1.0",
                description="A test package",
                author_name="Test Author",
                author_email="invalid-email",
                python_version="3.8",
                license_type="MIT",
                output_dir=str(self.output_dir),
            )

    def test_generate_package_invalid_python_version(self):
        """Test avec une version Python invalide."""
        with pytest.raises(ValueError, match="Version Python invalide"):
            generate_package_structure(
                project_name="test-package",
                package_name="test_package",
                version="0.1.0",
                description="A test package",
                author_name="Test Author",
                author_email="test@example.com",
                python_version="3",
                license_type="MIT",
                output_dir=str(self.output_dir),
            )

    def test_generate_package_pyproject_content(self):
        """Test que le contenu de pyproject.toml est correct."""
        package_dir = generate_package_structure(
            project_name="test-package",
            package_name="test_package",
            version="0.2.0",
            description="A test package description",
            author_name="Test Author",
            author_email="test@example.com",
            python_version="3.9",
            license_type="MIT",
            output_dir=str(self.output_dir),
        )

        package_path = Path(package_dir)
        pyproject_content = (package_path / "pyproject.toml").read_text(
            encoding="utf-8"
        )

        assert 'name = "test-package"' in pyproject_content
        assert 'version = "0.2.0"' in pyproject_content
        assert 'description = "A test package description"' in pyproject_content
        assert 'requires-python = ">=3.9"' in pyproject_content
        assert 'name = "Test Author"' in pyproject_content
        assert 'email = "test@example.com"' in pyproject_content
        assert 'packages = ["test_package"]' in pyproject_content

    def test_generate_package_readme_content(self):
        """Test que le contenu de README.md est correct."""
        package_dir = generate_package_structure(
            project_name="test-package",
            package_name="test_package",
            version="0.1.0",
            description="A test package description",
            author_name="Test Author",
            author_email="test@example.com",
            python_version="3.8",
            license_type="MIT",
            output_dir=str(self.output_dir),
        )

        package_path = Path(package_dir)
        readme_content = (package_path / "README.md").read_text(encoding="utf-8")

        assert "# test-package" in readme_content
        assert "A test package description" in readme_content
        assert "pip install test-package" in readme_content
        assert "Test Author" in readme_content

    def test_generate_package_license_mit(self):
        """Test que la licence MIT est générée correctement."""
        package_dir = generate_package_structure(
            project_name="test-package",
            package_name="test_package",
            version="0.1.0",
            description="A test package",
            author_name="Test Author",
            author_email="test@example.com",
            python_version="3.8",
            license_type="MIT",
            output_dir=str(self.output_dir),
        )

        package_path = Path(package_dir)
        license_content = (package_path / "LICENSE").read_text(encoding="utf-8")

        assert "MIT License" in license_content
        assert "Test Author" in license_content

    def test_generate_package_init_content(self):
        """Test que le __init__.py est généré correctement."""
        package_dir = generate_package_structure(
            project_name="test-package",
            package_name="test_package",
            version="0.1.0",
            description="A test package",
            author_name="Test Author",
            author_email="test@example.com",
            python_version="3.8",
            license_type="MIT",
            output_dir=str(self.output_dir),
        )

        package_path = Path(package_dir)
        init_content = (package_path / "test_package" / "__init__.py").read_text(
            encoding="utf-8"
        )

        assert "__version__" in init_content
        assert "0.1.0" in init_content
        assert "test_package" in init_content

    def test_generate_package_sanitizes_names(self):
        """Test que les noms sont correctement nettoyés."""
        package_dir = generate_package_structure(
            project_name="My Test-Package!",
            package_name="my-test_package",
            version="0.1.0",
            description="A test package",
            author_name="Test Author",
            author_email="test@example.com",
            python_version="3.8",
            license_type="MIT",
            output_dir=str(self.output_dir),
        )

        package_path = Path(package_dir)
        # Le nom du projet devrait être nettoyé
        assert package_path.name == "my-test-package"
        # Le package devrait exister avec le nom nettoyé
        assert (package_path / "my_test_package").exists()

    def test_generate_package_creates_nested_directories(self):
        """Test que les dossiers imbriqués sont créés."""
        nested_output = self.output_dir / "nested" / "path"
        package_dir = generate_package_structure(
            project_name="test-package",
            package_name="test_package",
            version="0.1.0",
            description="A test package",
            author_name="Test Author",
            author_email="test@example.com",
            python_version="3.8",
            license_type="MIT",
            output_dir=str(nested_output),
        )

        package_path = Path(package_dir)
        assert package_path.exists()
        assert package_path.parent == nested_output
