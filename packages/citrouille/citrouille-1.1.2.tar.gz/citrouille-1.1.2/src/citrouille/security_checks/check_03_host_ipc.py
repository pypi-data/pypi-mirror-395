from typing import List, Dict, Any

#
# check_host_ipc.py
#
# Check #3: Host IPC usage
# CWE-653: Improper Isolation or Compartmentalization
#

# Security check metadata
CHECK_ID = "3"
CHECK_NAME = "Host IPC usage"
CWE = "CWE-653"
SEVERITY = "HIGH"
RESOURCE_TYPE = "Deployment"
DETAILS = "Using the host IPC namespace allows access to System V IPC objects (shared memory, semaphores, message queues) on the host."


def check(deployments: List[Any]) -> List[Dict[str, Any]]:
    findings = []

    for deployment in deployments:
        deployment_name = deployment.metadata.name
        namespace = deployment.metadata.namespace

        if deployment.spec.template.spec.host_ipc:
            findings.append(
                {
                    "severity": SEVERITY,
                    "resource_type": RESOURCE_TYPE,
                    "resource_name": f"{namespace}/{deployment_name}",
                    "container": "N/A",
                    "check_id": CHECK_ID,
                    "check_name": CHECK_NAME,
                    "cwe": CWE,
                    "message": "Deployment is using the host's IPC namespace",
                    "details": DETAILS,
                }
            )

    return findings
