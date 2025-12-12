import time
import traceback

from k3ssleipnir import logger

import kr8s
from kr8s.objects import Namespace, ConfigMap, Secret


def get_node_names(
    k3s_config_file: str,
    context_name: str = "default",
    max_retries: int = 20,
    sleep_seconds_between_retries: int = 3,
) -> tuple:
    node_names = []
    retry_nr = 0
    do_check = True
    while do_check is True:
        try:
            client = kr8s.api(kubeconfig=k3s_config_file, context=context_name)
            for node in client.get("nodes"):
                node_names.append(node.name)
            if len(node_names) > 0:
                do_check = False
        except:
            logger.error(traceback.format_exc())
            if retry_nr == max_retries:
                logger.warning("Getting nodes for cluster failed - Max retries reached")
                return tuple()
            time.sleep(sleep_seconds_between_retries)
            retry_nr += 1
            logger.warning(
                "Getting nodes retry nr {} failed - sleeping and retrying again.".format(
                    retry_nr
                )
            )
    logger.info("Current Nodes: {}".format(node_names))
    return tuple(node_names)


def get_namespaces(
    k3s_config_file: str,
    context_name: str = "default",
) -> tuple:
    namespaces = []
    try:
        client = kr8s.api(kubeconfig=k3s_config_file, context=context_name)
        for namespace in client.get("namespaces"):
            namespaces.append(namespace.name)
    except:
        logger.error(traceback.format_exc())
    logger.debug("Namespaces: {}".format(namespaces))
    return tuple(namespaces)


def create_namespace(
    namespace_name: str,
    k3s_config_file: str,
    context_name: str = "default",
) -> bool:
    try:
        client = kr8s.api(kubeconfig=k3s_config_file, context=context_name)
        namespace = Namespace(
            resource={
                "apiVersion": "v1",
                "kind": "Namespace",
                "metadata": {
                    "name": namespace_name,
                },
            },
            api=client,
        )
        namespace.create()
        if namespace_name not in get_namespaces(
            k3s_config_file=k3s_config_file, context_name=context_name
        ):
            return False
    except:
        logger.error(traceback.format_exc())
    return True


def create_simple_data_object(
    name: str,
    namespace: str,
    data: dict,
    k3s_config_file: str,
    context_name: str = "default",
    kind: str = "ConfigMap",
) -> bool:
    if kind not in (
        "ConfigMap",
        "Secret",
    ):
        logger.warning('Kine "{}" not supported - ignored'.format(kind))
    data = {
        "apiVersion": "v1",
        "kind": kind,
        "metadata": {
            "name": name,
        },
        "data": data,
    }
    if namespace not in get_namespaces(
        k3s_config_file=k3s_config_file, context_name=context_name
    ):
        create_namespace(
            namespace_name=namespace,
            k3s_config_file=k3s_config_file,
            context_name=context_name,
        )
    if kind == "Secret":
        data["type"] = "Opaque"
        secret = Secret(data, namespace=namespace)
        secret.create()
    else:
        config_map = ConfigMap(data, namespace=namespace)
        config_map.create()

    return True
