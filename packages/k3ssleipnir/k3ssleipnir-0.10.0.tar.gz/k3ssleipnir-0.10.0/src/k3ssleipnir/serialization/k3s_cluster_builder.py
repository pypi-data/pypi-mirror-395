import json
from pathlib import Path
import os

from k3ssleipnir import logger
from k3ssleipnir.serialization import Deserialization, DeserializedInstance

from k3ssleipnir.models import (
    MetaData,
    K3sClusterServerItem,
    K3sClusterObject,
    K3sClusterSpec,
    K3ClusterEnvironmentVariableValue,
    K3sClusterDataObject,
    K3ClusterEnvironmentVariable,
    K3sClusterScriptVolumeConfiguration,
    K3sClusterScriptRuntimeConfiguration,
    K3sClusterPostProvisioningScriptItem,
    K3sClusterKubectlConfiguration,
)


def _extract_environment_valiables(spec: dict) -> list:
    logger.debug("spec: {}".format(json.dumps(spec)))
    environment_variables = []
    if "environmentVariables" in spec:
        for env_var_spec in spec["environmentVariables"]:
            name = env_var_spec["name"]
            ref_name = "sourceName"
            params = {
                "sourceType": env_var_spec["valueSource"]["sourceType"],
            }
            if env_var_spec["valueSource"]["sourceType"] == "scalar":
                ref_name = "staticValue"
            params[ref_name] = env_var_spec["valueSource"][ref_name]
            source = K3ClusterEnvironmentVariableValue(**params)
            expose_to_scripts = False
            if "exposeToPostProvisionScripts" in env_var_spec:
                expose_to_scripts = env_var_spec["exposeToPostProvisionScripts"]
            save_in_cluster = None
            if "saveInCluster" in env_var_spec:
                save_in_cluster = K3sClusterDataObject(
                    kind=env_var_spec["saveInCluster"]["kind"],
                    name=env_var_spec["saveInCluster"]["name"],
                    namespace=env_var_spec["saveInCluster"]["namespace"],
                )
            environment_variables.append(
                K3ClusterEnvironmentVariable(
                    name=name,
                    valueSource=source,
                    exposeToPostProvisionScripts=expose_to_scripts,
                    saveInCluster=save_in_cluster,
                )
            )
    return environment_variables


def _extract_post_provisioning_scripts(spec: dict) -> list:
    post_provision_scripts = []
    if "postProvisionScripts" in spec:
        for script_spec in spec["postProvisionScripts"]:
            order = 0
            if "order" in script_spec:
                order = int(script_spec["order"])
            runtime = script_spec["scriptRuntime"]
            runtime_volumes = None
            if "volumes" in runtime:
                runtime_volumes = []
                for vol_spec in runtime["volumes"]:
                    runtime_volumes.append(
                        K3sClusterScriptVolumeConfiguration(
                            localPath=vol_spec["localPath"],
                            containerPath=vol_spec["containerMountPoint"],
                        )
                    )
            container_command = "podman"
            if "containerCommand" in runtime:
                container_command = runtime["containerCommand"]
            targets = ["LOCALHOST"]
            if "targets" in script_spec:
                targets = script_spec["targets"]
            script_src = script_spec["script"]
            post_run_sleep = 0
            if "postRunSleepSeconds" in script_spec:
                post_run_sleep = int(script_spec["postRunSleepSeconds"])

            runtime_config_parameters = {
                "image": runtime["image"],
                "volumes": runtime_volumes,
                "containerCommand": container_command,
            }
            if "overrideRunParameters" in runtime:
                runtime_config_parameters["overrideRunParameters"] = runtime[
                    "overrideRunParameters"
                ]
            runtime_config = K3sClusterScriptRuntimeConfiguration(
                **runtime_config_parameters
            )

            post_provision_scripts.append(
                K3sClusterPostProvisioningScriptItem(
                    order=order,
                    targets=targets,
                    script=script_src,
                    scriptRuntime=runtime_config,
                    postRunSleepSeconds=post_run_sleep,
                )
            )
    return post_provision_scripts


def _extract_custom_kubectl_configuration(spec: dict) -> K3sClusterKubectlConfiguration:
    if "kubectlConfiguration" not in spec:
        return K3sClusterKubectlConfiguration()
    config = K3sClusterKubectlConfiguration()

    targetConfig = spec["kubectlConfiguration"]
    if "targetKubeConfig" in targetConfig:
        config.targetKubeConfig = "{}".format(targetConfig["targetKubeConfig"])

    if "apiEndPointOverrides" not in targetConfig:
        return config

    if "hostname" in targetConfig["apiEndPointOverrides"]:
        config.apiEndPointOverrides.hostname = targetConfig["apiEndPointOverrides"][
            "hostname"
        ]
        config.apiEndPointOverrides.use_hostname_override = True

    if "port" in targetConfig["apiEndPointOverrides"]:
        config.apiEndPointOverrides.port = targetConfig["apiEndPointOverrides"]["port"]
        config.apiEndPointOverrides.use_port_override = True

    return config


def _build_from_yaml(data: dict) -> DeserializedInstance:
    logger.debug("Converting data: {}".format(json.dumps(data)))

    metadata = MetaData(name=data["metadata"]["name"])
    spec = data["spec"]

    tasks = spec["tasks"]
    servers = []
    for server in spec["servers"]:
        control_plane = True
        if "controlPlane" in server:
            control_plane = server["controlPlane"]
        servers.append(
            K3sClusterServerItem(
                serverName=server["serverName"], controlPlane=control_plane
            )
        )
    kubectlConfiguration = _extract_custom_kubectl_configuration(spec=spec)
    create_namespaces = []
    if "createNamespaces" in spec:
        create_namespaces = spec["createNamespaces"]
    environment_variables = _extract_environment_valiables(spec=spec)
    post_provision_scripts = _extract_post_provisioning_scripts(spec=spec)

    return DeserializedInstance(
        instance_type="K3sCluster",
        instance_object=K3sClusterObject(
            metadata=metadata,
            spec=K3sClusterSpec(
                tasks=tasks,
                servers=servers,
                kubectlConfiguration=kubectlConfiguration,
                createNamespaces=create_namespaces,
                environmentVariables=environment_variables,
                postProvisionScripts=post_provision_scripts,
            ),
        ),
    )


def build(data: dict) -> Deserialization:
    return Deserialization(builder=_build_from_yaml, data=data)
