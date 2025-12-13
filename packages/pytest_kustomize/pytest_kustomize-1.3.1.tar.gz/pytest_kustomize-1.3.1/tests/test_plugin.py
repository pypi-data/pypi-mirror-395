import pytest

from pytest_kustomize import extract_externalsecret_data, resolve_configmaps


@pytest.mark.parametrize(
    "environment, value",
    [
        ("staging", "shared-db.staging.example.com"),
        ("production", "myservice-db.production.example.com"),
    ],
)
def test_database_matches_environment(kustomize_resources, environment, value):
    config = resolve_configmaps(kustomize_resources[environment])
    for deployment in ["webui", "api"]:
        assert config[deployment]["db_host"] == value


def test_production_has_no_staging_vault_paths(kustomize_resources):
    for secret in extract_externalsecret_data(kustomize_resources["production"]).values():
        assert "staging" not in secret["key"]


@pytest.mark.parametrize("environment", ["staging", "production"])
def test_jq(kustomize_jq, environment):
    for apiVersion in kustomize_jq(
        """.[] | select(."kind"=="ConfigMap").apiVersion""", environment
    ):
        assert apiVersion == "v1"
