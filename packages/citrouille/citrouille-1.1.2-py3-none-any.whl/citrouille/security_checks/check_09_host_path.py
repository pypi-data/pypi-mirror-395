from typing import List, Dict, Any

#
# check_host_path.py
#
# Check #9: hostPath usage
# CWE-668: Exposure of Resource to Wrong Sphere
#

# Security check metadata
CHECK_ID = "9"
CHECK_NAME = "hostPath usage"
CWE = "CWE-668"
SEVERITY = "HIGH"
RESOURCE_TYPE = "Deployment"
DETAILS = "Mounting host paths contradicts container isolation principles and can expose sensitive host files."


def check(deployments: List[Any]) -> List[Dict[str, Any]]:
    findings = []

    for deployment in deployments:
        deployment_name = deployment.metadata.name
        namespace = deployment.metadata.namespace

        if deployment.spec.template.spec.volumes:
            for volume in deployment.spec.template.spec.volumes:
                if volume.host_path:
                    findings.append(
                        {
                            "severity": SEVERITY,
                            "resource_type": RESOURCE_TYPE,
                            "resource_name": f"{namespace}/{deployment_name}",
                            "container": "N/A",
                            "check_id": CHECK_ID,
                            "check_name": CHECK_NAME,
                            "cwe": CWE,
                            "message": f"Volume '{volume.name}' uses hostPath: {volume.host_path.path}",
                            "details": DETAILS,
                        }
                    )

    return findings
