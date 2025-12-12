import pytest
from io import StringIO
from unittest.mock import patch, Mock
from datetime import datetime

from citrouille.cli import create_parser, main


class TestArgumentParser:
    #
    # test_parser_creation
    # Tests that the argument parser is created with correct program name
    #
    def test_parser_creation(self):
        parser = create_parser()
        assert parser is not None
        assert parser.prog == "citrouille"

    #
    # test_version_argument
    # Tests that --version flag exits successfully
    #
    def test_version_argument(self):
        parser = create_parser()
        with pytest.raises(SystemExit) as exc_info:
            parser.parse_args(["--version"])
        assert exc_info.value.code == 0

    #
    # test_help_argument
    # Tests that --help flag exits successfully
    #
    def test_help_argument(self):
        parser = create_parser()
        with pytest.raises(SystemExit) as exc_info:
            parser.parse_args(["--help"])
        assert exc_info.value.code == 0

    #
    # test_no_command_shows_help
    # Tests that running without a command displays help and exits
    #
    def test_no_command_shows_help(self):
        with patch("sys.argv", ["citrouille"]):
            with patch("sys.stdout", new_callable=StringIO):
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 0


class TestGlobalOptions:
    #
    # test_kubeconfig_option
    # Tests parsing of --kubeconfig global option
    #
    def test_kubeconfig_option(self):
        parser = create_parser()
        args = parser.parse_args(["--kubeconfig", "/path/to/config", "inventory"])
        assert args.kubeconfig == "/path/to/config"

    #
    # test_context_option
    # Tests parsing of --context global option
    #
    def test_context_option(self):
        parser = create_parser()
        args = parser.parse_args(["--context", "my-context", "inventory"])
        assert args.context == "my-context"

    #
    # test_output_option_table
    # Tests parsing of -o table output option
    #
    def test_output_option_table(self):
        parser = create_parser()
        args = parser.parse_args(["-o", "table", "inventory"])
        assert args.output == "table"

    #
    # test_output_option_json
    # Tests parsing of --output json option
    #
    def test_output_option_json(self):
        parser = create_parser()
        args = parser.parse_args(["--output", "json", "inventory"])
        assert args.output == "json"

    #
    # test_output_default
    # Tests that output format defaults to table
    #
    def test_output_default(self):
        parser = create_parser()
        args = parser.parse_args(["inventory"])
        assert args.output == "table"

    #
    # test_invalid_output_format
    # Tests that invalid output format causes parser to exit
    #
    def test_invalid_output_format(self):
        parser = create_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["--output", "yaml", "inventory"])


class TestInventoryCommand:
    #
    # test_inventory_command
    # Tests parsing of basic inventory command
    #
    def test_inventory_command(self):
        parser = create_parser()
        args = parser.parse_args(["inventory"])
        assert args.command == "inventory"
        assert args.namespace == "default"
        assert args.all_namespaces is False

    #
    # test_inventory_with_namespace
    # Tests inventory command with custom namespace argument
    #
    def test_inventory_with_namespace(self):
        parser = create_parser()
        args = parser.parse_args(["inventory", "production"])
        assert args.command == "inventory"
        assert args.namespace == "production"

    #
    # test_inventory_all_namespaces
    # Tests inventory command with -A flag for all namespaces
    #
    def test_inventory_all_namespaces(self):
        parser = create_parser()
        args = parser.parse_args(["inventory", "-A"])
        assert args.command == "inventory"
        assert args.all_namespaces is True

    #
    # test_inventory_all_namespaces_long
    # Tests inventory command with --all-namespaces flag
    #
    def test_inventory_all_namespaces_long(self):
        parser = create_parser()
        args = parser.parse_args(["inventory", "--all-namespaces"])
        assert args.command == "inventory"
        assert args.all_namespaces is True

    #
    # test_inventory_with_global_options
    # Tests inventory command combined with multiple global options
    #
    def test_inventory_with_global_options(self):
        parser = create_parser()
        args = parser.parse_args(
            [
                "--kubeconfig",
                "/custom/config",
                "--context",
                "prod-cluster",
                "-o",
                "json",
                "inventory",
                "kube-system",
            ]
        )
        assert args.command == "inventory"
        assert args.namespace == "kube-system"
        assert args.kubeconfig == "/custom/config"
        assert args.context == "prod-cluster"
        assert args.output == "json"

    #
    # test_inventory_help
    # Tests that inventory --help exits successfully
    #
    def test_inventory_help(self):
        parser = create_parser()
        with pytest.raises(SystemExit) as exc_info:
            parser.parse_args(["inventory", "--help"])
        assert exc_info.value.code == 0


class TestCompareCommand:
    #
    # test_compare_command
    # Tests parsing of basic compare command with two namespaces
    #
    def test_compare_command(self):
        parser = create_parser()
        args = parser.parse_args(["compare", "production", "staging"])
        assert args.command == "compare"
        assert args.namespace1 == "production"
        assert args.namespace2 == "staging"

    #
    # test_compare_requires_two_namespaces
    # Tests that compare command requires both namespace arguments
    #
    def test_compare_requires_two_namespaces(self):
        parser = create_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["compare", "production"])

    #
    # test_compare_with_global_options
    # Tests compare command combined with global options
    #
    def test_compare_with_global_options(self):
        parser = create_parser()
        args = parser.parse_args(
            ["--kubeconfig", "/custom/config", "-o", "json", "compare", "ns1", "ns2"]
        )
        assert args.command == "compare"
        assert args.namespace1 == "ns1"
        assert args.namespace2 == "ns2"
        assert args.kubeconfig == "/custom/config"
        assert args.output == "json"

    #
    # test_compare_help
    # Tests that compare --help exits successfully
    #
    def test_compare_help(self):
        parser = create_parser()
        with pytest.raises(SystemExit) as exc_info:
            parser.parse_args(["compare", "--help"])
        assert exc_info.value.code == 0


class TestSecurityCommand:
    #
    # test_security_command_default
    # Tests parsing of basic security command with default values
    #
    def test_security_command_default(self):
        parser = create_parser()
        args = parser.parse_args(["security"])
        assert args.command == "security"
        assert args.namespace == "default"
        assert args.check_config is False
        assert args.check_network is False

    #
    # test_security_with_namespace
    # Tests security command with custom namespace argument
    #
    def test_security_with_namespace(self):
        parser = create_parser()
        args = parser.parse_args(["security", "production"])
        assert args.command == "security"
        assert args.namespace == "production"

    #
    # test_security_check_config
    # Tests security command with --check-config flag
    #
    def test_security_check_config(self):
        parser = create_parser()
        args = parser.parse_args(["security", "--check-config"])
        assert args.check_config is True

    #
    # test_security_check_network
    # Tests security command with --check-network flag
    #
    def test_security_check_network(self):
        parser = create_parser()
        args = parser.parse_args(["security", "--check-network"])
        assert args.check_network is True

    #
    # test_security_all_flags
    # Tests security command with all security flags enabled
    #
    def test_security_all_flags(self):
        parser = create_parser()
        args = parser.parse_args(
            [
                "security",
                "production",
                "--check-config",
                "--check-network",
            ]
        )
        assert args.command == "security"
        assert args.namespace == "production"
        assert args.check_config is True
        assert args.check_network is True

    #
    # test_security_with_global_options
    # Tests security command combined with global options
    #
    def test_security_with_global_options(self):
        parser = create_parser()
        args = parser.parse_args(
            [
                "--context",
                "prod",
                "-o",
                "json",
                "security",
                "kube-system",
                "--check-config",
            ]
        )
        assert args.command == "security"
        assert args.namespace == "kube-system"
        assert args.context == "prod"
        assert args.output == "json"
        assert args.check_config is True

    #
    # test_security_help
    # Tests that security --help exits successfully
    #
    def test_security_help(self):
        parser = create_parser()
        with pytest.raises(SystemExit) as exc_info:
            parser.parse_args(["security", "--help"])
        assert exc_info.value.code == 0


class TestMainFunction:
    #
    # test_main_with_nonexistent_kubeconfig
    # Tests that main exits with error when kubeconfig file doesn't exist
    #
    def test_main_with_nonexistent_kubeconfig(self):
        with patch(
            "sys.argv", ["citrouille", "--kubeconfig", "/nonexistent/path", "inventory"]
        ):
            with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 1
                assert "kubeconfig file not found" in mock_stderr.getvalue()

    #
    # test_main_inventory_table_output
    # Tests main function executing inventory command with table output
    #
    @patch("citrouille.cli.KubeClient")
    def test_main_inventory_table_output(self, mock_kube_client):
        mock_k8s = Mock()
        mock_kube_client.return_value = mock_k8s
        mock_k8s.get_deployments.return_value = [
            {
                "name": "nginx",
                "namespace": "default",
                "images": ["nginx:1.21"],
                "created": datetime(2024, 11, 11, 10, 30, 0),
                "replicas": 3,
            }
        ]
        with patch("sys.argv", ["citrouille", "inventory", "default"]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                assert "nginx" in output
                assert "default" in output
                assert "nginx:1.21" in output

    #
    # test_main_inventory_json_output
    # Tests main function executing inventory command with JSON output
    #
    @patch("citrouille.cli.KubeClient")
    def test_main_inventory_json_output(self, mock_kube_client):
        mock_k8s = Mock()
        mock_kube_client.return_value = mock_k8s
        mock_k8s.get_deployments.return_value = [
            {
                "name": "nginx",
                "namespace": "default",
                "images": ["nginx:1.21"],
                "created": datetime(2024, 11, 11, 10, 30, 0),
                "replicas": 3,
            }
        ]
        with patch("sys.argv", ["citrouille", "-o", "json", "inventory", "default"]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                assert '"name": "nginx"' in output
                assert '"namespace": "default"' in output

    #
    # test_main_inventory_all_namespaces
    # Tests main function executing inventory with -A flag
    #
    @patch("citrouille.cli.KubeClient")
    def test_main_inventory_all_namespaces(self, mock_kube_client):
        mock_k8s = Mock()
        mock_kube_client.return_value = mock_k8s
        mock_k8s.get_all_deployments.return_value = []
        with patch("sys.argv", ["citrouille", "inventory", "-A"]):
            main()
            mock_k8s.get_all_deployments.assert_called_once()

    #
    # test_main_inventory_connection_error
    # Tests that main handles connection errors gracefully
    #
    @patch("citrouille.cli.KubeClient")
    def test_main_inventory_connection_error(self, mock_kube_client):
        mock_kube_client.side_effect = ConnectionError("Failed to connect")
        with patch("sys.argv", ["citrouille", "inventory"]):
            with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 1
                assert "Error:" in mock_stderr.getvalue()

    #
    # test_main_compare_table_output
    # Tests main function executing compare command with table output
    #
    @patch("citrouille.cli.KubeClient")
    def test_main_compare_table_output(self, mock_kube_client):
        mock_k8s = Mock()
        mock_kube_client.return_value = mock_k8s

        ns1_deployments = [
            {
                "name": "nginx",
                "namespace": "ns1",
                "images": ["nginx:1.21"],
                "created": datetime(2024, 11, 11, 10, 30, 0),
                "replicas": 3,
            }
        ]
        ns2_deployments = [
            {
                "name": "nginx",
                "namespace": "ns2",
                "images": ["nginx:1.22"],
                "created": datetime(2024, 11, 11, 10, 30, 0),
                "replicas": 3,
            }
        ]

        mock_k8s.get_deployments.side_effect = [ns1_deployments, ns2_deployments]

        with patch("sys.argv", ["citrouille", "compare", "ns1", "ns2"]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                assert "Comparing namespaces" in output
                assert "ns1" in output
                assert "ns2" in output
                assert "[~] Changed" in output

    #
    # test_main_compare_json_output
    # Tests main function executing compare command with JSON output
    #
    @patch("citrouille.cli.KubeClient")
    def test_main_compare_json_output(self, mock_kube_client):
        mock_k8s = Mock()
        mock_kube_client.return_value = mock_k8s

        ns1_deployments = [
            {
                "name": "app1",
                "namespace": "ns1",
                "images": ["app:v1"],
                "created": datetime(2024, 11, 11, 10, 30, 0),
                "replicas": 2,
            }
        ]
        ns2_deployments = []

        mock_k8s.get_deployments.side_effect = [ns1_deployments, ns2_deployments]

        with patch("sys.argv", ["citrouille", "-o", "json", "compare", "ns1", "ns2"]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                assert '"namespace1": "ns1"' in output
                assert '"namespace2": "ns2"' in output
                assert '"missing"' in output
                assert '"summary"' in output

    #
    # test_main_compare_connection_error
    # Tests that compare command handles connection errors gracefully
    #
    @patch("citrouille.cli.KubeClient")
    def test_main_compare_connection_error(self, mock_kube_client):
        mock_kube_client.side_effect = ConnectionError("Failed to connect")

        with patch("sys.argv", ["citrouille", "compare", "ns1", "ns2"]):
            with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 1
                assert "Error:" in mock_stderr.getvalue()

    #
    # test_main_compare_identical_namespaces
    # Tests compare command output when namespaces have identical deployments
    #
    @patch("citrouille.cli.KubeClient")
    def test_main_compare_identical_namespaces(self, mock_kube_client):
        mock_k8s = Mock()
        mock_kube_client.return_value = mock_k8s

        identical_deployments = [
            {
                "name": "app1",
                "namespace": "production",
                "images": ["app:v1"],
                "created": datetime(2024, 11, 11, 10, 30, 0),
                "replicas": 3,
            }
        ]

        mock_k8s.get_deployments.side_effect = [
            identical_deployments,
            identical_deployments,
        ]

        with patch("sys.argv", ["citrouille", "compare", "production", "staging"]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                assert "No differences found" in output

    #
    # test_main_security_placeholder
    # Tests that security command shows placeholder message
    #
    def test_main_security_no_findings(self):
        with patch("sys.argv", ["citrouille", "security"]):
            with patch("citrouille.cli.KubeClient") as mock_client:
                with patch("citrouille.cli.run_security_checks") as mock_checks:
                    # Mock empty findings (no security issues)
                    mock_checks.return_value = []
                    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                        main()
                        output = mock_stdout.getvalue()
                        assert "No security issues found" in output
