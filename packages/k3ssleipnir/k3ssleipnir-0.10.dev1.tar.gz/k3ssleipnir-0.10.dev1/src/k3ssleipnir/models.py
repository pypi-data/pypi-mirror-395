from typing_extensions import Self
from typing import List
import tempfile
import os
import json
import traceback
import string
import uuid
import hashlib
from pathlib import Path

from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    field_validator,
    model_validator,
    computed_field,
)
import pydantic_core

from k3ssleipnir import (
    logger,
    CONVERSION_FUNCTIONS,
    strip_url_creds,
    delete_directory,
    create_temp_directory,
    create_dir,
)
from k3ssleipnir.common import check_if_credentials_is_a_file, verify_ssl_certificate
from k3ssleipnir.integrations.aws import AwsIntegration
from k3ssleipnir.yaml_parser import load_yaml_manifest, dump_dict_to_yaml_file

from git import Repo

import paramiko


class MetaData(BaseModel):
    name: str = Field(
        title="Name",
        description="metadata.name field value",
        min_length=1,
        max_length=1024,
        examples=[
            "my-object-name",
        ],
    )


###############################################################################
###                                                                         ###
###   BASE SECRET MODEL                                                     ###
###                                                                         ###
###############################################################################


class Secret(BaseModel):
    name: str = Field(
        title="Secret Name",
        description="The name of the secret. Must be globally unique",
        min_length=1,
        max_length=256,
    )
    value: str = Field(
        title="Secret Value",
        description="The clear text value of the secret",
        min_length=1,
        max_length=10240,
    )
    original_manifest: dict = Field(
        title="Original Manifest", description="The original manifest data", default={}
    )


class Secrets:
    def __init__(self) -> None:
        self.secrets = {}

    def add_secret(self, secret: Secret):
        if secret.name in self.secrets:
            raise Exception('A secret named "{}" already exists'.format(secret.name))
        self.secrets[secret.name] = secret

    def get_secret_by_name(self, name: str) -> Secret:
        if name not in self.secrets:
            raise Exception('Secret named "{}" not found'.format(name))
        return self.secrets[name]

    def get_names(self) -> tuple:
        return tuple(self.secrets.keys())


###############################################################################
###                                                                         ###
###   AWS PROFILE MODEL                                                     ###
###                                                                         ###
###############################################################################


class AwsProfileSpec(BaseModel):
    defaultRegion: str = Field(
        title="AWS Region Name",
        description="The region that will be used for the session",
        min_length=1,
        max_length=256,
    )


class AwsProfileObject(BaseModel):
    metadata: MetaData = Field(
        title="metadata field",
        description="The MetaData values of a YAML Manifest object",
        examples=[MetaData(name="my-aws-profile")],
    )
    spec: AwsProfileSpec

    @computed_field
    @property
    def kind(self) -> str:
        return "AwsProfile"

    @computed_field
    @property
    def version(self) -> str:
        return "v1"


###############################################################################
###                                                                         ###
###   AWS SECRET MODEL                                                      ###
###                                                                         ###
###############################################################################


class AwsSecretSpec(BaseModel):
    awsProfile: str = Field(
        title="AWS Profile Name",
        description="Reference to a AwsProfile definition. The name here must match the metadata.name value of a AwsProfile.",
        min_length=1,
        max_length=1024,
    )
    conversion: str = Field(
        title="Conversion Function Name",
        description="If a function is defined here, the stored value will be first converted by this function",
        default="",
        min_length=0,
        max_length=1024,
    )
    mapping: dict = Field(
        title="Dictionary Mapping",
        description="Name/Value pairs that will map this secret dictionary Name to a new secret named by the Value",
        default={},
    )

    @field_validator("conversion", mode="before")
    @classmethod
    def is_conversion_function_supported(cls, value: str) -> str:
        supported_functions = tuple(CONVERSION_FUNCTIONS.keys())
        if value != "":
            if value not in supported_functions:
                raise ValueError(
                    'Conversion Function "{}" is not supported. Supported functions: {}'.format(
                        value, supported_functions
                    )
                )
        return value

    @field_validator("mapping", mode="before")
    @classmethod
    def is_mapping_structure_valie(cls, value: dict) -> dict:
        for k, v in value.items():
            if v is None:
                raise ValidationError('Value cannot be None for key "{}"'.format(k))
            if isinstance(v, str) is False:
                raise ValidationError(
                    'Value for key "{}" must be a string. Got {}'.format(k, type(value))
                )
        return value


class AwsSecretObject(BaseModel):
    metadata: MetaData = Field(
        title="metadata field",
        description="The MetaData values of a YAML Manifest object",
        examples=[MetaData(name="my-aws-secret")],
    )
    spec: AwsSecretSpec

    @computed_field
    @property
    def kind(self) -> str:
        return "AwsSecret"

    @computed_field
    @property
    def version(self) -> str:
        return "v1"


###############################################################################
###                                                                         ###
###   GIT REPOSITORY MODEL                                                  ###
###                                                                         ###
###############################################################################


class GitRepositoryCredentials(BaseModel):
    credentialsType: str = Field(
        title="Type of Credentials",
        description="Valid types can be 'ssh', 'password' or 'anonymous'.",
        default="anonymous",
        examples=["anonymous"],
    )
    value: str | None = Field(
        title="Credentials Value",
        description="Required for 'ssh' and 'password' credentialsType. Either the SSH private key path or the actual password. If a password is supplied, it must be the name of the password secret (kind: LabSecret)",
        default=None,
        examples=[
            None,
        ],
    )
    username: str | None = Field(
        title="Username",
        description="Required for 'ssh' and 'password' credentialsType. Username to use in combination with the SSH key or supplied password.",
        default=None,
        examples=[
            None,
        ],
    )

    @field_validator("credentialsType", mode="before")
    @classmethod
    def is_valid_crednentials_type(cls, value: str) -> str:
        lc_value = value.lower()
        if lc_value not in (
            "ssh",
            "password",
            "anonymous",
        ):
            raise ValueError("must be one of 'ssh', 'password' or 'anonymous'")
        return lc_value

    @model_validator(mode="after")
    def check_if_value_field_is_required(self) -> Self:
        if self.credentialsType in ("ssh", "password"):
            if self.value is None:
                raise ValueError(
                    "Value MUST be supplied of the type is either 'ssh' or 'password'"
                )
            if len(self.value) == 0:
                raise ValueError(
                    "Value must contain a valid string of at least ONE character when type is either 'ssh' or 'password'"
                )
            if self.username is None:
                raise ValueError(
                    "Username MUST be supplied of the type is either 'ssh' or 'password'"
                )
            if len(self.username) == 0:
                raise ValueError(
                    "Username must contain a valid string of at least ONE character when type is either 'ssh' or 'password'"
                )
        else:
            self.value = None
            self.username = None
        return self

    @model_validator(mode="after")
    def check_if_ssh_private_key_exists(self) -> Self:
        if self.credentialsType == "ssh":
            if check_if_credentials_is_a_file(credentials=self.value) is False:
                raise ValueError(
                    "When using SSH, the value must point to a SSH Private Key file on the local filesystem."
                )
        return self


class GitRepositoryPostCloneAction(BaseModel):
    actionType: str = Field(
        title="Action Type",
        description="Action type can be either 'provisioning' (parse source file as another manifest) or 'script' (execute the source file as a shell script)",
    )
    srcFilePath: str = Field(
        title="Source File Path",
        description="A file path, relative to the Git rpository. If the value starts with the system path seperator character, the file must still exist on the local system. The file existance will be tested only once the first attempt to access it is made.",
    )

    @field_validator("actionType", mode="before")
    @classmethod
    def is_valid_action_type(cls, value: str) -> str:
        lc_value = value.lower()
        if lc_value not in (
            "provisioning",
            "script",
        ):
            raise ValueError("must be one of 'provisioning' or 'script'")
        return lc_value


class GitRepositorySpec(BaseModel):
    url: str = Field(
        title="URL",
        description="The Git repository URI. Expecting either a HTTP, HTTPS or SSH like URI",
        min_length=7,
        max_length=2048,
        examples=[
            "ssh://git@codeberg.org/user/k3ssleipnir-configs.git",
        ],
    )
    branch: str = Field(
        title="branch",
        description="Reference (branch, commit or tag) to check-out post cloning",
        default="main",
        min_length=1,
        max_length=1024,
        examples=[
            "main",
        ],
    )
    credentials: GitRepositoryCredentials = Field(
        title="Git Repository Credentials",
        description="Credentials for the Git Repository",
        default=GitRepositoryCredentials(),
        examples=[
            GitRepositoryCredentials(
                credentialsType="password",
                value="a-secret-with-the-actual-password",
                username="user",
            ),
        ],
    )
    localWorkDir: str = Field(
        title="Local Working Directory",
        description="A base directory into which the repository will be cloned. If the project must NOT already exist in the directory.",
        default=tempfile.gettempdir(),
        examples=[
            tempfile.gettempdir(),
        ],
        min_length=1,
        max_length=2048,
    )
    httpInsecure: bool = Field(
        title="Enable HTTP Insecure Mode",
        description="iAllow cloning from HTTP sites as well as skipping SSL certificate validation. Set to true to run insecurely.",
        default=False,
        examples=[
            False,
        ],
    )
    postCleanup: bool = Field(
        title="Delete working directory",
        description="Delete working directory post processing",
        default=True,
        examples=[
            True,
        ],
    )
    postCloneActions: List[GitRepositoryPostCloneAction] = Field(
        title="POst Clone Actions",
        description="A list of tasks to run after the Git repository was cloned",
        default=[],
        examples=[
            GitRepositoryPostCloneAction(
                actionType="script", srcFilePath="/home/user/scripts/example.sh"
            )
        ],
    )

    @field_validator("localWorkDir", mode="before")
    @classmethod
    def is_work_dir_valid(cls, value: str | None) -> str:
        if value is None:
            return create_temp_directory()
        if value == "":
            return create_temp_directory()
        if os.path.exists(value) is True:
            raise ValueError(
                'Directory "{}" already exist. Specify a directory that does NOT exist. An Null/None type value as well as an empty string will force a random temporary directory to be created.'.format(
                    value
                )
            )
        create_dir(dir=value)
        return value

    @model_validator(mode="after")
    def check_for_insecure_http_usage(self) -> Self:
        if "http://" in self.url is True:
            if self.httpInsecure is False:
                raise ValueError(
                    "When using HTTP ensure that the httpInsecure value is set to true"
                )
        elif "https://" in self.url:
            if verify_ssl_certificate(hostname=self.url) is False:
                raise ValueError(
                    "Certificate validation failed for Git host {}".format(self.url)
                )
        return self


class GitRepositoryObject(BaseModel):
    metadata: MetaData = Field(
        title="metadata field",
        description="The MetaData values of a YAML Manifest object",
        examples=[MetaData(name="my-git-repository")],
    )
    spec: GitRepositorySpec

    @computed_field
    @property
    def kind(self) -> str:
        return "GitRepository"

    @computed_field
    @property
    def version(self) -> str:
        return "v1"


###############################################################################
###                                                                         ###
###   SERVERS MODEL                                                         ###
###                                                                         ###
###############################################################################


class ServerCredentials(BaseModel):
    credentialsType: str = Field(
        title="Type of Credentials",
        description="Valid types can be 'private-key' or 'password'.",
        examples=["private-key"],
    )
    value: str | None = Field(
        title="Credentials Value",
        description="Either the SSH private key path or the name of the secret containing the password.",
        examples=["/path/to/private-key", "name-of-secret-with-the-password"],
    )
    username: str | None = Field(
        title="Username",
        description="Username to use in combination with the SSH key or supplied password.",
        default=None,
        examples=[
            "user",
        ],
    )

    @field_validator("credentialsType", mode="before")
    @classmethod
    def is_valid_crednentials_type(cls, value: str) -> str:
        lc_value = value.lower()
        if lc_value not in (
            "private-key",
            "password",
        ):
            raise ValueError("must be one of 'ssh', 'password' or 'anonymous'")
        return lc_value

    @model_validator(mode="after")
    def check_if_ssh_private_key_exists(self) -> Self:
        if self.credentialsType == "private-key":
            if check_if_credentials_is_a_file(credentials=self.value) is False:
                raise ValueError(
                    "When using private key based authentication, the value must point to a SSH Private Key file on the local filesystem."
                )
        return self


class ServerSpec(BaseModel):
    address: str = Field(
        title="Server Address",
        description="Hostname or IP address of a server",
        min_length=1,
        max_length=1024,
        examples=[
            "10.0.0.1",
        ],
    )
    sshPort: int = Field(
        title="SSH Port",
        description="The TCP port to connect to. Expecting a SSH server to listen on this port on the server.",
        gt=0,
        lt=65535,
        default=22,
        examples=[
            22,
        ],
    )
    credentials: ServerCredentials = Field(
        title="Server Credentials",
        description="Definition of the server credentials",
        examples=[
            ServerCredentials(
                credentialsType="password",
                value="secret-name-containing-password",
                username="my-username-on-the-server",
            )
        ],
    )


class ServerObject(BaseModel):
    metadata: MetaData = Field(
        title="metadata field",
        description="The MetaData values of a YAML Manifest object",
        examples=[MetaData(name="server1")],
    )
    spec: ServerSpec

    @computed_field
    @property
    def kind(self) -> str:
        return "Server"

    @computed_field
    @property
    def version(self) -> str:
        return "v1"


class ServerControl:
    def __init__(self, server: ServerObject, secrets: Secrets) -> None:
        self.server = server
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connected = False
        self.is_primary = False
        self.is_control_plane_server = True
        self.cluster_name = ""

        self.credentials_value = ""
        if server.spec.credentials.credentialsType == "private-key":
            self.credentials_value = server.spec.credentials.value
        else:
            self.credentials_value = secrets.get_secret_by_name(
                name="{}".format(server.spec.credentials.value)
            ).value
        self._test()

    def _test(self):
        self.exec(command="hostname")
        self.exec(command="whoami")

    def set_primary(self):
        self.is_primary = True
        self.set_as_control_plane()

    def set_as_agent(self):
        self.is_control_plane_server = False

    def set_as_control_plane(self):
        self.is_control_plane_server = True

    def link_to_cluster(self, cluster_name: str):
        if self.cluster_name != "":
            raise Exception(
                'Cannot link server "{}" to cluster "{}" as it was previously linked to cluster named "{}"'.format(
                    self.server.metadata.name, cluster_name, self.cluster_name
                )
            )
        self.cluster_name = cluster_name

    def get_connection(self):
        if self.connected is True:
            return
        if self.server.spec.credentials.credentialsType == "password":
            self._auth_password()
        else:
            self._auth_private_key()
        self.connected = True

    def _auth_password(self):
        password = "{}".format(self.credentials_value)
        logger.debug(
            "SERVER AUTH: ssh -p {} {}@{} [{}]".format(
                self.server.spec.sshPort,
                self.server.spec.credentials.username,
                self.server.spec.address,
                "*" * len(password),
            )
        )
        self.ssh_client.connect(
            hostname=self.server.spec.address,
            port=self.server.spec.sshPort,
            username=self.server.spec.credentials.username,
            password=password,
        )

    def _auth_private_key(self):
        logger.debug(
            "SERVER AUTH: ssh -p {} -i {} {}@{}".format(
                self.server.spec.sshPort,
                self.credentials_value,
                self.server.spec.credentials.username,
                self.server.spec.address,
            )
        )
        self.ssh_client.connect(
            hostname=self.server.spec.address,
            port=self.server.spec.sshPort,
            username=self.server.spec.credentials.username,
            key_filename="{}".format(self.credentials_value),
        )

    def exec(self, command: str, tries: int = 0) -> tuple:
        logger.debug("EXEC COMMAND: {}".format(command))
        if tries == 3:
            raise Exception(
                "All retries to execute command on remote host failed! Host: {}".format(
                    self.server.spec.address
                )
            )
        retries_exchausted = False
        try:
            self.get_connection()
            stdin, stdout, stderr = self.ssh_client.exec_command(command)
            for line in stdout.readlines():
                logger.info(
                    "[{}] STDOUT: {}".format(self.server.metadata.name, line.strip())
                )
            for line in stderr.readlines():
                logger.error(
                    "[{}] STDERR: {}".format(self.server.metadata.name, line.strip())
                )
            return (
                stdin,
                stdout.readlines(),
                stderr.readlines(),
            )
        except:
            ex = traceback.format_exc()
            if tries < 3:
                print(ex)
                retries_exchausted = True
            else:
                return (None, None, ex)
        if retries_exchausted is True:
            raise Exception(
                "All attempts to execute command on remote server has failed. Server name: {}".format(
                    self.server.metadata.name
                )
            )
        return self.exec(command=command, tries=tries + 1)

    def scp(
        self, local_file: str, remote_file: str, operation: str = "get", tries: int = 0
    ) -> bool:
        if tries == 3:
            raise Exception(
                "All retries to execute command on remote host failed! Host: {}".format(
                    self.server.spec.address
                )
            )
        op = "G"
        if operation[0].upper() != "G":
            op = "P"
        retries_exchausted = False
        try:
            self.get_connection()
            # scp = SCPClient(self.ssh_client.get_transport())
            scp = self.ssh_client.open_sftp()
            if op == "G":
                logger.info(
                    'SCP geting "{}" and saving to "{}"'.format(remote_file, local_file)
                )
                scp.get(remotepath=remote_file, localpath=local_file)
            else:
                logger.info(
                    'SCP copy from "{}" and saving remotely to "{}"'.format(
                        local_file, remote_file
                    )
                )
                scp.put(localpath=local_file, remotepath=remote_file)
            return True
        except:
            ex = traceback.format_exc()
            if tries < 3:
                print(ex)
                retries_exchausted = True
            else:
                return False
        if retries_exchausted is True:
            raise Exception(
                "All attempts to SCP has failed. Server name: {}".format(
                    self.server.metadata.name
                )
            )
        return self.scp(
            local_file=local_file,
            remote_file=remote_file,
            operation=op,
            tries=tries + 1,
        )

    def to_dict(
        self,
        fields_to_include: tuple = (
            "name",
            "is_primary",
            "is_control_plane_server",
            "cluster_name",
        ),
    ) -> dict:
        data = {}
        if "name" in fields_to_include:
            data["serverName"] = self.server.metadata.name
        if "is_primary" in fields_to_include:
            data["isPrimary"] = self.is_primary
        if "is_control_plane_server" in fields_to_include:
            data["isControlPlaneServer"] = self.is_control_plane_server
        if "cluster_name" in fields_to_include:
            data["clusterName"] = self.cluster_name
        return data


class Servers:
    def __init__(self, server_control_collection: List[ServerControl] = []) -> None:
        self.server_control_collection = server_control_collection

    def get_all_server_names(self) -> tuple:
        server_names = []
        for server_control_instance in self.server_control_collection:
            server_names.append(server_control_instance.server.metadata.name)
        logger.debug("Server names: {}".format(server_names))
        return tuple(server_names)

    def get_server_by_name(self, server_name: str) -> ServerControl:
        if isinstance(server_name, str) is False:
            raise Exception(
                "Invalid key type. Expected a string which must be a server name"
            )
        s: ServerControl
        for s in self.server_control_collection:
            if server_name == s.server.metadata.name:
                return s
        raise Exception('Server named "{}" not found'.format(server_name))

    def server_exists_by_server_name(self, server_name: str) -> bool:
        server_instance = None
        try:
            server_instance = self.get_server_by_name(server_name=server_name)
        except:
            pass
        logger.debug(
            'Lookup result for server "{}" : Server instance type: {}'.format(
                server_name, type(server_instance)
            )
        )
        if server_instance is not None:
            return True
        return False

    def add_new_server(self, server: ServerObject, secrets: Secrets):
        logger.debug('Attempting to add server named "{}"'.format(server.metadata.name))
        if self.server_exists_by_server_name(server_name=server.metadata.name):
            raise Exception(
                'The server named "{}" was already defined. Duplicate names are not allowed.'.format(
                    server.metadata.name
                )
            )
        self.server_control_collection.append(
            ServerControl(server=server, secrets=secrets)
        )

    def named_server_is_already_cluster_bound(self, server_name: str) -> bool:
        server_control_instance = self.get_server_by_name(server_name=server_name)
        if server_control_instance.cluster_name == "":
            return False
        return True

    def server_is_allocated_to_named_cluster(
        self, cluster_name: str, server_name: str
    ) -> bool:
        if self.server_exists_by_server_name(server_name=server_name) is False:
            raise Exception('Server named "{}" does not exist'.format(server_name))
        server_control_instance = self.get_server_by_name(server_name=server_name)
        if server_control_instance.cluster_name == cluster_name:
            return True
        return False

    def replace_server_control_instance(self, server_control_instance: ServerControl):
        logger.debug(
            'Replacing new instance of server "{}"'.format(
                server_control_instance.server.metadata.name
            )
        )
        new_collection = []
        for sci in self.server_control_collection:
            if sci.server.metadata.name != server_control_instance.server.metadata.name:
                new_collection.append(sci)
        new_collection.append(server_control_instance)
        self.server_control_collection = new_collection

    def link_named_server_to_cluster(self, cluster_name: str, server_name: str):
        if self.named_server_is_already_cluster_bound(server_name=server_name) is True:
            raise Exception(
                'Server "{}" is already allocated to a cluster.'.format((server_name))
            )
        server_control_instance = self.get_server_by_name(server_name=server_name)
        server_control_instance.link_to_cluster(cluster_name=cluster_name)
        self.replace_server_control_instance(
            server_control_instance=server_control_instance
        )

    def mark_named_server_as_a_control_plane_server(self, server_name: str):
        server_control_instance = self.get_server_by_name(server_name=server_name)
        server_control_instance.set_as_control_plane()
        self.replace_server_control_instance(
            server_control_instance=server_control_instance
        )

    def mark_named_server_as_a_data_plane_server(self, server_name: str):
        server_control_instance = self.get_server_by_name(server_name=server_name)
        server_control_instance.set_as_agent()
        self.replace_server_control_instance(
            server_control_instance=server_control_instance
        )

    def mark_named_server_as_a_primary_server(self, server_name: str):
        server_control_instance = self.get_server_by_name(server_name=server_name)
        server_control_instance.set_primary()
        self.replace_server_control_instance(
            server_control_instance=server_control_instance
        )

    def get_servers_for_named_cluster(self, cluster_name: str) -> List[ServerControl]:
        servers = []
        for server_control_instance in self.server_control_collection:
            if server_control_instance.cluster_name == cluster_name:
                servers.append(server_control_instance)
        return servers

    def get_named_cluster_control_plane_servers(
        self, cluster_name: str, include_primary_server: bool = True
    ) -> List[ServerControl]:
        servers = []
        for server_control_instance in self.get_servers_for_named_cluster(
            cluster_name=cluster_name
        ):
            if server_control_instance.is_control_plane_server is True:
                if include_primary_server is True:
                    servers.append(server_control_instance)
                else:
                    if server_control_instance.is_primary is False:
                        servers.append(server_control_instance)
        return servers

    def get_named_cluster_data_plane_servers(
        self, cluster_name: str
    ) -> List[ServerControl]:
        servers = []
        for server_control_instance in self.get_servers_for_named_cluster(
            cluster_name=cluster_name
        ):
            if server_control_instance.is_control_plane_server is False:
                servers.append(server_control_instance)
        return servers

    def get_named_cluster_primary_control_plane_server(
        self, cluster_name: str
    ) -> ServerControl:
        for server_control_instance in self.get_named_cluster_control_plane_servers(
            cluster_name=cluster_name
        ):
            if server_control_instance.is_primary is True:
                return server_control_instance
        raise Exception(
            'No primary control plane server for cluster named "{}" found'.format(
                cluster_name
            )
        )

    def get_cluster_names(self) -> tuple:
        cluster_names = []
        server_control_instance: ServerControl
        for server_control_instance in self.server_control_collection:
            if server_control_instance.cluster_name is not None:
                if server_control_instance.cluster_name != "":
                    if server_control_instance.cluster_name not in cluster_names:
                        cluster_names.append(server_control_instance.cluster_name)
        return tuple(cluster_names)

    def get_servers_not_allocated_to_a_cluster(self) -> tuple:
        servers = []
        server_control_instance: ServerControl
        for server_control_instance in self.server_control_collection:
            if server_control_instance.cluster_name is None:
                servers.append(server_control_instance.server.metadata.name)
            if server_control_instance.cluster_name == "":
                servers.append(server_control_instance.server.metadata.name)
        return tuple(servers)

    def to_dict(self) -> dict:
        data = {}
        data["clusters"] = {}
        data["unAllocatedServers"] = self.get_servers_not_allocated_to_a_cluster()
        for cluster_name in self.get_cluster_names():
            data["clusters"][cluster_name] = {}
            data["clusters"][cluster_name]["primaryControlPlaneServerName"] = (
                self.get_named_cluster_primary_control_plane_server(
                    cluster_name=cluster_name
                ).server.metadata.name
            )

            data["clusters"][cluster_name]["controlPlaneServers"] = []
            for server_control_instance in self.get_named_cluster_control_plane_servers(
                cluster_name=cluster_name
            ):
                data["clusters"][cluster_name]["controlPlaneServers"].append(
                    server_control_instance.server.metadata.name
                )

            data["clusters"][cluster_name]["dataPlaneServers"] = []
            for server_control_instance in self.get_named_cluster_data_plane_servers(
                cluster_name=cluster_name
            ):
                data["clusters"][cluster_name]["dataPlaneServers"].append(
                    server_control_instance.server.metadata.name
                )

        return data


###############################################################################
###                                                                         ###
###   K3SCLUSTER MODEL                                                      ###
###                                                                         ###
###############################################################################


class K3sClusterApiEndPointOverrides(BaseModel):
    hostname: str = Field(
        title="Hostname",
        description="The hostname. By default this will be set to the primary server hostname.",
        examples=["my-server-addr"],
        default="not-set",
        max_length=1024,
    )
    port: int = Field(
        title="Port",
        description="The API end-point port, by default 6443",
        examples=[
            6443,
        ],
        default=6443,
        gt=0,
        lt=65535,
    )
    use_hostname_override: bool = Field(
        title="Flag for using Hostname Override",
        description="Set to true to use the hostname override",
        default=False,
        examples=[
            False,
        ],
        exclude=True,
    )
    use_port_override: bool = Field(
        title="Flag for using Port Override",
        description="Set to true to use the port override",
        default=False,
        examples=[
            False,
        ],
        exclude=True,
    )


class K3sClusterKubectlConfiguration(BaseModel):
    targetKubeConfig: str = Field(
        title="Target Kubeconfig file",
        description="The file the client configuration for `kubectl` will be written to. If no file is specified, the default will be `~/.kube/config`. If the file already exist, the new configuration will be merged.",
        default="{}{}.kube{}config".format(str(Path.home()), os.sep, os.sep),
        max_length=1024,
        examples=[
            "/home/user/cluster1.yaml",
        ],
    )
    apiEndPointOverrides: K3sClusterApiEndPointOverrides = Field(
        title="API End Point Overrides",
        description="Overrides one or both of the API end-point hostname and port",
        examples=[
            K3sClusterApiEndPointOverrides(),
        ],
        default=K3sClusterApiEndPointOverrides(),
    )


class K3sClusterServerItem(BaseModel):
    serverName: str = Field(
        title="Server Name",
        description="Reference to a `ServerObject.metadata.name`",
        examples=["my-server"],
    )
    controlPlane: bool = Field(
        title="Control Plane Indicator",
        description="Indicator if this server is a control plane server.",
        default=True,
        examples=[
            True,
        ],
    )


class K3ClusterEnvironmentVariableValue(BaseModel):
    sourceType: str = Field(
        title="Source Type",
        description="Indicates the source from where the value will be derived/fetched. Must be ONE of `gitRepo`, `secret` or `scalar`",
        examples=["gitRepo"],
    )
    sourceName: str = Field(
        title="Source Name",
        description="The metadata.name reference of a previously defined GitRepositoryObject or `Secret`",
        default="",
        examples=[
            "my-git-repo",
        ],
    )
    staticValue: str = Field(
        title="Static Value",
        description="For scalar types, the literal hard coded value",
        default="",
        examples=[
            "some-value",
        ],
    )

    @field_validator("sourceType", mode="before")
    @classmethod
    def is_work_dir_valid(cls, value: str) -> str:
        if value not in ("gitRepo", "secret", "scalar"):
            raise ValueError('Value must be one of "gitRepo", "secret" or "scalar".')
        return value

    @model_validator(mode="after")
    def check_for_insecure_http_usage(self) -> Self:
        if self.sourceType in (
            "gitRepo",
            "secret",
        ):
            if self.sourceName == "":
                raise ValueError(
                    'When the "sourceType" is "gitRepo" or "secret", the value for "sourceName" must be supplied.'
                )
            self.staticValue = ""
        else:
            if self.staticValue == "":
                raise ValueError(
                    'When the "sourceType" is "scalar", the value for "staticValue" must be supplied.'
                )
            self.sourceName = ""
        return self


class K3sClusterDataObject(BaseModel):
    kind: str = Field(
        title="Manifest Kind",
        description="Either a `ConfigMap` or `Secret` can be defined.",
        examples=[
            "ConfigMap",
        ],
    )
    name: str = Field(
        title="Name",
        description="The name of the object.",
        min_length=1,
        max_length=128,  # Technically this can be more, but keeping it shorter for practical purposes. See https://github.com/apache/airflow/pull/13299
        examples=[
            "my-configmap",
        ],
    )
    namespace: str | List[str] = Field(
        title="Namespace",
        description="The namespace(s) where this ConfigMap or Secret will be deployed. If only a single string value is supplied, only one namespace is targetted. For multiple namespace deployments, add a list of strings where each string is a namespace. The namespaces MUST exist.",
        min_length=1,
        max_length=128,
        examples=[
            "default",
        ],
    )


class K3ClusterEnvironmentVariable(BaseModel):
    name: str = Field(
        title="Variable Name",
        description="The name of the variable. NOTE: The name will be converted to uppercase and any non-alpha-numeric character will be converted to underscrore. Double underscores will be converted to a single underscore.",
        min_length=1,
        max_length=128,
        examples=[
            "APP_DIR",
        ],
    )
    valueSource: K3ClusterEnvironmentVariableValue = Field(
        title="Value Source",
        description="The object representing the source from where the variable valuable will be obtained or derived.",
        examples=[
            K3ClusterEnvironmentVariableValue(
                sourceType="scalar", staticValue="/opt/app"
            )
        ],
    )
    exposeToPostProvisionScripts: bool = Field(
        title="Expose to Provisioning Scripts",
        description="Indicator for also exposing this environment variable to the running scripts processed as part of the cluster provisioning.",
        default=False,
        examples=[
            True,
        ],
    )
    saveInCluster: K3sClusterDataObject | None = Field(
        title="Create Cluster Data Object",
        description="If supplied, defines how the variable will be exposed in the cluster",
        default=None,
        examples=[
            K3sClusterDataObject(
                kind="ConfigMap", name="application-directory", namespace="my-app"
            )
        ],
    )

    @field_validator("name", mode="before")
    @classmethod
    def name_conversion(cls, value: str) -> str:
        chars = string.ascii_letters + string.digits
        final_value = ""
        for c in value:
            if c not in chars:
                final_value = "{}_".format(final_value)
            else:
                final_value = "{}{}".format(final_value, c)
        while "__" in final_value:
            final_value = final_value.replace("__", "_")
        return final_value.upper()


class K3sClusterScriptVolumeConfiguration(BaseModel):
    localPath: str = Field(
        title="Local Path",
        description="The local directory on the target server(s) to mount during the running of the container.",
        min_length=1,
        max_length=1024,  # If you have a path name longer than 1 KiB, you should rethink your entire life...
        examples=[
            "/tmp",
        ],
    )
    containerPath: str = Field(
        title="Container Mount Point",
        description="The path on the container to mount the local path to. It will be mounted as Read Only!",
        min_length=1,
        max_length=1024,
        examples=["/tmp/host-tmp"],
    )


class K3sClusterScriptRuntimeConfiguration(BaseModel):
    image: str = Field(
        title="Image URI",
        description="The URI to the container image to use.",
        min_length=3,
        max_length=1024,
        examples=[
            "docker.io/bitnami/kubectl:1.33.4",
        ],
    )
    volumes: List[K3sClusterScriptVolumeConfiguration] | None = Field(
        title="Volume Mountpoints",
        description="The volumes to mount for script execution in a container",
        default=None,
        examples=[
            [
                K3sClusterScriptVolumeConfiguration(
                    localPath="/home/user/data", containerPath="/data"
                )
            ],
        ],
    )
    containerCommand: str = Field(
        title="Container Command",
        description="Set to either `podman` or `docker` depending on which container runtime is installed on the target server(s).",
        examples=[
            "podman",
        ],
    )
    overrideRunParameters: str = Field(
        title="Override Run Parameters",
        description="Overrides the default run parameters passed to the container command",
        examples=[
            "-it --rm",
        ],
        default='-it --rm --entrypoint=""',
        min_length=0,
        max_length=128,
    )

    @field_validator("containerCommand", mode="before")
    @classmethod
    def validate_container_command(cls, value: str) -> str:
        if value.lower() not in (
            "podman",
            "docker",
        ):
            raise ValueError(
                'Value for the containerCommand must be wither "docker" or "podman"'
            )
        return value.lower()


class K3sClusterPostProvisioningScriptItem(BaseModel):
    order: int = Field(
        title="Order Nr",
        description="An integer indicating the order in which this script will be executed. Lower numbers are executed first.",
        gt=0,
        lt=9999999,  # If you need more numbers, get a new life !!
        examples=[
            10,
        ],
    )
    targets: List[str] = Field(
        title="Target Servers",
        description="List of servers on which to run this script. Use LOCALHOST (all capital letters) for the current server the provisioning script is running on.",
        min_length=1,
        max_length=1024,
        examples=[
            "LOCALHOST",
        ],
    )
    script: str = Field(
        title="Script",
        description="The command(s) to execute. This can be a multi line script. The script will be run through the BASH interpreter.",
        min_length=1,
        max_length=1048576,  # 1 MiB Limit - should be really more than enough !!!
        examples=[
            "whoami",
        ],
    )
    scriptRuntime: K3sClusterScriptRuntimeConfiguration = Field(
        title="Script Runtime",
        description="Script Runtime configuration",
        examples=[
            K3sClusterScriptRuntimeConfiguration(
                image="docker.io/bitnami/kubectl:1.33.4",
                volumes=[
                    K3sClusterScriptVolumeConfiguration(
                        localPath="/some/path", containerPath="/data"
                    )
                ],
                containerCommand="podman",
            ),
        ],
    )
    postRunSleepSeconds: int = Field(
        title="Sleep Time",
        description="Number of seconds to sleep before proceeeding to the next script execution.",
        default=0,
        examples=[
            10,
        ],
    )


class K3sClusterSpec(BaseModel):
    tasks: List[str] = Field(
        title="Task List",
        description="Tasks to perform for cluster provisioning",
        examples=[
            [
                "cleanupPreviousClusterDeployment",
                "installK3s",
                "createNamespaces",
                "postProvisionScripts",
                "kubeconfig",
            ],
        ],
    )
    servers: List[K3sClusterServerItem] = Field(
        title="Servers",
        description="The list of servers for the control- and data plane on which to provision K3s. A single node cluster is also supported by supplying at least ONE server in the list",
        examples=[
            [
                K3sClusterServerItem(serverName="control1"),
                K3sClusterServerItem(serverName="control2"),
                K3sClusterServerItem(serverName="control3"),
                K3sClusterServerItem(serverName="agent1", controlPlane=False),
                K3sClusterServerItem(serverName="agent2", controlPlane=False),
                K3sClusterServerItem(serverName="agent3", controlPlane=False),
            ],
        ],
    )
    kubectlConfiguration: K3sClusterKubectlConfiguration = Field(
        title="Kubectl Configuration Overrides",
        description="Overrides for the kubectl configuration",
        default=K3sClusterKubectlConfiguration(),
        examples=[
            K3sClusterKubectlConfiguration(),
        ],
    )
    createNamespaces: List[str] = Field(
        title="Namespaces to Create",
        description="List of namespaces to create post-provisioning",
        default=[],
        examples=[
            "my-app",
        ],
    )
    environmentVariables: List[K3ClusterEnvironmentVariable] = Field(
        title="",
        description="",
        default=[],
        examples=[
            [
                K3ClusterEnvironmentVariable(
                    name="DEFAULT_APP_PATH",
                    valueSource=K3ClusterEnvironmentVariableValue(
                        sourceType="scalar", staticValue="/opt/app"
                    ),
                    saveInCluster=K3sClusterDataObject(
                        kind="ConfigMap",
                        name="default-app-path-cm",
                        namespace=[
                            "app1",
                            "app2",
                            "app3",
                            "app4",
                        ],
                    ),
                )
            ],
        ],
    )
    postProvisionScripts: List[K3sClusterPostProvisioningScriptItem] = Field(
        title="Post Provisioning Scripts",
        description="Scripts to run after a successful cluster deployment",
        default=[],
        examples=[
            [
                K3sClusterPostProvisioningScriptItem(
                    order=1,
                    targets=[
                        "LOCALHOST",
                    ],
                    scriptRuntime=K3sClusterScriptRuntimeConfiguration(
                        image="docker.io/bitnami/kubectl:1.33.4",
                        volumes=[
                            K3sClusterScriptVolumeConfiguration(
                                localPath="/home/user/data", containerPath="/opt/data"
                            )
                        ],
                        containerCommand="podman",
                    ),
                    script="whoami",
                    postRunSleepSeconds=30,
                ),
                K3sClusterPostProvisioningScriptItem(
                    order=2,
                    targets=[
                        "control1",
                        "control2",
                        "control3",
                    ],
                    scriptRuntime=K3sClusterScriptRuntimeConfiguration(
                        image="docker.io/bitnami/kubectl:1.33.4",
                        containerCommand="podman",
                    ),
                    script="whoami",
                ),
            ],
        ],
    )

    @field_validator("tasks", mode="before")
    @classmethod
    def validate_tasks(cls, value: list) -> list:
        supported_tasks = [
            "cleanupPreviousClusterDeployment",
            "installK3s",
            "createNamespaces",
            "postProvisionScripts",
            "kubeconfig",
        ]
        if len(value) == 0:
            raise ValueError("At least ONE task MUST be defined")
        for selected_task in value:
            if selected_task not in supported_tasks:
                raise ValueError(
                    'Task "{}" is not supported. Supported tasks: {}'.format(
                        value, supported_tasks
                    )
                )
        return value

    @computed_field
    @property
    def calculatedSharedToken(self) -> str:
        return "{}".format(
            str(hashlib.sha256(str(uuid.uuid4()).encode("utf-8")).hexdigest())
        )

    def get_post_provision_script_order_index(
        self,
    ) -> tuple[int]:
        order_index = []
        item: K3sClusterPostProvisioningScriptItem
        for item in self.postProvisionScripts:
            if item.order not in order_index:
                order_index.append(item.order)
        order_index.sort()
        return tuple(order_index)

    def get_post_provisions_scripts_for_order_index(
        self, index_position: int
    ) -> tuple[K3sClusterPostProvisioningScriptItem]:
        scripts = []
        item: K3sClusterPostProvisioningScriptItem
        for item in self.postProvisionScripts:
            if item.order == index_position:
                scripts.append(item)
        return tuple(scripts)


class K3sClusterObject(BaseModel):
    metadata: MetaData = Field(
        title="metadata field",
        description="The MetaData values of a YAML Manifest object",
        examples=[MetaData(name="cluster1")],
    )
    spec: K3sClusterSpec

    @computed_field
    @property
    def kind(self) -> str:
        return "Server"

    @computed_field
    @property
    def version(self) -> str:
        return "v1"


###############################################################################
###                                                                         ###
###   KUBECONFIG MODEL                                                      ###
###                                                                         ###
###############################################################################


class KubeConfigCluster(BaseModel):
    """Specification: https://kubernetes.io/docs/reference/config-api/kubeconfig.v1/#Cluster"""

    certificateAuthorityData: str | None = Field(
        title="Certificate Authority Data",
        description="CertificateAuthorityData contains PEM-encoded certificate authority certificates. Overrides CertificateAuthority",
        serialization_alias="certificate-authority-data",
        examples=[
            "LS0tLS1CRUdJTiBDRVJUSUZJQ0FUR....",
        ],
        default=None,
    )
    server: str = Field(
        title="Server",
        description="Server is the address of the kubernetes cluster (https://hostname:port).",
        min_length=1,
        max_length=1024,
        examples=[
            "https://127.0.0.1:6443",
        ],
    )
    tlsServerName: str | None = Field(
        title="TLS Server Name",
        description="TLSServerName is used to check server certificate. If TLSServerName is empty, the hostname used to contact the server is used.",
        serialization_alias="tls-server-name",
        examples=[
            "my-cluster",
        ],
        default=None,
    )
    insecureSkipTlsVerify: bool = Field(
        title="Insecure Skip TLS Verify",
        description="InsecureSkipTLSVerify skips the validity check for the server's certificate. This will make your HTTPS connections insecure.",
        serialization_alias="insecure-skip-tls-verify",
        examples=[
            True,
        ],
        default=False,
    )
    certificateAuthority: str | None = Field(
        title="Certificate Authority",
        description="CertificateAuthority is the path to a cert file for the certificate authority.",
        serialization_alias="certificate-authority",
        examples=[
            "/path/to/cert",
        ],
        default=None,
    )
    proxyUrl: str | None = Field(
        title="Proxy URL",
        description='ProxyURL is the URL to the proxy to be used for all requests made by this client. URLs with "http", "https", and "socks5" schemes are supported. If this configuration is not provided or the empty string, the client attempts to construct a proxy configuration from http_proxy and https_proxy environment variables. If these environment variables are not set, the client does not attempt to proxy requests. socks5 proxying does not currently support spdy streaming endpoints (exec, attach, port forward).',
        serialization_alias="proxy-url",
        examples=[
            "https://my-proxy:3128",
        ],
        default=None,
    )
    disableCompression: bool = Field(
        title="Disable Compression",
        description="DisableCompression allows client to opt-out of response compression for all requests to the server. This is useful to speed up requests (specifically lists) when client-server network bandwidth is ample, by saving time on compression (server-side) and decompression (client-side): https://github.com/kubernetes/kubernetes/issues/112296.",
        serialization_alias="disable-compression",
        examples=[
            True,
        ],
        default=False,
    )
    extensions: list | None = Field(
        title="Extensions",
        description="Extensions holds additional information. This is useful for extenders so that reads and writes don't clobber unknown fields",
        default=None,
    )


class KubeConfigNamedCluster(BaseModel):
    """Specification: https://kubernetes.io/docs/reference/config-api/kubeconfig.v1/#NamedCluster"""

    cluster: KubeConfigCluster = Field(
        title="Cluster",
        description="Cluster holds the cluster information",
        examples=[
            KubeConfigCluster(
                certificateAuthorityData="LS0tLS1CRUdJTiBDRVJUSUZJQ0FUR....",
                server="https://127.0.0.1:6443",
            )
        ],
    )
    name: str = Field(
        title="Cluster Name",
        description="Name is the nickname for this Cluster",
        min_length=1,
        max_length=1024,
        examples=[
            "my-cluster",
        ],
        default="default",
    )


class KubeConfigAuthInfo(BaseModel):
    """Specification: https://kubernetes.io/docs/reference/config-api/kubeconfig.v1/#AuthInfo"""

    clientCertificate: str | None = Field(
        title="Client Certificate",
        description="ClientCertificate is the path to a client cert file for TLS.",
        serialization_alias="client-certificate",
        examples=[
            "/path/to/cert",
        ],
        default=None,
    )
    clientCertificateData: str | None = Field(
        title="Client Certificate Data",
        description="ClientCertificateData contains PEM-encoded data from a client cert file for TLS. Overrides ClientCertificate",
        serialization_alias="client-certificate-data",
        examples=[
            "LS0tLS1CRUdJTiBDRVJUSUZJQ0FUR....",
        ],
        default=None,
    )
    clientKey: str | None = Field(
        title="Client Key",
        description="ClientKey is the path to a client key file for TLS.",
        serialization_alias="client-key",
        examples=[
            "/path/to/key",
        ],
        default=None,
    )
    clientKeyData: str | None = Field(
        title="Client Key Data",
        description="ClientKeyData contains PEM-encoded data from a client key file for TLS. Overrides ClientKey",
        serialization_alias="client-key-data",
        examples=[
            "LS0tLS1CRUdJTiBDRVJUSUZJQ0FUR....",
        ],
        default=None,
    )
    token: str | None = Field(
        title="Token",
        description="Token is the bearer token for authentication to the kubernetes cluster.",
        examples=[
            "abc...",
        ],
        default=None,
    )
    tokenFile: str | None = Field(
        title="Token File",
        description="TokenFile is a pointer to a file that contains a bearer token (as described above). If both Token and TokenFile are present, the TokenFile will be periodically read and the last successfully read value takes precedence over Token.",
        examples=[
            "/path/to/token",
        ],
        default=None,
    )
    impersonateAs: str | None = Field(
        title="Impersonate As",
        description="Impersonate is the username to impersonate. The name matches the flag.",
        serialization_alias="as",
        examples=[
            "other-user",
        ],
        default=None,
    )
    asUid: str | None = Field(
        title="As UID",
        description="ImpersonateUID is the uid to impersonate.",
        serialization_alias="as-uid",
        examples=[
            "1000",
        ],
        default=None,
    )
    asGroups: List[str] | None = Field(
        title="As Groups",
        description="ImpersonateGroups is the groups to impersonate.",
        serialization_alias="as-groups",
        examples=[
            ["group1", "group2"],
        ],
        default=None,
    )
    asUserExtra: dict | list | None = Field(
        title="As User Extra",
        description="ImpersonateUserExtra contains additional information for impersonated user.",
        serialization_alias="as-user-extra",
        examples=[
            None,
        ],
        default=None,
    )
    username: str | None = Field(
        title="Username",
        description="Username is the username for basic authentication to the kubernetes cluster.",
        examples=[
            "user1",
        ],
        default=None,
    )
    password: str | None = Field(
        title="Password",
        description="Password is the password for basic authentication to the kubernetes cluster.",
        examples=[
            "sup3rStr0ngPa3SwoRD",
        ],
        default=None,
    )
    authProvider: dict | None = Field(
        title="Auth Provider",
        description="",
        serialization_alias="auth-provider",
        examples=[
            None,
        ],
        default=None,
    )
    exec: dict | None = Field(
        title="Exec",
        description="Exec specifies a custom exec-based authentication plugin for the kubernetes cluster.",
        examples=[
            None,
        ],
        default=None,
    )
    extensions: list | None = Field(
        title="Extensions",
        description="Extensions holds additional information. This is useful for extenders so that reads and writes don't clobber unknown fields",
        examples=[
            None,
        ],
        default=None,
    )


class KubeConfigNamedAuthInfo(BaseModel):
    """Specification: https://kubernetes.io/docs/reference/config-api/kubeconfig.v1/#NamedAuthInfo"""

    name: str = Field(
        title="Name",
        description="Name is the nickname for this AuthInfo",
        examples=[
            "default",
        ],
        min_length=1,
        max_length=1024,
    )
    user: KubeConfigAuthInfo = Field(
        title="User",
        description="AuthInfo holds the auth information",
        examples=[
            KubeConfigAuthInfo(clientCertificateData="abc...", clientKeyData="def...")
        ],
    )


class KubeConfigContext(BaseModel):
    cluster: str = Field(
        title="Cluster",
        description="Cluster is the name of the cluster for this context",
        min_length=1,
        max_length=1024,
        examples=[
            "default",
        ],
    )
    user: str = Field(
        title="User",
        description="Name of the authInfo for this context",
        min_length=1,
        max_length=1025,
        examples=["default,"],
    )
    namespace: str | None = Field(
        title="Namespace",
        description="Namespace is the default namespace to use on unspecified requests",
        examples=[
            "default",
        ],
        default=None,
    )
    extensions: list | None = Field(
        title="Extensions",
        description="Extensions holds additional information. This is useful for extenders so that reads and writes don't clobber unknown fields",
        default=None,
    )


class KubeConfigNamedContext(BaseModel):
    """Specification: https://kubernetes.io/docs/reference/config-api/kubeconfig.v1/#NamedContext"""

    name: str = Field(
        title="Name",
        description="",
        examples=[
            "default",
        ],
    )
    context: KubeConfigContext = Field(
        title="Context",
        description="Context holds the context information",
        examples=[
            KubeConfigContext(cluster="default", user="default"),
        ],
    )


class KubeConfig(BaseModel):
    """Specification: https://kubernetes.io/docs/reference/config-api/kubeconfig.v1/

    Aligned with version 1.34 at the time of creating this model
    """

    clusters: List[KubeConfigNamedCluster] = Field(
        title="Cluster Definitions",
        description="List of cluster definitions",
        examples=[
            [
                KubeConfigNamedCluster(
                    cluster=KubeConfigCluster(
                        certificateAuthorityData="LS0tLS1CRUdJTiBDRVJUSUZJQ0FUR....",
                        server="https://127.0.0.1:6443",
                    ),
                    name="my-cluster",
                )
            ],
        ],
    )
    currentContext: str = Field(
        title="Current Context",
        description="The currently selected context",
        serialization_alias="current-context",
        default="default",
    )
    preferences: dict = Field(
        title="Preferences", description="Preferences", default={}, deprecated=True
    )
    extensions: list | None = Field(
        title="Extensions",
        description="Extensions holds additional information. This is useful for extenders so that reads and writes don't clobber unknown fields",
        default=None,
    )
    users: List[KubeConfigNamedAuthInfo] = Field(
        title="Users",
        description="AuthInfos is a map of referenceable names to user configs",
        examples=[
            [
                KubeConfigNamedAuthInfo(
                    name="default",
                    user=KubeConfigAuthInfo(
                        clientCertificateData="abc...", clientKeyData="def..."
                    ),
                )
            ]
        ],
    )
    contexts: List[KubeConfigNamedContext] = Field(
        title="Contexts",
        description="Contexts is a map of referenceable names to context configs",
        examples=[
            [
                KubeConfigNamedContext(
                    name="default",
                    context=KubeConfigContext(cluster="default", user="default"),
                )
            ]
        ],
    )

    def add_new_cluster(self, cluster: KubeConfigNamedCluster):
        new_items = []
        for item in self.clusters:
            if item.name != cluster.name:
                new_items.append(item)
        new_items.append(cluster)
        self.clusters = new_items

    def add_new_user(self, user: KubeConfigNamedAuthInfo):
        new_items = []
        for item in self.users:
            if item.name != user.name:
                new_items.append(item)
        new_items.append(user)
        self.users = new_items

    def add_new_context(self, context: KubeConfigNamedContext):
        new_items = []
        for item in self.contexts:
            if item.name != context.name:
                new_items.append(item)
        new_items.append(context)
        self.contexts = new_items

    def add_config(
        self,
        cluster: KubeConfigNamedCluster,
        user: KubeConfigNamedAuthInfo,
        context: KubeConfigNamedContext,
        set_context_as_active: bool = True,
    ):
        self.add_new_cluster(cluster=cluster)
        self.add_new_user(user=user)
        self.add_new_context(context=context)
        if set_context_as_active is True:
            self.currentContext = context.name

    @computed_field
    @property
    def apiVersion(self) -> str:
        """Legacy field from pkg/api/types.go TypeMeta. TODO(jlowdermilk): remove this after eliminating downstream dependencies."""
        return "v1"

    @computed_field
    @property
    def kind(self) -> str:
        """Legacy field from pkg/api/types.go TypeMeta. TODO(jlowdermilk): remove this after eliminating downstream dependencies."""
        return "Config"


###############################################################################
###                                                                         ###
###   MODEL COLLECTION                                                      ###
###                                                                         ###
###############################################################################


class ConfigurationCollection:
    def __init__(self) -> None:
        self.git_repositories = {}
        self.git_repository_cloned_objects = {}
        self.aws_profiles = {}
        self.aws_sessions = {}
        self.aws_secrets = {}
        self.server_instances = {}
        self.clusters = {}
        self.secrets = Secrets()
        self.servers = Servers()
        self.kubeconfig_collection = {}  # file_path: KubeConfig

    def _merge_kubeconfig(self, kubeconfig: KubeConfig, target_file: str) -> KubeConfig:
        logger.debug(
            "KUBECONFIG: Current Config: {}".format(
                kubeconfig.model_dump_json(indent=4)
            )
        )
        final_kubeconfig = kubeconfig
        if target_file in self.kubeconfig_collection:
            final_kubeconfig = self.kubeconfig_collection[target_file]
            for cluster in kubeconfig.clusters:
                final_kubeconfig.add_new_cluster(cluster=cluster)
                logger.debug(
                    'kubeconfig: [{}] - added new cluster "{}" - total clusters: {}'.format(
                        target_file, cluster.name, len(final_kubeconfig.clusters)
                    )
                )
            for user in kubeconfig.users:
                final_kubeconfig.add_new_user(user=user)
                logger.debug(
                    'kubeconfig: [{}] - added new user "{}" - total users: {}'.format(
                        target_file, user.name, len(final_kubeconfig.users)
                    )
                )
            for context in kubeconfig.contexts:
                final_kubeconfig.add_new_context(context=context)
                logger.debug(
                    'kubeconfig: [{}] - added new context "{}" - total contexts: {}'.format(
                        target_file, context.name, len(final_kubeconfig.contexts)
                    )
                )
                final_kubeconfig.currentContext = context.name
        logger.debug(
            "KUBECONFIG: Post Merge Config: {}".format(
                kubeconfig.model_dump_json(indent=4)
            )
        )
        return final_kubeconfig

    def save_kubeconfig(
        self, kubeconfig: KubeConfig, target_file: str, exclude_none: bool = True
    ):
        dump_dict_to_yaml_file(
            data=json.loads(
                kubeconfig.model_dump_json(exclude_none=exclude_none, by_alias=True)
            ),
            target_file=target_file,
        )

    def upsert_kubeconfig(
        self, kubeconfig: KubeConfig, target_file: str, exclude_none: bool = True
    ):
        final_kubeconfig = self._merge_kubeconfig(
            kubeconfig=kubeconfig, target_file=target_file
        )
        logger.debug(
            'KUBECONFIG: Creating kubectl configuarion file at "{}"'.format(target_file)
        )
        self.kubeconfig_collection[target_file] = final_kubeconfig
        self.save_kubeconfig(
            kubeconfig=final_kubeconfig,
            target_file=target_file,
            exclude_none=exclude_none,
        )

    def _kubectl_construct_cluster_obj_from_data(self, data: dict) -> KubeConfigCluster:
        if "server" not in data:
            raise Exception('Required field "server" not present in data')

        parameters = {"server": data["server"]}
        if "tls-server-name" in data:
            parameters["tlsServerName"] = data["tls-server-name"]
        if "insecure-skip-tls-verify" in data:
            parameters["insecureSkipTlsVerify"] = data["insecure-skip-tls-verify"]
        if "certificate-authority" in data:
            parameters["certificateAuthority"] = data["certificate-authority"]
        if "certificate-authority-data" in data:
            parameters["certificateAuthorityData"] = data["certificate-authority-data"]
        if "proxy-url" in data:
            parameters["proxyUrl"] = data["proxy-url"]
        if "disable-compression" in data:
            parameters["disableCompression"] = data["disable-compression"]
        if "extensions" in data:
            parameters["extensions"] = data["extensions"]

        kubeconfig_cluster = KubeConfigCluster(**parameters)
        return kubeconfig_cluster

    def _kubectl_construct_user_obj_from_data(self, data: dict) -> KubeConfigAuthInfo:
        parameters = {}

        if "client-certificate" in data:
            parameters["clientCertificate"] = data["client-certificate"]
        if "client-certificate-data" in data:
            parameters["clientCertificateData"] = data["client-certificate-data"]
        if "client-key" in data:
            parameters["clientKey"] = data["client-key"]
        if "client-key-data" in data:
            parameters["clientKeyData"] = data["client-key-data"]
        if "token" in data:
            parameters["token"] = data["token"]
        if "tokenFile" in data:
            parameters["tokenFile"] = data["tokenFile"]
        if "as" in data:
            parameters["impersonateAs"] = data["as"]
        if "as-uid" in data:
            parameters["asUid"] = data["as-uid"]
        if "as-groups" in data:
            parameters["asGroups"] = data["as-groups"]
        if "as-user-extra" in data:
            parameters["asUserExtra"] = data["as-user-extra"]
        if "username" in data:
            parameters["username"] = data["username"]
        if "password" in data:
            parameters["password"] = data["password"]
        if "auth-provider" in data:
            parameters["authProvider"] = data["auth-provider"]
        if "exec" in data:
            parameters["exec"] = data["exec"]
        if "extensions" in data:
            parameters["extensions"] = data["extensions"]

        kubeconfig_user = KubeConfigAuthInfo(**parameters)
        return kubeconfig_user

    def _kubectl_construct_context_obj_from_data(self, data: dict) -> KubeConfigContext:
        parameters = {}

        if "cluster" in data:
            parameters["cluster"] = data["cluster"]
        if "user" in data:
            parameters["user"] = data["user"]
        if "namespace" in data:
            parameters["namespace"] = data["namespace"]
        if "extensions" in data:
            parameters["extensions"] = data["extensions"]

        kubeconfig_cluster = KubeConfigContext(**parameters)
        return kubeconfig_cluster

    def _load_kubeconfig_file_into_model(self, file: str) -> KubeConfig:
        loaded_yaml_data_as_tuple = load_yaml_manifest(manifest_file=file)
        logger.debug(
            'KUBECONFIG: Loaded YAML from "{}":\n----------\n{}\n----------'.format(
                file, loaded_yaml_data_as_tuple
            )
        )
        if len(loaded_yaml_data_as_tuple) == 0:
            raise Exception('There was no data to load from file "{}"'.format(file))
        data = loaded_yaml_data_as_tuple[0]

        parameters = {}
        current_context_name = ""

        if "preferences" in data:
            parameters["preferences"] = data["preferences"]
        if "extensions" in data:
            parameters["extensions"] = data["extensions"]
        if "users" in data:
            users = []
            for user_data in data["users"]:
                users.append(
                    KubeConfigNamedAuthInfo(
                        name=user_data["name"],
                        user=self._kubectl_construct_user_obj_from_data(
                            data=user_data["user"]
                        ),
                    )
                )
            parameters["users"] = users
        if "clusters" in data:
            clusters = []
            for cluster_data in data["clusters"]:
                clusters.append(
                    KubeConfigNamedCluster(
                        name=cluster_data["name"],
                        cluster=self._kubectl_construct_cluster_obj_from_data(
                            data=cluster_data["cluster"]
                        ),
                    )
                )
            parameters["clusters"] = clusters
        if "contexts" in data:
            contexts = []
            for context_data in data["contexts"]:
                current_context_name = context_data["name"]
                contexts.append(
                    KubeConfigNamedContext(
                        name=context_data["name"],
                        context=self._kubectl_construct_context_obj_from_data(
                            data=context_data["context"]
                        ),
                    )
                )
            parameters["contexts"] = contexts
        parameters["currentContext"] = current_context_name
        if "current-context" in data:
            parameters["currentContext"] = data["current-context"]

        kubeconfig = KubeConfig(**parameters)
        logger.debug(
            'KUBECONFIG: Loaded file "{}":\n----------\n{}\n----------'.format(
                file, kubeconfig.model_dump_json(indent=4)
            )
        )
        return kubeconfig

    def get_kubeconfig_from_file_origin(
        self,
        kubeconfig_source_file: str,
        force_reload: bool = False,
    ) -> KubeConfig:
        if kubeconfig_source_file in self.kubeconfig_collection:
            if force_reload is False:
                return self.kubeconfig_collection[kubeconfig_source_file]

        return self._load_kubeconfig_file_into_model(file=kubeconfig_source_file)

    def add_cluster(self, cluster: K3sClusterObject):
        cluster_name = cluster.metadata.name
        primary_set = False
        cluster_server: K3sClusterServerItem
        for cluster_server in cluster.spec.servers:
            server_name = cluster_server.serverName
            logger.info(
                'Linking server "{}" to cluster "{}"'.format(
                    server_name, cluster.metadata.name
                )
            )
            self.servers.link_named_server_to_cluster(
                cluster_name=cluster_name, server_name=server_name
            )
            if cluster_server.controlPlane is True:
                self.servers.mark_named_server_as_a_control_plane_server(
                    server_name=server_name
                )
                if primary_set is False:
                    self.servers.mark_named_server_as_a_primary_server(
                        server_name=server_name
                    )
                    primary_set = True
            else:
                self.servers.mark_named_server_as_a_data_plane_server(
                    server_name=server_name
                )
        if (
            len(
                self.servers.get_named_cluster_control_plane_servers(
                    cluster_name=cluster_name
                )
            )
            == 0
        ):
            raise Exception(
                'For cluster named "{}" there seems to be no control plane servers defiend'.format(
                    cluster_name
                )
            )
        self.servers.get_named_cluster_primary_control_plane_server(
            cluster_name=cluster_name
        )
        self.clusters[cluster.metadata.name] = cluster

    def add_aws_profile(self, aws_profile: AwsProfileObject):
        self.aws_sessions[aws_profile.metadata.name] = AwsIntegration(
            region=aws_profile.spec.defaultRegion,
            profile_name=aws_profile.metadata.name,
        )
        self.aws_profiles[aws_profile.metadata.name] = aws_profile

    def _store_normal_aws_secret(
        self, name: str, origin_aws_secret: AwsSecretObject, final_value
    ):
        self.secrets.add_secret(
            secret=Secret(
                name=name,
                value=final_value,
                original_manifest=json.loads(origin_aws_secret.model_dump_json()),
            )
        )

    def _store_mapped_dictionary_secret(
        self, aws_secret: AwsSecretObject, secret_value
    ):
        mapping_key: str
        target_secret_name: str
        for mapping_key, target_secret_name in aws_secret.spec.mapping.items():
            if mapping_key in secret_value:
                self._store_normal_aws_secret(
                    name=target_secret_name,
                    origin_aws_secret=aws_secret,
                    final_value=secret_value[mapping_key],
                )

    def add_aws_secret(self, aws_secret: AwsSecretObject):
        if aws_secret.metadata.name in self.aws_secrets:
            raise Exception(
                'AWS Secret named "{}" was already defined'.format(
                    aws_secret.metadata.name
                )
            )
        aws_profile_name = aws_secret.spec.awsProfile
        secret_value = self.aws_sessions[aws_profile_name].get_secret_value(
            secret_name=aws_secret.metadata.name
        )
        if aws_secret.spec.conversion in CONVERSION_FUNCTIONS:
            secret_value = CONVERSION_FUNCTIONS[aws_secret.spec.conversion](
                secret_value
            )
        if aws_secret.spec.conversion == "" and len(aws_secret.spec.mapping) == 0:
            self._store_normal_aws_secret(
                name=aws_secret.metadata.name,
                origin_aws_secret=aws_secret,
                final_value=secret_value,
            )
        elif len(aws_secret.spec.mapping) > 0:
            self._store_mapped_dictionary_secret(
                aws_secret=aws_secret, secret_value=secret_value
            )
        self.aws_secrets[aws_secret.metadata.name] = aws_secret

    def _validate_git_http_creds_usage(
        self,
        repo: GitRepositoryObject,
    ) -> tuple:
        url_username, url_password, clean_url = strip_url_creds(
            url_string=repo.spec.url
        )
        final_username = ""
        if repo.spec.credentials.username is not None:
            final_username = "{}".format(repo.spec.credentials.username)
        final_password = ""
        final_url = repo.spec.url

        if repo.spec.credentials.value is not None:
            if len(
                repo.spec.credentials.value
            ) > 0 and repo.spec.url.lower().startswith("http"):
                final_password = self.secrets.get_secret_by_name(
                    name=repo.spec.credentials.value
                ).value

        if repo.spec.httpInsecure is False:
            if url_password is not None:
                raise Exception(
                    'In Git repository named "{}", the URL appears to contain credentials. If you comitted this manifest to a Git repository, consider your credentials compromised. To ignore this exception, configure the credentials with the "httpInsecure" option set to true and use the anonymous "credentialsType"'.format(
                        repo.metadata.name
                    )
                )
        else:
            if (
                repo.spec.credentials.credentialsType != "anonymous"
                and url_password is not None
            ):
                raise Exception(
                    'In Git repository named "{}", the URL appears to contain credentials. If you comitted this manifest to a Git repository, consider your credentials compromised. To ignore this exception, configure the credentials with the "httpInsecure" option set to true and use the anonymous "credentialsType"'.format(
                        repo.metadata.name
                    )
                )
            if clean_url.startswith("http"):
                final_username = "{}".format(url_username)
                final_password = "{}".format(url_password)
                final_url = clean_url

        masked_password = ""
        log_url = "{}".format(final_url)
        if len(final_password) > 0:
            masked_password = "*" * len(final_password)
            log_url = log_url.replace(final_password, masked_password)

        logger.info(
            'Cloning git repository "{}" from "{}" into "{}"'.format(
                repo.metadata.name, log_url, repo.spec.localWorkDir
            )
        )

        return (final_username, final_password, final_url)

    def _build_final_git_http_url(
        self, final_username: str, final_password: str, clean_url: str
    ) -> str:
        final_url = "{}".format(clean_url)

        if clean_url.startswith("http"):
            creds = ""
            if len(final_username) > 0:
                creds = final_username
                if len(final_password) > 0:
                    creds = "{}:{}".format(final_username, final_password)
            if len(creds) > 0:
                clean_url_elements = clean_url.split("://")
                final_url = "{}://{}@{}".format(
                    clean_url_elements[0], creds, clean_url_elements[1]
                )
        return final_url

    def _build_git_final_parameters(
        self, repo: GitRepositoryObject, final_url: str
    ) -> dict:
        env = None
        if repo.spec.url.lower().startswith("ssh:") is True:
            if repo.spec.credentials.credentialsType == "ssh":
                git_ssh_cmd = "ssh -i {}".format(repo.spec.credentials.value)
                env = dict(GIT_SSH_COMMAND=git_ssh_cmd)
                logger.info(
                    'Git repository "{}" using private key "{}"'.format(
                        repo.spec.url, repo.spec.credentials.value
                    )
                )
            else:
                raise Exception(
                    'For Git repository named "{}", if the credentialType is SSH, the URL must start with ssh://'.format(
                        repo.metadata.name
                    )
                )
        elif repo.spec.url.lower().startswith("http") is True:
            if repo.spec.httpInsecure is True:
                env = dict(GIT_SSL_NO_VERIFY="1")
                logger.info(
                    'Git repository "{}" using INSECURE authentication'.format(
                        repo.spec.url
                    )
                )
        else:
            raise Exception(
                'The URL "{}" in repository named "{}" has an unsupported protocol. Currently only SSH, HTTP/HTTPS is supported.'.format(
                    repo.spec.url, repo.metadata.name
                )
            )
        return {
            "url": final_url,
            "to_path": repo.spec.localWorkDir,
            "env": env,
            "branch": repo.spec.branch,
        }

    def _git_clone(self, repo: GitRepositoryObject):
        final_username, final_password, clean_url = self._validate_git_http_creds_usage(
            repo=repo
        )
        final_url = "{}".format(clean_url)
        if clean_url.lower().startswith("http") is True:
            final_url = self._build_final_git_http_url(
                final_username=final_username,
                final_password=final_password,
                clean_url=clean_url,
            )

        params = self._build_git_final_parameters(repo=repo, final_url=final_url)
        self.git_repository_cloned_objects[repo.metadata.name] = Repo.clone_from(
            **params
        )

    def add_git_repository(self, repo: GitRepositoryObject):
        if repo.metadata.name in self.git_repositories:
            raise Exception(
                'GitRepository named "{}" was already processed - ensure each GitRepository definition uses a unique name'.format(
                    repo.metadata.name
                )
            )
        self._git_clone(repo=repo)
        if repo.metadata.name in self.git_repository_cloned_objects:
            self.git_repositories[repo.metadata.name] = repo

    def add_server(self, server: ServerObject):
        self.servers.add_new_server(server=server, secrets=self.secrets)

    def search_by_name(self, kind: str, name: str) -> GitRepositoryObject:
        if kind == "GitRepository":
            if name in self.git_repositories is True:
                return self.git_repositories[name]
            raise Exception('GitRepository named "{}" not found'.format(name))
        # TODO: Add other types to search for...
        raise Exception('Unsupported kind "{}"'.format(kind))

    def get_kinds(self) -> tuple:
        kinds = []
        if len(self.git_repositories) > 0:
            kinds.append("GitRepository")
        if len(self.aws_profiles) > 0:
            kinds.append("AwsProfile")
        if len(self.secrets.secrets) > 0:
            kinds.append("Secret")
        if len(self.servers.server_control_collection) > 0:
            kinds.append("Server")
        return tuple(kinds)

    def get_names_by_kind(self, kind: str) -> tuple:
        if kind.lower() == "GitRepository".lower():
            return tuple(self.git_repositories.keys())
        elif kind.lower() == "AwsProfile".lower():
            return tuple(self.aws_profiles.keys())
        elif kind.lower() == "Secret".lower():
            return tuple(self.secrets.secrets.keys())
        elif kind.lower() == "Server".lower():
            return self.servers.get_all_server_names()
        raise Exception('Unsupported kind "{}"'.format(kind))

    def git_cleanup(self):
        repo_name: str
        repo: GitRepositoryObject
        for repo_name, repo in self.git_repositories.items():
            if repo.spec.postCleanup is True:
                logger.info(
                    'Cleaning up repository named "{}" in local working directory "{}"'.format(
                        repo_name, repo.spec.localWorkDir
                    )
                )
                delete_directory(dir=repo.spec.localWorkDir)

    def qty(self) -> dict:
        return {
            "GitRepository": len(self.git_repositories),
            "AwsProfile": len(self.aws_profiles),
            "Secret": len(self.secrets.secrets),
            "K3sCluster": len(self.clusters),
            "Server": len(self.servers.get_all_server_names()),
        }
