import json
from typing import Callable

from pydantic import BaseModel

from k3ssleipnir import logger
from k3ssleipnir.models import (
    GitRepositoryObject,
    AwsProfileObject,
    AwsSecretObject,
    ServerObject,
    K3sClusterObject,
)


class DeserializedInstance(BaseModel):
    instance_type: str
    instance_object: (
        BaseModel
        | GitRepositoryObject
        | AwsProfileObject
        | AwsSecretObject
        | ServerObject
        | K3sClusterObject
    )


def builder_template(data: dict) -> DeserializedInstance:
    logger.debug("Converting data: {}".format(json.dumps(data)))
    return DeserializedInstance(instance_type="undefined", instance_object=BaseModel())


class Deserialization:
    def __init__(
        self,
        builder: Callable[
            [
                dict,
            ],
            DeserializedInstance,
        ],
        data: dict,
    ) -> None:
        self.instance: DeserializedInstance = self._load(builder=builder, data=data)

    def _load(
        self,
        builder: Callable[
            [
                dict,
            ],
            DeserializedInstance,
        ],
        data: dict,
    ) -> DeserializedInstance:
        return builder(data)

    def __str__(self) -> str:
        return self.instance.instance_object.model_dump_json(exclude_none=True)

    def __repr__(self) -> str:
        return self.instance.instance_object.model_dump_json(exclude_none=True)

    def to_dict(self) -> dict:
        return json.loads(
            self.instance.instance_object.model_dump_json(exclude_none=True)
        )
