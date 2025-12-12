import json
from datetime import datetime
from citrouille.formatters import TableFormatter, JSONFormatter

#
# test_formatters.py
#
# Tests for formatters.py
#


class TestTableFormatter:
    #
    # test_format_empty_deployments
    # Tests formatting behavior when the deployment list is empty
    #
    def test_format_empty_deployments(self):
        deployments = []
        result = TableFormatter.format_deployments(deployments)
        assert result == "No deployments found."

    #
    # test_format_single_deployment
    # Tests table formatting with a single deployment entry
    #
    def test_format_single_deployment(self):
        deployments = [
            {
                "name": "nginx",
                "namespace": "default",
                "images": ["nginx:1.21"],
                "created": datetime(2024, 11, 11, 10, 30, 0),
                "replicas": 3,
            }
        ]
        result = TableFormatter.format_deployments(deployments)
        assert "NAME" in result
        assert "NAMESPACE" in result
        assert "IMAGES" in result
        assert "CREATED" in result
        assert "REPLICAS" in result
        assert "nginx" in result
        assert "default" in result
        assert "nginx:1.21" in result
        assert "2024-11-11" in result
        assert "3" in result

    #
    # test_format_multiple_deployments
    # Tests table formatting with multiple deployment entries
    #
    def test_format_multiple_deployments(self):
        deployments = [
            {
                "name": "nginx",
                "namespace": "default",
                "images": ["nginx:1.21"],
                "created": datetime(2024, 11, 11, 10, 30, 0),
                "replicas": 3,
            },
            {
                "name": "redis",
                "namespace": "cache",
                "images": ["redis:7.0"],
                "created": datetime(2024, 11, 10, 15, 45, 0),
                "replicas": 1,
            },
        ]
        result = TableFormatter.format_deployments(deployments)
        assert "nginx" in result
        assert "redis" in result
        assert "default" in result
        assert "cache" in result

    #
    # test_format_deployment_with_multiple_images
    # Tests formatting of deployments containing multiple container images
    #
    def test_format_deployment_with_multiple_images(self):
        deployments = [
            {
                "name": "app",
                "namespace": "production",
                "images": ["app:v1.0", "sidecar:v2.1", "logger:latest"],
                "created": datetime(2024, 11, 11, 10, 30, 0),
                "replicas": 5,
            }
        ]
        result = TableFormatter.format_deployments(deployments)
        assert "app:v1.0, sidecar:v2.1, logger:latest" in result

    #
    # test_format_deployment_with_no_images
    # Tests formatting when a deployment has an empty images list
    #
    def test_format_deployment_with_no_images(self):
        deployments = [
            {
                "name": "empty",
                "namespace": "default",
                "images": [],
                "created": datetime(2024, 11, 11, 10, 30, 0),
                "replicas": 0,
            }
        ]
        result = TableFormatter.format_deployments(deployments)
        assert "None" in result

    #
    # test_format_deployment_with_none_timestamp
    # Tests formatting when the created timestamp is None
    #
    def test_format_deployment_with_none_timestamp(self):
        deployments = [
            {
                "name": "test",
                "namespace": "default",
                "images": ["test:latest"],
                "created": None,
                "replicas": 1,
            }
        ]
        result = TableFormatter.format_deployments(deployments)
        assert "Unknown" in result


class TestJSONFormatter:
    #
    # test_format_empty_deployments
    # Tests JSON formatting behavior when the deployment list is empty
    #
    def test_format_empty_deployments(self):
        deployments = []
        result = JSONFormatter.format_deployments(deployments)
        parsed = json.loads(result)
        assert parsed == []

    #
    # test_format_single_deployment
    # Tests JSON formatting with a single deployment entry
    #
    def test_format_single_deployment(self):
        deployments = [
            {
                "name": "nginx",
                "namespace": "default",
                "images": ["nginx:1.21"],
                "created": datetime(2024, 11, 11, 10, 30, 0),
                "replicas": 3,
            }
        ]
        result = JSONFormatter.format_deployments(deployments)
        parsed = json.loads(result)
        assert len(parsed) == 1
        assert parsed[0]["name"] == "nginx"
        assert parsed[0]["namespace"] == "default"
        assert parsed[0]["images"] == ["nginx:1.21"]
        assert parsed[0]["replicas"] == 3
        assert "2024-11-11" in parsed[0]["created"]

    #
    # test_format_multiple_deployments
    # Tests JSON formatting with multiple deployment entries
    #
    def test_format_multiple_deployments(self):
        deployments = [
            {
                "name": "nginx",
                "namespace": "default",
                "images": ["nginx:1.21"],
                "created": datetime(2024, 11, 11, 10, 30, 0),
                "replicas": 3,
            },
            {
                "name": "redis",
                "namespace": "cache",
                "images": ["redis:7.0"],
                "created": datetime(2024, 11, 10, 15, 45, 0),
                "replicas": 1,
            },
        ]
        result = JSONFormatter.format_deployments(deployments)
        parsed = json.loads(result)
        assert len(parsed) == 2
        assert parsed[0]["name"] == "nginx"
        assert parsed[1]["name"] == "redis"

    #
    # test_format_deployment_with_none_timestamp
    # Tests JSON formatting when the created timestamp is None
    #
    def test_format_deployment_with_none_timestamp(self):
        deployments = [
            {
                "name": "test",
                "namespace": "default",
                "images": ["test:latest"],
                "created": None,
                "replicas": 1,
            }
        ]
        result = JSONFormatter.format_deployments(deployments)
        parsed = json.loads(result)
        assert parsed[0]["created"] is None

    #
    # test_json_is_valid
    # Tests that the formatter produces valid, parseable JSON
    #
    def test_json_is_valid(self):
        deployments = [
            {
                "name": "test",
                "namespace": "default",
                "images": ["test:latest"],
                "created": datetime(2024, 11, 11, 10, 30, 0),
                "replicas": 1,
            }
        ]
        result = JSONFormatter.format_deployments(deployments)
        parsed = json.loads(result)
        assert isinstance(parsed, list)


class TestTableFormatterComparison:
    #
    # test_format_comparison_no_differences
    # Tests comparison table output when namespaces are identical
    #
    def test_format_comparison_no_differences(self):
        comparison = {"missing": [], "extra": [], "changed": []}
        result = TableFormatter.format_comparison(
            comparison, "namespace1", "namespace2"
        )
        assert "namespace1" in result
        assert "namespace2" in result
        assert "No differences found" in result

    #
    # test_format_comparison_missing_deployments
    # Tests comparison output when deployments are missing in second namespace
    #
    def test_format_comparison_missing_deployments(self):
        comparison = {
            "missing": [
                {
                    "name": "app1",
                    "namespace": "namespace1",
                    "images": ["nginx:1.21"],
                    "created": datetime(2024, 11, 1, 10, 0, 0),
                    "replicas": 3,
                }
            ],
            "extra": [],
            "changed": [],
        }
        result = TableFormatter.format_comparison(
            comparison, "namespace1", "namespace2"
        )
        assert "[-] Missing" in result
        assert "app1" in result
        assert "nginx:1.21" in result
        assert "Summary: 1 missing, 0 extra, 0 changed" in result

    #
    # test_format_comparison_extra_deployments
    # Tests comparison output when deployments are extra in second namespace
    #
    def test_format_comparison_extra_deployments(self):
        comparison = {
            "missing": [],
            "extra": [
                {
                    "name": "app2",
                    "namespace": "namespace2",
                    "images": ["redis:7.0"],
                    "created": datetime(2024, 11, 2, 10, 0, 0),
                    "replicas": 2,
                }
            ],
            "changed": [],
        }
        result = TableFormatter.format_comparison(
            comparison, "namespace1", "namespace2"
        )
        assert "[+] Extra" in result
        assert "app2" in result
        assert "redis:7.0" in result
        assert "Summary: 0 missing, 1 extra, 0 changed" in result

    #
    # test_format_comparison_changed_images
    # Tests comparison output when deployments have different container images
    #
    def test_format_comparison_changed_images(self):
        comparison = {
            "missing": [],
            "extra": [],
            "changed": [
                {
                    "name": "app1",
                    "ns1": {
                        "name": "app1",
                        "namespace": "namespace1",
                        "images": ["nginx:1.21"],
                        "created": datetime(2024, 11, 1, 10, 0, 0),
                        "replicas": 3,
                    },
                    "ns2": {
                        "name": "app1",
                        "namespace": "namespace2",
                        "images": ["nginx:1.22"],
                        "created": datetime(2024, 11, 1, 10, 0, 0),
                        "replicas": 3,
                    },
                    "differences": {
                        "images": {"ns1": ["nginx:1.21"], "ns2": ["nginx:1.22"]}
                    },
                }
            ],
        }
        result = TableFormatter.format_comparison(
            comparison, "namespace1", "namespace2"
        )
        assert "[~] Changed" in result
        assert "app1" in result
        assert "nginx:1.21" in result
        assert "nginx:1.22" in result
        assert "Summary: 0 missing, 0 extra, 1 changed" in result

    #
    # test_format_comparison_changed_replicas
    # Tests comparison output when deployments have different replica counts
    #
    def test_format_comparison_changed_replicas(self):
        comparison = {
            "missing": [],
            "extra": [],
            "changed": [
                {
                    "name": "app1",
                    "ns1": {
                        "name": "app1",
                        "namespace": "namespace1",
                        "images": ["nginx:1.21"],
                        "created": datetime(2024, 11, 1, 10, 0, 0),
                        "replicas": 3,
                    },
                    "ns2": {
                        "name": "app1",
                        "namespace": "namespace2",
                        "images": ["nginx:1.21"],
                        "created": datetime(2024, 11, 1, 10, 0, 0),
                        "replicas": 5,
                    },
                    "differences": {"replicas": {"ns1": 3, "ns2": 5}},
                }
            ],
        }
        result = TableFormatter.format_comparison(
            comparison, "namespace1", "namespace2"
        )
        assert "[~] Changed" in result
        assert "Replicas:" in result
        assert "3" in result
        assert "5" in result

    #
    # test_format_comparison_complex_scenario
    # Tests comparison output with a mix of missing, extra, and changed deployments
    #
    def test_format_comparison_complex_scenario(self):
        comparison = {
            "missing": [
                {
                    "name": "app1",
                    "namespace": "namespace1",
                    "images": ["nginx:1.21"],
                    "created": datetime(2024, 11, 1, 10, 0, 0),
                    "replicas": 3,
                }
            ],
            "extra": [
                {
                    "name": "app3",
                    "namespace": "namespace2",
                    "images": ["postgres:15"],
                    "created": datetime(2024, 11, 3, 10, 0, 0),
                    "replicas": 1,
                }
            ],
            "changed": [
                {
                    "name": "app2",
                    "ns1": {
                        "name": "app2",
                        "namespace": "namespace1",
                        "images": ["redis:7.0"],
                        "created": datetime(2024, 11, 2, 10, 0, 0),
                        "replicas": 2,
                    },
                    "ns2": {
                        "name": "app2",
                        "namespace": "namespace2",
                        "images": ["redis:7.2"],
                        "created": datetime(2024, 11, 2, 10, 0, 0),
                        "replicas": 2,
                    },
                    "differences": {
                        "images": {"ns1": ["redis:7.0"], "ns2": ["redis:7.2"]}
                    },
                }
            ],
        }
        result = TableFormatter.format_comparison(
            comparison, "namespace1", "namespace2"
        )
        assert "[-] Missing" in result
        assert "[+] Extra" in result
        assert "[~] Changed" in result
        assert "Summary: 1 missing, 1 extra, 1 changed" in result


class TestJSONFormatterComparison:
    #
    # test_format_comparison_no_differences
    # Tests JSON comparison output when namespaces are identical
    #
    def test_format_comparison_no_differences(self):
        comparison = {"missing": [], "extra": [], "changed": []}
        result = JSONFormatter.format_comparison(comparison, "namespace1", "namespace2")
        parsed = json.loads(result)
        assert parsed["namespace1"] == "namespace1"
        assert parsed["namespace2"] == "namespace2"
        assert len(parsed["missing"]) == 0
        assert len(parsed["extra"]) == 0
        assert len(parsed["changed"]) == 0
        assert parsed["summary"]["identical"] is True

    #
    # test_format_comparison_missing_deployments
    # Tests JSON comparison output when deployments are missing in second namespace
    #
    def test_format_comparison_missing_deployments(self):
        comparison = {
            "missing": [
                {
                    "name": "app1",
                    "namespace": "namespace1",
                    "images": ["nginx:1.21"],
                    "created": datetime(2024, 11, 1, 10, 0, 0),
                    "replicas": 3,
                }
            ],
            "extra": [],
            "changed": [],
        }
        result = JSONFormatter.format_comparison(comparison, "namespace1", "namespace2")
        parsed = json.loads(result)
        assert len(parsed["missing"]) == 1
        assert parsed["missing"][0]["name"] == "app1"
        assert parsed["missing"][0]["images"] == ["nginx:1.21"]
        assert parsed["summary"]["missing_count"] == 1
        assert parsed["summary"]["identical"] is False

    #
    # test_format_comparison_extra_deployments
    # Tests JSON comparison output when deployments are extra in second namespace
    #
    def test_format_comparison_extra_deployments(self):
        comparison = {
            "missing": [],
            "extra": [
                {
                    "name": "app2",
                    "namespace": "namespace2",
                    "images": ["redis:7.0"],
                    "created": datetime(2024, 11, 2, 10, 0, 0),
                    "replicas": 2,
                }
            ],
            "changed": [],
        }
        result = JSONFormatter.format_comparison(comparison, "namespace1", "namespace2")
        parsed = json.loads(result)
        assert len(parsed["extra"]) == 1
        assert parsed["extra"][0]["name"] == "app2"
        assert parsed["summary"]["extra_count"] == 1

    #
    # test_format_comparison_changed_deployments
    # Tests JSON comparison output when deployments have differences between namespaces
    #
    def test_format_comparison_changed_deployments(self):
        comparison = {
            "missing": [],
            "extra": [],
            "changed": [
                {
                    "name": "app1",
                    "ns1": {
                        "name": "app1",
                        "namespace": "namespace1",
                        "images": ["nginx:1.21"],
                        "created": datetime(2024, 11, 1, 10, 0, 0),
                        "replicas": 3,
                    },
                    "ns2": {
                        "name": "app1",
                        "namespace": "namespace2",
                        "images": ["nginx:1.22"],
                        "created": datetime(2024, 11, 1, 10, 0, 0),
                        "replicas": 3,
                    },
                    "differences": {
                        "images": {"ns1": ["nginx:1.21"], "ns2": ["nginx:1.22"]}
                    },
                }
            ],
        }
        result = JSONFormatter.format_comparison(comparison, "namespace1", "namespace2")
        parsed = json.loads(result)
        assert len(parsed["changed"]) == 1
        assert parsed["changed"][0]["name"] == "app1"
        assert "differences" in parsed["changed"][0]
        assert "images" in parsed["changed"][0]["differences"]
        assert parsed["summary"]["changed_count"] == 1

    #
    # test_format_comparison_timestamp_serialization
    # Tests that datetime timestamps are properly serialized to ISO format in JSON
    #
    def test_format_comparison_timestamp_serialization(self):
        comparison = {
            "missing": [
                {
                    "name": "app1",
                    "namespace": "namespace1",
                    "images": ["nginx:1.21"],
                    "created": datetime(2024, 11, 1, 10, 0, 0),
                    "replicas": 3,
                }
            ],
            "extra": [],
            "changed": [],
        }
        result = JSONFormatter.format_comparison(comparison, "namespace1", "namespace2")
        parsed = json.loads(result)
        # Check that timestamp is serialized as ISO format string
        assert "2024-11-01" in parsed["missing"][0]["created"]

    #
    # test_format_comparison_valid_json
    # Tests that the comparison formatter produces valid, parseable JSON
    #
    def test_format_comparison_valid_json(self):
        comparison = {"missing": [], "extra": [], "changed": []}
        result = JSONFormatter.format_comparison(comparison, "namespace1", "namespace2")
        # Should not raise an exception
        parsed = json.loads(result)
        assert isinstance(parsed, dict)

    #
    # test_format_comparison_summary_counts
    # Tests that summary counts accurately reflect missing, extra, and changed deployments
    #
    def test_format_comparison_summary_counts(self):
        comparison = {
            "missing": [
                {
                    "name": "app1",
                    "namespace": "ns1",
                    "images": [],
                    "created": None,
                    "replicas": 1,
                }
            ],
            "extra": [
                {
                    "name": "app2",
                    "namespace": "ns2",
                    "images": [],
                    "created": None,
                    "replicas": 1,
                },
                {
                    "name": "app3",
                    "namespace": "ns2",
                    "images": [],
                    "created": None,
                    "replicas": 1,
                },
            ],
            "changed": [
                {
                    "name": "app4",
                    "ns1": {
                        "name": "app4",
                        "namespace": "ns1",
                        "images": ["v1"],
                        "created": None,
                        "replicas": 1,
                    },
                    "ns2": {
                        "name": "app4",
                        "namespace": "ns2",
                        "images": ["v2"],
                        "created": None,
                        "replicas": 1,
                    },
                    "differences": {"images": {"ns1": ["v1"], "ns2": ["v2"]}},
                }
            ],
        }
        result = JSONFormatter.format_comparison(comparison, "namespace1", "namespace2")
        parsed = json.loads(result)
        assert parsed["summary"]["missing_count"] == 1
        assert parsed["summary"]["extra_count"] == 2
        assert parsed["summary"]["changed_count"] == 1
        assert parsed["summary"]["identical"] is False
