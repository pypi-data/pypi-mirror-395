import json
import tempfile

from k3ssleipnir import logger
from k3ssleipnir.serialization import Deserialization, DeserializedInstance

from k3ssleipnir.models import (
    MetaData,
    GitRepositoryCredentials,
    GitRepositoryPostCloneAction,
    GitRepositorySpec,
    GitRepositoryObject,
)


def _build_from_yaml(data: dict) -> DeserializedInstance:
    logger.debug("Converting data: {}".format(json.dumps(data)))

    metadata = MetaData(name=data["metadata"]["name"])
    spec = data["spec"]
    url = spec["url"]
    credentials = GitRepositoryCredentials(credentialsType="anonymous")
    branch = "main"
    local_working_directory = tempfile.gettempdir()
    http_insecure = False
    post_cleanup = True
    post_clone_actions = []

    if "credentials" in spec:
        credential_data = {}
        for key in (
            "credentialsType",
            "value",
            "username",
        ):
            if key in spec["credentials"]:
                credential_data[key] = spec["credentials"][key]
        if len(credential_data) > 0:
            credentials = GitRepositoryCredentials(**credential_data)
    if "branch" in spec:
        branch = spec["branch"]
    if "localWorkDir" in spec:
        local_working_directory = spec["localWorkDir"]
    if "httpInsecure" in spec:
        http_insecure = spec["httpInsecure"]
    if "postCleanup" in spec:
        post_cleanup = spec["postCleanup"]
    if "postCloneActions" in spec:
        for action_definition in spec["postCloneActions"]:
            post_clone_actions.append(
                GitRepositoryPostCloneAction(
                    actionType=action_definition["actionType"],
                    srcFilePath=action_definition["srcFilePath"],
                )
            )

    final_spec = {
        "url": url,
        "branch": branch,
        "credentials": credentials,
        "localWorkDir": local_working_directory,
        "httpInsecure": http_insecure,
        "postCleanup": post_cleanup,
    }
    if len(post_clone_actions) > 0:
        final_spec["postCloneActions"] = post_clone_actions

    git_repo = GitRepositoryObject(
        metadata=metadata, spec=GitRepositorySpec(**final_spec)
    )

    logger.info(
        'Cloned Git repository "{}" into "{}".'.format(
            git_repo.spec.url, git_repo.spec.localWorkDir
        )
    )

    return DeserializedInstance(
        instance_type="GitRepository",
        instance_object=git_repo,
    )


def build(data: dict) -> Deserialization:
    return Deserialization(builder=_build_from_yaml, data=data)
