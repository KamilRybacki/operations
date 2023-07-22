# Development environment

This environment is used for development and testing purposes.
It uses a locally deployed `kind` cluster, with Python virtual environments manages with `pyenv`.

Thus, in the `group_vars/dev.yml` file, the `ansible_python_interpreter` variable is set to the Python 3 shim located in `$HOME/.pyenv/shims/python3`.

For connection with local cluster, the `ansible_connection` variable is explicitly set to `local`.
