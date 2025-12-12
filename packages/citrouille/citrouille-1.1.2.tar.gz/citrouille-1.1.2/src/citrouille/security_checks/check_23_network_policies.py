from typing import List, Dict, Any

#
# check_network_policies.py
#
# Check #23: Misconfigured NetworkPolicy
# CWE-923: Improper Restriction of Communication Channel to Intended Endpoints
#

# Security check metadata
CHECK_ID = "23"
CWE = "CWE-923"
SEVERITY_HIGH = "HIGH"
SEVERITY_MEDIUM = "MEDIUM"
RESOURCE_TYPE = "NetworkPolicy"

# Check names
CHECK_NAME_MISSING = "Missing NetworkPolicy"
CHECK_NAME_PERMISSIVE = "Permissive NetworkPolicy"
DETAILS_MISSING = "Without NetworkPolicies, all pods can communicate with each other and external networks, going against the principle of least privilege."
DETAILS_INGRESS_ALLOW_ALL = "This policy has an ingress rule without 'from' selectors, allowing traffic from any source."
DETAILS_EGRESS_ALLOW_ALL = "This policy has an egress rule without 'to' selectors, allowing traffic to any destination."


def check(network_policies: List[Any], namespace: str) -> List[Dict[str, Any]]:
    findings = []

    # Check if there are any network policies in the namespace
    if not network_policies or len(network_policies) == 0:
        findings.append(
            {
                "severity": SEVERITY_HIGH,
                "resource_type": RESOURCE_TYPE,
                "resource_name": f"{namespace}/N/A",
                "container": "N/A",
                "check_id": CHECK_ID,
                "check_name": CHECK_NAME_MISSING,
                "cwe": CWE,
                "message": f"Namespace '{namespace}' has no NetworkPolicies",
                "details": DETAILS_MISSING,
            }
        )
    else:
        # If policies exist, check for overly permissive ones
        for policy in network_policies:
            policy_name = policy.metadata.name

            # Check for empty podSelector (applies to all pods)
            if policy.spec.pod_selector and not policy.spec.pod_selector.match_labels:
                # Check if ingress rules are too permissive
                if policy.spec.ingress:
                    for ingress_rule in policy.spec.ingress:
                        if not ingress_rule._from:
                            findings.append(
                                {
                                    "severity": SEVERITY_MEDIUM,
                                    "resource_type": RESOURCE_TYPE,
                                    "resource_name": f"{namespace}/{policy_name}",
                                    "container": "N/A",
                                    "check_id": CHECK_ID,
                                    "check_name": CHECK_NAME_PERMISSIVE,
                                    "cwe": CWE,
                                    "message": f"NetworkPolicy '{policy_name}' allows all ingress traffic",
                                    "details": DETAILS_INGRESS_ALLOW_ALL,
                                }
                            )

                # Check if egress rules are too permissive
                if policy.spec.egress:
                    for egress_rule in policy.spec.egress:
                        if not egress_rule.to:
                            findings.append(
                                {
                                    "severity": SEVERITY_MEDIUM,
                                    "resource_type": RESOURCE_TYPE,
                                    "resource_name": f"{namespace}/{policy_name}",
                                    "container": "N/A",
                                    "check_id": CHECK_ID,
                                    "check_name": CHECK_NAME_PERMISSIVE,
                                    "cwe": CWE,
                                    "message": f"NetworkPolicy '{policy_name}' allows all egress traffic",
                                    "details": DETAILS_EGRESS_ALLOW_ALL,
                                }
                            )

    return findings
