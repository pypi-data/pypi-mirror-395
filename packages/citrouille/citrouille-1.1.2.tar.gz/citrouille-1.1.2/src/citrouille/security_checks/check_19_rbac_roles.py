from typing import List, Dict, Any

#
# check_rbac_roles.py
#
# Check #19: Misconfigured Role or ClusterRole
# CWE-269: Improper Privilege Management
#

# Security check metadata
CHECK_ID = "19"
CHECK_NAME = "Misconfigured RBAC role"
CWE = "CWE-269"
SEVERITY_CRITICAL = "CRITICAL"
SEVERITY_HIGH = "HIGH"
DETAILS_WILDCARD_VERBS = "Wildcard verbs go against the principle of least privilege."
DETAILS_WILDCARD_RESOURCES = (
    "Wildcard resources go against the principle of least privilege."
)
DETAILS_WILDCARD_API_GROUPS = (
    "Wildcard API groups go against the principle of least privilege."
)

# Dangerous permission combinations
DANGEROUS_COMBOS = [
    {
        "verbs": ["create"],
        "resources": ["pods"],
        "message": "Can create pods with arbitrary privileges",
    },
    {
        "verbs": ["create", "patch"],
        "resources": ["pods/exec", "pods/attach"],
        "message": "Can execute commands in any pod",
    },
    {
        "verbs": ["get", "list", "watch"],
        "resources": ["secrets"],
        "message": "Can read all secrets including service account tokens",
    },
    {
        "verbs": ["impersonate"],
        "resources": None,
        "message": "Can impersonate any user/group/service account",
    },
    {
        "verbs": ["bind", "escalate"],
        "resources": ["roles", "clusterroles"],
        "message": "Can assign roles with more permissions than currently held",
    },
    {
        "verbs": ["patch", "update"],
        "resources": ["nodes", "nodes/status"],
        "message": "Can modify node configuration",
    },
    {
        "verbs": ["create", "update"],
        "resources": ["persistentvolumes"],
        "message": "Can create PVs with hostPath access",
    },
    {
        "verbs": ["create", "update"],
        "resources": ["podsecuritypolicies"],
        "message": "Can create permissive PSPs",
    },
    {
        "verbs": ["create"],
        "resources": ["serviceaccounts/token"],
        "message": "Can create tokens for any service account",
    },
]


def check(roles: List[Any], cluster_roles: List[Any]) -> List[Dict[str, Any]]:
    findings = []

    # Check Roles
    for role in roles:
        findings.extend(_check_role(role, "Role"))

    # Check ClusterRoles
    for cluster_role in cluster_roles:
        findings.extend(_check_role(cluster_role, "ClusterRole"))

    return findings


def _check_role(role: Any, role_type: str) -> List[Dict[str, Any]]:
    findings = []
    role_name = role.metadata.name
    namespace = role.metadata.namespace if role_type == "Role" else "cluster-wide"

    if not role.rules:
        return findings

    for rule in role.rules:
        verbs = rule.verbs or []
        resources = rule.resources or []
        api_groups = rule.api_groups or []

        # Check for wildcards
        if "*" in verbs:
            findings.append(
                {
                    "severity": SEVERITY_CRITICAL,
                    "resource_type": role_type,
                    "resource_name": f"{namespace}/{role_name}",
                    "container": "N/A",
                    "check_id": CHECK_ID,
                    "check_name": CHECK_NAME,
                    "cwe": CWE,
                    "message": f"{role_type} '{role_name}' grants wildcard verbs (*)",
                    "details": DETAILS_WILDCARD_VERBS,
                }
            )

        if "*" in resources:
            findings.append(
                {
                    "severity": SEVERITY_CRITICAL,
                    "resource_type": role_type,
                    "resource_name": f"{namespace}/{role_name}",
                    "container": "N/A",
                    "check_id": CHECK_ID,
                    "check_name": CHECK_NAME,
                    "cwe": CWE,
                    "message": f"{role_type} '{role_name}' grants access to all resources (*)",
                    "details": DETAILS_WILDCARD_RESOURCES,
                }
            )

        if "*" in api_groups:
            findings.append(
                {
                    "severity": SEVERITY_HIGH,
                    "resource_type": role_type,
                    "resource_name": f"{namespace}/{role_name}",
                    "container": "N/A",
                    "check_id": CHECK_ID,
                    "check_name": CHECK_NAME,
                    "cwe": CWE,
                    "message": f"{role_type} '{role_name}' grants access to all API groups (*)",
                    "details": DETAILS_WILDCARD_API_GROUPS,
                }
            )

        # Check for dangerous permission combinations
        for combo in DANGEROUS_COMBOS:
            required_verbs = combo["verbs"]
            required_resources = combo["resources"]

            # Check if this rule has the dangerous verbs
            has_verbs = any(verb in verbs or "*" in verbs for verb in required_verbs)

            # Check resources if specified
            has_resources = True
            if required_resources:
                has_resources = any(
                    resource in resources or "*" in resources
                    for resource in required_resources
                )

            if has_verbs and has_resources:
                findings.append(
                    {
                        "severity": SEVERITY_CRITICAL,
                        "resource_type": role_type,
                        "resource_name": f"{namespace}/{role_name}",
                        "container": "N/A",
                        "check_id": CHECK_ID,
                        "check_name": CHECK_NAME,
                        "cwe": CWE,
                        "message": f"{role_type} '{role_name}' has dangerous permissions: {combo['message']}",
                        "details": f"This combination of verbs {required_verbs} and resources {required_resources} can lead to privilege escalation.",
                    }
                )

    return findings
