import os
from k3ssleipnir import logger
from k3ssleipnir.yaml_parser import load_yaml_manifest

from k3ssleipnir.serialization.git_builder import build as git_repository_builder
from k3ssleipnir.serialization.aws_profile_builder import build as aws_profile_builder
from k3ssleipnir.serialization.aws_secrets_builder import build as aws_secret_builder
from k3ssleipnir.serialization.server_builder import build as server_builder
from k3ssleipnir.serialization.k3s_cluster_builder import build as k3s_cluster_builder

from k3ssleipnir.models import (
    AwsProfileObject,
    AwsSecretObject,
    GitRepositoryObject,
    ConfigurationCollection,
    ServerObject,
    GitRepositoryPostCloneAction,
    K3sClusterObject,
)


def _process_git_side_effects(
    repo: GitRepositoryObject, collection: ConfigurationCollection
) -> ConfigurationCollection:
    post_clone_action: GitRepositoryPostCloneAction
    for post_clone_action in repo.spec.postCloneActions:
        if post_clone_action.actionType == "provisioning":
            logger.info(
                "Ingesting additional file: {}".format(post_clone_action.srcFilePath)
            )
            next_manifest = "{}".format(post_clone_action.srcFilePath)
            if next_manifest.startswith(os.sep) is False:
                next_manifest = "{}{}{}".format(
                    repo.spec.localWorkDir, os.sep, next_manifest
                )
            collection = construct(
                raw_material_file=next_manifest,
                collection=collection,
            )
        elif post_clone_action.actionType == "script":
            logger.warning("Script Action for GitRepository is not yet implemented...")
    return collection


def _ingest_aws_profiles(
    elements: tuple, collection: ConfigurationCollection = ConfigurationCollection()
) -> ConfigurationCollection:
    for data in elements:
        if "kind" in data:
            if data["kind"] == "AwsProfile":
                aws_profile: AwsProfileObject
                aws_profile = aws_profile_builder(data=data).instance.instance_object
                logger.debug(
                    "Serialized AwsProfile Object: {}".format(
                        aws_profile.model_dump_json(indent=4, exclude_none=True)
                    )
                )
                collection.add_aws_profile(aws_profile=aws_profile)
    return collection


def _ingest_aws_secrets(
    elements: tuple, collection: ConfigurationCollection = ConfigurationCollection()
) -> ConfigurationCollection:
    for data in elements:
        if "kind" in data:
            if data["kind"] == "AwsSecret":
                aws_secret: AwsSecretObject
                aws_secret = aws_secret_builder(data=data).instance.instance_object
                logger.debug(
                    "Serialized AwsSecret Object: {}".format(
                        aws_secret.model_dump_json(indent=4, exclude_none=True)
                    )
                )
                collection.add_aws_secret(aws_secret=aws_secret)

    logger.debug(
        "Retreieved secrets: {}".format(collection.get_names_by_kind(kind="Secret"))
    )
    return collection


def _ingest_git_repository(
    elements: tuple, collection: ConfigurationCollection = ConfigurationCollection()
) -> ConfigurationCollection:
    for data in elements:
        if "kind" in data:
            if data["kind"] == "GitRepository":
                repo: GitRepositoryObject
                repo = git_repository_builder(data=data).instance.instance_object
                logger.debug(
                    "Serialized GitRepository Object: {}".format(
                        repo.model_dump_json(indent=4, exclude_none=True)
                    )
                )
                collection.add_git_repository(repo=repo)
                collection = _process_git_side_effects(repo=repo, collection=collection)
    return collection


def _ingest_server(
    elements: tuple, collection: ConfigurationCollection = ConfigurationCollection()
) -> ConfigurationCollection:
    for data in elements:
        if "kind" in data:
            if data["kind"] == "Server":
                server: ServerObject
                server = server_builder(data=data).instance.instance_object
                logger.debug(
                    "Serialized Server Object: {}".format(
                        server.model_dump_json(indent=4, exclude_none=True)
                    )
                )
                collection.add_server(server=server)
    return collection


def _ingest_k3s_cluster(
    elements: tuple, collection: ConfigurationCollection = ConfigurationCollection()
) -> ConfigurationCollection:
    for data in elements:
        if "kind" in data:
            if data["kind"] == "K3sCluster":
                cluster: K3sClusterObject
                cluster = k3s_cluster_builder(data=data).instance.instance_object
                logger.debug(
                    "Serialized Cluster Object: {}".format(
                        cluster.model_dump_json(indent=4, exclude_none=True)
                    )
                )
                collection.add_cluster(cluster=cluster)
    return collection


def construct(
    raw_material_file: str,
    collection: ConfigurationCollection = ConfigurationCollection(),
) -> ConfigurationCollection:
    elements = load_yaml_manifest(manifest_file=raw_material_file)
    logger.info(
        'Loaded {} elements from file "{}"'.format(len(elements), raw_material_file)
    )

    # First ingest the Cloud Account Profiles and Secrets. We do this as later
    # objects may depend on the secrets.
    collection = _ingest_aws_profiles(elements=elements, collection=collection)

    # Now that we have the AWS Profiles, load all the defined secrets (if any)
    collection = _ingest_aws_secrets(elements=elements, collection=collection)

    # Now ingest all the GitRepository objects that may have dependcies on
    # secrets that should have been ingested by the previous step
    collection = _ingest_git_repository(elements=elements, collection=collection)

    # Finally we can consume any server definitions
    collection = _ingest_server(elements=elements, collection=collection)

    # And now that all the pre-requisite configurations are loaded, we can
    # create the cluster objects
    collection = _ingest_k3s_cluster(elements=elements, collection=collection)

    return collection
