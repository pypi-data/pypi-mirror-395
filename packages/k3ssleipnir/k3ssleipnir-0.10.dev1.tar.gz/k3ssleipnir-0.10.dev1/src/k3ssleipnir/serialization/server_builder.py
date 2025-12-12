import json

from k3ssleipnir import logger
from k3ssleipnir.serialization import Deserialization, DeserializedInstance

from k3ssleipnir.models import MetaData, ServerCredentials, ServerSpec, ServerObject


def _build_from_yaml(data: dict) -> DeserializedInstance:
    logger.debug("Converting data: {}".format(json.dumps(data)))

    metadata = MetaData(name=data["metadata"]["name"])
    spec = data["spec"]
    port = 22

    if "sshPort" in spec:
        port = int(spec["sshPort"])

    return DeserializedInstance(
        instance_type="Server",
        instance_object=ServerObject(
            metadata=metadata,
            spec=ServerSpec(
                address=spec["address"],
                sshPort=port,
                credentials=ServerCredentials(
                    credentialsType=spec["credentials"]["credentialsType"],
                    value=spec["credentials"]["value"],
                    username=spec["credentials"]["username"],
                ),
            ),
        ),
    )


def build(data: dict) -> Deserialization:
    return Deserialization(builder=_build_from_yaml, data=data)
