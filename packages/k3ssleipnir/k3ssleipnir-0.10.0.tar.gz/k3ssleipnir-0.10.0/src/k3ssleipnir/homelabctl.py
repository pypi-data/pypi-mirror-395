import argparse
import os
import json
import copy

from k3ssleipnir import logger, configure_logging
from k3ssleipnir.models import ConfigurationCollection, K3sClusterObject
from k3ssleipnir.serialization.factory import construct
from k3ssleipnir.commands.delete import execute as cmd_delete
from k3ssleipnir.commands.apply import execute as cmd_apply


def main():
    # 1. Create the main parser
    parser = argparse.ArgumentParser(
        prog="k3ssleipnirctl",
        description="Deployes one or more K3s cluster in a k3ssleipnir context",
        epilog="WARNING: This is not for public solutions but intended for deployment in a private network with outgoing Internet access only.",
    )

    # Add arguments that apply to the whole app (e.g., global debug flag)
    parser.add_argument(
        "-d",
        dest="debug_mode",
        required=False,
        help="Enable Debug Mode. To enable, pass a value of '1', 'yes', 'true' or 'enabled'. NOTE: You must also specify a log file with --log-file for this option to have any real effect.",
        default="0",
    )
    parser.add_argument(
        "--log-file",
        dest="log_file",
        required=False,
        help="Enable Logging Mode. Logs will be written to the specified log file.",
        default=os.devnull,
    )

    # 2. Create the subparsers container
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Available commands"
    )

    # 3. Define the 'apply' command
    apply_parser = subparsers.add_parser("apply", help="Apply the manifest")
    apply_parser.add_argument(
        "-f",
        dest="manifest",
        required=True,
        help="YAML based manifest file to parse. This file contains the deployment configuration.",
    )
    apply_parser.add_argument(
        "--dump-secret-values",
        dest="dump_secret_values",
        required=False,
        help="Will not try to exclude secret values from log output. To enable, pass a value of '1', 'yes', 'true' or 'enabled'",
        default="0",
    )
    apply_parser.set_defaults(func=apply_command)

    # 4. Define the 'delete' command
    delete_parser = subparsers.add_parser("delete", help="Delete the manifest")
    delete_parser.add_argument(
        "-f",
        dest="manifest",
        required=True,
        help="YAML based manifest file to parse. This file contains the deployment configuration.",
    )
    delete_parser.set_defaults(func=delete_command)

    # Parse arguments
    args = parser.parse_args()
    debug = False
    if args.debug_mode.lower()[0] in ("1", "y", "t", "e"):
        debug = True
    configure_logging(log_file=args.log_file, debug=debug)

    # Call the function assigned to the command
    args.func(args)


def _house_keeping(collection: ConfigurationCollection):
    collection.git_cleanup()


# --- Command Handler Functions ---


def apply_command(args):
    logger.info("--- Running 'apply' Command ---")
    logger.debug("DEBUG ENABLED")
    collection = construct(raw_material_file=args.manifest)
    logger.info(
        "Configuration QTY per Kind: {}".format(json.dumps(collection.qty(), indent=4))
    )

    clusters = copy.deepcopy(collection.clusters)

    cluster_name: str
    cluster: K3sClusterObject
    for cluster_name, cluster in clusters.items():
        logger.info('Running apply command on cluster named "{}"'.format(cluster_name))
        print('> Provisioning of cluster named "{}"'.format(cluster_name))
        print("  Please be patient...")
        if "cleanupPreviousClusterDeployment" in cluster.spec.tasks:
            logger.info(
                'Running previous cluster cleanup on cluster "{}"'.format(cluster_name)
            )
            cmd_delete(configuration_collection=collection, target_cluster=cluster)
        cmd_apply(configuration_collection=collection, target_cluster=cluster)

    _house_keeping(collection=collection)
    logger.info("SUMMARY: \n{}\n\n".format(json.dumps(collection.qty(), indent=4)))


def delete_command(args):
    logger.info("--- Running 'delete' Command ---")
    logger.debug("DEBUG ENABLED")
    collection = construct(raw_material_file=args.manifest_file)
    logger.info(
        "Configuration QTY per Kind: {}".format(json.dumps(collection.qty(), indent=4))
    )

    clusters = copy.deepcopy(collection.clusters)

    cluster_name: str
    cluster: K3sClusterObject
    for cluster_name, cluster in clusters.items():
        logger.info('Running delete command on cluster named "{}"'.format(cluster_name))
        cmd_delete(configuration_collection=collection, target_cluster=cluster)

    _house_keeping(collection=collection)


if __name__ == "__main__":
    main()
