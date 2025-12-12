from typing import List, Dict, Any

#
# check_shared_process_ns.py
#
# Check #21: Shared process namespace
# CWE-653: Improper Isolation or Compartmentalization
#

# Security check metadata
CHECK_ID = "21"
CHECK_NAME = "Shared process namespace"
CWE = "CWE-653"
SEVERITY = "MEDIUM"
RESOURCE_TYPE = "Deployment"
DETAILS = "Sharing process namespace allows containers to see and interact with each other's processes."


def check(deployments: List[Any]) -> List[Dict[str, Any]]:
    findings = []

    for deployment in deployments:
        deployment_name = deployment.metadata.name
        namespace = deployment.metadata.namespace

        if deployment.spec.template.spec.share_process_namespace:
            findings.append(
                {
                    "severity": SEVERITY,
                    "resource_type": RESOURCE_TYPE,
                    "resource_name": f"{namespace}/{deployment_name}",
                    "container": "N/A",
                    "check_id": CHECK_ID,
                    "check_name": CHECK_NAME,
                    "cwe": CWE,
                    "message": "Deployment shares process namespace between containers",
                    "details": DETAILS,
                }
            )

    return findings
