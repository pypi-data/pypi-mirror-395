from typing import List, Dict, Any

#
# check_emptydir_limits.py
#
# Check #17: Unset emptyDir size limits
# CWE-770: Allocation of Resources Without Limits or Throttling
#

# Security check metadata
CHECK_ID = "17"
CHECK_NAME = "Unset emptyDir size limits"
CWE = "CWE-770"
SEVERITY = "MEDIUM"
RESOURCE_TYPE = "Deployment"
DETAILS = (
    "Not setting a size limit for emptyDir exposes nodes to denial-of-service attacks."
)


def check(deployments: List[Any]) -> List[Dict[str, Any]]:
    findings = []

    for deployment in deployments:
        deployment_name = deployment.metadata.name
        namespace = deployment.metadata.namespace

        if deployment.spec.template.spec.volumes:
            for volume in deployment.spec.template.spec.volumes:
                if volume.empty_dir:
                    if not volume.empty_dir.size_limit:
                        findings.append(
                            {
                                "severity": SEVERITY,
                                "resource_type": RESOURCE_TYPE,
                                "resource_name": f"{namespace}/{deployment_name}",
                                "container": "N/A",
                                "check_id": CHECK_ID,
                                "check_name": CHECK_NAME,
                                "cwe": CWE,
                                "message": f"emptyDir volume '{volume.name}' has no size limit",
                                "details": DETAILS,
                            }
                        )

    return findings
