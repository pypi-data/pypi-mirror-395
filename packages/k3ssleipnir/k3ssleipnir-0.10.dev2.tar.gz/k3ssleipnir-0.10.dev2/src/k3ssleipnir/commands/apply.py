import time
import os
import tempfile
import json
import traceback
from base64 import b64encode
import subprocess

from k3ssleipnir import logger

from k3ssleipnir.models import (
    K3sClusterObject,
    ConfigurationCollection,
    ServerControl,
    KubeConfig,
    KubeConfigCluster,
    KubeConfigNamedCluster,
    KubeConfigAuthInfo,
    KubeConfigNamedAuthInfo,
    KubeConfigContext,
    KubeConfigNamedContext,
    K3ClusterEnvironmentVariable,
    K3ClusterEnvironmentVariableValue,
    GitRepositoryObject,
    Secret,
    K3sClusterPostProvisioningScriptItem,
    K3sClusterScriptVolumeConfiguration,
)

from k3ssleipnir.commands import (
    CONTROL_PLANE_INSTALL_SCRIPT_CONTENT_INITIAL,
    CONTROL_PLANE_INSTALL_SCRIPT_CONTENT_GENERAL,
    DATA_PLANE_INSTALL_SCRIPT_CONTENT,
)
from k3ssleipnir.yaml_parser import load_yaml_manifest, dump_dict_to_yaml_file
from k3ssleipnir.integrations.kubernetes import (
    get_node_names,
    create_namespace,
    create_simple_data_object,
)


def _build_environment_values_map(
    configuration_collection: ConfigurationCollection,
    target_cluster: K3sClusterObject,
    only_for_script: bool = False,
) -> dict:
    environment_variables_and_values = {}

    var: K3ClusterEnvironmentVariable
    for var in target_cluster.spec.environmentVariables:
        if only_for_script is True and var.exposeToPostProvisionScripts is False:
            logger.warning(
                'Environment variable "{}" is NOT intended for script consumption - ignoring'.format(
                    var.name
                )
            )
            continue
        value_source: K3ClusterEnvironmentVariableValue
        value_source = var.valueSource
        logger.info(
            'Building environment variable "{}" value for cluster "{}"'.format(
                var.name, target_cluster.metadata.name
            )
        )
        if value_source.sourceType == "scalar":
            environment_variables_and_values[var.name] = "{}".format(
                value_source.staticValue
            )
        elif value_source.sourceType == "gitRepo":
            repo_name = value_source.sourceName
            git_repo: GitRepositoryObject
            git_repo = configuration_collection.git_repositories[repo_name]
            environment_variables_and_values[var.name] = "{}".format(
                git_repo.spec.localWorkDir
            )
        elif value_source.sourceType == "secret":
            secret: Secret
            secret = configuration_collection.secrets.get_secret_by_name(
                name=value_source.sourceName
            )
            environment_variables_and_values[var.name] = "{}".format(secret.value)
        else:
            logger.warning(
                'Value Source type "{}" not yet supported - this variable will NOT be available.'.format(
                    value_source
                )
            )

    logger.debug(
        "Available environment variables: {}".format(
            tuple(environment_variables_and_values.keys())
        )
    )
    for k, v in environment_variables_and_values.items():
        logger.debug("Environment Variable Value: {}={}".format(k, v))
    return environment_variables_and_values


def _adapt_configuration(
    k3s_config_source_file: str,
    cluster_name: str,
    api_addr: str,
    api_port: int = 6443,
) -> KubeConfig:
    config = load_yaml_manifest(manifest_file=k3s_config_source_file)[0]
    user = "{}".format(cluster_name)
    logger.debug(
        'Cluster "{}" config: {}'.format(cluster_name, json.dumps(config, indent=4))
    )
    config["clusters"][0]["cluster"]["server"] = "https://{}:{}".format(
        api_addr, api_port
    )
    config["clusters"][0]["name"] = "{}".format(cluster_name)
    config["users"][0]["name"] = "{}".format(user)
    config["contexts"][0]["context"]["cluster"] = "{}".format(cluster_name)
    config["contexts"][0]["context"]["user"] = "{}".format(user)
    config["contexts"][0]["name"] = "{}".format(cluster_name)
    config["current-context"] = "{}".format(cluster_name)

    # Update the local once off copy of the kubectl config as well
    dump_dict_to_yaml_file(data=config, target_file=k3s_config_source_file)

    cluster_data = config["clusters"][0]
    user_data = config["users"][0]
    return KubeConfig(
        clusters=[
            KubeConfigNamedCluster(
                name=cluster_data["name"],
                cluster=KubeConfigCluster(
                    certificateAuthorityData=cluster_data["cluster"][
                        "certificate-authority-data"
                    ],
                    server="https://{}:{}".format(api_addr, api_port),
                ),
            ),
        ],
        users=[
            KubeConfigNamedAuthInfo(
                name=user_data["name"],
                user=KubeConfigAuthInfo(
                    clientCertificateData=user_data["user"]["client-certificate-data"],
                    clientKeyData=user_data["user"]["client-key-data"],
                ),
            ),
        ],
        contexts=[
            KubeConfigNamedContext(
                name=cluster_name,
                context=KubeConfigContext(cluster=cluster_name, user=cluster_name),
            )
        ],
        currentContext=cluster_data["name"],
    )


def _provision_primary_control_node(
    configuration_collection: ConfigurationCollection,
    target_cluster: K3sClusterObject,
    shared_token: str,
) -> ConfigurationCollection:
    initial_server: ServerControl
    initial_server = (
        configuration_collection.servers.get_named_cluster_primary_control_plane_server(
            cluster_name=target_cluster.metadata.name
        )
    )
    logger.info(
        'Provisioning initial control plane server named "{}"'.format(
            initial_server.server.metadata.name
        )
    )
    primary_server_addr = initial_server.server.spec.address
    initial_command = "{}".format(CONTROL_PLANE_INSTALL_SCRIPT_CONTENT_INITIAL)
    initial_command = initial_command.replace("__TOKEN__", shared_token)
    initial_command = initial_command.replace("__IP__", primary_server_addr)
    logger.debug(
        "INITIAL_COMMAND: \n----------\n{}\n----------\n".format(initial_command)
    )
    cmd_file = "{}{}k3s_cluster_init.sh".format(tempfile.gettempdir(), os.sep)
    k3s_tmp_config_file = "{}{}k3s_config_{}.yaml".format(
        tempfile.gettempdir(), os.sep, target_cluster.metadata.name
    )
    logger.debug(
        'Writing initial cluster bootstrap script to file "{}"'.format(cmd_file)
    )
    with open(cmd_file, "w") as f:
        f.write(initial_command)
    initial_server.scp(
        local_file=cmd_file, remote_file="/tmp/k3s_install.sh", operation="push"
    )
    initial_server.exec(command="chmod 775 /tmp/k3s_install.sh")
    initial_server.exec(command="sudo /tmp/k3s_install.sh")
    initial_server.scp(local_file=k3s_tmp_config_file, remote_file="/tmp/k3s.yaml")

    logger.info(
        'Attempting to create kubectl configuration file at "{}"'.format(
            target_cluster.spec.kubectlConfiguration.targetKubeConfig
        )
    )

    if os.path.exists(target_cluster.spec.kubectlConfiguration.targetKubeConfig):
        configuration_collection.get_kubeconfig_from_file_origin(
            kubeconfig_source_file=target_cluster.spec.kubectlConfiguration.targetKubeConfig,
            force_reload=True,
        )

    api_addr = (
        configuration_collection.servers.get_named_cluster_primary_control_plane_server(
            cluster_name=target_cluster.metadata.name
        ).server.spec.address
    )
    api_port = 6443
    if (
        target_cluster.spec.kubectlConfiguration.apiEndPointOverrides.use_hostname_override
        is True
    ):
        api_addr = (
            target_cluster.spec.kubectlConfiguration.apiEndPointOverrides.hostname
        )
    if (
        target_cluster.spec.kubectlConfiguration.apiEndPointOverrides.use_port_override
        is True
    ):
        api_port = target_cluster.spec.kubectlConfiguration.apiEndPointOverrides.port
    adapted_kubeconfig = _adapt_configuration(
        k3s_config_source_file=k3s_tmp_config_file,
        cluster_name=target_cluster.metadata.name,
        api_addr=api_addr,
        api_port=api_port,
    )

    # Create the combined configuration
    configuration_collection.upsert_kubeconfig(
        kubeconfig=adapted_kubeconfig,
        target_file=target_cluster.spec.kubectlConfiguration.targetKubeConfig,
    )

    node_names = get_node_names(
        k3s_config_file=k3s_tmp_config_file, context_name=target_cluster.metadata.name
    )
    if len(node_names) == 0:
        raise Exception(
            'Failed to instantiate primary node for cluster named "{}". Quiting.'.format(
                target_cluster.metadata.name
            )
        )

    os.unlink(cmd_file)
    os.unlink(k3s_tmp_config_file)

    print(
        '   - Server "{}" provisioned as PRIMARY control node for cluster "{}"'.format(
            initial_server.server.metadata.name, target_cluster.metadata.name
        )
    )
    return configuration_collection


def _check_node_joins_cluster(
    kubeconfg_file: str,
    context_name: str,
    expected_node_name: str,
    max_retries: int = 20,
    sleep_seconds_between_retries: int = 3,
    raise_Exception_if_node_does_not_join: bool = False,
) -> bool:
    logger.debug("kubeconfig_file    : {}".format(kubeconfg_file))
    logger.debug("context_name       : {}".format(context_name))
    logger.debug("expected_node_name : {}".format(expected_node_name))
    retry_nr = 0
    while True:
        retry_nr += 1
        try:
            if expected_node_name in get_node_names(
                k3s_config_file=kubeconfg_file, context_name=context_name
            ):
                return True
            else:
                logger.warning(
                    'Expected node name "{}" not yet joined to cluster.'.format(
                        expected_node_name
                    )
                )
        except:
            logger.error(traceback.format_exc())
        if retry_nr == max_retries:
            if raise_Exception_if_node_does_not_join is True:
                raise Exception(
                    'Node "{}" failed to join cluster'.format(expected_node_name)
                )
            logger.warning(
                'After {} attempts, node "{}" failed to join cluster.'.format(
                    retry_nr, expected_node_name
                )
            )
            return False
        time.sleep(sleep_seconds_between_retries)
        logger.warning(
            "Getting nodes retry nr {} failed - sleeping and retrying again.".format(
                retry_nr
            )
        )


def _provision_remaining_servers(
    configuration_collection: ConfigurationCollection,
    target_cluster: K3sClusterObject,
    shared_token: str,
    is_control_plane: bool = True,
) -> ConfigurationCollection:
    initial_server: ServerControl
    initial_server = (
        configuration_collection.servers.get_named_cluster_primary_control_plane_server(
            cluster_name=target_cluster.metadata.name
        )
    )
    primary_server_addr = initial_server.server.spec.address

    servers_collection = []
    if is_control_plane is True:
        servers_collection = (
            configuration_collection.servers.get_named_cluster_control_plane_servers(
                cluster_name=target_cluster.metadata.name, include_primary_server=False
            )
        )
    else:
        servers_collection = (
            configuration_collection.servers.get_named_cluster_data_plane_servers(
                cluster_name=target_cluster.metadata.name
            )
        )

    server: ServerControl
    for server in servers_collection:
        logger.info('Provisioning node named "{}"'.format(server.server.metadata.name))
        provisioning_command = "{}".format(CONTROL_PLANE_INSTALL_SCRIPT_CONTENT_GENERAL)
        if is_control_plane is False:
            provisioning_command = "{}".format(DATA_PLANE_INSTALL_SCRIPT_CONTENT)
        provisioning_command = provisioning_command.replace("__TOKEN__", shared_token)
        provisioning_command = provisioning_command.replace(
            "__IP__", primary_server_addr
        )
        logger.debug(
            "INITIAL_COMMAND: \n----------\n{}\n----------\n".format(
                provisioning_command
            )
        )
        cmd_file = "{}{}k3s_cluster_bootstrap_{}.sh".format(
            tempfile.gettempdir(), os.sep, server.server.metadata.name
        )
        logger.debug(
            'Writing initial cluster bootstrap script to file "{}"'.format(cmd_file)
        )
        with open(cmd_file, "w") as f:
            f.write(provisioning_command)
        server.scp(
            local_file=cmd_file, remote_file="/tmp/k3s_install.sh", operation="push"
        )
        server.exec(command="chmod 775 /tmp/k3s_install.sh")
        server.exec(command="sudo /tmp/k3s_install.sh")
        os.unlink(cmd_file)
        node_joined_cluster = _check_node_joins_cluster(
            kubeconfg_file=target_cluster.spec.kubectlConfiguration.targetKubeConfig,
            context_name=target_cluster.metadata.name,
            expected_node_name=server.server.metadata.name,
            raise_Exception_if_node_does_not_join=False,
        )
        if node_joined_cluster is True:
            print(
                '   - Server "{}" JOINED cluster "{}"'.format(
                    server.server.metadata.name, target_cluster.metadata.name
                )
            )
        else:
            print(
                '   - Server "{}" FAILED to join cluster "{}"'.format(
                    server.server.metadata.name, target_cluster.metadata.name
                )
            )

    return configuration_collection


def _create_in_cluster_data_objects(
    configuration_collection: ConfigurationCollection, target_cluster: K3sClusterObject
) -> ConfigurationCollection:
    environment_variables_and_values = _build_environment_values_map(
        configuration_collection=configuration_collection, target_cluster=target_cluster
    )

    kubeconfg_file = target_cluster.spec.kubectlConfiguration.targetKubeConfig
    context_name = target_cluster.metadata.name
    var: K3ClusterEnvironmentVariable
    for var in target_cluster.spec.environmentVariables:
        if var.saveInCluster is None:
            continue
        kind = "ConfigMap"
        if var.saveInCluster.kind.lower() == "secret":
            kind = "Secret"
        namespaces = []
        if isinstance(var.saveInCluster.namespace, str):
            namespaces.append(var.saveInCluster.namespace)
        else:
            namespaces = var.saveInCluster.namespace
        logger.info(
            'Saving variable "{}" in cluster "{}" as kind "{}" in namespaces: {}'.format(
                var.saveInCluster.name,
                target_cluster.metadata.name,
                var.saveInCluster.kind,
                namespaces,
            )
        )
        final_value = "{}".format(environment_variables_and_values[var.name])
        if kind == "Secret":
            final_value = b64encode(final_value.encode()).decode()
        for namespace in namespaces:
            create_simple_data_object(
                name=var.saveInCluster.name,
                namespace=namespace,
                data={"value": final_value},
                k3s_config_file=kubeconfg_file,
                context_name=context_name,
                kind=kind,
            )
    return configuration_collection


def _process_install_k3s_task(
    configuration_collection: ConfigurationCollection, target_cluster: K3sClusterObject
) -> ConfigurationCollection:
    shared_token = target_cluster.spec.calculatedSharedToken
    configuration_collection = _provision_primary_control_node(
        configuration_collection=configuration_collection,
        target_cluster=target_cluster,
        shared_token=shared_token,
    )

    configuration_collection = _provision_remaining_servers(
        configuration_collection=configuration_collection,
        target_cluster=target_cluster,
        shared_token=shared_token,
    )

    configuration_collection = _provision_remaining_servers(
        configuration_collection=configuration_collection,
        target_cluster=target_cluster,
        shared_token=shared_token,
        is_control_plane=False,
    )

    print(
        '   - Cluster "{}" configuration file located at "{}"'.format(
            target_cluster.metadata.name,
            target_cluster.spec.kubectlConfiguration.targetKubeConfig,
        )
    )
    configuration_collection = _create_in_cluster_data_objects(
        configuration_collection=configuration_collection, target_cluster=target_cluster
    )

    return configuration_collection


def _create_namespaces(
    configuration_collection: ConfigurationCollection, target_cluster: K3sClusterObject
) -> ConfigurationCollection:
    if target_cluster.spec.createNamespaces is None:
        return configuration_collection
    for namespace_name in target_cluster.spec.createNamespaces:
        if (
            create_namespace(
                namespace_name=namespace_name,
                k3s_config_file=target_cluster.spec.kubectlConfiguration.targetKubeConfig,
                context_name=target_cluster.metadata.name,
            )
            is False
        ):
            print(
                '   - Namespace "{}" create FAILED in cluster "{}"'.format(
                    namespace_name, target_cluster.metadata.name
                )
            )
        else:
            print(
                '   - Namespace "{}" CREATED in cluster "{}"'.format(
                    namespace_name, target_cluster.metadata.name
                )
            )
    return configuration_collection


def _volume_mounts_as_string(
    volumes: list[K3sClusterScriptVolumeConfiguration],
    environment_variables_and_value: dict,
) -> str:
    volumes_str = ""
    volume: K3sClusterScriptVolumeConfiguration
    for volume in volumes:
        local = volume.localPath
        if volume.localPath.startswith("$"):
            env_var_name_1 = volume.localPath.split("$")[1]
            local = environment_variables_and_value[env_var_name_1]
        remote = volume.containerPath
        if volume.containerPath.startswith("$"):
            env_var_name_2 = volume.containerPath.split("$")[1]
            remote = environment_variables_and_value[env_var_name_2]
        if len(volumes_str) == 0:
            volumes_str = "  -v {}:{} \\".format(local, remote)
        else:
            volumes_str = "{}\n  -v {}:{} \\".format(volumes_str, local, remote)
    logger.debug('Extra Volumes: "{}"'.format(volumes_str))
    return volumes_str


def _env_mounts_as_string(
    environment_variables_and_value: dict,
) -> str:
    env_str = ""
    for k, v in environment_variables_and_value.items():
        if len(env_str) == 0:
            env_str = '  -e {}="{}" \\'.format(k, v)
        else:
            env_str = '{}\n  -e {}="{}" \\'.format(env_str, k, v)
    logger.debug('Extra Environment Variables: "{}"'.format(env_str))
    return env_str


def _prepare_script_content_in_local_staging_file(
    environment_variables_and_values: dict,
    extra_env_for_localhost: str,
    script_base_path: str,
    script_item: K3sClusterPostProvisioningScriptItem,
    target_cluster: K3sClusterObject,
    script_counter: int,
    server_target_name: str,
) -> str:
    # Prepare Script Content
    script_file_content = "#!/usr/bin/env bash\n\n"
    for env_key, env_val in environment_variables_and_values.items():
        script_file_content = '{}export {}="{}"\n'.format(
            script_file_content, env_key, env_val
        )
    script_file_content = "{}\n__LOCALHOST_ENV__\n".format(script_file_content)
    script_file_content = "{}\n{}".format(script_file_content, script_item.script)
    logger.debug("Prepared script with size {} bytes".format(len(script_file_content)))

    local_script_file = "{}{}-{}-{}.sh".format(
        script_base_path,
        target_cluster.metadata.name,
        script_counter,
        server_target_name.lower(),
    )
    final_script_content = "{}".format(script_file_content)
    if server_target_name == "LOCALHOST":
        extra_env_for_localhost = (
            "{}\n\nkubectl config set-context --current --context {}\n\n".format(
                extra_env_for_localhost,
                target_cluster.metadata.name,
            )
        )
        final_script_content = final_script_content.replace(
            "__LOCALHOST_ENV__", extra_env_for_localhost
        )
    else:
        final_script_content = final_script_content.replace(
            "__LOCALHOST_ENV__",
            "# NOT RUNNING ON LOCALHOST - Kubernetes cluster config NOT available",
        )
    if os.path.exists(local_script_file):
        logger.info('Removing previous script file "{}"'.format(local_script_file))
        os.unlink(local_script_file)
    logger.info('Creating local staging script file "{}"'.format(local_script_file))
    with open(local_script_file, "w") as f:
        f.write(final_script_content)
    return local_script_file


def _prepare_script_container_execute_script(
    environment_variables_and_values: dict,
    script_base_path: str,
    target_cluster: K3sClusterObject,
    script_counter: int,
    server_target_name: str,
    container_cmd: str,
    image: str,
    script_file_path_to_execute: str,
    override_run_parameters: str,
    volumes: list,
) -> str:
    script_file_content = "#!/usr/bin/env bash\n\n"
    script_file_content = "{}\n{} run {} \\".format(
        script_file_content, container_cmd, override_run_parameters
    )

    container_run_file = "{}{}-{}-{}-execute.sh".format(
        script_base_path,
        target_cluster.metadata.name,
        script_counter,
        server_target_name.lower(),
    )
    if server_target_name == "LOCALHOST":
        script_file_content = "{}\n  -v {}:/tmp/cluster.yaml \\".format(
            script_file_content,
            target_cluster.spec.kubectlConfiguration.targetKubeConfig,
        )
        script_file_content = '{}\n  -e "KUBECONFIG=/tmp/cluster.yaml" \\'.format(
            script_file_content
        )
    script_file_content = "{}\n  -v {}:/tmp/exec.sh:ro \\".format(
        script_file_content, script_file_path_to_execute
    )

    extra_volumes = _volume_mounts_as_string(
        volumes=volumes,
        environment_variables_and_value=environment_variables_and_values,
    )
    if len(extra_volumes) > 0:
        script_file_content = "{}\n{}".format(script_file_content, extra_volumes)

    extra_env = _env_mounts_as_string(
        environment_variables_and_value=environment_variables_and_values
    )
    if len(extra_env) > 0:
        script_file_content = "{}\n{}".format(script_file_content, extra_env)

    script_file_content = "{}\n  {} bash /tmp/exec.sh".format(
        script_file_content, image
    )

    if os.path.exists(container_run_file):
        logger.info('Removing previous script file "{}"'.format(container_run_file))
        os.unlink(container_run_file)
    logger.info('Creating local staging script file "{}"'.format(container_run_file))
    with open(container_run_file, "w") as f:
        f.write(script_file_content)
    return container_run_file


def _process_post_provision_scripts(
    configuration_collection: ConfigurationCollection, target_cluster: K3sClusterObject
) -> ConfigurationCollection:
    environment_variables_and_values = _build_environment_values_map(
        configuration_collection=configuration_collection,
        target_cluster=target_cluster,
        only_for_script=True,
    )

    # Add some additioal environment variables that may be handy to have, i.e. the Kubernetes API address
    environment_variables_and_values["KUBERNETES_API_ADDRESS"] = (
        configuration_collection.servers.get_named_cluster_primary_control_plane_server(
            cluster_name=target_cluster.metadata.name
        ).server.spec.address
    )

    extra_env_for_localhost = """# Extra environment variables for localhost scripts
export KUBECONFIG=/tmp/cluster.yaml
export KUBECONFIG_CONTEXT_NAME={}
    """.format(target_cluster.metadata.name)
    # NOTE: The extra_env_for_localhost is only usefull for scripts running on LOCALHOST and if they use a container image with `kubectl` installed. The configuration file will only be mounted on scripts executing on LOCALHOST and therefore the file will not exist on other hosts.

    script_base_path = "{}{}".format(tempfile.gettempdir(), os.sep)
    script_counter = 0
    files_to_cleanup = []
    for index_key in target_cluster.spec.get_post_provision_script_order_index():
        script_item: K3sClusterPostProvisioningScriptItem
        for (
            script_item
        ) in target_cluster.spec.get_post_provisions_scripts_for_order_index(
            index_position=index_key
        ):
            script_counter += 1

            for server_target_name in script_item.targets:
                # Write out script file
                local_script_file = _prepare_script_content_in_local_staging_file(
                    environment_variables_and_values=environment_variables_and_values,
                    extra_env_for_localhost=extra_env_for_localhost,
                    script_base_path=script_base_path,
                    script_item=script_item,
                    target_cluster=target_cluster,
                    script_counter=script_counter,
                    server_target_name=server_target_name,
                )
                volumes = []
                if script_item.scriptRuntime.volumes is not None:
                    volumes = script_item.scriptRuntime.volumes
                container_execute_file = _prepare_script_container_execute_script(
                    environment_variables_and_values=environment_variables_and_values,
                    script_base_path=script_base_path,
                    target_cluster=target_cluster,
                    script_counter=script_counter,
                    server_target_name=server_target_name,
                    container_cmd=script_item.scriptRuntime.containerCommand,
                    image=script_item.scriptRuntime.image,
                    script_file_path_to_execute=local_script_file,
                    override_run_parameters=script_item.scriptRuntime.overrideRunParameters,
                    volumes=volumes,
                )
                files_to_cleanup.append(local_script_file)
                files_to_cleanup.append(container_execute_file)

                # Run the script
                logger.info(
                    'Running script "{}" on target "{}", executed by "{}"'.format(
                        local_script_file, server_target_name, container_execute_file
                    )
                )
                target_server_ref = "localhost"
                if server_target_name != "LOCALHOST":
                    target_server_ref = server_target_name
                    remote_server: ServerControl
                    remote_server = configuration_collection.servers.get_server_by_name(
                        server_name=target_server_ref
                    )
                    remote_server.scp(
                        local_file=local_script_file,
                        remote_file=local_script_file,
                        operation="put",
                    )
                    remote_server.scp(
                        local_file=container_execute_file,
                        remote_file=container_execute_file,
                        operation="put",
                    )
                    remote_server.exec(command="bash {}".format(container_execute_file))
                else:
                    cmd_result = subprocess.run(
                        [
                            "bash",
                            container_execute_file,
                        ],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                    if cmd_result.stdout is not None:
                        logger.info(
                            "Local Shell Command: STDOUT: {}".format(
                                cmd_result.stdout.decode("utf-8")
                            )
                        )
                    if cmd_result.stderr is not None:
                        logger.info(
                            "Local Shell Command: STDERR: {}".format(
                                cmd_result.stderr.decode("utf-8")
                            )
                        )

                print(
                    '   - Executed script in staging file "{}" on server "{}"'.format(
                        local_script_file, target_server_ref
                    )
                )

            logger.info(
                "Post script run sleep time in seconds: {}".format(
                    script_item.postRunSleepSeconds
                )
            )
            if script_item.postRunSleepSeconds > 0:
                time.sleep(script_item.postRunSleepSeconds)

    for file in files_to_cleanup:
        logger.debug('Removing file "{}"'.format(file))
        os.unlink(file)

    return configuration_collection


TASK_FUNCTION_MAP = {
    "installK3s": _process_install_k3s_task,
    "createNamespaces": _create_namespaces,
    "postProvisionScripts": _process_post_provision_scripts,
}
TASK_ORDER = (
    "installK3s",
    "createNamespaces",
    "postProvisionScripts",
)


def execute(
    configuration_collection: ConfigurationCollection, target_cluster: K3sClusterObject
) -> ConfigurationCollection:
    for task_name in TASK_ORDER:
        if task_name not in TASK_FUNCTION_MAP:
            print(
                "   - Task {} skipped (task name not defined or not implemented)".format(
                    task_name
                )
            )
            continue
        if task_name in target_cluster.spec.tasks:
            configuration_collection = TASK_FUNCTION_MAP[task_name](
                configuration_collection=configuration_collection,
                target_cluster=target_cluster,
            )
            print("   - Task {} completed".format(task_name))
        else:
            print("   - Task {} skipped (excluded by configuration)".format(task_name))

    return configuration_collection
