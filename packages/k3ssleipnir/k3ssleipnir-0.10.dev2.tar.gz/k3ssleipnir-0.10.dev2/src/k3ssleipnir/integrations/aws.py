from k3ssleipnir import normal_base_64_encode

import boto3
import boto3.session


class AwsIntegration:
    def __init__(self, region: str, profile_name: str) -> None:
        self.session = boto3.session.Session(
            region_name=region, profile_name=profile_name
        )

    def get_secret_value(self, secret_name: str) -> str:
        client = self.session.client("secretsmanager")
        response = client.get_secret_value(SecretId=secret_name)
        if "SecretBinary" in response:
            if len(response["SecretBinary"]) > 0:
                return normal_base_64_encode(value=response["SecretBinary"])
        if "SecretString" in response:
            if len(response["SecretString"]) > 0:
                return response["SecretString"]
        raise Exception('Unable to retrieve secret named "{}"'.format(secret_name))
