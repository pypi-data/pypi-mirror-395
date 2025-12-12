import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from citrouille.kube_client import KubeClient

#
# test_kube_client.py
#
# Tests for kube_client.py
#


class TestKubeClient:
    #
    # test_init_default_config
    # Tests KubeClient initialization with default configuration (no kubeconfig or context specified)
    #
    @patch("citrouille.kube_client.config.load_kube_config")
    @patch("citrouille.kube_client.client.AppsV1Api")
    @patch("citrouille.kube_client.client.CoreV1Api")
    def test_init_default_config(self, mock_core_v1, mock_apps_v1, mock_load_config):
        k8s = KubeClient()
        mock_load_config.assert_called_once_with(context=None)
        assert k8s.kubeconfig is None
        assert k8s.context is None

    #
    # test_init_with_kubeconfig
    # Tests KubeClient initialization with a custom kubeconfig file path
    #
    @patch("citrouille.kube_client.config.load_kube_config")
    @patch("citrouille.kube_client.client.AppsV1Api")
    @patch("citrouille.kube_client.client.CoreV1Api")
    def test_init_with_kubeconfig(self, mock_core_v1, mock_apps_v1, mock_load_config):
        k8s = KubeClient(kubeconfig="/path/to/config")
        mock_load_config.assert_called_once_with(
            config_file="/path/to/config", context=None
        )
        assert k8s.kubeconfig == "/path/to/config"

    #
    # test_init_with_context
    # Tests KubeClient initialization with a specific Kubernetes context
    #
    @patch("citrouille.kube_client.config.load_kube_config")
    @patch("citrouille.kube_client.client.AppsV1Api")
    @patch("citrouille.kube_client.client.CoreV1Api")
    def test_init_with_context(self, mock_core_v1, mock_apps_v1, mock_load_config):
        k8s = KubeClient(context="my-context")
        mock_load_config.assert_called_once_with(context="my-context")
        assert k8s.context == "my-context"

    #
    # test_init_connection_error
    # Tests that KubeClient raises ConnectionError when Kubernetes connection fails
    #
    @patch("citrouille.kube_client.config.load_kube_config")
    @patch("citrouille.kube_client.client.AppsV1Api")
    @patch("citrouille.kube_client.client.CoreV1Api")
    def test_init_connection_error(self, mock_core_v1, mock_apps_v1, mock_load_config):
        mock_load_config.side_effect = Exception("Connection failed")
        with pytest.raises(ConnectionError, match="Failed to connect to Kubernetes"):
            KubeClient()

    #
    # test_get_namespaces
    # Tests retrieving list of all namespaces from Kubernetes cluster
    #
    @patch("citrouille.kube_client.config.load_kube_config")
    @patch("citrouille.kube_client.client.AppsV1Api")
    @patch("citrouille.kube_client.client.CoreV1Api")
    def test_get_namespaces(self, mock_core_v1_class, mock_apps_v1, mock_load_config):
        # Setup mock
        mock_core_v1 = Mock()
        mock_core_v1_class.return_value = mock_core_v1

        mock_ns1 = Mock()
        mock_ns1.metadata.name = "default"

        mock_ns2 = Mock()
        mock_ns2.metadata.name = "kube-system"

        mock_response = Mock()
        mock_response.items = [mock_ns1, mock_ns2]
        mock_core_v1.list_namespace.return_value = mock_response

        k8s = KubeClient()
        namespaces = k8s.get_namespaces()

        assert namespaces == ["default", "kube-system"]
        mock_core_v1.list_namespace.assert_called_once()

    #
    # test_get_deployments
    # Tests retrieving deployments from a specific namespace with single container
    #
    @patch("citrouille.kube_client.config.load_kube_config")
    @patch("citrouille.kube_client.client.AppsV1Api")
    @patch("citrouille.kube_client.client.CoreV1Api")
    def test_get_deployments(self, mock_core_v1, mock_apps_v1_class, mock_load_config):
        mock_apps_v1 = Mock()
        mock_apps_v1_class.return_value = mock_apps_v1

        mock_deployment = Mock()
        mock_deployment.metadata.name = "nginx"
        mock_deployment.metadata.namespace = "default"
        mock_deployment.metadata.creation_timestamp = datetime(2024, 11, 11, 10, 30, 0)
        mock_deployment.spec.replicas = 3

        mock_container = Mock()
        mock_container.image = "nginx:1.21"

        mock_deployment.spec.template.spec.containers = [mock_container]

        mock_response = Mock()
        mock_response.items = [mock_deployment]
        mock_apps_v1.list_namespaced_deployment.return_value = mock_response

        k8s = KubeClient()
        deployments = k8s.get_deployments(namespace="default")

        assert len(deployments) == 1
        assert deployments[0]["name"] == "nginx"
        assert deployments[0]["namespace"] == "default"
        assert deployments[0]["images"] == ["nginx:1.21"]
        assert deployments[0]["replicas"] == 3
        mock_apps_v1.list_namespaced_deployment.assert_called_once_with("default")

    #
    # test_get_deployments_multiple_containers
    # Tests retrieving deployments with multiple containers (main app + sidecar)
    #
    @patch("citrouille.kube_client.config.load_kube_config")
    @patch("citrouille.kube_client.client.AppsV1Api")
    @patch("citrouille.kube_client.client.CoreV1Api")
    def test_get_deployments_multiple_containers(
        self, mock_core_v1, mock_apps_v1_class, mock_load_config
    ):
        mock_apps_v1 = Mock()
        mock_apps_v1_class.return_value = mock_apps_v1

        mock_deployment = Mock()
        mock_deployment.metadata.name = "app"
        mock_deployment.metadata.namespace = "production"
        mock_deployment.metadata.creation_timestamp = datetime(2024, 11, 11, 10, 30, 0)
        mock_deployment.spec.replicas = 5

        mock_container1 = Mock()
        mock_container1.image = "app:v1.0"

        mock_container2 = Mock()
        mock_container2.image = "sidecar:v2.1"

        mock_deployment.spec.template.spec.containers = [
            mock_container1,
            mock_container2,
        ]

        mock_response = Mock()
        mock_response.items = [mock_deployment]
        mock_apps_v1.list_namespaced_deployment.return_value = mock_response

        k8s = KubeClient()
        deployments = k8s.get_deployments(namespace="production")

        assert len(deployments) == 1
        assert deployments[0]["images"] == ["app:v1.0", "sidecar:v2.1"]

    #
    # test_get_all_deployments
    # Tests retrieving all deployments across all namespaces in the cluster
    #
    @patch("citrouille.kube_client.config.load_kube_config")
    @patch("citrouille.kube_client.client.AppsV1Api")
    @patch("citrouille.kube_client.client.CoreV1Api")
    def test_get_all_deployments(
        self, mock_core_v1, mock_apps_v1_class, mock_load_config
    ):
        mock_apps_v1 = Mock()
        mock_apps_v1_class.return_value = mock_apps_v1

        mock_deployment1 = Mock()
        mock_deployment1.metadata.name = "nginx"
        mock_deployment1.metadata.namespace = "default"
        mock_deployment1.metadata.creation_timestamp = datetime(2024, 11, 11, 10, 30, 0)
        mock_deployment1.spec.replicas = 3
        mock_container1 = Mock()
        mock_container1.image = "nginx:1.21"
        mock_deployment1.spec.template.spec.containers = [mock_container1]

        mock_deployment2 = Mock()
        mock_deployment2.metadata.name = "redis"
        mock_deployment2.metadata.namespace = "cache"
        mock_deployment2.metadata.creation_timestamp = datetime(2024, 11, 10, 15, 45, 0)
        mock_deployment2.spec.replicas = 1
        mock_container2 = Mock()
        mock_container2.image = "redis:7.0"
        mock_deployment2.spec.template.spec.containers = [mock_container2]

        mock_response = Mock()
        mock_response.items = [mock_deployment1, mock_deployment2]
        mock_apps_v1.list_deployment_for_all_namespaces.return_value = mock_response

        k8s = KubeClient()
        deployments = k8s.get_all_deployments()

        assert len(deployments) == 2
        assert deployments[0]["name"] == "nginx"
        assert deployments[0]["namespace"] == "default"
        assert deployments[1]["name"] == "redis"
        assert deployments[1]["namespace"] == "cache"

        mock_apps_v1.list_deployment_for_all_namespaces.assert_called_once()

    #
    # test_get_deployments_none_replicas
    # Tests handling deployments where replica count is None (defaults to 0)
    #
    @patch("citrouille.kube_client.config.load_kube_config")
    @patch("citrouille.kube_client.client.AppsV1Api")
    @patch("citrouille.kube_client.client.CoreV1Api")
    def test_get_deployments_none_replicas(
        self, mock_core_v1, mock_apps_v1_class, mock_load_config
    ):
        mock_apps_v1 = Mock()
        mock_apps_v1_class.return_value = mock_apps_v1

        mock_deployment = Mock()
        mock_deployment.metadata.name = "test"
        mock_deployment.metadata.namespace = "default"
        mock_deployment.metadata.creation_timestamp = datetime(2024, 11, 11, 10, 30, 0)
        mock_deployment.spec.replicas = None

        mock_container = Mock()
        mock_container.image = "test:latest"
        mock_deployment.spec.template.spec.containers = [mock_container]

        mock_response = Mock()
        mock_response.items = [mock_deployment]
        mock_apps_v1.list_namespaced_deployment.return_value = mock_response

        k8s = KubeClient()
        deployments = k8s.get_deployments(namespace="default")

        assert deployments[0]["replicas"] == 0
