import pytest
from unittest.mock import Mock
from datetime import datetime


# Import all security check functions
from citrouille.security_checks.check_01_privileged_containers import (
    check as check_privileged,
)
from citrouille.security_checks.check_02_host_pid import check as check_host_pid
from citrouille.security_checks.check_03_host_ipc import check as check_host_ipc
from citrouille.security_checks.check_04_host_network import check as check_host_network
from citrouille.security_checks.check_05_run_as_root import check as check_run_as_root
from citrouille.security_checks.check_06_privilege_escalation import (
    check as check_privilege_escalation,
)
from citrouille.security_checks.check_07_capabilities import check as check_capabilities
from citrouille.security_checks.check_08_resource_limits import (
    check as check_resource_limits,
)
from citrouille.security_checks.check_09_host_path import check as check_host_path
from citrouille.security_checks.check_10_readonly_filesystem import (
    check as check_readonly_filesystem,
)
from citrouille.security_checks.check_11_seccomp import check as check_seccomp
from citrouille.security_checks.check_12_service_account_token import (
    check as check_service_account_token,
)
from citrouille.security_checks.check_13_image_tags import check as check_image_tags
from citrouille.security_checks.check_14_hardcoded_secrets import (
    check as check_hardcoded_secrets,
)
from citrouille.security_checks.check_15_pss_enforcement import (
    check as check_pss_enforcement,
)
from citrouille.security_checks.check_16_immutable_config import (
    check as check_immutable_config,
)
from citrouille.security_checks.check_17_emptydir_limits import (
    check as check_emptydir_limits,
)
from citrouille.security_checks.check_18_proc_mount import check as check_proc_mount
from citrouille.security_checks.check_19_rbac_roles import check as check_rbac_roles
from citrouille.security_checks.check_20_rbac_bindings import (
    check as check_rbac_bindings,
)
from citrouille.security_checks.check_21_shared_process_ns import (
    check as check_shared_process_ns,
)
from citrouille.security_checks.check_22_sysctls import check as check_sysctls
from citrouille.security_checks.check_23_network_policies import (
    check as check_network_policies,
)


def create_mock_deployment(
    name="test-deployment",
    namespace="default",
    containers=None,
    init_containers=None,
    pod_security_context=None,
):
    deployment = Mock()
    deployment.metadata = Mock()
    deployment.metadata.name = name
    deployment.metadata.namespace = namespace

    deployment.spec = Mock()
    deployment.spec.template = Mock()
    deployment.spec.template.spec = Mock()

    # Set containers
    deployment.spec.template.spec.containers = containers or []
    deployment.spec.template.spec.init_containers = init_containers

    # Set pod-level security context
    deployment.spec.template.spec.security_context = pod_security_context

    # Set volumes
    deployment.spec.template.spec.volumes = []

    # Initialize attributes that checks look for directly on spec
    deployment.spec.template.spec.host_pid = None
    deployment.spec.template.spec.host_ipc = None
    deployment.spec.template.spec.host_network = None
    deployment.spec.template.spec.share_process_namespace = None
    deployment.spec.template.spec.automount_service_account_token = None
    deployment.spec.template.spec.service_account_name = None

    return deployment


def create_mock_container(
    name="test-container",
    image="nginx:1.21",
    security_context=None,
    resources=None,
    env=None,
):
    container = Mock()
    container.name = name
    container.image = image
    container.security_context = security_context
    container.resources = resources
    container.env = env
    return container


def create_mock_security_context(
    privileged=None,
    allow_privilege_escalation=None,
    run_as_user=None,
    run_as_non_root=None,
    read_only_root_filesystem=None,
    capabilities=None,
    seccomp_profile=None,
    proc_mount=None,
):
    ctx = Mock()
    ctx.privileged = privileged
    ctx.allow_privilege_escalation = allow_privilege_escalation
    ctx.run_as_user = run_as_user
    ctx.run_as_non_root = run_as_non_root
    ctx.read_only_root_filesystem = read_only_root_filesystem
    ctx.capabilities = capabilities
    ctx.seccomp_profile = seccomp_profile
    ctx.proc_mount = proc_mount
    return ctx


def create_mock_pod_security_context(
    host_pid=None,
    host_ipc=None,
    host_network=None,
    run_as_user=None,
    run_as_non_root=None,
    share_process_namespace=None,
    sysctls=None,
):
    ctx = Mock()
    ctx.host_pid = host_pid
    ctx.host_ipc = host_ipc
    ctx.host_network = host_network
    ctx.run_as_user = run_as_user
    ctx.run_as_non_root = run_as_non_root
    ctx.share_process_namespace = share_process_namespace
    ctx.sysctls = sysctls
    return ctx


def create_mock_resources(
    limits_memory=None,
    limits_cpu=None,
    requests_memory=None,
    requests_cpu=None,
):
    resources = Mock()

    limits = {}
    if limits_memory:
        limits["memory"] = limits_memory
    if limits_cpu:
        limits["cpu"] = limits_cpu

    requests = {}
    if requests_memory:
        requests["memory"] = requests_memory
    if requests_cpu:
        requests["cpu"] = requests_cpu

    resources.limits = limits if limits else None
    resources.requests = requests if requests else None

    return resources


def create_mock_capabilities(add=None, drop=None):
    caps = Mock()
    caps.add = add
    caps.drop = drop
    return caps


def create_mock_env_var(name, value=None, value_from=None):
    env = Mock()
    env.name = name
    env.value = value
    env.value_from = value_from
    return env


def create_mock_volume(name, host_path=None, empty_dir=None):
    volume = Mock()
    volume.name = name
    volume.host_path = host_path
    volume.empty_dir = empty_dir
    return volume


def create_mock_namespace(name="default", labels=None):
    ns = Mock()
    ns.metadata = Mock()
    ns.metadata.name = name
    ns.metadata.labels = labels or {}
    return ns


def create_mock_configmap(name="test-cm", namespace="default", immutable=None):
    cm = Mock()
    cm.metadata = Mock()
    cm.metadata.name = name
    cm.metadata.namespace = namespace
    cm.immutable = immutable
    return cm


def create_mock_secret(name="test-secret", namespace="default", immutable=None):
    secret = Mock()
    secret.metadata = Mock()
    secret.metadata.name = name
    secret.metadata.namespace = namespace
    secret.immutable = immutable
    return secret


def create_mock_role(name="test-role", namespace="default", rules=None):
    role = Mock()
    role.metadata = Mock()
    role.metadata.name = name
    role.metadata.namespace = namespace
    role.rules = rules or []
    return role


def create_mock_cluster_role(name="test-cluster-role", rules=None):
    role = Mock()
    role.metadata = Mock()
    role.metadata.name = name
    role.metadata.namespace = None
    role.rules = rules or []
    return role


def create_mock_role_rule(verbs=None, resources=None, api_groups=None):
    rule = Mock()
    rule.verbs = verbs or []
    rule.resources = resources or []
    rule.api_groups = api_groups or []
    return rule


def create_mock_role_binding(
    name="test-binding",
    namespace="default",
    role_ref_name="test-role",
    subjects=None,
):
    binding = Mock()
    binding.metadata = Mock()
    binding.metadata.name = name
    binding.metadata.namespace = namespace

    binding.role_ref = Mock()
    binding.role_ref.name = role_ref_name

    binding.subjects = subjects or []
    return binding


def create_mock_cluster_role_binding(
    name="test-cluster-binding",
    role_ref_name="test-role",
    subjects=None,
):
    binding = Mock()
    binding.metadata = Mock()
    binding.metadata.name = name
    binding.metadata.namespace = None

    binding.role_ref = Mock()
    binding.role_ref.name = role_ref_name

    binding.subjects = subjects or []
    return binding


def create_mock_subject(kind="ServiceAccount", name="default"):
    subject = Mock()
    subject.kind = kind
    subject.name = name
    return subject


def create_mock_network_policy(
    name="test-policy",
    namespace="default",
    pod_selector=None,
    ingress=None,
    egress=None,
):
    policy = Mock()
    policy.metadata = Mock()
    policy.metadata.name = name
    policy.metadata.namespace = namespace

    policy.spec = Mock()
    policy.spec.pod_selector = pod_selector
    policy.spec.ingress = ingress
    policy.spec.egress = egress

    return policy


def create_mock_network_policy_peer(pod_selector=None, namespace_selector=None):
    peer = Mock()
    peer.pod_selector = pod_selector
    peer.namespace_selector = namespace_selector
    return peer


def create_mock_network_policy_ingress_rule(from_peers=None):
    rule = Mock()
    rule._from = from_peers
    return rule


def create_mock_network_policy_egress_rule(to_peers=None):
    rule = Mock()
    rule.to = to_peers
    return rule


#
# Test Classes
#


class TestCheckPrivilegedContainers:
    #
    # test_detects_privileged_container
    # Tests that check #1 detects containers running in privileged mode
    #
    def test_detects_privileged_container(self):
        sec_ctx = create_mock_security_context(privileged=True)
        container = create_mock_container(security_context=sec_ctx)
        deployment = create_mock_deployment(containers=[container])

        findings = check_privileged([deployment])

        assert len(findings) == 1
        assert findings[0]["severity"] == "CRITICAL"
        assert findings[0]["check_id"] == "1"
        assert "privileged mode" in findings[0]["message"]

    #
    # test_no_issue_when_not_privileged
    # Tests that check #1 doesn't flag non-privileged containers
    #
    def test_no_issue_when_not_privileged(self):
        sec_ctx = create_mock_security_context(privileged=False)
        container = create_mock_container(security_context=sec_ctx)
        deployment = create_mock_deployment(containers=[container])

        findings = check_privileged([deployment])

        assert len(findings) == 0

    #
    # test_detects_privileged_init_container
    # Tests that check #1 detects privileged init containers
    #
    def test_detects_privileged_init_container(self):
        sec_ctx = create_mock_security_context(privileged=True)
        init_container = create_mock_container(name="init", security_context=sec_ctx)
        deployment = create_mock_deployment(init_containers=[init_container])

        findings = check_privileged([deployment])

        assert len(findings) == 1
        assert "Init container" in findings[0]["message"]


class TestCheckHostPid:
    #
    # test_detects_host_pid
    # Tests that check #2 detects hostPID usage
    #
    def test_detects_host_pid(self):
        deployment = create_mock_deployment()
        deployment.spec.template.spec.host_pid = True

        findings = check_host_pid([deployment])

        assert len(findings) == 1
        assert findings[0]["severity"] == "HIGH"
        assert findings[0]["check_id"] == "2"
        assert "PID namespace" in findings[0]["message"]

    #
    # test_no_issue_when_host_pid_false
    # Tests that check #2 doesn't flag when hostPID is false
    #
    def test_no_issue_when_host_pid_false(self):
        deployment = create_mock_deployment()
        deployment.spec.template.spec.host_pid = False

        findings = check_host_pid([deployment])

        assert len(findings) == 0


class TestCheckHostIpc:
    #
    # test_detects_host_ipc
    # Tests that check #3 detects hostIPC usage
    #
    def test_detects_host_ipc(self):
        deployment = create_mock_deployment()
        deployment.spec.template.spec.host_ipc = True

        findings = check_host_ipc([deployment])

        assert len(findings) == 1
        assert findings[0]["severity"] == "HIGH"
        assert findings[0]["check_id"] == "3"
        assert "IPC namespace" in findings[0]["message"]

    #
    # test_no_issue_when_host_ipc_false
    # Tests that check #3 doesn't flag when hostIPC is false
    #
    def test_no_issue_when_host_ipc_false(self):
        deployment = create_mock_deployment()
        deployment.spec.template.spec.host_ipc = False

        findings = check_host_ipc([deployment])

        assert len(findings) == 0


class TestCheckHostNetwork:
    #
    # test_detects_host_network
    # Tests that check #4 detects hostNetwork usage
    #
    def test_detects_host_network(self):
        deployment = create_mock_deployment()
        deployment.spec.template.spec.host_network = True

        findings = check_host_network([deployment])

        assert len(findings) == 1
        assert findings[0]["severity"] == "HIGH"
        assert findings[0]["check_id"] == "4"
        assert "network namespace" in findings[0]["message"]

    #
    # test_no_issue_when_host_network_false
    # Tests that check #4 doesn't flag when hostNetwork is false
    #
    def test_no_issue_when_host_network_false(self):
        deployment = create_mock_deployment()
        deployment.spec.template.spec.host_network = False

        findings = check_host_network([deployment])

        assert len(findings) == 0


class TestCheckRunAsRoot:
    #
    # test_detects_run_as_user_zero
    # Tests that check #5 detects containers running as user 0
    #
    def test_detects_run_as_user_zero(self):
        sec_ctx = create_mock_security_context(run_as_user=0)
        container = create_mock_container(security_context=sec_ctx)
        deployment = create_mock_deployment(containers=[container])

        findings = check_run_as_root([deployment])

        assert len(findings) == 1
        assert findings[0]["severity"] == "HIGH"
        assert findings[0]["check_id"] == "5"
        assert "running as root" in findings[0]["message"]

    #
    # test_detects_missing_run_as_non_root
    # Tests that check #5 detects when runAsNonRoot is not set
    #
    def test_detects_missing_run_as_non_root(self):
        sec_ctx = create_mock_security_context(run_as_non_root=None)
        container = create_mock_container(security_context=sec_ctx)
        deployment = create_mock_deployment(containers=[container])

        findings = check_run_as_root([deployment])

        assert len(findings) == 1
        assert "runAsNonRoot is not set to true" in findings[0]["message"]

    #
    # test_no_issue_when_properly_configured
    # Tests that check #5 doesn't flag properly configured containers
    #
    def test_no_issue_when_properly_configured(self):
        sec_ctx = create_mock_security_context(run_as_non_root=True, run_as_user=1000)
        container = create_mock_container(security_context=sec_ctx)
        deployment = create_mock_deployment(containers=[container])

        findings = check_run_as_root([deployment])

        assert len(findings) == 0

    #
    # test_inherits_pod_level_settings
    # Tests that container inherits pod-level security context
    #
    def test_inherits_pod_level_settings(self):
        pod_sec_ctx = create_mock_pod_security_context(
            run_as_non_root=True, run_as_user=1000
        )
        container = create_mock_container()
        deployment = create_mock_deployment(
            containers=[container], pod_security_context=pod_sec_ctx
        )

        findings = check_run_as_root([deployment])

        assert len(findings) == 0


class TestCheckPrivilegeEscalation:
    #
    # test_detects_allow_privilege_escalation_true
    # Tests that check #6 detects allowPrivilegeEscalation: true
    #
    def test_detects_allow_privilege_escalation_true(self):
        sec_ctx = create_mock_security_context(allow_privilege_escalation=True)
        container = create_mock_container(security_context=sec_ctx)
        deployment = create_mock_deployment(containers=[container])

        findings = check_privilege_escalation([deployment])

        assert len(findings) == 1
        assert findings[0]["severity"] == "MEDIUM"
        assert findings[0]["check_id"] == "6"
        assert "allowPrivilegeEscalation" in findings[0]["message"]

    #
    # test_detects_missing_allow_privilege_escalation
    # Tests that check #6 detects when allowPrivilegeEscalation is not set
    #
    def test_detects_missing_allow_privilege_escalation(self):
        sec_ctx = None
        container = create_mock_container(security_context=sec_ctx)
        deployment = create_mock_deployment(containers=[container])

        findings = check_privilege_escalation([deployment])

        assert len(findings) == 1
        assert (
            "does not explicitly set allowPrivilegeEscalation to false"
            in findings[0]["message"]
        )

    #
    # test_no_issue_when_false
    # Tests that check #6 doesn't flag when allowPrivilegeEscalation is false
    #
    def test_no_issue_when_false(self):
        sec_ctx = create_mock_security_context(allow_privilege_escalation=False)
        container = create_mock_container(security_context=sec_ctx)
        deployment = create_mock_deployment(containers=[container])

        findings = check_privilege_escalation([deployment])

        assert len(findings) == 0


class TestCheckCapabilities:
    #
    # test_detects_dangerous_capabilities
    # Tests that check #7 detects dangerous capabilities
    #
    def test_detects_dangerous_capabilities(self):
        caps = create_mock_capabilities(add=["SYS_ADMIN", "NET_ADMIN"])
        sec_ctx = create_mock_security_context(capabilities=caps)
        container = create_mock_container(security_context=sec_ctx)
        deployment = create_mock_deployment(containers=[container])

        findings = check_capabilities([deployment])

        # Should find 2 issues: dangerous caps added, and ALL not dropped
        assert len(findings) == 2
        dangerous_finding = [
            f for f in findings if "dangerous capabilities" in f["message"]
        ][0]
        assert dangerous_finding["severity"] == "CRITICAL"
        assert "SYS_ADMIN" in dangerous_finding["message"]

    #
    # test_detects_missing_drop_all
    # Tests that check #7 detects when ALL capabilities are not dropped
    #
    def test_detects_missing_drop_all(self):
        caps = create_mock_capabilities(drop=[])
        sec_ctx = create_mock_security_context(capabilities=caps)
        container = create_mock_container(security_context=sec_ctx)
        deployment = create_mock_deployment(containers=[container])

        findings = check_capabilities([deployment])

        assert len(findings) == 1
        assert "does not drop all capabilities" in findings[0]["message"]

    #
    # test_detects_no_capabilities_configured
    # Tests that check #7 detects when capabilities are not configured
    #
    def test_detects_no_capabilities_configured(self):
        container = create_mock_container()
        deployment = create_mock_deployment(containers=[container])

        findings = check_capabilities([deployment])

        assert len(findings) == 1
        assert "does not drop all capabilities" in findings[0]["message"]

    #
    # test_no_issue_when_properly_configured
    # Tests that check #7 doesn't flag when ALL is dropped
    #
    def test_no_issue_when_properly_configured(self):
        caps = create_mock_capabilities(drop=["ALL"])
        sec_ctx = create_mock_security_context(capabilities=caps)
        container = create_mock_container(security_context=sec_ctx)
        deployment = create_mock_deployment(containers=[container])

        findings = check_capabilities([deployment])

        assert len(findings) == 0


class TestCheckResourceLimits:
    #
    # test_detects_no_resources
    # Tests that check #8 detects containers without resource configuration
    #
    def test_detects_no_resources(self):
        container = create_mock_container(resources=None)
        deployment = create_mock_deployment(containers=[container])

        findings = check_resource_limits([deployment])

        assert len(findings) == 1
        assert findings[0]["severity"] == "MEDIUM"
        assert findings[0]["check_id"] == "8"
        assert "no resources configured" in findings[0]["message"]

    #
    # test_detects_missing_limits
    # Tests that check #8 detects missing resource limits
    #
    def test_detects_missing_limits(self):
        resources = create_mock_resources()
        container = create_mock_container(resources=resources)
        deployment = create_mock_deployment(containers=[container])

        findings = check_resource_limits([deployment])

        assert len(findings) == 1
        assert "no limits set" in findings[0]["message"]

    #
    # test_detects_missing_memory_limit
    # Tests that check #8 detects missing memory limit
    #
    def test_detects_missing_memory_limit(self):
        resources = create_mock_resources(limits_cpu="500m")
        container = create_mock_container(resources=resources)
        deployment = create_mock_deployment(containers=[container])

        findings = check_resource_limits([deployment])

        assert len(findings) == 1
        assert "no memory limit" in findings[0]["message"]

    #
    # test_no_issue_when_properly_configured
    # Tests that check #8 doesn't flag when resources are properly set
    #
    def test_no_issue_when_properly_configured(self):
        resources = create_mock_resources(
            limits_memory="256Mi",
            limits_cpu="500m",
            requests_memory="128Mi",
            requests_cpu="250m",
        )
        container = create_mock_container(resources=resources)
        deployment = create_mock_deployment(containers=[container])

        findings = check_resource_limits([deployment])

        assert len(findings) == 0


class TestCheckHostPath:
    #
    # test_detects_hostpath_volume
    # Tests that check #9 detects hostPath volumes
    #
    def test_detects_hostpath_volume(self):
        host_path = Mock()
        host_path.path = "/var/run/docker.sock"
        volume = create_mock_volume(name="docker-sock", host_path=host_path)

        deployment = create_mock_deployment()
        deployment.spec.template.spec.volumes = [volume]

        findings = check_host_path([deployment])

        assert len(findings) == 1
        assert findings[0]["severity"] == "HIGH"
        assert findings[0]["check_id"] == "9"
        assert "hostPath" in findings[0]["message"]

    #
    # test_no_issue_without_hostpath
    # Tests that check #9 doesn't flag deployments without hostPath
    #
    def test_no_issue_without_hostpath(self):
        deployment = create_mock_deployment()
        deployment.spec.template.spec.volumes = []

        findings = check_host_path([deployment])

        assert len(findings) == 0


class TestCheckReadOnlyFilesystem:
    #
    # test_detects_missing_readonly_filesystem
    # Tests that check #10 detects when readOnlyRootFilesystem is not set
    #
    def test_detects_missing_readonly_filesystem(self):
        sec_ctx = None
        container = create_mock_container(security_context=sec_ctx)
        deployment = create_mock_deployment(containers=[container])

        findings = check_readonly_filesystem([deployment])

        assert len(findings) == 1
        assert findings[0]["severity"] == "MEDIUM"
        assert findings[0]["check_id"] == "10"
        assert "writable root filesystem" in findings[0]["message"]

    #
    # test_detects_readonly_filesystem_false
    # Tests that check #10 detects when readOnlyRootFilesystem is false
    #
    def test_detects_readonly_filesystem_false(self):
        sec_ctx = create_mock_security_context(read_only_root_filesystem=False)
        container = create_mock_container(security_context=sec_ctx)
        deployment = create_mock_deployment(containers=[container])

        findings = check_readonly_filesystem([deployment])

        assert len(findings) == 1

    #
    # test_no_issue_when_readonly_true
    # Tests that check #10 doesn't flag when readOnlyRootFilesystem is true
    #
    def test_no_issue_when_readonly_true(self):
        sec_ctx = create_mock_security_context(read_only_root_filesystem=True)
        container = create_mock_container(security_context=sec_ctx)
        deployment = create_mock_deployment(containers=[container])

        findings = check_readonly_filesystem([deployment])

        assert len(findings) == 0


class TestCheckSeccomp:
    #
    # test_detects_missing_seccomp
    # Tests that check #11 detects missing seccomp profile
    #
    def test_detects_missing_seccomp(self):
        sec_ctx = None
        container = create_mock_container(security_context=sec_ctx)
        deployment = create_mock_deployment(containers=[container])

        findings = check_seccomp([deployment])

        assert len(findings) == 1
        assert findings[0]["severity"] == "MEDIUM"
        assert findings[0]["check_id"] == "11"
        assert "does not specify a seccomp profile" in findings[0]["message"]

    #
    # test_detects_unconfined_seccomp
    # Tests that check #11 detects Unconfined seccomp profile
    #
    def test_detects_unconfined_seccomp(self):
        seccomp = Mock()
        seccomp.type = "Unconfined"
        sec_ctx = create_mock_security_context(seccomp_profile=seccomp)
        container = create_mock_container(security_context=sec_ctx)
        deployment = create_mock_deployment(containers=[container])

        findings = check_seccomp([deployment])

        assert len(findings) == 1
        assert "Unconfined" in findings[0]["message"]

    #
    # test_no_issue_with_runtime_default
    # Tests that check #11 doesn't flag RuntimeDefault profile
    #
    def test_no_issue_with_runtime_default(self):
        seccomp = Mock()
        seccomp.type = "RuntimeDefault"
        sec_ctx = create_mock_security_context(seccomp_profile=seccomp)
        container = create_mock_container(security_context=sec_ctx)
        deployment = create_mock_deployment(containers=[container])

        findings = check_seccomp([deployment])

        assert len(findings) == 0


class TestCheckServiceAccountToken:
    #
    # test_detects_auto_mount_token_true
    # Tests that check #12 detects automountServiceAccountToken: true
    #
    def test_detects_auto_mount_token_true(self):
        deployment = create_mock_deployment()
        deployment.spec.template.spec.automount_service_account_token = True
        deployment.spec.template.spec.service_account_name = "custom-sa"

        findings = check_service_account_token([deployment])

        # Should find automount issue (service account is custom)
        assert len(findings) >= 1
        assert findings[0]["severity"] == "MEDIUM"
        assert findings[0]["check_id"] == "12"
        assert "automounted" in findings[0]["message"]

    #
    # test_detects_auto_mount_token_not_set
    # Tests that check #12 detects when automountServiceAccountToken is not set
    #
    def test_detects_auto_mount_token_not_set(self):
        deployment = create_mock_deployment()
        deployment.spec.template.spec.automount_service_account_token = None
        deployment.spec.template.spec.service_account_name = None

        findings = check_service_account_token([deployment])

        assert len(findings) == 2  # automount + default service account

    #
    # test_no_issue_when_false
    # Tests that check #12 doesn't flag when automountServiceAccountToken is false
    #
    def test_no_issue_when_false(self):
        deployment = create_mock_deployment()
        deployment.spec.template.spec.automount_service_account_token = False
        deployment.spec.template.spec.service_account_name = "custom-sa"

        findings = check_service_account_token([deployment])

        assert len(findings) == 0


class TestCheckImageTags:
    #
    # test_detects_latest_tag
    # Tests that check #13 detects :latest tag
    #
    def test_detects_latest_tag(self):
        container = create_mock_container(image="nginx:latest")
        deployment = create_mock_deployment(containers=[container])

        findings = check_image_tags([deployment])

        assert len(findings) == 1
        assert findings[0]["severity"] == "HIGH"
        assert findings[0]["check_id"] == "13"
        assert "mutable image tag" in findings[0]["message"]

    #
    # test_detects_no_tag
    # Tests that check #13 detects images without tags
    #
    def test_detects_no_tag(self):
        container = create_mock_container(image="nginx")
        deployment = create_mock_deployment(containers=[container])

        findings = check_image_tags([deployment])

        assert len(findings) == 1
        assert findings[0]["severity"] == "HIGH"

    #
    # test_detects_version_tag
    # Tests that check #13 detects version tags (still mutable)
    #
    def test_detects_version_tag(self):
        container = create_mock_container(image="nginx:1.21")
        deployment = create_mock_deployment(containers=[container])

        findings = check_image_tags([deployment])

        assert len(findings) == 1
        assert findings[0]["severity"] == "MEDIUM"

    #
    # test_no_issue_with_digest
    # Tests that check #13 doesn't flag image digests
    #
    def test_no_issue_with_digest(self):
        container = create_mock_container(
            image="nginx@sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
        )
        deployment = create_mock_deployment(containers=[container])

        findings = check_image_tags([deployment])

        assert len(findings) == 0


class TestCheckHardcodedSecrets:
    #
    # test_detects_hardcoded_password
    # Tests that check #14 detects hardcoded passwords
    #
    def test_detects_hardcoded_password(self):
        env_var = create_mock_env_var(name="DB_PASSWORD", value="secret123")
        container = create_mock_container(env=[env_var])
        deployment = create_mock_deployment(containers=[container])

        findings = check_hardcoded_secrets([deployment])

        assert len(findings) == 1
        assert findings[0]["severity"] == "CRITICAL"
        assert findings[0]["check_id"] == "14"
        assert "hardcoded secret" in findings[0]["message"]

    #
    # test_detects_hardcoded_api_key
    # Tests that check #14 detects hardcoded API keys
    #
    def test_detects_hardcoded_api_key(self):
        env_var = create_mock_env_var(name="API_KEY", value="abc123")
        container = create_mock_container(env=[env_var])
        deployment = create_mock_deployment(containers=[container])

        findings = check_hardcoded_secrets([deployment])

        assert len(findings) == 1

    #
    # test_no_issue_with_value_from
    # Tests that check #14 doesn't flag secrets from valueFrom
    #
    def test_no_issue_with_value_from(self):
        value_from = Mock()
        env_var = create_mock_env_var(name="DB_PASSWORD", value_from=value_from)
        container = create_mock_container(env=[env_var])
        deployment = create_mock_deployment(containers=[container])

        findings = check_hardcoded_secrets([deployment])

        assert len(findings) == 0

    #
    # test_no_issue_with_non_secret_env
    # Tests that check #14 doesn't flag regular environment variables
    #
    def test_no_issue_with_non_secret_env(self):
        env_var = create_mock_env_var(name="LOG_LEVEL", value="info")
        container = create_mock_container(env=[env_var])
        deployment = create_mock_deployment(containers=[container])

        findings = check_hardcoded_secrets([deployment])

        assert len(findings) == 0


class TestCheckPssEnforcement:
    #
    # test_detects_missing_enforce_label
    # Tests that check #15 detects missing PSS enforce label
    #
    def test_detects_missing_enforce_label(self):
        namespace = create_mock_namespace(name="test-ns", labels={})

        findings = check_pss_enforcement(namespace)

        # Should find 3 issues: missing enforce, warn, and audit labels
        assert len(findings) == 3
        enforce_finding = [
            f for f in findings if "enforce" in f["message"] and f["severity"] == "HIGH"
        ][0]
        assert enforce_finding["check_id"] == "15"
        assert "does not enforce" in enforce_finding["message"]

    #
    # test_detects_weak_enforce_level
    # Tests that check #15 detects weak PSS enforcement level
    #
    def test_detects_weak_enforce_level(self):
        namespace = create_mock_namespace(
            labels={"pod-security.kubernetes.io/enforce": "privileged"}
        )

        findings = check_pss_enforcement(namespace)

        # Should detect weak enforcement + missing warn/audit
        weak_finding = [f for f in findings if "weak PSS enforcement" in f["message"]][
            0
        ]
        assert weak_finding["severity"] == "MEDIUM"

    #
    # test_no_issue_with_restricted
    # Tests that check #15 doesn't flag restricted enforcement
    #
    def test_no_issue_with_restricted(self):
        namespace = create_mock_namespace(
            labels={
                "pod-security.kubernetes.io/enforce": "restricted",
                "pod-security.kubernetes.io/warn": "restricted",
                "pod-security.kubernetes.io/audit": "restricted",
            }
        )

        findings = check_pss_enforcement(namespace)

        assert len(findings) == 0


class TestCheckImmutableConfig:
    #
    # test_detects_mutable_configmap
    # Tests that check #16 detects mutable ConfigMaps
    #
    def test_detects_mutable_configmap(self):
        cm = create_mock_configmap(immutable=None)

        findings = check_immutable_config([cm], [])

        assert len(findings) == 1
        assert findings[0]["severity"] == "LOW"
        assert findings[0]["check_id"] == "16"
        assert "mutable" in findings[0]["message"]

    #
    # test_detects_mutable_secret
    # Tests that check #16 detects mutable Secrets
    #
    def test_detects_mutable_secret(self):
        secret = create_mock_secret(immutable=None)

        findings = check_immutable_config([], [secret])

        assert len(findings) == 1
        assert findings[0]["severity"] == "MEDIUM"

    #
    # test_no_issue_with_immutable_resources
    # Tests that check #16 doesn't flag immutable resources
    #
    def test_no_issue_with_immutable_resources(self):
        cm = create_mock_configmap(immutable=True)
        secret = create_mock_secret(immutable=True)

        findings = check_immutable_config([cm], [secret])

        assert len(findings) == 0


class TestCheckEmptydirLimits:
    #
    # test_detects_emptydir_without_sizelimit
    # Tests that check #17 detects emptyDir volumes without sizeLimit
    #
    def test_detects_emptydir_without_sizelimit(self):
        empty_dir = Mock()
        empty_dir.size_limit = None
        volume = create_mock_volume(name="temp", empty_dir=empty_dir)

        deployment = create_mock_deployment()
        deployment.spec.template.spec.volumes = [volume]

        findings = check_emptydir_limits([deployment])

        assert len(findings) == 1
        assert findings[0]["severity"] == "MEDIUM"
        assert findings[0]["check_id"] == "17"
        assert "no size limit" in findings[0]["message"]

    #
    # test_no_issue_with_sizelimit
    # Tests that check #17 doesn't flag emptyDir with sizeLimit
    #
    def test_no_issue_with_sizelimit(self):
        empty_dir = Mock()
        empty_dir.size_limit = "1Gi"
        volume = create_mock_volume(name="temp", empty_dir=empty_dir)

        deployment = create_mock_deployment()
        deployment.spec.template.spec.volumes = [volume]

        findings = check_emptydir_limits([deployment])

        assert len(findings) == 0


class TestCheckProcMount:
    #
    # test_detects_unmasked_proc
    # Tests that check #18 detects unmasked /proc
    #
    def test_detects_unmasked_proc(self):
        sec_ctx = create_mock_security_context(proc_mount="Unmasked")
        container = create_mock_container(security_context=sec_ctx)
        deployment = create_mock_deployment(containers=[container])

        findings = check_proc_mount([deployment])

        assert len(findings) == 1
        assert findings[0]["severity"] == "MEDIUM"
        assert findings[0]["check_id"] == "18"
        assert "unmasked /proc" in findings[0]["message"]

    #
    # test_no_issue_with_default_proc
    # Tests that check #18 doesn't flag Default procMount
    #
    def test_no_issue_with_default_proc(self):
        sec_ctx = create_mock_security_context(proc_mount="Default")
        container = create_mock_container(security_context=sec_ctx)
        deployment = create_mock_deployment(containers=[container])

        findings = check_proc_mount([deployment])

        assert len(findings) == 0


class TestCheckRbacRoles:
    #
    # test_detects_wildcard_verbs
    # Tests that check #19 detects wildcard verbs
    #
    def test_detects_wildcard_verbs(self):
        rule = create_mock_role_rule(verbs=["*"], resources=["pods"], api_groups=[""])
        role = create_mock_role(rules=[rule])

        findings = check_rbac_roles([role], [])

        assert len(findings) >= 1
        wildcard_finding = [f for f in findings if "wildcard verbs" in f["message"]][0]
        assert wildcard_finding["severity"] == "CRITICAL"
        assert wildcard_finding["check_id"] == "19"

    #
    # test_detects_wildcard_resources
    # Tests that check #19 detects wildcard resources
    #
    def test_detects_wildcard_resources(self):
        rule = create_mock_role_rule(verbs=["get"], resources=["*"], api_groups=[""])
        role = create_mock_role(rules=[rule])

        findings = check_rbac_roles([role], [])

        assert len(findings) >= 1
        wildcard_finding = [f for f in findings if "all resources" in f["message"]][0]
        assert wildcard_finding["severity"] == "CRITICAL"

    #
    # test_detects_dangerous_permission_combo
    # Tests that check #19 detects dangerous permission combinations
    #
    def test_detects_dangerous_permission_combo(self):
        rule = create_mock_role_rule(
            verbs=["get", "list"], resources=["secrets"], api_groups=[""]
        )
        role = create_mock_role(rules=[rule])

        findings = check_rbac_roles([role], [])

        assert len(findings) >= 1
        dangerous_finding = [f for f in findings if "read all secrets" in f["message"]][
            0
        ]
        assert dangerous_finding["severity"] == "CRITICAL"

    #
    # test_checks_cluster_roles
    # Tests that check #19 checks ClusterRoles
    #
    def test_checks_cluster_roles(self):
        rule = create_mock_role_rule(verbs=["*"], resources=["*"], api_groups=["*"])
        cluster_role = create_mock_cluster_role(rules=[rule])

        findings = check_rbac_roles([], [cluster_role])

        # Should detect wildcard verbs, resources, and api_groups
        assert len(findings) >= 3


class TestCheckRbacBindings:
    #
    # test_detects_cluster_admin_binding
    # Tests that check #20 detects cluster-admin role binding
    #
    def test_detects_cluster_admin_binding(self):
        binding = create_mock_role_binding(role_ref_name="cluster-admin")

        findings = check_rbac_bindings([binding], [])

        assert len(findings) == 1
        assert findings[0]["severity"] == "CRITICAL"
        assert findings[0]["check_id"] == "20"
        assert "cluster-admin" in findings[0]["message"]

    #
    # test_detects_anonymous_user
    # Tests that check #20 detects bindings to anonymous users
    #
    def test_detects_anonymous_user(self):
        subject = create_mock_subject(kind="User", name="system:anonymous")
        binding = create_mock_role_binding(subjects=[subject])

        findings = check_rbac_bindings([binding], [])

        assert len(findings) == 1
        assert "system:anonymous" in findings[0]["message"]

    #
    # test_detects_unauthenticated_group
    # Tests that check #20 detects bindings to unauthenticated group
    #
    def test_detects_unauthenticated_group(self):
        subject = create_mock_subject(kind="Group", name="system:unauthenticated")
        binding = create_mock_role_binding(subjects=[subject])

        findings = check_rbac_bindings([binding], [])

        assert len(findings) == 1
        assert "system:unauthenticated" in findings[0]["message"]

    #
    # test_warns_about_authenticated_group
    # Tests that check #20 warns about system:authenticated group
    #
    def test_warns_about_authenticated_group(self):
        subject = create_mock_subject(kind="Group", name="system:authenticated")
        binding = create_mock_role_binding(subjects=[subject])

        findings = check_rbac_bindings([binding], [])

        assert len(findings) == 1
        assert findings[0]["severity"] == "HIGH"
        assert "all authenticated users" in findings[0]["message"]


class TestCheckSharedProcessNs:
    #
    # test_detects_shared_process_namespace
    # Tests that check #21 detects shared process namespace
    #
    def test_detects_shared_process_namespace(self):
        deployment = create_mock_deployment()
        deployment.spec.template.spec.share_process_namespace = True

        findings = check_shared_process_ns([deployment])

        assert len(findings) == 1
        assert findings[0]["severity"] == "MEDIUM"
        assert findings[0]["check_id"] == "21"
        assert "process namespace" in findings[0]["message"]

    #
    # test_no_issue_when_false
    # Tests that check #21 doesn't flag when shareProcessNamespace is false
    #
    def test_no_issue_when_false(self):
        deployment = create_mock_deployment()
        deployment.spec.template.spec.share_process_namespace = False

        findings = check_shared_process_ns([deployment])

        assert len(findings) == 0


class TestCheckSysctls:
    #
    # test_detects_unsafe_sysctls
    # Tests that check #22 detects unsafe sysctls
    #
    def test_detects_unsafe_sysctls(self):
        sysctl = Mock()
        sysctl.name = "kernel.shm_rmid_forced"
        sysctl.value = "1"

        sec_ctx = Mock()
        sec_ctx.sysctls = [sysctl]
        deployment = create_mock_deployment()
        deployment.spec.template.spec.security_context = sec_ctx

        findings = check_sysctls([deployment])

        assert len(findings) == 1
        assert findings[0]["severity"] == "CRITICAL"
        assert findings[0]["check_id"] == "22"
        assert "unsafe sysctl" in findings[0]["message"]

    #
    # test_allows_safe_sysctls
    # Tests that check #22 allows safe sysctls
    #
    def test_allows_safe_sysctls(self):
        sysctl = Mock()
        sysctl.name = "net.ipv4.ip_local_port_range"
        sysctl.value = "32768 60999"

        sec_ctx = Mock()
        sec_ctx.sysctls = [sysctl]
        deployment = create_mock_deployment()
        deployment.spec.template.spec.security_context = sec_ctx

        findings = check_sysctls([deployment])

        # Even "safe" sysctls get flagged with MEDIUM severity
        assert len(findings) == 1
        assert findings[0]["severity"] == "MEDIUM"


class TestCheckNetworkPolicies:
    #
    # test_detects_missing_network_policies
    # Tests that check #23 detects namespaces without NetworkPolicies
    #
    def test_detects_missing_network_policies(self):
        findings = check_network_policies([], "test-namespace")

        assert len(findings) == 1
        assert findings[0]["severity"] == "HIGH"
        assert findings[0]["check_id"] == "23"
        assert "no NetworkPolicies" in findings[0]["message"]

    #
    # test_detects_permissive_ingress
    # Tests that check #23 detects permissive ingress rules
    #
    def test_detects_permissive_ingress(self):
        pod_selector = Mock()
        pod_selector.match_labels = {}

        ingress_rule = create_mock_network_policy_ingress_rule(from_peers=None)
        policy = create_mock_network_policy(
            pod_selector=pod_selector, ingress=[ingress_rule]
        )

        findings = check_network_policies([policy], "test-namespace")

        assert len(findings) >= 1
        permissive_finding = [
            f for f in findings if "allows all ingress" in f["message"]
        ][0]
        assert permissive_finding["severity"] == "MEDIUM"

    #
    # test_detects_permissive_egress
    # Tests that check #23 detects permissive egress rules
    #
    def test_detects_permissive_egress(self):
        pod_selector = Mock()
        pod_selector.match_labels = {}

        egress_rule = create_mock_network_policy_egress_rule(to_peers=None)
        policy = create_mock_network_policy(
            pod_selector=pod_selector, egress=[egress_rule]
        )

        findings = check_network_policies([policy], "test-namespace")

        assert len(findings) >= 1
        permissive_finding = [
            f for f in findings if "allows all egress" in f["message"]
        ][0]
        assert permissive_finding["severity"] == "MEDIUM"

    #
    # test_no_issue_with_restrictive_policies
    # Tests that check #23 doesn't flag restrictive policies
    #
    def test_no_issue_with_restrictive_policies(self):
        pod_selector = Mock()
        pod_selector.match_labels = {"app": "web"}

        peer = create_mock_network_policy_peer()
        ingress_rule = create_mock_network_policy_ingress_rule(from_peers=[peer])
        policy = create_mock_network_policy(
            pod_selector=pod_selector, ingress=[ingress_rule]
        )

        findings = check_network_policies([policy], "test-namespace")

        # Should not flag the policy itself, only if there are no policies
        assert len(findings) == 0


class TestSecurityChecksIntegration:
    #
    # test_multiple_findings_same_deployment
    # Tests that multiple checks can find issues in the same deployment
    #
    def test_multiple_findings_same_deployment(self):
        # Create a deployment with multiple security issues
        sec_ctx = create_mock_security_context(
            privileged=True,
            run_as_user=0,
            allow_privilege_escalation=True,
        )
        container = create_mock_container(
            image="nginx:latest",
            security_context=sec_ctx,
            resources=None,
        )
        deployment = create_mock_deployment(containers=[container])

        # Run multiple checks
        findings_privileged = check_privileged([deployment])
        findings_root = check_run_as_root([deployment])
        findings_escalation = check_privilege_escalation([deployment])
        findings_image = check_image_tags([deployment])
        findings_resources = check_resource_limits([deployment])

        # Each check should find at least one issue
        assert len(findings_privileged) >= 1
        assert len(findings_root) >= 1
        assert len(findings_escalation) >= 1
        assert len(findings_image) >= 1
        assert len(findings_resources) >= 1

    #
    # test_secure_deployment_passes_all_checks
    # Tests that a properly secured deployment passes all checks
    #
    def test_secure_deployment_passes_all_checks(self):
        # Create a secure deployment
        caps = create_mock_capabilities(drop=["ALL"])
        seccomp = Mock()
        seccomp.type = "RuntimeDefault"

        sec_ctx = create_mock_security_context(
            privileged=False,
            run_as_user=1000,
            run_as_non_root=True,
            allow_privilege_escalation=False,
            read_only_root_filesystem=True,
            capabilities=caps,
            seccomp_profile=seccomp,
        )

        resources = create_mock_resources(
            limits_memory="256Mi",
            limits_cpu="500m",
            requests_memory="128Mi",
            requests_cpu="250m",
        )

        env_var = create_mock_env_var(name="LOG_LEVEL", value="info")

        container = create_mock_container(
            image="nginx@sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            security_context=sec_ctx,
            resources=resources,
            env=[env_var],
        )

        pod_sec_ctx = create_mock_pod_security_context(
            host_pid=False,
            host_ipc=False,
            host_network=False,
            share_process_namespace=False,
        )

        deployment = create_mock_deployment(
            containers=[container], pod_security_context=pod_sec_ctx
        )
        deployment.spec.template.spec.automount_service_account_token = False
        deployment.spec.template.spec.service_account_name = "custom-sa"
        deployment.spec.template.spec.host_pid = False
        deployment.spec.template.spec.host_ipc = False
        deployment.spec.template.spec.host_network = False
        deployment.spec.template.spec.share_process_namespace = False

        # Run all deployment-related checks
        assert len(check_privileged([deployment])) == 0
        assert len(check_host_pid([deployment])) == 0
        assert len(check_host_ipc([deployment])) == 0
        assert len(check_host_network([deployment])) == 0
        assert len(check_run_as_root([deployment])) == 0
        assert len(check_privilege_escalation([deployment])) == 0
        assert len(check_capabilities([deployment])) == 0
        assert len(check_resource_limits([deployment])) == 0
        assert len(check_host_path([deployment])) == 0
        assert len(check_readonly_filesystem([deployment])) == 0
        assert len(check_seccomp([deployment])) == 0
        assert len(check_service_account_token([deployment])) == 0
        assert len(check_image_tags([deployment])) == 0
        assert len(check_hardcoded_secrets([deployment])) == 0
        assert len(check_emptydir_limits([deployment])) == 0
        assert len(check_proc_mount([deployment])) == 0
        assert len(check_shared_process_ns([deployment])) == 0
        assert len(check_sysctls([deployment])) == 0
