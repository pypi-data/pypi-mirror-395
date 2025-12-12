from typing import List, Dict, Any

#
# check_seccomp.py
#
# Check #11: Unspecified seccomp profile
# CWE-250: Execution with Unnecessary Privileges
#

# Security check metadata
CHECK_ID = "11"
CHECK_NAME = "Unspecified seccomp profile"
CWE = "CWE-250"
SEVERITY = "MEDIUM"
RESOURCE_TYPE = "Deployment"
DETAILS_NO_PROFILE = "seccompProfile should be set to 'RuntimeDefault' to restrict syscalls and prevent container escapes."
DETAILS_WRONG_PROFILE = "Unless you know what you are doing, set seccompProfile to 'RuntimeDefault' to restrict syscalls and prevent container escapes."


def check(deployments: List[Any]) -> List[Dict[str, Any]]:
    findings = []

    for deployment in deployments:
        deployment_name = deployment.metadata.name
        namespace = deployment.metadata.namespace
        pod_spec = deployment.spec.template.spec

        # Check pod-level seccomp profile
        pod_seccomp = None
        if pod_spec.security_context and pod_spec.security_context.seccomp_profile:
            pod_seccomp = pod_spec.security_context.seccomp_profile

        # Check containers
        if pod_spec.containers:
            for container in pod_spec.containers:
                container_seccomp = pod_seccomp

                # Container-level overrides pod-level
                if (
                    container.security_context
                    and container.security_context.seccomp_profile
                ):
                    container_seccomp = container.security_context.seccomp_profile

                # Check if seccomp is properly configured
                if not container_seccomp:
                    findings.append(
                        {
                            "severity": SEVERITY,
                            "resource_type": RESOURCE_TYPE,
                            "resource_name": f"{namespace}/{deployment_name}",
                            "container": container.name,
                            "check_id": CHECK_ID,
                            "check_name": CHECK_NAME,
                            "cwe": CWE,
                            "message": f"Container '{container.name}' does not specify a seccomp profile",
                            "details": DETAILS_NO_PROFILE,
                        }
                    )
                elif container_seccomp.type != "RuntimeDefault":
                    findings.append(
                        {
                            "severity": SEVERITY,
                            "resource_type": RESOURCE_TYPE,
                            "resource_name": f"{namespace}/{deployment_name}",
                            "container": container.name,
                            "check_id": CHECK_ID,
                            "check_name": CHECK_NAME,
                            "cwe": CWE,
                            "message": f"Container '{container.name}' uses seccomp profile type '{container_seccomp.type}' instead of 'RuntimeDefault'",
                            "details": DETAILS_WRONG_PROFILE,
                        }
                    )

        # Check init containers
        if pod_spec.init_containers:
            for container in pod_spec.init_containers:
                container_seccomp = pod_seccomp

                if (
                    container.security_context
                    and container.security_context.seccomp_profile
                ):
                    container_seccomp = container.security_context.seccomp_profile

                if not container_seccomp:
                    findings.append(
                        {
                            "severity": SEVERITY,
                            "resource_type": RESOURCE_TYPE,
                            "resource_name": f"{namespace}/{deployment_name}",
                            "container": container.name,
                            "check_id": CHECK_ID,
                            "check_name": CHECK_NAME,
                            "cwe": CWE,
                            "message": f"Init container '{container.name}' does not specify a seccomp profile",
                            "details": DETAILS_NO_PROFILE,
                        }
                    )
                elif container_seccomp.type != "RuntimeDefault":
                    findings.append(
                        {
                            "severity": SEVERITY,
                            "resource_type": RESOURCE_TYPE,
                            "resource_name": f"{namespace}/{deployment_name}",
                            "container": container.name,
                            "check_id": CHECK_ID,
                            "check_name": CHECK_NAME,
                            "cwe": CWE,
                            "message": f"Init container '{container.name}' uses seccomp profile type '{container_seccomp.type}' instead of 'RuntimeDefault'",
                            "details": DETAILS_WRONG_PROFILE,
                        }
                    )

    return findings
