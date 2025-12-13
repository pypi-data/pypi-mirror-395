import os.path

import pytest


@pytest.fixture(scope="session")
def kustomize_root_directory():
    return os.path.dirname(__file__) + "/fixture"


@pytest.fixture(scope="session")
def kustomize_environment_names():
    return ["staging", "production"]
