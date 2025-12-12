from typing import List, Dict, Any

#
# check_proc_mount.py
#
# Check #18: Unspecified securityContext.procMount
# CWE-200: Exposure of Sensitive Information to an Unauthorized Actor
#

# Security check metadata
CHECK_ID = "18"
CHECK_NAME = "Unmasked procMount"
CWE = "CWE-200"
SEVERITY = "MEDIUM"
RESOURCE_TYPE = "Deployment"
DETAILS = "Unmasked /proc exposes sensitive host information. Do not set procMount to 'Unmasked' or use the default 'Default' value."


def check(deployments: List[Any]) -> List[Dict[str, Any]]:
    findings = []

    for deployment in deployments:
        deployment_name = deployment.metadata.name
        namespace = deployment.metadata.namespace

        # Check containers
        if deployment.spec.template.spec.containers:
            for container in deployment.spec.template.spec.containers:
                if (
                    container.security_context
                    and container.security_context.proc_mount == "Unmasked"
                ):
                    findings.append(
                        {
                            "severity": SEVERITY,
                            "resource_type": RESOURCE_TYPE,
                            "resource_name": f"{namespace}/{deployment_name}",
                            "container": container.name,
                            "check_id": CHECK_ID,
                            "check_name": CHECK_NAME,
                            "cwe": CWE,
                            "message": f"Container '{container.name}' has unmasked /proc mount",
                            "details": DETAILS,
                        }
                    )

        # Check init containers
        if deployment.spec.template.spec.init_containers:
            for container in deployment.spec.template.spec.init_containers:
                if (
                    container.security_context
                    and container.security_context.proc_mount == "Unmasked"
                ):
                    findings.append(
                        {
                            "severity": SEVERITY,
                            "resource_type": RESOURCE_TYPE,
                            "resource_name": f"{namespace}/{deployment_name}",
                            "container": container.name,
                            "check_id": CHECK_ID,
                            "check_name": CHECK_NAME,
                            "cwe": CWE,
                            "message": f"Init container '{container.name}' has unmasked /proc mount",
                            "details": DETAILS,
                        }
                    )

    return findings
