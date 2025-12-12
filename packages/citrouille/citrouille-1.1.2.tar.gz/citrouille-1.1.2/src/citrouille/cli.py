import argparse
import sys
from pathlib import Path

from citrouille.kube_client import KubeClient
from citrouille.formatters import TableFormatter, JSONFormatter, SecurityFormatter
from citrouille.comparator import compare_deployments
from citrouille.security_checks import run_security_checks
from citrouille.config import load_config, resolve_cluster


__version__ = "1.1.2"


def create_parser():
    parser = argparse.ArgumentParser(
        prog="citrouille",
        description="Kubernetes deployment inventory and security analysis tool",
        epilog="For more information, visit: https://github.com/Chelsea486MHz/citrouille",
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    parser.add_argument(
        "--kubeconfig",
        type=str,
        default=None,
        metavar="PATH",
        help="Path to kubeconfig file (default: ~/.kube/config)",
    )

    parser.add_argument(
        "--context",
        type=str,
        default=None,
        metavar="NAME",
        help="Kubernetes context to use (default: current-context)",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        choices=["table", "json"],
        default="table",
        metavar="FORMAT",
        help="Output format: table, json (default: table)",
    )

    subparsers = parser.add_subparsers(
        dest="command", help="Available commands", required=False
    )

    inventory_parser = subparsers.add_parser(
        "inventory",
        help="List deployments in a namespace",
        description="Generate an inventory of deployments with their images and timestamps",
    )

    inventory_parser.add_argument(
        "namespace",
        type=str,
        nargs="?",
        default="default",
        help="Target namespace (default: default)",
    )

    inventory_parser.add_argument(
        "-A",
        "--all-namespaces",
        action="store_true",
        help="List deployments across all namespaces",
    )

    compare_parser = subparsers.add_parser(
        "compare",
        help="Compare two namespaces",
        description="Compare deployments between two namespaces to identify drift",
    )

    compare_parser.add_argument("namespace1", type=str, help="First namespace (source)")

    compare_parser.add_argument(
        "namespace2", type=str, help="Second namespace (target)"
    )

    security_parser = subparsers.add_parser(
        "security",
        help="Perform security analysis",
        description="Analyze deployments for security vulnerabilities and misconfigurations",
    )

    security_parser.add_argument(
        "namespace",
        type=str,
        nargs="?",
        default="default",
        help="Target namespace (default: default)",
    )

    security_parser.add_argument(
        "--check-config",
        action="store_true",
        help="Perform configuration security checks",
    )

    security_parser.add_argument(
        "--check-network", action="store_true", help="Analyze network security"
    )

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Load configuration file
    config = load_config()

    # Apply kubeconfig from config if not provided via CLI
    if args.kubeconfig is None and "kubeconfig" in config:
        args.kubeconfig = config["kubeconfig"]

    # Validate kubeconfig path if provided
    if args.kubeconfig:
        kubeconfig_path = Path(args.kubeconfig).expanduser()
        if not kubeconfig_path.exists():
            print(
                f"Error: kubeconfig file not found: {args.kubeconfig}", file=sys.stderr
            )
            sys.exit(1)

    if args.command == "inventory":
        handle_inventory(args, config)
    elif args.command == "compare":
        handle_compare(args, config)
    elif args.command == "security":
        handle_security(args, config)


#
# Inventory generation
#
def handle_inventory(args, config):
    try:
        # Resolve cluster alias to get namespace and context
        if args.all_namespaces:
            # Use CLI context if provided, otherwise use default
            k8s = KubeClient(kubeconfig=args.kubeconfig, context=args.context)
            deployments = k8s.get_all_deployments()
        else:
            namespace, cluster_context = resolve_cluster(args.namespace, config)
            # CLI context takes precedence over cluster config context
            context = args.context if args.context else cluster_context
            k8s = KubeClient(kubeconfig=args.kubeconfig, context=context)
            deployments = k8s.get_deployments(namespace=namespace)

        if args.output == "json":
            output = JSONFormatter.format_deployments(deployments)
        else:
            output = TableFormatter.format_deployments(deployments)

        print(output)

    except ConnectionError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


#
# Comparison between namespaces
#
def handle_compare(args, config):
    try:
        # Resolve cluster aliases to get namespace and context for each
        namespace1, cluster_context1 = resolve_cluster(args.namespace1, config)
        namespace2, cluster_context2 = resolve_cluster(args.namespace2, config)

        # CLI context takes precedence over cluster config context
        # If CLI context is provided, it applies to both namespaces
        if args.context:
            context1 = args.context
            context2 = args.context
        else:
            context1 = cluster_context1
            context2 = cluster_context2

        # Create separate clients if contexts differ, otherwise reuse one client
        if context1 == context2:
            client = KubeClient(kubeconfig=args.kubeconfig, context=context1)
            deployments_ns1 = client.get_deployments(namespace1)
            deployments_ns2 = client.get_deployments(namespace2)
        else:
            client1 = KubeClient(kubeconfig=args.kubeconfig, context=context1)
            client2 = KubeClient(kubeconfig=args.kubeconfig, context=context2)
            deployments_ns1 = client1.get_deployments(namespace1)
            deployments_ns2 = client2.get_deployments(namespace2)

        comparison = compare_deployments(deployments_ns1, deployments_ns2)

        if args.output == "json":
            formatter = JSONFormatter()
            output = formatter.format_comparison(comparison, namespace1, namespace2)
        else:
            formatter = TableFormatter()
            output = formatter.format_comparison(comparison, namespace1, namespace2)

        print(output)

    except ConnectionError as e:
        print(f"Error: Unable to connect to Kubernetes cluster: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


#
# Security analysis
#
def handle_security(args, config):
    try:
        # Resolve cluster alias to get namespace and context
        namespace, cluster_context = resolve_cluster(args.namespace, config)

        # CLI context takes precedence over cluster config context
        context = args.context if args.context else cluster_context

        kube_client = KubeClient(kubeconfig=args.kubeconfig, context=context)

        check_config = args.check_config
        check_network = args.check_network

        # If no specific checks are specified, run all checks
        if not check_config and not check_network:
            check_config = True
            check_network = True

        findings = run_security_checks(
            kube_client=kube_client,
            namespace=namespace,
            check_config=check_config,
            check_network=check_network,
        )

        output = SecurityFormatter.format_findings(findings, args.output)
        print(output)

        critical_high = [
            f for f in findings if f.get("severity") in ["CRITICAL", "HIGH"]
        ]
        if critical_high:
            sys.exit(1)

    except ConnectionError as e:
        print(f"Error: Unable to connect to Kubernetes cluster: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
