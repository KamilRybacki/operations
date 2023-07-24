# Development environment

This environment is used for development and testing purposes.
It uses a locally deployed `kind` cluster, with Python virtual environments manages with `pyenv`.

Thus, in the `group_vars/dev.yml` file, the `ansible_python_interpreter` variable is set to the Python 3 shim located in `$HOME/.pyenv/shims/python3`.

For connection with local cluster, the `ansible_connection` variable is explicitly set to `local`.

## Variables

These variables are used by playbooks connected to operations on Kubernetes clusters:

* `manifests_and_configs_path` - path where auxiliary files e.g. Jinja2 templates will be rendered to **on host machine** that will be applying manifests to a K8s cluster (default: `"/tmp"`)
* `kubeconfig_path` - path to Kubeconfig **on host machine** to be used i.e. where the cluster entry/context will be added (default: `"{{ lookup('ansible.builtin.env', 'HOME') }}/.kube/config"`)
