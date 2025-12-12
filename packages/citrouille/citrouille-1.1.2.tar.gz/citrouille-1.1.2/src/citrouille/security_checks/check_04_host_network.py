from typing import List, Dict, Any

#
# check_host_network.py
#
# Check #4: Host network access
# CWE-653: Improper Isolation or Compartmentalization
#

# Security check metadata
CHECK_ID = "4"
CHECK_NAME = "Host network access"
CWE = "CWE-653"
SEVERITY = "HIGH"
RESOURCE_TYPE = "Deployment"
DETAILS = "Using the host network namespace allows the container to sniff traffic on the host or bind to its ports."


def check(deployments: List[Any]) -> List[Dict[str, Any]]:
    findings = []

    for deployment in deployments:
        deployment_name = deployment.metadata.name
        namespace = deployment.metadata.namespace

        if deployment.spec.template.spec.host_network:
            findings.append(
                {
                    "severity": SEVERITY,
                    "resource_type": RESOURCE_TYPE,
                    "resource_name": f"{namespace}/{deployment_name}",
                    "container": "N/A",
                    "check_id": CHECK_ID,
                    "check_name": CHECK_NAME,
                    "cwe": CWE,
                    "message": "Deployment is using the host's network namespace",
                    "details": DETAILS,
                }
            )

    return findings
