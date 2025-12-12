from typing import List, Dict, Any
from .check_01_privileged_containers import check as check_privileged
from .check_02_host_pid import check as check_host_pid
from .check_03_host_ipc import check as check_host_ipc
from .check_04_host_network import check as check_host_network
from .check_05_run_as_root import check as check_run_as_root
from .check_06_privilege_escalation import check as check_privilege_escalation
from .check_07_capabilities import check as check_capabilities
from .check_08_resource_limits import check as check_resource_limits
from .check_09_host_path import check as check_host_path
from .check_10_readonly_filesystem import check as check_readonly_filesystem
from .check_11_seccomp import check as check_seccomp
from .check_12_service_account_token import check as check_service_account_token
from .check_13_image_tags import check as check_image_tags
from .check_14_hardcoded_secrets import check as check_hardcoded_secrets
from .check_15_pss_enforcement import check as check_pss_enforcement
from .check_16_immutable_config import check as check_immutable_config
from .check_17_emptydir_limits import check as check_emptydir_limits
from .check_18_proc_mount import check as check_proc_mount
from .check_19_rbac_roles import check as check_rbac_roles
from .check_20_rbac_bindings import check as check_rbac_bindings
from .check_21_shared_process_ns import check as check_shared_process_ns
from .check_22_sysctls import check as check_sysctls
from .check_23_network_policies import check as check_network_policies

#
# __init__.py
#
# Main entry point for security checks module
#


def run_security_checks(
    kube_client: Any,
    namespace: str = "default",
    check_config: bool = False,
    check_network: bool = False,
) -> List[Dict[str, Any]]:
    findings = []

    if check_config:
        deployments = kube_client.get_raw_deployments(namespace)
        namespace_obj = kube_client.get_namespace_details(namespace)
        config_maps = kube_client.get_config_maps(namespace)
        secrets = kube_client.get_secrets(namespace)
        roles = kube_client.get_roles(namespace)
        cluster_roles = kube_client.get_cluster_roles()
        role_bindings = kube_client.get_role_bindings(namespace)
        cluster_role_bindings = kube_client.get_cluster_role_bindings()

        findings.extend(check_privileged(deployments))
        findings.extend(check_host_pid(deployments))
        findings.extend(check_host_ipc(deployments))
        findings.extend(check_host_network(deployments))
        findings.extend(check_run_as_root(deployments))
        findings.extend(check_privilege_escalation(deployments))
        findings.extend(check_capabilities(deployments))
        findings.extend(check_resource_limits(deployments))
        findings.extend(check_host_path(deployments))
        findings.extend(check_readonly_filesystem(deployments))
        findings.extend(check_seccomp(deployments))
        findings.extend(check_service_account_token(deployments))
        findings.extend(check_image_tags(deployments))
        findings.extend(check_hardcoded_secrets(deployments))
        findings.extend(check_pss_enforcement(namespace_obj))
        findings.extend(check_immutable_config(config_maps, secrets))
        findings.extend(check_emptydir_limits(deployments))
        findings.extend(check_proc_mount(deployments))
        findings.extend(check_rbac_roles(roles, cluster_roles))
        findings.extend(check_rbac_bindings(role_bindings, cluster_role_bindings))
        findings.extend(check_shared_process_ns(deployments))
        findings.extend(check_sysctls(deployments))

    if check_network:
        network_policies = kube_client.get_network_policies(namespace)
        findings.extend(check_network_policies(network_policies, namespace))

    return findings
