from typing import List, Dict, Any

#
# check_run_as_root.py
#
# Check #5: Running as root
# CWE-250: Execution with Unnecessary Privileges
#

# Security check metadata
CHECK_ID = "5"
CHECK_NAME = "Running as root"
CWE = "CWE-250"
SEVERITY = "HIGH"
RESOURCE_TYPE = "Deployment"
DETAILS = "Containers should not run as root."


def check(deployments: List[Any]) -> List[Dict[str, Any]]:
    findings = []

    for deployment in deployments:
        deployment_name = deployment.metadata.name
        namespace = deployment.metadata.namespace
        pod_spec = deployment.spec.template.spec

        # Check pod-level security context
        pod_run_as_non_root = None
        pod_run_as_user = None
        if pod_spec.security_context:
            pod_run_as_non_root = pod_spec.security_context.run_as_non_root
            pod_run_as_user = pod_spec.security_context.run_as_user

        # Check containers
        if pod_spec.containers:
            for container in pod_spec.containers:
                container_run_as_non_root = pod_run_as_non_root
                container_run_as_user = pod_run_as_user

                # Container-level settings override pod-level
                if container.security_context:
                    if container.security_context.run_as_non_root is not None:
                        container_run_as_non_root = (
                            container.security_context.run_as_non_root
                        )
                    if container.security_context.run_as_user is not None:
                        container_run_as_user = container.security_context.run_as_user

                # Check if running as root
                issues = []
                if container_run_as_user == 0:
                    issues.append("runAsUser is set to 0 (root)")
                if not container_run_as_non_root:
                    issues.append("runAsNonRoot is not set to true")

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
                            "message": f"Container '{container.name}' may be running as root: {', '.join(issues)}",
                            "details": DETAILS,
                        }
                    )

        # Check init containers
        if pod_spec.init_containers:
            for container in pod_spec.init_containers:
                container_run_as_non_root = pod_run_as_non_root
                container_run_as_user = pod_run_as_user

                if container.security_context:
                    if container.security_context.run_as_non_root is not None:
                        container_run_as_non_root = (
                            container.security_context.run_as_non_root
                        )
                    if container.security_context.run_as_user is not None:
                        container_run_as_user = container.security_context.run_as_user

                issues = []
                if container_run_as_user == 0:
                    issues.append("runAsUser is set to 0 (root)")
                if not container_run_as_non_root:
                    issues.append("runAsNonRoot is not set to true")

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
                            "message": f"Init container '{container.name}' may be running as root: {', '.join(issues)}",
                            "details": DETAILS,
                        }
                    )

    return findings
