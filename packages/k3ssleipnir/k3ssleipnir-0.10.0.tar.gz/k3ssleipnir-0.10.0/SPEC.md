# Configuration Definitions

<!-- toc -->

- [YAML Specification](#yaml-specification)
- [Kind: AwsProfile](#kind-awsprofile)
- [Kind: AwsSecret](#kind-awssecret)
  * [Conversion Options](#conversion-options)
  * [Mapping Options](#mapping-options)
- [Kind: GitRepository](#kind-gitrepository)
  * [credentials](#credentials)
  * [postCloneActions](#postcloneactions)
    + [Action type `provisioning`](#action-type-provisioning)
    + [Action type `script`](#action-type-script)
- [Kind: K3sCluster](#kind-k3scluster)
  * [Kubectl Configuration](#kubectl-configuration)
  * [Tasks](#tasks)
  * [Server Definition](#server-definition)
  * [Environment Variables](#environment-variables)
    + [Environment Variable Value Object](#environment-variable-value-object)
    + [Save Variable in Cluster](#save-variable-in-cluster)
  * [Post Provisioning Scripts](#post-provisioning-scripts)
    + [Script Runtime](#script-runtime)
    + [Script Runtime Volumes](#script-runtime-volumes)
- [Kind: Server](#kind-server)
  * [Server Credentials](#server-credentials)

<!-- tocstop -->

## YAML Specification

Although the manifests are not intended to be deployed in a Kubernetes cluster, the format is roughly consistent with [Kubernetes manifests](https://kubernetes.io/docs/concepts/overview/working-with-objects/) to minimize the adoption and/or usage of the configuration of new clusters.

The following is a minimal structure that all `kind` definitions must have:

```yaml
apiVersion: v1
kind: KindName
metadata:
  name: identifier
spec: {}
```

A name defined as metadata is always required.

The rest of this document describes the `spec` for each of the following kinds:

- AwsProfile
- AwsSecret
- GitRepository
- K3sCluster
- Server

## Kind: AwsProfile

Links to an already pre-defined AWS profile for easy interaction with AWS services such as AWS Secrets Manager.

Minimal Example:

```yaml
---
apiVersion: v1
kind: AwsProfile
metadata:
  name: my-aws-profile
spec:
  defaultRegion: eu-central-1
```


| Field Name | Type | Description |
|---|---|---|
| (REQUIRED) `defaultRegion` | string | A valid AWS region. The connection object will be bound to this region. |


## Kind: AwsSecret

Reference to a secret stored in AWS Secrets Manager that will be retrieved and that can be used in variables in parts of the cluster configuration.

Depends on: [Kind: AwsProfile](#kind-awsprofile)

Minimal Example:

```yaml
---
apiVersion: v1
kind: AwsSecret
metadata:
  name: my-secret
spec:
  awsProfile: my-aws-profile
```


| Field Name | Type | Description |
|---|---|---|
| (REQUIRED) `awsProfile` | string | The name of the [AwsProfile](#kind-awsprofile) configuration. The secret will be retrieved from the secret named `my-secret` (as in the example) and is expected to be in the region as defined in the `AwsProfile` configuration |
| `conversion` | string | See [Conversion Options](#conversion-options) |
| `mapping` | dictionary | see [Mapping Options](#mapping-options) |

### Conversion Options

Part of [Kind: AwsSecret](#kind-awssecret)

| Option | Description |
|---|---|
| `json_to_dict` | The string value from the secret is expected to be JSON and will be converted to a dictionary object in order to work with the fields. |

### Mapping Options

Part of [Kind: AwsSecret](#kind-awssecret)

When needed:

- The secret value contains a JSON object with simple key/value pairs
- (REQUIRED) the `conversion` option `json_to_dict` (see [Conversion Options](#conversion-options))

Defines a simple key/value pair, where each key is used as the key within the JSON data and the value maps to the target secret name that will hold the value.

For example, consider the secret with the following JSON value:

```json
{
  "Username": "some-user",
  "Password": "some-super-secret-password"
}
```

The following mapping can be defined:

```yaml
apiVersion: v1
kind: AwsSecret
metadata:
  name: my-db-credentials
spec:
  awsProfile: my-aws-profile
  conversion: json_to_dict
  mapping:
    Username: my-db-username
    Password: my-db-password
```

With the above configuration, an AWS Secret with the name `my-db-credentials` will be retrieved with the JSON payload as defined earlier. A Kubernetes secret, also with the name `my-db-credentials`, will be created and will hold the original JSON value as a normal string value.

In addition, two more Kubernetes secrets will be created:

- `my-db-username` with the string value `some-user`
- `my-db-password` with the string value `some-super-secret-password`

## Kind: GitRepository

Clones a remote Git repository. Handy for ingesting other manifests or running of scripts.

If multiple `GitRepository` definitions exist, the processing order is random.

Example:

```yaml
---
apiVersion: v1
kind: GitRepository
metadata:
  name: homelab-repo
spec:
  url: ssh://git@git-server/user/project.git
  branch: main
  credentials:
    credentialsType: ssh
    value: /path/to/private-key
    username: git
  localWorkDir: /tmp/repos/homelab-configs
  postCleanup: true
  postCloneActions:
    - actionType: provisioning
      srcFilePath: repo-relative-path/to/homelab-secondary-cluster.yaml
    - actionType: script
      srcFilePath: /local-path-outside-git-repo/to/script.sh

```

| Field Name | Type | Description |
|---|---|---|
| (REQUIRED) `url` | string | The SSH or HTTP(S) URL to the Git repository. |
| `branch` | string | A branch (or TAG reference) which will be checked out after cloning. DEFAULT=`main` |
| `credentials` | object | See [credentials](#credentials). |
| `localWorkDir` | string | The base working directory into which the Git repository will be cloned. A subdirectory with the same name as the Git repository must not exist. DEFAULT=`/tmp` (or as programatically being determined as the system temporary directory) |
| `postCleanup` | boolean | Indicator if the Git repository should be deleted after provisioning is completed (without errors). DEFAULT=`true` |
| `postCloneActions` | array | See [postCloneActions](#postcloneactions). DEFAULT=`[]` |

### credentials

> [!NOTE]
> If no credentials are supplied, the assumption is that it is a public accessible repository, and therefore an `anonymous` type of credentials will be assumed.

| Field Name | Type | Description |
|---|---|---|
| (REQUIRED) `credentialsType` | string | One of `ssh`, `password` or `anonymous`. With `anonymous` credentials, no value or username is required. |
| `value` | string | In the case of `ssh`, the value points to a private key file on the local file system. In the case of `password`, the value points to the NAME of the secret that holds the password value. DO NOT supply passwords in clear text in configuration files !!! |
| (conditionally REQUIRED) `usernama` | string | Required for `ssh` and `password` credentials types. |

### postCloneActions

Part of [Kind: GitRepository](#kind-gitrepository)

This configuration defines additional actions that must be performed after the main manifest have been ingested, but before any processing is done. All `GitRepository` definitions would at least be cloned and therefore file or script references could point to other repository files, although this is considered a bad practice.

Each array element is a dictionary with two mandatory fields:

| Field Name | Type | Description |
|---|---|---|
| (REQUIRED) `actionType` | string | One of `provisioning` or `script`. NOTE: `script` currently has no effect |
| (REQUIRED) `srcFilePath` | string | Path and filename of the file to process. The path can be relative to the cloned Git repository root, but when the path starts with the operating system path sperator (slash or `/` on most systems), it will be interpreted to be a full path to a file that may not neccesarily be in the cloned Git repository. |

#### Action type `provisioning`

When this action is defined, the specified file MUST be a YAML file that contains further K3s related manifests.

It is a convenient way to use a root configuration manifest to point to multipole cluster configurations.

All defined manifests will be parsed first and only after ALL manifests are parsed will script actions be run. No attempt is made to check for duplicate actions between different manifests.

#### Action type `script`

The specified file MUST exist and will be executed with the `bash` shell. STDOUT and STDERR will be combined and echoed as a single output to STDOUT, with STDERR last (after the STDOUT output, if any).

Errors or non-zero exit codes will be ignored.

The shell script does not have to be executable, but the parent process user must have at least read privileges of the file.

No attempt is made to check for duplicate scripts between different manifests and therefore it will be possible to run the same script more than once.

## Kind: K3sCluster

Defines a cluster made up of at least ONE node, but can also include several control plane and data plane servers. Optionally also defines some additional deployments that can be done once the cluster is up and running.

Example:

```yaml
---
apiVersion: v1
kind: K3sCluster
metadata:
  name: cluster1
spec:
  tasks:
    - cleanupPreviousClusterDeployment
    - installK3s
    - createNamespaces
    - postProvisionScripts
  servers:
    - serverName: main1
    - serverName: main2
    - serverName: agent1
      controlPlane: false
    - serverName: agent2
      controlPlane: false
  kubectlConfiguration:
    targetKubeConfig: /home/user/homelab_clusters.yaml
    apiEndPointOverrides:
      hostname: localhost
      port: 7021
  createNamespaces:
    - bootstrapping
  environmentVariables:
    - name: MANIFEST_PATH
      valueSource:
        sourceType: gitRepo
        sourceName: homelab-repo
      exposeToPostProvisionScripts: true
    - name: EMAIL
      valueSource:
        sourceType: scalar
        staticValue: user@domain.tld
      saveInCluster:
        kind: ConfigMap
        name: admin-email-address-cm
        namespace: bootstrapping
    - name: KUBECONFIG
      valueSource:
        sourceType: scalar
        staticValue: /tmp/config
      exposeToPostProvisionScripts: true
    - name: DNS_AWS_ACCESS_KEY_ID
      valueSource:
        sourceType: secret
        sourceName: route53-credentials-key
      saveInCluster:
        kind: Secret
        name: dns-aws-access-key-id-secret
        namespace: bootstrapping
    - name: DNS_AWS_SECRET_ACCESS_KEY
      valueSource:
        sourceType: secret
        sourceName: route53-credentials-secret
      saveInCluster:
        kind: Secret
        name: dns-aws-secret-access-key-secret
        namespace: bootstrapping
  postProvisionScripts:
    - order: 10
      scriptRuntime:
        image: docker.io/bitnami/kubectl:1.33.4
        volumes:
          - localPath: "$MANIFEST_PATH"
            containerMountPoint: /repo
          - localPath: /home/user/homelab_clusters.yaml
            containerMountPoint: /tmp/config
        containerCommand: podman
      targets:
        - LOCALHOST
      script: |
        # Since we run on localhost and using a KUBECONFIG with multiple
        # contexts, the context name must be supplied.
        export KUBECONFIG=/tmp/config
        kubectl apply -f /repo/some-manifest.yaml --context=cluster1
      postRunSleepSeconds: 3
    - order: 20
      scriptRuntime:
        image: docker.io/bitnami/kubectl:1.33.4
        volumes:
          - localPath: "$MANIFEST_PATH"
            containerMountPoint: /repo
          - localPath: /home/user/homelab_clusters.yaml
            containerMountPoint: /tmp/config
        containerCommand: podman
      targets:
        - control1
      script: |
        # Since we run this command on the control plane, make sure to use the
        # local KUBECONFIG file. In this example we do not need to set the
        # context as there is only 1 defined.
        export KUBECONFIG=/tmp/config
        kubectl apply -f /repo/my-manifest.yaml
      postRunSleepSeconds: 3
```

> [!NOTE]
> In the `metadata`, and labels will also be applied as node labels to both control plane and data plane servers.

| Field Name | Type | Description |
|---|---|---|
| (REQUIRED) `tasks` | array | See [Tasks](#tasks) |
| (REQUIRED) `servers` | array | See [Server Definition](#server-definition) |
| `agents` | array | Agents are also servers, but exclusively for the data plane. It is OPTIONAL to provide agents.|
| `createNamespaces` | array | An optional list of extra namespaces to be created. |
| `kubectlConfiguration` | object | See XXX |
| `environmentVariables` | array | See [Environment Variables](#environment-variables) |
| `postProvisionScripts` | object | See [Post Provisioning Scripts](#post-provisioning-scripts) |

### Kubectl Configuration

By default the `kubectl` configuration will be written to `~/.kube/config`. If the file already exists, it will be updated and the new configuration will be added/updated.

The default behaviour is also to use the defined primary control plane server address as the target address in the configuration. However, it is also possible to override this behaviour by specifying a host name and port. The default port is typically `6443`.

| Field Name | Type | Description |
|---|:-:|---|
| `targetKubeConfig` | string | The file in which the configuration for `kubectl` will be added. If the file already exists, the new cluster context will simply be added. If no file is provided, the default `kubectl` configuration (`~/.kube/config`) will be updated. |
| `apiEndPointOverrides` | object | Optional overrides for the API end-point for this cluster. |

The `apiEndPointOverrides` object requires at least one of the following fields:

| Field Name | Type | Description |
|---|:-:|---|
| `hostname` | string | The hostname or IP address to use |
| `port` | integer | The TCP port to use. |

### Tasks

Part of [Kind: K3sCluster](#kind-k3scluster)

At least one of the following tasks need to be defined:

| Task Name | Processing Order | Task Outcome |
|---|:-:|---|
| `cleanupPreviousClusterDeployment` | 1 | Deletes the K3s installation on the defined servers. All deployments on those nodes will be lost. |
| `installK3s` | 2 | Run the installation steps for control plane and data plane servers. Not specifying this task will no install K3s on any linked `server` or `agent` servers. |
| `createNamespaces` | 3 | If additional namespaces are listed, ensure that the namespaces are created. The listed namespaces will only be created if this task is in the list. |
| `postProvisionScripts` | 4 | If any `postProvisionScripts` are defined, run them. If this task is not listed, not additional post provisioning tasks will be run. |

### Server Definition

Part of [Kind: K3sCluster](#kind-k3scluster)

At least ONE server needs to be defined in the list. The first control plane server will be the initial primary server on which K3s
will be installed. All other servers and agents will be initialized with this server as a starting point.

Each list item has the following object structure:

| Field Name | Type | Description |
|---|---|---|
| (REQUIRED) `serverName` | string | A name of one of the earlier defined `Server` definitions. See [Kind: Server](#kind-server) |
| `controlPlane` | boolean | Set to `false` to mark this server as an agent. Default value is `true` (marking the server as a control plane server) |


### Environment Variables

Part of [Kind: K3sCluster](#kind-k3scluster)

The list element is a data structure defined as follow:

| Field Name | Type | Description |
|---|---|---|
| (REQUIRED) `name` | string | The name of the environment variable. This is also the name exposed on the target execution platform. Case is not important, but the names will be exposed as CAPITAL names and any non-alpha-numeric character will be converted to an underscore. |
| (REQUIRED) `valueSource` | object | See [Environment Variable Value Object](#environment-variable-value-object) |
| `exposeToPostProvisionScripts` | boolean | If set to `true`, the environment variable will also be exposed in scripts from `postProvisionScripts` |
| `saveInCluster` | object | See [Save Variable in Cluster](#save-variable-in-cluster) |

> [!IMPORTANT]
> Either one of the `exposeToPostProvisionScripts` and `saveInCluster` options must be supplied. Both can also be supplied.

#### Environment Variable Value Object

Part of [Environment Variables](#environment-variables)

Each `sourceType` can contain one of the following:

- `gitRepo` - This will cause the working directory of the named Git repository to be exposed with this environment variable.
- `scalar` - This will export the literal value with this environment variable.
- `secret` - The value of the named secret will be exposed with this environment variable.

The full object field definition:


| Field Name | Type | Description |
|---|---|---|
| (REQUIRED) `sourceType` | string | One of `gitRepo`, `scalar` or `secret` |
| `sourceName` | string | The name of one of the `gitRepo` or `secret` objects defined earlier. |
| `staticValue` | string | The literal value of a `scalar`. |

> [!NOTE]
> Either ONE of `sourceName` or `staticValue` is required, based on the value of `sourceType`

#### Save Variable in Cluster

Part of [Environment Variables](#environment-variables)

When the `saveInCluster` option is used, either a `ConfgiMap` or a `Secret` will be created.

Fields:

| Field Name | Type | Description |
|---|---|---|
| (REQUIRED) `kind` | string | Either `ConfigMap` or `Secret` |
| (REQUIRED) `name` | string | The name of the `ConfigMap` or `Secret` |
| (REQUIRED) `namespace` | string | The namespace in which the `ConfigMap` or `Secret` must be created. This will run after any new namespaces was created, and you can therefore specify a namespace that does not by default exists, as long as it is specified in the `createNamespaces` list AND the `createNamespaces` task is also added to the `tasks` list. |

### Post Provisioning Scripts

Part of [Kind: K3sCluster](#kind-k3scluster)

When configured, these scripts will run on the specified list of servers. When the server name is `LOCALHOST` (capital letters !!) the script will be run locally.

This is an ideal way to do post installation tasks, such as adding deployments etc. in the newly created cluster.

> [!IMPORTANT]
> Either `podman` or `docker` MUST be installed on the server(s) on which the command will be run.

The script will be run in a container, and therefore a container image to be used must be provided. When the script executes, the supplied script data will be put into a temporary file and then executed with the `bash` command.

| Field Name | Type | Description |
|---|---|---|
| (REQUIRED) `order` | integer | The scripts will be executed in numeric order. |
| (REQUIRED) `scriptRuntime` | object | See [Script Runtime](#script-runtime) |
| (REQUIRED) `targets` | array | List of servers on which to execute the script. A special name `LOCALHOST` (all capital letters) refers to the system on which the provisioning script is running. |
| (REQUIRED) `script` | string | The commands or script content to execute |
| `postRunSleepSeconds` | integer | Seconds to sleep after the command is executed. |

#### Script Runtime

Part of [Post Provisioning Scripts](#post-provisioning-scripts)

The script runtime configuration contains the following fields:


| Field Name | Type | Description |
|---|---|---|
| (REQUIRED) `image` | string | URI of the container image to use. |
| (REQUIRED) `containerCommand` | string | Set to either `podman` or `docker` - which ever is installed on the target server |
| `volumes` | array | See [Script Runtime Volumes](#script-runtime-volumes) |
| `overrideRunParameters` | str | The default container run parameters (excluding volumes and environment variables) are `-it --rm --entrypoint=""` |

The script execution is done in the following way:

1. The script content (`spec.postProvisionScripts[].script`) is saved to a file on the host with a unique name (for reference, we say the file is in `$SCRIPT_FILE`)
2. The container execution command is created in a separate file and will by default run (at minimum) the following: `$CONTAINER_CMD run -it --rm --entrypoint="" -v $SCRIPT_FILE:/tmp/exec.sh:ro $IMAGE bash /tmp/exec.sh`
3. If the script need to run on remote hosts, they are also copied via `scp` to those hosts.
4. The container `STDOUT` will be echoed in the logs

#### Script Runtime Volumes

Part of [Script Runtime](#script-runtime)

Each item of the array is an object with the following fields:

| Field Name | Type | Description |
|---|---|---|
| (REQUIRED) `localPath` | string | The path on the server executing the command, that must be mounted in the container |
| (REQUIRED) `containerMountPoint` | string | The mount point in the container (no option to mount read-only for now) |

> [!IMPORTANT]
> Ensure the path and files to mount is actually available on the servers in scope for this script execution

## Kind: Server

> [!IMPORTANT]
> To ensure the server joins the cluster, the server host name is verified to be in the list of cluster node names. It is therefore important to set `metadata.name` to the actual host name of the server, or otherwise the verification step will fail (or at the very least be inaccurate).

Example:

```yaml
---
apiVersion: v1
kind: Server
metadata:
  name: server1
spec:
  address: 10.0.0.1
  sshPort: 22
  credentials:
    credentialsType: private-key
    value: /path/to/private-key
    username: user
---
apiVersion: v1
kind: Server
metadata:
  name: server2
spec:
  address: 10.0.0.2
  sshPort: 22
  credentials:
    credentialsType: password
    value: secret-name-containing-password
    username: user
```


| Field Name | Type | Description |
|---|---|---|
| (REQUIRED) `address` | string | The IP address or hostname of a server. |
| (REQUIRED) `credentials` | object | See [Server Credentials](#server-credentials) |
| `sshPort` | integer | The SSH port on the server. Default is port 22. |

### Server Credentials

| Field Name | Type | Description |
|---|---|---|
| (REQUIRED) `credentialsType` | string | Either `private-key` or `password` |
| (REQUIRED) `value` | string | In the case of a `private-key`, the path to the private key. In the case of `password`, the name of the `Secret` that holds the password value. |
| (REQUIRED) `username` | string | The username to use when logging in. |

