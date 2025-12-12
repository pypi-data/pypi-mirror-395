from typing import Dict, Any

#
# check_pss_enforcement.py
#
# Check #15: Namespace enforcement of PSS (Pod Security Standards)
# CWE-693: Protection Mechanism Failure
#

# Security check metadata
CHECK_ID = "15"
CHECK_NAME = "PSS enforcement"
CWE = "CWE-693"
SEVERITY_HIGH = "HIGH"
SEVERITY_MEDIUM = "MEDIUM"
SEVERITY_LOW = "LOW"
RESOURCE_TYPE = "Namespace"
DETAILS_NO_ENFORCE = "Set label 'pod-security.kubernetes.io/enforce' to 'restricted' or 'baseline' to prevent insecure pod configurations."
DETAILS_WEAK_ENFORCE = (
    "Use 'restricted' or 'baseline' for pod-security.kubernetes.io/enforce label."
)
DETAILS_NO_WARN = "Set label 'pod-security.kubernetes.io/warn' to provide warnings for policy violations."
DETAILS_NO_AUDIT = "Set label 'pod-security.kubernetes.io/audit' for audit logging of policy violations."


def check(namespace_obj: Any) -> list[Dict[str, Any]]:
    findings = []

    namespace_name = namespace_obj.metadata.name
    labels = namespace_obj.metadata.labels or {}

    # Check for PSS labels
    enforce_label = labels.get("pod-security.kubernetes.io/enforce")
    warn_label = labels.get("pod-security.kubernetes.io/warn")
    audit_label = labels.get("pod-security.kubernetes.io/audit")

    # Check enforce label
    if not enforce_label:
        findings.append(
            {
                "severity": SEVERITY_HIGH,
                "resource_type": RESOURCE_TYPE,
                "resource_name": namespace_name,
                "container": "N/A",
                "check_id": CHECK_ID,
                "check_name": CHECK_NAME,
                "cwe": CWE,
                "message": "Namespace does not enforce Pod Security Standards",
                "details": DETAILS_NO_ENFORCE,
            }
        )
    elif enforce_label not in ["restricted", "baseline"]:
        findings.append(
            {
                "severity": SEVERITY_MEDIUM,
                "resource_type": RESOURCE_TYPE,
                "resource_name": namespace_name,
                "container": "N/A",
                "check_id": CHECK_ID,
                "check_name": CHECK_NAME,
                "cwe": CWE,
                "message": f"Namespace has weak PSS enforcement level: {enforce_label}",
                "details": DETAILS_WEAK_ENFORCE,
            }
        )

    # Check warn label
    if not warn_label:
        findings.append(
            {
                "severity": SEVERITY_LOW,
                "resource_type": RESOURCE_TYPE,
                "resource_name": namespace_name,
                "container": "N/A",
                "check_id": CHECK_ID,
                "check_name": CHECK_NAME,
                "cwe": CWE,
                "message": "Namespace does not have PSS warn label set",
                "details": DETAILS_NO_WARN,
            }
        )

    # Check audit label
    if not audit_label:
        findings.append(
            {
                "severity": SEVERITY_LOW,
                "resource_type": RESOURCE_TYPE,
                "resource_name": namespace_name,
                "container": "N/A",
                "check_id": CHECK_ID,
                "check_name": CHECK_NAME,
                "cwe": CWE,
                "message": "Namespace does not have PSS audit label set",
                "details": DETAILS_NO_AUDIT,
            }
        )

    return findings
