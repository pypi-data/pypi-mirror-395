from typing import List, Dict, Any
import re

#
# check_image_tags.py
#
# Check #13: Mutable image tags
# CWE-494: Download of Code Without Integrity Check
#

# Security check metadata
CHECK_ID = "13"
CHECK_NAME = "Mutable image tags"
CWE = "CWE-494"
SEVERITY_HIGH = "HIGH"
SEVERITY_MEDIUM = "MEDIUM"
RESOURCE_TYPE = "Deployment"
DETAILS = "Using tags or latest instead of image hashes for deployment exposes the cluster to runtime reconfiguration in case of registry compromission"


def check(deployments: List[Any]) -> List[Dict[str, Any]]:
    findings = []

    # Regex to check if image uses digest (sha256:...)
    digest_pattern = re.compile(r"@sha256:[a-f0-9]{64}$")

    for deployment in deployments:
        deployment_name = deployment.metadata.name
        namespace = deployment.metadata.namespace

        # Check containers
        if deployment.spec.template.spec.containers:
            for container in deployment.spec.template.spec.containers:
                image = container.image

                # Check if using digest
                if not digest_pattern.search(image):
                    # Determine severity based on tag
                    severity = SEVERITY_MEDIUM
                    if ":latest" in image or ":" not in image:
                        severity = SEVERITY_HIGH

                    findings.append(
                        {
                            "severity": severity,
                            "resource_type": RESOURCE_TYPE,
                            "resource_name": f"{namespace}/{deployment_name}",
                            "container": container.name,
                            "check_id": CHECK_ID,
                            "check_name": CHECK_NAME,
                            "cwe": CWE,
                            "message": f"Container '{container.name}' uses mutable image tag: {image}",
                            "details": DETAILS,
                        }
                    )

        # Check init containers
        if deployment.spec.template.spec.init_containers:
            for container in deployment.spec.template.spec.init_containers:
                image = container.image

                if not digest_pattern.search(image):
                    severity = SEVERITY_MEDIUM
                    if ":latest" in image or ":" not in image:
                        severity = SEVERITY_HIGH

                    findings.append(
                        {
                            "severity": severity,
                            "resource_type": RESOURCE_TYPE,
                            "resource_name": f"{namespace}/{deployment_name}",
                            "container": container.name,
                            "check_id": CHECK_ID,
                            "check_name": CHECK_NAME,
                            "cwe": CWE,
                            "message": f"Init container '{container.name}' uses mutable image tag: {image}",
                            "details": DETAILS,
                        }
                    )

    return findings
