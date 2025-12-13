import os
import os.path
import subprocess

import jq
import pytest
import yaml


@pytest.fixture(scope="session")
def kustomize_root_directory():
    return os.path.join(os.getcwd(), "k8s")


@pytest.fixture(scope="session")
def kustomize_environment_names(kustomize_root_directory):
    result = []
    for name in os.listdir(kustomize_root_directory):
        path = os.path.join(kustomize_root_directory, name)
        if not os.path.exists(os.path.join(path, "kustomization.yaml")):
            continue
        result.append(name)
    return result


@pytest.fixture(scope="session")
def kustomize_manifests(request, kustomize_root_directory, kustomize_environment_names):
    out = request.config.pluginmanager.getplugin("terminalreporter")
    cap = request.config.pluginmanager.getplugin("capturemanager")
    with cap.global_and_fixture_disabled():
        out.ensure_newline()
        out.write("Loading kustomize data...", flush=True)
        result = {}
        for name in kustomize_environment_names:
            path = os.path.join(kustomize_root_directory, name)
            result[name] = subprocess.run(
                f"kustomize build {path}",
                check=True,
                shell=True,
                capture_output=True,
            ).stdout
        out.write_line("done.")
        return result


@pytest.fixture(scope="session")
def kustomize_resources(kustomize_manifests):
    return {k: list(yaml.safe_load_all(v)) for k, v in kustomize_manifests.items()}


@pytest.fixture(scope="session")
def kustomize_jq(kustomize_resources):
    def _jq_k(query: str, environment: str) -> jq._ProgramWithInput:
        return jq.compile(query).input_value(kustomize_resources[environment])

    return _jq_k
