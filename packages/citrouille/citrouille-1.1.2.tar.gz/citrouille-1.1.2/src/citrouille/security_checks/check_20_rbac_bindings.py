from typing import List, Dict, Any

#
# check_rbac_bindings.py
#
# Check #20: Misconfigured RoleBinding or ClusterRoleBinding
# CWE-269: Improper Privilege Management
#

# Security check metadata
CHECK_ID = "20"
CHECK_NAME = "Misconfigured RBAC binding"
CWE = "CWE-269"
SEVERITY_CRITICAL = "CRITICAL"
SEVERITY_HIGH = "HIGH"

# Issue and remediation details
DETAILS_CLUSTER_ADMIN = (
    "The cluster-admin role goes against the principle of least privilege."
)
DETAILS_ANONYMOUS = "Granting permissions to {subject_name} allows unauthorized access."
DETAILS_AUTHENTICATED = "The system:authenticated group includes all authenticated users, going against the principle of least privilege."


def check(
    role_bindings: List[Any], cluster_role_bindings: List[Any]
) -> List[Dict[str, Any]]:
    findings = []

    # Check RoleBindings
    for binding in role_bindings:
        findings.extend(_check_binding(binding, "RoleBinding"))

    # Check ClusterRoleBindings
    for binding in cluster_role_bindings:
        findings.extend(_check_binding(binding, "ClusterRoleBinding"))

    return findings


def _check_binding(binding: Any, binding_type: str) -> List[Dict[str, Any]]:
    findings = []
    binding_name = binding.metadata.name
    namespace = (
        binding.metadata.namespace if binding_type == "RoleBinding" else "cluster-wide"
    )

    # Check if binding to cluster-admin
    if binding.role_ref.name == "cluster-admin":
        findings.append(
            {
                "severity": SEVERITY_CRITICAL,
                "resource_type": binding_type,
                "resource_name": f"{namespace}/{binding_name}",
                "container": "N/A",
                "check_id": CHECK_ID,
                "check_name": CHECK_NAME,
                "cwe": CWE,
                "message": f"{binding_type} '{binding_name}' grants cluster-admin role",
                "details": DETAILS_CLUSTER_ADMIN,
            }
        )

    # Check subjects
    if binding.subjects:
        for subject in binding.subjects:
            subject_name = subject.name

            # Check for anonymous or unauthenticated users
            if subject_name in ["system:anonymous", "system:unauthenticated"]:
                findings.append(
                    {
                        "severity": SEVERITY_CRITICAL,
                        "resource_type": binding_type,
                        "resource_name": f"{namespace}/{binding_name}",
                        "container": "N/A",
                        "check_id": CHECK_ID,
                        "check_name": CHECK_NAME,
                        "cwe": CWE,
                        "message": f"{binding_type} '{binding_name}' grants permissions to {subject_name}",
                        "details": DETAILS_ANONYMOUS.format(subject_name=subject_name),
                    }
                )

            # Warn about system:authenticated (all authenticated users)
            if subject_name == "system:authenticated":
                findings.append(
                    {
                        "severity": SEVERITY_HIGH,
                        "resource_type": binding_type,
                        "resource_name": f"{namespace}/{binding_name}",
                        "container": "N/A",
                        "check_id": CHECK_ID,
                        "check_name": CHECK_NAME,
                        "cwe": CWE,
                        "message": f"{binding_type} '{binding_name}' grants permissions to all authenticated users",
                        "details": DETAILS_AUTHENTICATED,
                    }
                )

    return findings
