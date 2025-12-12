import unittest
from datetime import datetime
from citrouille.comparator import (
    compare_deployments,
    _deployments_differ,
    _get_differences,
)

#
# test_comparator.py
#
# Tests for comparator.py
#


class TestComparatorFunctions(unittest.TestCase):
    #
    # setUp
    # Initializes test fixtures with sample deployment data
    #
    def setUp(self):
        self.deployment1 = {
            "name": "app1",
            "namespace": "default",
            "images": ["nginx:1.21"],
            "created": datetime(2024, 11, 1, 10, 0, 0),
            "replicas": 3,
        }

        self.deployment2 = {
            "name": "app2",
            "namespace": "default",
            "images": ["redis:7.0"],
            "created": datetime(2024, 11, 2, 10, 0, 0),
            "replicas": 2,
        }

        self.deployment3 = {
            "name": "app3",
            "namespace": "default",
            "images": ["postgres:15"],
            "created": datetime(2024, 11, 3, 10, 0, 0),
            "replicas": 1,
        }

    #
    # test_compare_identical_namespaces
    # Tests comparison when both namespaces have identical deployments
    #
    def test_compare_identical_namespaces(self):
        deployments_ns1 = [self.deployment1, self.deployment2]
        deployments_ns2 = [self.deployment1.copy(), self.deployment2.copy()]

        result = compare_deployments(deployments_ns1, deployments_ns2)

        self.assertEqual(len(result["missing"]), 0)
        self.assertEqual(len(result["extra"]), 0)
        self.assertEqual(len(result["changed"]), 0)

    #
    # test_compare_missing_deployments
    # Tests comparison when deployments are missing in second namespace
    #
    def test_compare_missing_deployments(self):
        deployments_ns1 = [self.deployment1, self.deployment2, self.deployment3]
        deployments_ns2 = [self.deployment2.copy()]

        result = compare_deployments(deployments_ns1, deployments_ns2)

        self.assertEqual(len(result["missing"]), 2)
        self.assertEqual(len(result["extra"]), 0)
        self.assertEqual(len(result["changed"]), 0)

        missing_names = [dep["name"] for dep in result["missing"]]
        self.assertIn("app1", missing_names)
        self.assertIn("app3", missing_names)

    #
    # test_compare_extra_deployments
    # Tests comparison when deployments are extra in second namespace
    #
    def test_compare_extra_deployments(self):
        deployments_ns1 = [self.deployment1]
        deployments_ns2 = [self.deployment1.copy(), self.deployment2, self.deployment3]

        result = compare_deployments(deployments_ns1, deployments_ns2)

        self.assertEqual(len(result["missing"]), 0)
        self.assertEqual(len(result["extra"]), 2)
        self.assertEqual(len(result["changed"]), 0)

        extra_names = [dep["name"] for dep in result["extra"]]
        self.assertIn("app2", extra_names)
        self.assertIn("app3", extra_names)

    #
    # test_compare_changed_images
    # Tests comparison when deployments have different container images
    #
    def test_compare_changed_images(self):
        deployments_ns1 = [self.deployment1]
        deployment1_modified = self.deployment1.copy()
        deployment1_modified["images"] = ["nginx:1.22"]
        deployments_ns2 = [deployment1_modified]

        result = compare_deployments(deployments_ns1, deployments_ns2)

        self.assertEqual(len(result["missing"]), 0)
        self.assertEqual(len(result["extra"]), 0)
        self.assertEqual(len(result["changed"]), 1)

        changed = result["changed"][0]
        self.assertEqual(changed["name"], "app1")
        self.assertIn("images", changed["differences"])
        self.assertEqual(changed["differences"]["images"]["ns1"], ["nginx:1.21"])
        self.assertEqual(changed["differences"]["images"]["ns2"], ["nginx:1.22"])

    #
    # test_compare_changed_replicas
    # Tests comparison when deployments have different replica counts
    #
    def test_compare_changed_replicas(self):
        deployments_ns1 = [self.deployment1]
        deployment1_modified = self.deployment1.copy()
        deployment1_modified["replicas"] = 5
        deployments_ns2 = [deployment1_modified]

        result = compare_deployments(deployments_ns1, deployments_ns2)

        self.assertEqual(len(result["missing"]), 0)
        self.assertEqual(len(result["extra"]), 0)
        self.assertEqual(len(result["changed"]), 1)

        changed = result["changed"][0]
        self.assertEqual(changed["name"], "app1")
        self.assertIn("replicas", changed["differences"])
        self.assertEqual(changed["differences"]["replicas"]["ns1"], 3)
        self.assertEqual(changed["differences"]["replicas"]["ns2"], 5)

    #
    # test_compare_changed_multiple_fields
    # Tests comparison when deployments differ in both images and replica counts
    #
    def test_compare_changed_multiple_fields(self):
        deployments_ns1 = [self.deployment1]
        deployment1_modified = self.deployment1.copy()
        deployment1_modified["images"] = ["nginx:1.23"]
        deployment1_modified["replicas"] = 10
        deployments_ns2 = [deployment1_modified]

        result = compare_deployments(deployments_ns1, deployments_ns2)

        self.assertEqual(len(result["changed"]), 1)

        changed = result["changed"][0]
        self.assertIn("images", changed["differences"])
        self.assertIn("replicas", changed["differences"])

    #
    # test_compare_empty_namespaces
    # Tests comparison when both namespaces are empty
    #
    def test_compare_empty_namespaces(self):
        result = compare_deployments([], [])

        self.assertEqual(len(result["missing"]), 0)
        self.assertEqual(len(result["extra"]), 0)
        self.assertEqual(len(result["changed"]), 0)

    #
    # test_compare_empty_vs_populated
    # Tests comparison when first namespace has deployments and second is empty
    #
    def test_compare_empty_vs_populated(self):
        deployments_ns1 = [self.deployment1, self.deployment2]
        deployments_ns2 = []

        result = compare_deployments(deployments_ns1, deployments_ns2)

        self.assertEqual(len(result["missing"]), 2)
        self.assertEqual(len(result["extra"]), 0)
        self.assertEqual(len(result["changed"]), 0)

    #
    # test_compare_multi_container_pods
    # Tests comparison of deployments with multiple container images
    #
    def test_compare_multi_container_pods(self):
        deployment_multi = {
            "name": "multi-app",
            "namespace": "default",
            "images": ["nginx:1.21", "redis:7.0", "busybox:latest"],
            "created": datetime(2024, 11, 4, 10, 0, 0),
            "replicas": 2,
        }

        deployment_multi_modified = deployment_multi.copy()
        deployment_multi_modified["images"] = [
            "nginx:1.21",
            "redis:7.2",
            "busybox:latest",
        ]

        result = compare_deployments([deployment_multi], [deployment_multi_modified])

        self.assertEqual(len(result["changed"]), 1)
        self.assertIn("images", result["changed"][0]["differences"])

    #
    # test_compare_empty_images
    # Tests comparison when deployments have empty image lists
    #
    def test_compare_empty_images(self):
        deployment_no_images = {
            "name": "no-images",
            "namespace": "default",
            "images": [],
            "created": datetime(2024, 11, 5, 10, 0, 0),
            "replicas": 1,
        }

        result = compare_deployments(
            [deployment_no_images], [deployment_no_images.copy()]
        )

        self.assertEqual(len(result["changed"]), 0)

    #
    # test_deployments_differ_same_deployments
    # Tests that identical deployments are not flagged as different
    #
    def test_deployments_differ_same_deployments(self):
        self.assertFalse(_deployments_differ(self.deployment1, self.deployment1))

    #
    # test_deployments_differ_different_images
    # Tests that deployments with different images are flagged as different
    #
    def test_deployments_differ_different_images(self):
        dep_modified = self.deployment1.copy()
        dep_modified["images"] = ["nginx:1.22"]
        self.assertTrue(_deployments_differ(self.deployment1, dep_modified))

    #
    # test_deployments_differ_different_replicas
    # Tests that deployments with different replica counts are flagged as different
    #
    def test_deployments_differ_different_replicas(self):
        dep_modified = self.deployment1.copy()
        dep_modified["replicas"] = 5
        self.assertTrue(_deployments_differ(self.deployment1, dep_modified))

    #
    # test_deployments_differ_image_order_matters
    # Tests that image order is considered when comparing deployments
    #
    def test_deployments_differ_image_order_matters(self):
        dep1 = {
            "name": "test",
            "namespace": "default",
            "images": ["nginx:1.21", "redis:7.0"],
            "created": datetime(2024, 11, 6, 10, 0, 0),
            "replicas": 1,
        }
        dep2 = dep1.copy()
        dep2["images"] = ["redis:7.0", "nginx:1.21"]

        self.assertTrue(_deployments_differ(dep1, dep2))

    #
    # test_get_differences_images_only
    # Tests extracting differences when only images differ
    #
    def test_get_differences_images_only(self):
        dep1 = self.deployment1
        dep2 = self.deployment1.copy()
        dep2["images"] = ["nginx:1.22"]

        differences = _get_differences(dep1, dep2)

        self.assertIn("images", differences)
        self.assertNotIn("replicas", differences)
        self.assertEqual(differences["images"]["ns1"], ["nginx:1.21"])
        self.assertEqual(differences["images"]["ns2"], ["nginx:1.22"])

    #
    # test_get_differences_replicas_only
    # Tests extracting differences when only replica counts differ
    #
    def test_get_differences_replicas_only(self):
        dep1 = self.deployment1
        dep2 = self.deployment1.copy()
        dep2["replicas"] = 10

        differences = _get_differences(dep1, dep2)

        self.assertNotIn("images", differences)
        self.assertIn("replicas", differences)
        self.assertEqual(differences["replicas"]["ns1"], 3)
        self.assertEqual(differences["replicas"]["ns2"], 10)

    #
    # test_get_differences_both_fields
    # Tests extracting differences when both images and replicas differ
    #
    def test_get_differences_both_fields(self):
        dep1 = self.deployment1
        dep2 = self.deployment1.copy()
        dep2["images"] = ["nginx:1.23"]
        dep2["replicas"] = 7

        differences = _get_differences(dep1, dep2)

        self.assertIn("images", differences)
        self.assertIn("replicas", differences)

    #
    # test_get_differences_no_differences
    # Tests that no differences are returned for identical deployments
    #
    def test_get_differences_no_differences(self):
        differences = _get_differences(self.deployment1, self.deployment1)

        self.assertEqual(len(differences), 0)

    #
    # test_compare_results_are_sorted
    # Tests that comparison results are sorted by deployment name
    #
    def test_compare_results_are_sorted(self):
        deployments_ns1 = [self.deployment3, self.deployment1, self.deployment2]
        deployments_ns2 = []

        result = compare_deployments(deployments_ns1, deployments_ns2)

        missing_names = [dep["name"] for dep in result["missing"]]
        self.assertEqual(missing_names, ["app1", "app2", "app3"])

    #
    # test_compare_complex_scenario
    # Tests comparison with a complex mix of missing, extra, and changed deployments
    #
    def test_compare_complex_scenario(self):

        deployment4 = {
            "name": "app4",
            "namespace": "production",
            "images": ["mysql:8.0"],
            "created": datetime(2024, 11, 7, 10, 0, 0),
            "replicas": 2,
        }

        deployment5 = {
            "name": "app5",
            "namespace": "production",
            "images": ["rabbitmq:3.11"],
            "created": datetime(2024, 11, 8, 10, 0, 0),
            "replicas": 1,
        }

        deployment2_modified = self.deployment2.copy()
        deployment2_modified["images"] = ["redis:7.2"]

        deployments_ns1 = [self.deployment1, self.deployment2, self.deployment3]
        deployments_ns2 = [deployment2_modified, deployment4, deployment5]

        result = compare_deployments(deployments_ns1, deployments_ns2)

        self.assertEqual(len(result["missing"]), 2)
        self.assertEqual(len(result["extra"]), 2)
        self.assertEqual(len(result["changed"]), 1)

        missing_names = [dep["name"] for dep in result["missing"]]
        self.assertIn("app1", missing_names)
        self.assertIn("app3", missing_names)

        extra_names = [dep["name"] for dep in result["extra"]]
        self.assertIn("app4", extra_names)
        self.assertIn("app5", extra_names)

        self.assertEqual(result["changed"][0]["name"], "app2")
        self.assertIn("images", result["changed"][0]["differences"])


if __name__ == "__main__":
    unittest.main()
