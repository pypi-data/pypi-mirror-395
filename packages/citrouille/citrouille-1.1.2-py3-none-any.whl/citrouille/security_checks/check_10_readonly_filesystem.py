from typing import List, Dict, Any

#
# check_readonly_filesystem.py
#
# Check #10: Writable root filesystem
# CWE-732: Incorrect Permission Assignment for Critical Resource
#

# Security check metadata
CHECK_ID = "10"
CHECK_NAME = "Writable root filesystem"
CWE = "CWE-732"
SEVERITY = "MEDIUM"
RESOURCE_TYPE = "Deployment"
DETAILS = "Writable filesystems allow for malware persistence and runtime tampering."


def check(deployments: List[Any]) -> List[Dict[str, Any]]:
    findings = []

    for deployment in deployments:
        deployment_name = deployment.metadata.name
        namespace = deployment.metadata.namespace

        # Check containers
        if deployment.spec.template.spec.containers:
            for container in deployment.spec.template.spec.containers:
                read_only = False
                if (
                    container.security_context
                    and container.security_context.read_only_root_filesystem
                ):
                    read_only = True

                if not read_only:
                    findings.append(
                        {
                            "severity": SEVERITY,
                            "resource_type": RESOURCE_TYPE,
                            "resource_name": f"{namespace}/{deployment_name}",
                            "container": container.name,
                            "check_id": CHECK_ID,
                            "check_name": CHECK_NAME,
                            "cwe": CWE,
                            "message": f"Container '{container.name}' has a writable root filesystem",
                            "details": DETAILS,
                        }
                    )

        # Check init containers
        if deployment.spec.template.spec.init_containers:
            for container in deployment.spec.template.spec.init_containers:
                read_only = False
                if (
                    container.security_context
                    and container.security_context.read_only_root_filesystem
                ):
                    read_only = True

                if not read_only:
                    findings.append(
                        {
                            "severity": SEVERITY,
                            "resource_type": RESOURCE_TYPE,
                            "resource_name": f"{namespace}/{deployment_name}",
                            "container": container.name,
                            "check_id": CHECK_ID,
                            "check_name": CHECK_NAME,
                            "cwe": CWE,
                            "message": f"Init container '{container.name}' has a writable root filesystem",
                            "details": DETAILS,
                        }
                    )

    return findings
