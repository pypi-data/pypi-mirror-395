"""Tests pour le générateur de routes Django Ninja."""

import shutil
import tempfile
from pathlib import Path

import pytest

from pyfastcli.generators.ninja_routes import (
    _escape_string,
    _sanitize_func_name,
    _validate_http_method,
    _validate_url_path,
    generate_ninja_route_file,
)


class TestSanitizeFuncName:
    """Tests pour la fonction _sanitize_func_name."""

    def test_simple_name(self):
        """Test avec un nom simple."""
        assert _sanitize_func_name("get_orders") == "get_orders"

    def test_name_with_spaces(self):
        """Test avec des espaces."""
        assert _sanitize_func_name("get orders") == "get_orders"

    def test_name_with_dashes(self):
        """Test avec des tirets."""
        assert _sanitize_func_name("get-orders") == "get_orders"

    def test_name_starting_with_digit(self):
        """Test avec un nom commençant par un chiffre."""
        assert _sanitize_func_name("123orders") == "_123orders"

    def test_empty_name(self):
        """Test avec un nom vide."""
        assert _sanitize_func_name("") == "endpoint"
        assert _sanitize_func_name("   ") == "endpoint"

    def test_name_with_special_chars(self):
        """Test avec des caractères spéciaux."""
        assert _sanitize_func_name("get@orders#test") == "get_orders_test"

    def test_name_with_underscores(self):
        """Test avec des underscores existants."""
        assert _sanitize_func_name("get__orders") == "get__orders"


class TestValidateHttpMethod:
    """Tests pour la fonction _validate_http_method."""

    def test_valid_methods(self):
        """Test avec des méthodes valides."""
        assert _validate_http_method("get") == "get"
        assert _validate_http_method("POST") == "post"
        assert _validate_http_method("  Put  ") == "put"
        assert _validate_http_method("DELETE") == "delete"
        assert _validate_http_method("patch") == "patch"
        assert _validate_http_method("head") == "head"
        assert _validate_http_method("options") == "options"

    def test_invalid_method(self):
        """Test avec une méthode invalide."""
        with pytest.raises(ValueError, match="Méthode HTTP invalide"):
            _validate_http_method("invalid")

    def test_case_insensitive(self):
        """Test que la validation est insensible à la casse."""
        assert _validate_http_method("GET") == "get"
        assert _validate_http_method("Post") == "post"


class TestValidateUrlPath:
    """Tests pour la fonction _validate_url_path."""

    def test_path_with_slash(self):
        """Test avec un chemin commençant par /."""
        assert _validate_url_path("/orders") == "/orders"

    def test_path_without_slash(self):
        """Test avec un chemin sans / initial."""
        assert _validate_url_path("orders") == "/orders"

    def test_path_with_spaces(self):
        """Test avec des espaces."""
        assert _validate_url_path("  /orders  ") == "/orders"

    def test_empty_path(self):
        """Test avec un chemin vide."""
        assert _validate_url_path("") == "/"


class TestEscapeString:
    """Tests pour la fonction _escape_string."""

    def test_string_with_double_quotes(self):
        """Test avec des guillemets doubles."""
        assert _escape_string('test"value') == 'test\\"value'

    def test_string_with_single_quotes(self):
        """Test avec des guillemets simples."""
        assert _escape_string("test'value") == "test\\'value"

    def test_string_with_both_quotes(self):
        """Test avec les deux types de guillemets."""
        result = _escape_string("test\"value'other")
        assert '"' not in result or result.count('\\"') > 0
        assert "'" not in result or result.count("\\'") > 0

    def test_normal_string(self):
        """Test avec une chaîne normale."""
        assert _escape_string("normal_string") == "normal_string"


class TestGenerateNinjaRouteFile:
    """Tests pour la fonction generate_ninja_route_file."""

    def setup_method(self):
        """Configuration avant chaque test."""
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir) / "routes"

    def teardown_method(self):
        """Nettoyage après chaque test."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_generate_get_route(self):
        """Test génération d'une route GET."""
        file_path = generate_ninja_route_file(
            module_name="api",
            function_name="get_orders",
            url_path="/orders",
            http_method="get",
            tag="Orders",
            output_dir=str(self.output_dir),
        )

        assert Path(file_path).exists()
        assert Path(file_path).name == "get_orders.py"

        content = Path(file_path).read_text(encoding="utf-8")
        assert "from ninja import Router" in content
        assert 'router = Router(tags=["Orders"])' in content
        assert '@router.get("/orders")' in content
        assert "def get_orders(request):" in content

    def test_generate_post_route(self):
        """Test génération d'une route POST."""
        file_path = generate_ninja_route_file(
            module_name="api",
            function_name="create_order",
            url_path="/orders",
            http_method="post",
            tag="Orders",
            output_dir=str(self.output_dir),
        )

        content = Path(file_path).read_text(encoding="utf-8")
        assert '@router.post("/orders")' in content
        assert "def create_order(request):" in content

    def test_generate_route_with_description(self):
        """Test génération avec description."""
        file_path = generate_ninja_route_file(
            module_name="api",
            function_name="get_order",
            url_path="/orders/{id}",
            http_method="get",
            tag="Orders",
            output_dir=str(self.output_dir),
            description="Récupère une commande par ID",
        )

        content = Path(file_path).read_text(encoding="utf-8")
        assert "Récupère une commande par ID" in content

    def test_generate_route_without_description(self):
        """Test génération sans description."""
        file_path = generate_ninja_route_file(
            module_name="api",
            function_name="get_items",
            url_path="/items",
            http_method="get",
            tag="Items",
            output_dir=str(self.output_dir),
        )

        content = Path(file_path).read_text(encoding="utf-8")
        assert "Endpoint get_items" in content

    def test_generate_route_creates_directory(self):
        """Test que le dossier est créé s'il n'existe pas."""
        new_dir = self.output_dir / "subdir"
        assert not new_dir.exists()

        generate_ninja_route_file(
            module_name="api",
            function_name="test",
            url_path="/test",
            http_method="get",
            tag="Test",
            output_dir=str(new_dir),
        )

        assert new_dir.exists()

    def test_generate_route_file_exists_error(self):
        """Test que FileExistsError est levée si le fichier existe."""
        # Créer le fichier d'abord
        file_path = self.output_dir / "existing.py"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text("existing content")

        with pytest.raises(FileExistsError, match="existe déjà"):
            generate_ninja_route_file(
                module_name="api",
                function_name="existing",
                url_path="/test",
                http_method="get",
                tag="Test",
                output_dir=str(self.output_dir),
            )

    def test_generate_route_invalid_method(self):
        """Test avec une méthode HTTP invalide."""
        with pytest.raises(ValueError, match="Méthode HTTP invalide"):
            generate_ninja_route_file(
                module_name="api",
                function_name="test",
                url_path="/test",
                http_method="invalid",
                tag="Test",
                output_dir=str(self.output_dir),
            )

    def test_generate_route_sanitizes_function_name(self):
        """Test que le nom de fonction est nettoyé."""
        file_path = generate_ninja_route_file(
            module_name="api",
            function_name="get-orders test",
            url_path="/orders",
            http_method="get",
            tag="Orders",
            output_dir=str(self.output_dir),
        )

        assert Path(file_path).name == "get_orders_test.py"
        content = Path(file_path).read_text(encoding="utf-8")
        assert "def get_orders_test(request):" in content

    def test_generate_route_normalizes_url_path(self):
        """Test que le chemin d'URL est normalisé."""
        file_path = generate_ninja_route_file(
            module_name="api",
            function_name="test",
            url_path="orders",  # Sans le / initial
            http_method="get",
            tag="Orders",
            output_dir=str(self.output_dir),
        )

        content = Path(file_path).read_text(encoding="utf-8")
        assert '@router.get("/orders")' in content

    def test_generate_route_all_methods(self):
        """Test génération avec toutes les méthodes HTTP."""
        methods = ["get", "post", "put", "delete", "patch", "head", "options"]

        for method in methods:
            file_path = generate_ninja_route_file(
                module_name="api",
                function_name=f"test_{method}",
                url_path=f"/test/{method}",
                http_method=method,
                tag="Test",
                output_dir=str(self.output_dir),
            )

            content = Path(file_path).read_text(encoding="utf-8")
            assert f"@router.{method}(" in content

    def test_generate_route_escapes_special_chars(self):
        """Test que les caractères spéciaux sont échappés."""
        file_path = generate_ninja_route_file(
            module_name="api",
            function_name="test",
            url_path='/test"path',
            http_method="get",
            tag='Test"Tag',
            output_dir=str(self.output_dir),
            description='Test "description"',
        )

        content = Path(file_path).read_text(encoding="utf-8")
        # Vérifier que les guillemets sont échappés
        assert (
            '\\"' in content or content.count('"') <= 2
        )  # Seulement les guillemets du code
