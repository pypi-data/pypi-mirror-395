CONTROL_PLANE_INSTALL_SCRIPT_CONTENT_INITIAL = """#!/usr/bin/env bash

export TOKEN=__TOKEN__

curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="server" sh -s - --disable=traefik --kubelet-arg="node-ip=0.0.0.0" --cluster-init --token=$TOKEN --tls-san "__IP__"

cp -vf /var/lib/rancher/k3s/server/node-token > /tmp/k3s_token
chown $USER:$USER /tmp/k3s_token

cp -vf /etc/rancher/k3s/k3s.yaml /tmp/k3s.yaml
chown $USER:$USER /tmp/k3s.yaml
chmod 644 /tmp/k3s.yaml
"""

CONTROL_PLANE_INSTALL_SCRIPT_CONTENT_GENERAL = """#!/usr/bin/env bash

export TOKEN=__TOKEN__
export SERVER_ADDR="https://__IP__"

curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="server" sh -s - \
  --disable traefik \
  --kubelet-arg "node-ip=0.0.0.0" \
  --token $TOKEN \
  --server "$SERVER_ADDR:6443" \
  --tls-san "__IP__"
"""

DATA_PLANE_INSTALL_SCRIPT_CONTENT = """#!/usr/bin/env bash

export TOKEN=__TOKEN__
export SERVER_ADDR="https://__IP__"

curl -sfL https://get.k3s.io | K3S_URL="$SERVER_ADDR:6443" K3S_TOKEN="$TOKEN" sh -
"""
