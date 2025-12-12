from typing import Dict, List, Any

#
# comparator.py
#
# Namespace comparison logic is performed here.
#


def compare_deployments(
    deployments_ns1: List[Dict[str, Any]], deployments_ns2: List[Dict[str, Any]]
) -> Dict[str, List[Dict[str, Any]]]:
    ns1_by_name = {dep["name"]: dep for dep in deployments_ns1}
    ns2_by_name = {dep["name"]: dep for dep in deployments_ns2}

    names_ns1 = set(ns1_by_name.keys())
    names_ns2 = set(ns2_by_name.keys())

    missing_names = names_ns1 - names_ns2
    missing = [ns1_by_name[name] for name in missing_names]

    extra_names = names_ns2 - names_ns1
    extra = [ns2_by_name[name] for name in extra_names]

    common_names = names_ns1 & names_ns2
    changed = []

    for name in common_names:
        dep_ns1 = ns1_by_name[name]
        dep_ns2 = ns2_by_name[name]

        if _deployments_differ(dep_ns1, dep_ns2):
            changed.append(
                {
                    "name": name,
                    "ns1": dep_ns1,
                    "ns2": dep_ns2,
                    "differences": _get_differences(dep_ns1, dep_ns2),
                }
            )

    return {
        "missing": sorted(missing, key=lambda x: x["name"]),
        "extra": sorted(extra, key=lambda x: x["name"]),
        "changed": sorted(changed, key=lambda x: x["name"]),
    }


def _deployments_differ(dep1: Dict[str, Any], dep2: Dict[str, Any]) -> bool:
    if dep1.get("images", []) != dep2.get("images", []):
        return True
    if dep1.get("replicas", 0) != dep2.get("replicas", 0):
        return True

    return False


def _get_differences(dep1: Dict[str, Any], dep2: Dict[str, Any]) -> Dict[str, Any]:
    differences = {}
    images1 = dep1.get("images", [])
    images2 = dep2.get("images", [])
    if images1 != images2:
        differences["images"] = {"ns1": images1, "ns2": images2}
    replicas1 = dep1.get("replicas", 0)
    replicas2 = dep2.get("replicas", 0)
    if replicas1 != replicas2:
        differences["replicas"] = {"ns1": replicas1, "ns2": replicas2}

    return differences
