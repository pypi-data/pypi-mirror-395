import pytest

from pytest_kustomize import resolve_configmaps


parametrize = pytest.mark.parametrize


@parametrize("environment", ["staging", "production"])
def test_name_transform_removes_configmap_hash(kustomize_resources, environment):
    config = resolve_configmaps(kustomize_resources[environment])
    for deployment in ["webui", "api"]:
        assert config[deployment]["global_setting"] == "42"


@parametrize("environment", ["staging", "production"])
def test_resolve_configmaps_extracts_init_containers(kustomize_resources, environment):
    config = resolve_configmaps(kustomize_resources[environment])
    assert config["api"]["global_setting"] == "42"
    assert config["api-app"]["global_setting"] == "42"
    assert config["api-init-init"]["global_setting"] == "7"
