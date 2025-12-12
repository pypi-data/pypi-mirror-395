from typing import List, Dict, Any
import re

#
# check_hardcoded_secrets.py
#
# Check #14: Hardcoded secrets in environment variables
# CWE-798: Use of Hard-coded Credentials
#

# Security check metadata
CHECK_ID = "14"
CHECK_NAME = "Hardcoded secrets"
CWE = "CWE-798"
SEVERITY = "CRITICAL"
RESOURCE_TYPE = "Deployment"
DETAILS = (
    "Hardcoded secrets can be exposed in clear text through kubectl, etcd, and backups."
)

# Patterns that suggest secrets in environment variable names
SECRET_PATTERNS = [
    r".*password.*",
    r".*secret.*",
    r".*key.*",
    r".*token.*",
    r".*api[_-]?key.*",
    r".*auth.*",
    r".*credential.*",
    r".*private.*",
]


def check(deployments: List[Any]) -> List[Dict[str, Any]]:
    findings = []

    for deployment in deployments:
        deployment_name = deployment.metadata.name
        namespace = deployment.metadata.namespace

        # Check containers
        if deployment.spec.template.spec.containers:
            for container in deployment.spec.template.spec.containers:
                if container.env:
                    for env_var in container.env:
                        # Check if value is hardcoded (not from valueFrom)
                        if env_var.value and not env_var.value_from:
                            # Check if env var name suggests it's a secret
                            env_name_lower = env_var.name.lower()
                            is_secret = any(
                                re.match(pattern, env_name_lower, re.IGNORECASE)
                                for pattern in SECRET_PATTERNS
                            )

                            if is_secret:
                                findings.append(
                                    {
                                        "severity": SEVERITY,
                                        "resource_type": RESOURCE_TYPE,
                                        "resource_name": f"{namespace}/{deployment_name}",
                                        "container": container.name,
                                        "check_id": CHECK_ID,
                                        "check_name": CHECK_NAME,
                                        "cwe": CWE,
                                        "message": f"Container '{container.name}' has hardcoded secret in environment variable '{env_var.name}'",
                                        "details": DETAILS,
                                    }
                                )

        # Check init containers
        if deployment.spec.template.spec.init_containers:
            for container in deployment.spec.template.spec.init_containers:
                if container.env:
                    for env_var in container.env:
                        if env_var.value and not env_var.value_from:
                            env_name_lower = env_var.name.lower()
                            is_secret = any(
                                re.match(pattern, env_name_lower, re.IGNORECASE)
                                for pattern in SECRET_PATTERNS
                            )

                            if is_secret:
                                findings.append(
                                    {
                                        "severity": SEVERITY,
                                        "resource_type": RESOURCE_TYPE,
                                        "resource_name": f"{namespace}/{deployment_name}",
                                        "container": container.name,
                                        "check_id": CHECK_ID,
                                        "check_name": CHECK_NAME,
                                        "cwe": CWE,
                                        "message": f"Init container '{container.name}' has hardcoded secret in environment variable '{env_var.name}'",
                                        "details": DETAILS,
                                    }
                                )

    return findings
