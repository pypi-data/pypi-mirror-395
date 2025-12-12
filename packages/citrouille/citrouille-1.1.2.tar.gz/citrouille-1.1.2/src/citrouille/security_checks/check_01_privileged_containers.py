from typing import List, Dict, Any

#
# check_privileged_containers.py
#
# Check #1: Privileged containers
# CWE-250: Execution with Unnecessary Privileges
#

# Security check metadata
CHECK_ID = "1"
CHECK_NAME = "Privileged containers"
CWE = "CWE-250"
SEVERITY = "CRITICAL"
RESOURCE_TYPE = "Deployment"
DETAILS = "Privileged containers have access to dangerous host features like kernel modules and /dev/."


def check(deployments: List[Any]) -> List[Dict[str, Any]]:
    findings = []

    for deployment in deployments:
        deployment_name = deployment.metadata.name
        namespace = deployment.metadata.namespace

        # Check containers
        if deployment.spec.template.spec.containers:
            for container in deployment.spec.template.spec.containers:
                if container.security_context and container.security_context.privileged:
                    findings.append(
                        {
                            "severity": SEVERITY,
                            "resource_type": RESOURCE_TYPE,
                            "resource_name": f"{namespace}/{deployment_name}",
                            "container": container.name,
                            "check_id": CHECK_ID,
                            "check_name": CHECK_NAME,
                            "cwe": CWE,
                            "message": f"Container '{container.name}' is running in privileged mode",
                            "details": DETAILS,
                        }
                    )

        # Check init containers
        if deployment.spec.template.spec.init_containers:
            for container in deployment.spec.template.spec.init_containers:
                if container.security_context and container.security_context.privileged:
                    findings.append(
                        {
                            "severity": SEVERITY,
                            "resource_type": RESOURCE_TYPE,
                            "resource_name": f"{namespace}/{deployment_name}",
                            "container": container.name,
                            "check_id": CHECK_ID,
                            "check_name": CHECK_NAME,
                            "cwe": CWE,
                            "message": f"Init container '{container.name}' is running in privileged mode",
                            "details": DETAILS,
                        }
                    )

    return findings
