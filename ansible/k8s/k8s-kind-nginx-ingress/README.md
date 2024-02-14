# Kind local cluster with NGINX ingress controller

## Usage

To install Kind cluster (if not present) and apply NGINX ingress manifests, run the following command:

```bash
ansible-playbook -i ../environments/<environment> install.yml
```

To change the group of target hosts, edit the `apply.yml` file accordingly.

**The default group of target hosts is set to**: `hosts: "all"`.

To remove the cluster, use the `delete.yml` playbook.

## Requirements

For Ansible:

* `kubernetes.core` collection

## Variables

As default, the cluster will be created with one node of the `control-plane` role.
These variables are to be defined in the `environments/<environment>/group_vars/<group_name>.yml` file:

* `k8s_kind_nginx_ingress_cluster_name` - cluster name suffix (default: `"local-dev"`)
* (*optional*) `k8s_kind_nginx_ingress_cluster_extra_nodes` - definition of extra nodes (default: `[]`)
  Each node is defined as a dictionary with the following keys:
  * `role` - node role (available: `"worker"`, `"control-plane"`)
  * `memory` - human-readable memory size (e.g. `"1Gi"`)
  * `cpu` - number of CPUs (e.g. `2`)
  * `amount` - number of nodes with the same configuration (default: `1`)
  * (*optional*) `extraMounts` - list of extra mounts to apply to the node (default: `[]`):
    * `containerPath` - container path to mount to
    * `hostPath` - host path to mount
    * (*optional*) `readOnly` - whether the mount should be read-only (default: `false`)
    * (*optional*) `selinuxRelabel` - whether the mount should be relabeled by SELinux (default: `false`)
    * (*optional*) `mountPropagation` - mount propagation mode (default: `"None"`)
  * (*optional*) `extraLabels` - list of extra labels to apply to the node (default: `[]`):
    * `name` - label key
    * `value` - label value
  * (*optional*) `extraPortMappings` - list of extra port mappings to apply to the node (default: `[]`):
    * `containerPort` - container port to map
    * `hostPort` - host port to map
    * (*optional*) `listenAddress` - address to listen on (default: `"127.0.0.1"`)
    * (*optional*) `protocol` - protocol to use (default: `"TCP"`)
  * (*optional*) `extraKubeadmPatches` - list of extra kubeadm patches to apply to the node (default: `[]`)

**Important**: if for any node type fields `extraMounts` and/or `extraPortMappings` are defined, the `amount` field is automatically set to `1`, even if its value is specified by the user!
