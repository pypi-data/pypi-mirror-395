from typing import List, Dict, Any

#
# check_service_account_token.py
#
# Check #12: Automounted account tokens
# CWE-522: Insufficiently Protected Credentials
#

# Security check metadata
CHECK_ID = "12"
CHECK_NAME = "Automounted account tokens"
CWE = "CWE-522"
SEVERITY_MEDIUM = "MEDIUM"
SEVERITY_LOW = "LOW"
RESOURCE_TYPE = "Deployment"
DETAILS_AUTOMOUNT = "Automounting ServiceAccounToken allows compromised containers access to the Kubernetes API"
DETAILS_DEFAULT_SA = "Deployments should each have an individual ServiceAccount to follow the principle of least privilege."


def check(deployments: List[Any]) -> List[Dict[str, Any]]:
    findings = []

    for deployment in deployments:
        deployment_name = deployment.metadata.name
        namespace = deployment.metadata.namespace
        pod_spec = deployment.spec.template.spec

        # Check if automountServiceAccountToken is explicitly set to false
        automount = True  # Default is true
        if pod_spec.automount_service_account_token is not None:
            automount = pod_spec.automount_service_account_token

        if automount:
            findings.append(
                {
                    "severity": SEVERITY_MEDIUM,
                    "resource_type": RESOURCE_TYPE,
                    "resource_name": f"{namespace}/{deployment_name}",
                    "container": "N/A",
                    "check_id": CHECK_ID,
                    "check_name": CHECK_NAME,
                    "cwe": CWE,
                    "message": "Service account token is automounted",
                    "details": DETAILS_AUTOMOUNT,
                }
            )

        # Check if using default service account
        service_account = pod_spec.service_account_name or "default"
        if service_account == "default":
            findings.append(
                {
                    "severity": SEVERITY_LOW,
                    "resource_type": RESOURCE_TYPE,
                    "resource_name": f"{namespace}/{deployment_name}",
                    "container": "N/A",
                    "check_id": CHECK_ID,
                    "check_name": CHECK_NAME,
                    "cwe": CWE,
                    "message": "Deployment uses default service account",
                    "details": DETAILS_DEFAULT_SA,
                }
            )

    return findings
