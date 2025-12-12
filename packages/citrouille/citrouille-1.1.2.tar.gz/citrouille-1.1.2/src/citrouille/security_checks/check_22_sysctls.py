from typing import List, Dict, Any

#
# check_sysctls.py
#
# Check #22: Kernel tampering via sysctls
# CWE-250: Execution with Unnecessary Privileges
#

# Security check metadata
CHECK_ID = "22"
CHECK_NAME = "Kernel tampering"
CWE = "CWE-250"
SEVERITY_CRITICAL = "CRITICAL"
SEVERITY_MEDIUM = "MEDIUM"
RESOURCE_TYPE = "Deployment"
DETAILS_KERNEL_SYSCTL = "The sysctl '{sysctl_name}' affects the entire node's kernel and can be exploited by compromised containers."
DETAILS_ANY_SYSCTL = "Sysctls modify kernel parameters and should be avoided unless absolutely necessary."


def check(deployments: List[Any]) -> List[Dict[str, Any]]:
    findings = []

    for deployment in deployments:
        deployment_name = deployment.metadata.name
        namespace = deployment.metadata.namespace

        if (
            deployment.spec.template.spec.security_context
            and deployment.spec.template.spec.security_context.sysctls
        ):
            sysctls = deployment.spec.template.spec.security_context.sysctls

            for sysctl in sysctls:
                sysctl_name = sysctl.name

                # Check for kernel.* sysctls (affect the entire node)
                if sysctl_name.startswith("kernel."):
                    findings.append(
                        {
                            "severity": SEVERITY_CRITICAL,
                            "resource_type": RESOURCE_TYPE,
                            "resource_name": f"{namespace}/{deployment_name}",
                            "container": "N/A",
                            "check_id": CHECK_ID,
                            "check_name": CHECK_NAME,
                            "cwe": CWE,
                            "message": f"Deployment uses unsafe sysctl: {sysctl_name}",
                            "details": DETAILS_KERNEL_SYSCTL.format(
                                sysctl_name=sysctl_name
                            ),
                        }
                    )
                else:
                    # Warn about any sysctl usage
                    findings.append(
                        {
                            "severity": SEVERITY_MEDIUM,
                            "resource_type": RESOURCE_TYPE,
                            "resource_name": f"{namespace}/{deployment_name}",
                            "container": "N/A",
                            "check_id": CHECK_ID,
                            "check_name": CHECK_NAME,
                            "cwe": CWE,
                            "message": f"Deployment uses sysctl: {sysctl_name}",
                            "details": DETAILS_ANY_SYSCTL,
                        }
                    )

    return findings
