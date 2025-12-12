from typing import List, Dict, Any

#
# check_capabilities.py
#
# Check #7: Dangerous capabilities
# CWE-250: Execution with Unnecessary Privileges
#

# Security check metadata
CHECK_ID = "7"
CHECK_NAME = "Dangerous capabilities"
CWE = "CWE-250"
SEVERITY_CRITICAL = "CRITICAL"
SEVERITY_MEDIUM = "MEDIUM"
RESOURCE_TYPE = "Deployment"
DETAILS_NO_DROP_ALL = "Capabilities should be explicitly configured."
DETAILS_DANGEROUS_CAPS = "These capabilities grant excessive privileges."
DETAILS_NOT_DROPPED = "Unspecified capabilities"

# List of particularly dangerous capabilities
DANGEROUS_CAPABILITIES = {
    "SYS_ADMIN",
    "NET_ADMIN",
    "SYS_PTRACE",
    "SYS_MODULE",
    "SYS_RAWIO",
    "DAC_READ_SEARCH",
    "DAC_OVERRIDE",
    "CHOWN",
    "SETUID",
    "SETGID",
    "SYS_BOOT",
    "SYS_TIME",
    "MAC_ADMIN",
    "NET_RAW",
}


def check(deployments: List[Any]) -> List[Dict[str, Any]]:
    findings = []

    for deployment in deployments:
        deployment_name = deployment.metadata.name
        namespace = deployment.metadata.namespace

        # Check containers
        if deployment.spec.template.spec.containers:
            for container in deployment.spec.template.spec.containers:
                if (
                    not container.security_context
                    or not container.security_context.capabilities
                ):
                    # No capabilities configuration - should drop ALL
                    findings.append(
                        {
                            "severity": SEVERITY_MEDIUM,
                            "resource_type": RESOURCE_TYPE,
                            "resource_name": f"{namespace}/{deployment_name}",
                            "container": container.name,
                            "check_id": CHECK_ID,
                            "check_name": CHECK_NAME,
                            "cwe": CWE,
                            "message": f"Container '{container.name}' does not drop all capabilities",
                            "details": DETAILS_NO_DROP_ALL,
                        }
                    )
                else:
                    caps = container.security_context.capabilities

                    # Check for dangerous added capabilities
                    if caps.add:
                        dangerous_added = [
                            cap for cap in caps.add if cap in DANGEROUS_CAPABILITIES
                        ]
                        if dangerous_added:
                            findings.append(
                                {
                                    "severity": SEVERITY_CRITICAL,
                                    "resource_type": RESOURCE_TYPE,
                                    "resource_name": f"{namespace}/{deployment_name}",
                                    "container": container.name,
                                    "check_id": CHECK_ID,
                                    "check_name": CHECK_NAME,
                                    "cwe": CWE,
                                    "message": f"Container '{container.name}' adds dangerous capabilities: {', '.join(dangerous_added)}",
                                    "details": DETAILS_DANGEROUS_CAPS,
                                }
                            )

                    # Check if ALL capabilities are dropped
                    if not caps.drop or "ALL" not in caps.drop:
                        findings.append(
                            {
                                "severity": SEVERITY_MEDIUM,
                                "resource_type": RESOURCE_TYPE,
                                "resource_name": f"{namespace}/{deployment_name}",
                                "container": container.name,
                                "check_id": CHECK_ID,
                                "check_name": CHECK_NAME,
                                "cwe": CWE,
                                "message": f"Container '{container.name}' does not drop all capabilities",
                                "details": DETAILS_NOT_DROPPED,
                            }
                        )

        # Check init containers
        if deployment.spec.template.spec.init_containers:
            for container in deployment.spec.template.spec.init_containers:
                if (
                    not container.security_context
                    or not container.security_context.capabilities
                ):
                    findings.append(
                        {
                            "severity": SEVERITY_MEDIUM,
                            "resource_type": RESOURCE_TYPE,
                            "resource_name": f"{namespace}/{deployment_name}",
                            "container": container.name,
                            "check_id": CHECK_ID,
                            "check_name": CHECK_NAME,
                            "cwe": CWE,
                            "message": f"Init container '{container.name}' does not drop all capabilities",
                            "details": DETAILS_NO_DROP_ALL,
                        }
                    )
                else:
                    caps = container.security_context.capabilities

                    if caps.add:
                        dangerous_added = [
                            cap for cap in caps.add if cap in DANGEROUS_CAPABILITIES
                        ]
                        if dangerous_added:
                            findings.append(
                                {
                                    "severity": SEVERITY_CRITICAL,
                                    "resource_type": RESOURCE_TYPE,
                                    "resource_name": f"{namespace}/{deployment_name}",
                                    "container": container.name,
                                    "check_id": CHECK_ID,
                                    "check_name": CHECK_NAME,
                                    "cwe": CWE,
                                    "message": f"Init container '{container.name}' adds dangerous capabilities: {', '.join(dangerous_added)}",
                                    "details": DETAILS_DANGEROUS_CAPS,
                                }
                            )

                    if not caps.drop or "ALL" not in caps.drop:
                        findings.append(
                            {
                                "severity": SEVERITY_MEDIUM,
                                "resource_type": RESOURCE_TYPE,
                                "resource_name": f"{namespace}/{deployment_name}",
                                "container": container.name,
                                "check_id": CHECK_ID,
                                "check_name": CHECK_NAME,
                                "cwe": CWE,
                                "message": f"Init container '{container.name}' does not drop all capabilities",
                                "details": DETAILS_NOT_DROPPED,
                            }
                        )

    return findings
