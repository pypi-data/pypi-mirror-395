from typing import List, Dict, Any

#
# check_resource_limits.py
#
# Check #8: No resource limits
# CWE-770: Allocation of Resources Without Limits or Throttling
#

# Security check metadata
CHECK_ID = "8"
CHECK_NAME = "No resource limits"
CWE = "CWE-770"
SEVERITY = "MEDIUM"
RESOURCE_TYPE = "Deployment"
DETAILS = "Set resource limits and requests to prevent denial of service attacks. Configure resources.limits.memory, resources.limits.cpu, resources.requests.memory, and resources.requests.cpu."


def check(deployments: List[Any]) -> List[Dict[str, Any]]:
    findings = []

    for deployment in deployments:
        deployment_name = deployment.metadata.name
        namespace = deployment.metadata.namespace

        # Check containers
        if deployment.spec.template.spec.containers:
            for container in deployment.spec.template.spec.containers:
                issues = []

                if not container.resources:
                    issues.append("no resources configured")
                else:
                    # Check limits
                    if not container.resources.limits:
                        issues.append("no limits set")
                    else:
                        if not container.resources.limits.get("memory"):
                            issues.append("no memory limit")
                        if not container.resources.limits.get("cpu"):
                            issues.append("no CPU limit")

                    # Check requests
                    if not container.resources.requests:
                        issues.append("no requests set")
                    else:
                        if not container.resources.requests.get("memory"):
                            issues.append("no memory request")
                        if not container.resources.requests.get("cpu"):
                            issues.append("no CPU request")

                if issues:
                    findings.append(
                        {
                            "severity": SEVERITY,
                            "resource_type": RESOURCE_TYPE,
                            "resource_name": f"{namespace}/{deployment_name}",
                            "container": container.name,
                            "check_id": CHECK_ID,
                            "check_name": CHECK_NAME,
                            "cwe": CWE,
                            "message": f"Container '{container.name}' has missing resource configuration: {', '.join(issues)}",
                            "details": DETAILS,
                        }
                    )

        # Check init containers
        if deployment.spec.template.spec.init_containers:
            for container in deployment.spec.template.spec.init_containers:
                issues = []

                if not container.resources:
                    issues.append("no resources configured")
                else:
                    if not container.resources.limits:
                        issues.append("no limits set")
                    else:
                        if not container.resources.limits.get("memory"):
                            issues.append("no memory limit")
                        if not container.resources.limits.get("cpu"):
                            issues.append("no CPU limit")

                    if not container.resources.requests:
                        issues.append("no requests set")
                    else:
                        if not container.resources.requests.get("memory"):
                            issues.append("no memory request")
                        if not container.resources.requests.get("cpu"):
                            issues.append("no CPU request")

                if issues:
                    findings.append(
                        {
                            "severity": SEVERITY,
                            "resource_type": RESOURCE_TYPE,
                            "resource_name": f"{namespace}/{deployment_name}",
                            "container": container.name,
                            "check_id": CHECK_ID,
                            "check_name": CHECK_NAME,
                            "cwe": CWE,
                            "message": f"Init container '{container.name}' has missing resource configuration: {', '.join(issues)}",
                            "details": DETAILS,
                        }
                    )

    return findings
