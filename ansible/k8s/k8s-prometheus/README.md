# Basic K8s Prometheus Operator setup with CRDs

## Usage

To install Prometheus Operator with CRDs required to deploy appropiate monitors etc. at target K8s cluster, run the following command:

```bash
ansible-playbook -i ../environments/<environment> install.yml
```

To change the group of target hosts, edit the `install.yml` file accordingly.

**The default group of target hosts is set to**: `hosts: "all"`.

To uninstall Prometheus from the target cluster, use the `uninstall.yml` playbook.

## Requirements

For Ansible:

* `kubernetes.core` collection

## Variables

* `k8s_prometheus_target_cluster_name` - name of K8s cluster on which to install Prometheus Operator
