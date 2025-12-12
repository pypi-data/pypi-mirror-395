import pytest
import tempfile
import yaml
from pathlib import Path
from unittest.mock import patch, mock_open

from citrouille.config import load_config, resolve_cluster, get_config_path


class TestConfigPath:
    #
    # test_get_config_path
    # Tests that config path is correctly constructed
    #
    def test_get_config_path(self):
        path = get_config_path()
        assert path == Path.home() / ".config" / "citrouille" / "config.yaml"
        assert isinstance(path, Path)


class TestLoadConfig:
    #
    # test_load_config_file_not_found
    # Tests that missing config file returns empty dict without error
    #
    def test_load_config_file_not_found(self):
        with patch("citrouille.config.get_config_path") as mock_path:
            mock_path.return_value = Path("/nonexistent/config.yaml")
            config = load_config()
            assert config == {}

    #
    # test_load_config_valid_yaml
    # Tests loading a valid YAML configuration file
    #
    def test_load_config_valid_yaml(self):
        valid_yaml = """
kubeconfig: /path/to/kubeconfig
clusters:
  prod:
    namespace: production
    context: prod-cluster
  stg:
    namespace: staging
    context: staging-cluster
"""
        with patch("citrouille.config.get_config_path") as mock_path:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".yaml", delete=False
            ) as f:
                f.write(valid_yaml)
                temp_path = Path(f.name)

            try:
                mock_path.return_value = temp_path
                config = load_config()

                assert config["kubeconfig"] == "/path/to/kubeconfig"
                assert config["clusters"]["prod"]["namespace"] == "production"
                assert config["clusters"]["prod"]["context"] == "prod-cluster"
                assert config["clusters"]["stg"]["namespace"] == "staging"
                assert config["clusters"]["stg"]["context"] == "staging-cluster"
            finally:
                temp_path.unlink()

    #
    # test_load_config_empty_file
    # Tests that empty YAML file returns empty dict
    #
    def test_load_config_empty_file(self):
        with patch("citrouille.config.get_config_path") as mock_path:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".yaml", delete=False
            ) as f:
                f.write("")
                temp_path = Path(f.name)

            try:
                mock_path.return_value = temp_path
                config = load_config()
                assert config == {}
            finally:
                temp_path.unlink()

    #
    # test_load_config_invalid_yaml
    # Tests that invalid YAML returns empty dict with warning
    #
    def test_load_config_invalid_yaml(self):
        invalid_yaml = """
kubeconfig: /path
  invalid: yaml: structure
    - broken
"""
        with patch("citrouille.config.get_config_path") as mock_path:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".yaml", delete=False
            ) as f:
                f.write(invalid_yaml)
                temp_path = Path(f.name)

            try:
                mock_path.return_value = temp_path
                config = load_config()
                assert config == {}
            finally:
                temp_path.unlink()

    #
    # test_load_config_non_dict_yaml
    # Tests that YAML with non-dict content returns empty dict
    #
    def test_load_config_non_dict_yaml(self):
        non_dict_yaml = """
- item1
- item2
- item3
"""
        with patch("citrouille.config.get_config_path") as mock_path:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".yaml", delete=False
            ) as f:
                f.write(non_dict_yaml)
                temp_path = Path(f.name)

            try:
                mock_path.return_value = temp_path
                config = load_config()
                assert config == {}
            finally:
                temp_path.unlink()


class TestResolveCluster:
    #
    # test_resolve_cluster_with_alias
    # Tests that cluster alias is correctly resolved to (namespace, context)
    #
    def test_resolve_cluster_with_alias(self):
        config = {
            "clusters": {
                "prod": {"namespace": "production", "context": "prod-cluster"},
                "stg": {"namespace": "staging", "context": "staging-cluster"},
            }
        }

        assert resolve_cluster("prod", config) == ("production", "prod-cluster")
        assert resolve_cluster("stg", config) == ("staging", "staging-cluster")

    #
    # test_resolve_cluster_without_alias
    # Tests that non-aliased cluster is returned as (namespace, None)
    #
    def test_resolve_cluster_without_alias(self):
        config = {
            "clusters": {"prod": {"namespace": "production", "context": "prod-cluster"}}
        }

        assert resolve_cluster("default", config) == ("default", None)
        assert resolve_cluster("kube-system", config) == ("kube-system", None)

    #
    # test_resolve_cluster_no_clusters_section
    # Tests that cluster is returned as (namespace, None) when no clusters section exists
    #
    def test_resolve_cluster_no_clusters_section(self):
        config = {"kubeconfig": "/path/to/config"}

        assert resolve_cluster("production", config) == ("production", None)
        assert resolve_cluster("default", config) == ("default", None)

    #
    # test_resolve_cluster_empty_config
    # Tests that cluster is returned as (namespace, None) with empty config
    #
    def test_resolve_cluster_empty_config(self):
        config = {}

        assert resolve_cluster("production", config) == ("production", None)
        assert resolve_cluster("default", config) == ("default", None)

    #
    # test_resolve_cluster_invalid_clusters_section
    # Tests that cluster is returned as (namespace, None) when clusters section is invalid
    #
    def test_resolve_cluster_invalid_clusters_section(self):
        config = {"clusters": "not-a-dict"}

        assert resolve_cluster("production", config) == ("production", None)

    #
    # test_resolve_cluster_case_sensitive
    # Tests that cluster alias resolution is case-sensitive
    #
    def test_resolve_cluster_case_sensitive(self):
        config = {
            "clusters": {"prod": {"namespace": "production", "context": "prod-cluster"}}
        }

        assert resolve_cluster("prod", config) == ("production", "prod-cluster")
        assert resolve_cluster("Prod", config) == ("Prod", None)
        assert resolve_cluster("PROD", config) == ("PROD", None)

    #
    # test_resolve_cluster_complex_aliases
    # Tests resolving complex cluster configurations
    #
    def test_resolve_cluster_complex_aliases(self):
        config = {
            "clusters": {
                "prod-east": {
                    "namespace": "microservices-production",
                    "context": "us-east-1-prod",
                },
                "prod-west": {
                    "namespace": "microservices-production",
                    "context": "us-west-2-prod",
                },
                "dev": {
                    "namespace": "microservices-development",
                    "context": "dev-cluster",
                },
            }
        }

        assert resolve_cluster("prod-east", config) == (
            "microservices-production",
            "us-east-1-prod",
        )
        assert resolve_cluster("prod-west", config) == (
            "microservices-production",
            "us-west-2-prod",
        )
        assert resolve_cluster("dev", config) == (
            "microservices-development",
            "dev-cluster",
        )

    #
    # test_resolve_cluster_only_namespace
    # Tests cluster config with only namespace field (no context)
    #
    def test_resolve_cluster_only_namespace(self):
        config = {
            "clusters": {
                "prod": {"namespace": "production"},
            }
        }

        assert resolve_cluster("prod", config) == ("production", None)

    #
    # test_resolve_cluster_only_context
    # Tests cluster config with only context field (namespace defaults to alias)
    #
    def test_resolve_cluster_only_context(self):
        config = {
            "clusters": {
                "prod": {"context": "prod-cluster"},
            }
        }

        assert resolve_cluster("prod", config) == ("prod", "prod-cluster")

    #
    # test_resolve_cluster_invalid_cluster_config
    # Tests that invalid cluster config returns (alias, None)
    #
    def test_resolve_cluster_invalid_cluster_config(self):
        config = {
            "clusters": {
                "prod": "not-a-dict",
            }
        }

        assert resolve_cluster("prod", config) == ("prod", None)
