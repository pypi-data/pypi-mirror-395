import json

from k3ssleipnir import logger
from k3ssleipnir.serialization import Deserialization, DeserializedInstance

from k3ssleipnir.models import MetaData, AwsProfileSpec, AwsProfileObject

import boto3.session


REGION_STATUS_SUPPORTED = [
    "ENABLED",
    "ENABLING",
    "ENABLED_BY_DEFAULT",
]


def _get_enabled_regions_for_profile(profile_name: str, next_token: str = "") -> tuple:
    supported_regions = []
    session = boto3.session.Session(profile_name=profile_name)
    aws_account = session.client("account")
    response = {}
    if next_token != "":
        response = aws_account.list_regions(
            NextToken=next_token,
            RegionOptStatusContains=REGION_STATUS_SUPPORTED,
        )
    else:
        response = aws_account.list_regions(
            RegionOptStatusContains=REGION_STATUS_SUPPORTED,
        )
    if "NextToken" in response:
        supported_regions += list(
            _get_enabled_regions_for_profile(
                profile_name=profile_name, next_token=response["NextToken"]
            )
        )
    for region_data in response["Regions"]:
        supported_regions.append(region_data["RegionName"])

    return tuple(supported_regions)


def _build_from_yaml(data: dict) -> DeserializedInstance:
    logger.debug("Converting data: {}".format(json.dumps(data)))

    metadata = MetaData(name=data["metadata"]["name"])
    spec = data["spec"]
    profile_name = metadata.name
    supported_regions = _get_enabled_regions_for_profile(profile_name=profile_name)
    default_region = supported_regions[0]

    logger.debug(
        'The initial default region for AWS Profile "{}" is "{}"'.format(
            profile_name, default_region
        )
    )

    if "defaultRegion" in spec:
        if spec["defaultRegion"] is not None:
            if spec["defaultRegion"] != "":
                selected_region = spec["defaultRegion"]
                if selected_region not in supported_regions:
                    raise Exception(
                        'For AWS Profile "{}", the selected region "{}" is not in the list of currently enabled regions for this profile. Enabled regions: {}'.format(
                            profile_name, selected_region, supported_regions
                        )
                    )
                default_region = "{}".format(selected_region)

    logger.info(
        'Default region for AWS Profile "{}": {}'.format(profile_name, default_region)
    )

    return DeserializedInstance(
        instance_type="AwsProfile",
        instance_object=AwsProfileObject(
            metadata=metadata, spec=AwsProfileSpec(defaultRegion=default_region)
        ),
    )


def build(data: dict) -> Deserialization:
    return Deserialization(builder=_build_from_yaml, data=data)
