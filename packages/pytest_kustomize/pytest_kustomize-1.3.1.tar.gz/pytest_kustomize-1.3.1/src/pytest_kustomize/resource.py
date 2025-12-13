def split_dash(text):
    return text.rsplit("-", 1)[0]


def by_kind(manifest, kind, name_transform=split_dash):
    result = {}
    for resource in manifest:
        if resource["kind"] != kind:
            continue
        name = name_transform(resource["metadata"]["name"])
        result[name] = resource
    return result


def resolve_configmaps(manifest, name_transform=split_dash):
    result = {}
    configmaps = {k: v.get("data", {}) for k, v in by_kind(manifest, "ConfigMap").items()}
    for depl_name, deployment in by_kind(manifest, "Deployment").items():
        for i, container in enumerate(
            deployment["spec"]["template"]["spec"].get("containers", ()),
        ):
            name, config = _container_config(container, configmaps, name_transform)
            result[f"{depl_name}-{name}"] = config
            if i == 0:  # convenience
                result[depl_name] = config

        for i, container in enumerate(
            deployment["spec"]["template"]["spec"].get("initContainers", ())
        ):
            name, config = _container_config(container, configmaps, name_transform)
            result[f"{depl_name}-init-{name}"] = config
            if i == 0:  # convenience
                result[f"{depl_name}-init"] = config
    return result


def _container_config(container, configmaps, name_transform):
    config = {}
    for item in container.get("envFrom", ()):
        if "configMapRef" in item:
            config.update(configmaps[name_transform(item["configMapRef"]["name"])])
    return name_transform(container["name"]), config


def extract_externalsecret_data(manifest, name_transform=split_dash):
    result = {}
    for name, item in by_kind(manifest, "ExternalSecret", name_transform).items():
        for secret in item["spec"]["data"]:
            result[name + secret["secretKey"]] = secret["remoteRef"]
    return result
