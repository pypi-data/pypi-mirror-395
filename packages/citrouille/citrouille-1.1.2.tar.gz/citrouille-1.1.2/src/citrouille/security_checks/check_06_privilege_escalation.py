from typing import List, Dict, Any

#
# check_privilege_escalation.py
#
# Check #6: allowPrivilegeEscalation set to true
# CWE-269: Improper Privilege Management
#

# Security check metadata
CHECK_ID = "6"
CHECK_NAME = "allowPrivilegeEscalation"
CWE = "CWE-269"
SEVERITY = "MEDIUM"
RESOURCE_TYPE = "Deployment"
DETAILS = "Privilege escalation allows use of setUID binaries and should be explicitly disabled."


def check(deployments: List[Any]) -> List[Dict[str, Any]]:
    findings = []

    for deployment in deployments:
        deployment_name = deployment.metadata.name
        namespace = deployment.metadata.namespace

        # Check containers
        if deployment.spec.template.spec.containers:
            for container in deployment.spec.template.spec.containers:
                allow_priv_esc = None
                if (
                    container.security_context
                    and container.security_context.allow_privilege_escalation
                    is not None
                ):
                    allow_priv_esc = (
                        container.security_context.allow_privilege_escalation
                    )

                # Flag if not explicitly set to false
                if allow_priv_esc is None or allow_priv_esc:
                    findings.append(
                        {
                            "severity": SEVERITY,
                            "resource_type": RESOURCE_TYPE,
                            "resource_name": f"{namespace}/{deployment_name}",
                            "container": container.name,
                            "check_id": CHECK_ID,
                            "check_name": CHECK_NAME,
                            "cwe": CWE,
                            "message": f"Container '{container.name}' does not explicitly set allowPrivilegeEscalation to false",
                            "details": DETAILS,
                        }
                    )

        # Check init containers
        if deployment.spec.template.spec.init_containers:
            for container in deployment.spec.template.spec.init_containers:
                allow_priv_esc = None
                if (
                    container.security_context
                    and container.security_context.allow_privilege_escalation
                    is not None
                ):
                    allow_priv_esc = (
                        container.security_context.allow_privilege_escalation
                    )

                if allow_priv_esc is None or allow_priv_esc:
                    findings.append(
                        {
                            "severity": SEVERITY,
                            "resource_type": RESOURCE_TYPE,
                            "resource_name": f"{namespace}/{deployment_name}",
                            "container": container.name,
                            "check_id": CHECK_ID,
                            "check_name": CHECK_NAME,
                            "cwe": CWE,
                            "message": f"Init container '{container.name}' does not explicitly set allowPrivilegeEscalation to false",
                            "details": DETAILS,
                        }
                    )

    return findings
