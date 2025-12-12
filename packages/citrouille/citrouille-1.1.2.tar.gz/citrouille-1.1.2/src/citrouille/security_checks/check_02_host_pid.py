from typing import List, Dict, Any

#
# check_host_pid.py
#
# Check #2: Host PID namespace sharing
# CWE-653: Improper Isolation or Compartmentalization
#

# Security check metadata
CHECK_ID = "2"
CHECK_NAME = "Host PID namespace sharing"
CWE = "CWE-653"
SEVERITY = "HIGH"
RESOURCE_TYPE = "Deployment"
DETAILS = "Sharing the host PID namespace allows the container to see and potentially interact with all processes on the host."


def check(deployments: List[Any]) -> List[Dict[str, Any]]:
    findings = []

    for deployment in deployments:
        deployment_name = deployment.metadata.name
        namespace = deployment.metadata.namespace

        if deployment.spec.template.spec.host_pid:
            findings.append(
                {
                    "severity": SEVERITY,
                    "resource_type": RESOURCE_TYPE,
                    "resource_name": f"{namespace}/{deployment_name}",
                    "container": "N/A",
                    "check_id": CHECK_ID,
                    "check_name": CHECK_NAME,
                    "cwe": CWE,
                    "message": "Deployment is sharing the host's PID namespace",
                    "details": DETAILS,
                }
            )

    return findings
