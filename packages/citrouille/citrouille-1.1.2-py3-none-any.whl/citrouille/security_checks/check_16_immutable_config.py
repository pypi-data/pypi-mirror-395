from typing import List, Dict, Any

#
# check_immutable_config.py
#
# Check #16: Mutable configMap/secret instances
# CWE-471: Modification of Assumed-Immutable Data (MAID)
#

# Security check metadata
CHECK_ID = "16"
CHECK_NAME = "Mutable configuration"
CWE = "CWE-471"
SEVERITY_LOW = "LOW"
SEVERITY_MEDIUM = "MEDIUM"
RESOURCE_TYPE_CONFIGMAP = "ConfigMap"
RESOURCE_TYPE_SECRET = "Secret"
DETAILS_CONFIGMAP = "Mutable configMap instances enable runtime tampering."
DETAILS_SECRET = "Mutable Secret instances enable runtime tampering."


def check(config_maps: List[Any], secrets: List[Any]) -> List[Dict[str, Any]]:
    findings = []

    # Check ConfigMaps
    for cm in config_maps:
        if not cm.immutable:
            findings.append(
                {
                    "severity": SEVERITY_LOW,
                    "resource_type": RESOURCE_TYPE_CONFIGMAP,
                    "resource_name": f"{cm.metadata.namespace}/{cm.metadata.name}",
                    "container": "N/A",
                    "check_id": CHECK_ID,
                    "check_name": CHECK_NAME,
                    "cwe": CWE,
                    "message": f"ConfigMap '{cm.metadata.name}' is mutable",
                    "details": DETAILS_CONFIGMAP,
                }
            )

    # Check Secrets
    for secret in secrets:
        if not secret.immutable:
            findings.append(
                {
                    "severity": SEVERITY_MEDIUM,
                    "resource_type": RESOURCE_TYPE_SECRET,
                    "resource_name": f"{secret.metadata.namespace}/{secret.metadata.name}",
                    "container": "N/A",
                    "check_id": CHECK_ID,
                    "check_name": CHECK_NAME,
                    "cwe": CWE,
                    "message": f"Secret '{secret.metadata.name}' is mutable",
                    "details": DETAILS_SECRET,
                }
            )

    return findings
