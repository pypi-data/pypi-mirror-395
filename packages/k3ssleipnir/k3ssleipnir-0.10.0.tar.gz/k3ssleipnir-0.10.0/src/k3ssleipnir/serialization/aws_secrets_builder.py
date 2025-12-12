import json

from k3ssleipnir import logger
from k3ssleipnir.serialization import Deserialization, DeserializedInstance

from k3ssleipnir.models import MetaData, AwsSecretSpec, AwsSecretObject


def _build_from_yaml(data: dict) -> DeserializedInstance:
    logger.debug("Converting data: {}".format(json.dumps(data)))

    metadata = MetaData(name=data["metadata"]["name"])
    spec = data["spec"]

    aws_profile = spec["awsProfile"]
    conversion = ""
    mapping = {}

    if "conversion" in spec:
        conversion = spec["conversion"]

    if "mapping" in spec:
        mapping = spec["mapping"]

    return DeserializedInstance(
        instance_type="AwsProfile",
        instance_object=AwsSecretObject(
            metadata=metadata,
            spec=AwsSecretSpec(
                awsProfile=aws_profile, conversion=conversion, mapping=mapping
            ),
        ),
    )


def build(data: dict) -> Deserialization:
    return Deserialization(builder=_build_from_yaml, data=data)
