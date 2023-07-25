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

These variables are to be defined in the `environments/<environment>/group_vars/<group_name>.yml` file:

* `kind_cluster_name` - cluster name suffix (default: `"local-dev"`)
