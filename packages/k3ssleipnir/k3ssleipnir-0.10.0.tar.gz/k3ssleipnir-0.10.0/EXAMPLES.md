# Examples

The following document briefly discuss the examples found in the `examples/` directory

> [!NOTE]
> The full specification is documented in the [SPEC.md](./SPEC.md) file.

## Minimal Example

File: [minimal.yaml](./examples/minimal.yaml)

A simple example to provide a single-node cluster on a server using the absolute minimal configuration.

## Only Run Command(s) on Remote Node(s)

File: [only_run_command_on_remote_node.yaml](./examples/only_run_command_on_remote_node.yaml)

The intent of this scenario is to demonstrate how commands can be run through this tool on cluster nodes without changing anything else on the cluster.

It is assumed that the cluster was previously created through a different manifest.

As a bonus, it also demonstrates how both private keys and normal passwords (stored in AWS Secrets Manager) can be used for remote server authentication.

This approach is useful to run run the exact same command on one or more nodes as a maintenance task after the initial setup of the server. In this way, as a practical example, the remote nodes can be patched. If each node needs to be rebooted, consider placing the update command in separate script blocks and use the `postRunSleepSeconds` value to give the server enough time to reboot before running the commands on the next server.

For the patch scenario to work, as well as for any command tat requires `sudo`, remember to add the relevant entries into the `sudoers` file to allow the commands to be run with `root` privileges without requiring a password. For the example, the following entry would be needed in the `sudoers` file:

```text
k3s ALL = NOPASSWD: /opt/patch_and_reboot.sh
```

The script `/opt/patch_and_reboot.sh` may have the following content:

```bash
apt update 
apt upgrade -y
apt autoremove -y
reboot
```

## Maintaining All Files in Git

Assuming you have manifest like `minimal.yaml` and `only_run_command_on_remote_node.yaml` in version control on a remote Git repository, it is possible to just use a simple local manifest that will clone the remote repository and ingest the manifest file(S).

An example:

```yaml
---
apiVersion: v1
kind: GitRepository
metadata:
  name: homelab-repo
spec:
  url: ssh://git@codeberg.org/user/homelab-configs.git
  branch: main
  credentials:
    credentialsType: ssh
    value: /home/user/.ssh/my-codeberg-key
    username: git
  localWorkDir: /tmp/repos/homelab-repo
  postCleanup: true
  postCloneActions:
    - actionType: provisioning
      srcFilePath: minimal.yaml

```
