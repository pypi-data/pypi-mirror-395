from k3ssleipnir import logger

from k3ssleipnir.models import (
    K3sClusterObject,
    ConfigurationCollection,
    ServerControl,
)


def execute(
    configuration_collection: ConfigurationCollection, target_cluster: K3sClusterObject
) -> ConfigurationCollection:
    # First, cleanup agents
    server_control_instance: ServerControl
    for (
        server_control_instance
    ) in configuration_collection.servers.get_named_cluster_data_plane_servers(
        cluster_name=target_cluster.metadata.name
    ):
        logger.info(
            'Cleanup of agent server "{}"'.format(
                server_control_instance.server.metadata.name
            )
        )
        server_control_instance.exec(
            command="sudo /usr/local/bin/k3s-agent-uninstall.sh"
        )

    # Finally, cleanup control plane
    server_control_instance: ServerControl
    for (
        server_control_instance
    ) in configuration_collection.servers.get_named_cluster_control_plane_servers(
        cluster_name=target_cluster.metadata.name
    ):
        logger.info(
            'Cleanup of control plane server "{}"'.format(
                server_control_instance.server.metadata.name
            )
        )
        server_control_instance.exec(command="sudo /usr/local/bin/k3s-uninstall.sh")

    return configuration_collection
