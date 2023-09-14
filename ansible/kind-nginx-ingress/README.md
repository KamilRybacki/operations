# Kind local cluster with NGINX ingress controller

## Usage

To install Kind (if not present) and NGINX ingress controller on aa new, local cluster, run the following command:

```bash
ansible-playbook -i ../environments/<environment> install.yml
```

To change the group of target hosts, edit the `apply.yml` file accordingly. 

**The default group of target hosts is set to**: `hosts: "all"`.

## Requirements

For Ansible:

* `kubernetes.core` collection

## Variables

As default, the cluster will be created with one node of the `control-plane` role.
These variables are to be defined in the `environments/<environment>/group_vars/<group_name>.yml` file:

* `kind_nginx_ingress_cluster_name` - cluster name suffix (default: `"local-dev"`)
* `kind_nginx_ingress_cluster_extra_nodes` - definition of extra nodes (default: `[]`)
  Each node is defined as a dictionary with the following keys:
  * `role` - node role (available: `"worker"`, `"control-plane"`)
  * `memory` - human-readable memory size (e.g. `"1Gi"`)
  * `cpu` - number of CPUs (e.g. `2`)
  * `amount` - number of nodes with the same configuration (e.g. `2`)
  * (*optional*) `extraKubeadmPatches` - list of extra kubeadm patches to apply to the node (default: `[]`)
