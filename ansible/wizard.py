#!/usr/bin/env python3
"""
This module contains the Ansible Wizard CLI.

The Ansible Wizard CLI is a tool for generating Ansible playbooks and roles.
"""
import os
import sys
import typing

import jinja2
import typer

ansible_wizard = typer.Typer(
    rich_markup_mode="rich"
)

templating_engine = jinja2.Environment(
    loader=jinja2.FileSystemLoader(searchpath='./utils/templates/')
)

role_directory_structure = [
    'tasks',
    'handlers',
    'templates',
    'files',
    'vars',
    'defaults',
    'meta',
]


def generate_readme(
    name: str,
    kind: str,
    directory: str,
) -> None:
    """
        Generates a README.md file for a playbook or role.
    """
    typer.echo('Please complete the following description')
    description = typer.prompt(f'{name} is a {kind} that')
    readme_path = f'{directory}/README.md'
    typer.echo(f'Creating {readme_path}')
    template = templating_engine.get_template('README.md.j2')
    rendered_readme = template.render(
        title=name,
        kind=kind,
        description=description,
    ) + '\n'
    with open(readme_path, 'w', encoding='utf-8') as readme_file:
        readme_file.write(rendered_readme)


def setup_role(role_path: str) -> None:
    """
        Sets up the directory structure for a role.
    """
    typer.echo('Setting up role directory structure')
    for directory in role_directory_structure:
        os.mkdir(f'{role_path}/{directory}')
        main_file_path = f'{role_path}/{directory}/main.yml'
        with open(main_file_path, 'w', encoding='utf-8') as main_file:
            main_file.write('---\n')


@ansible_wizard.command()
def playbook(
    name: str = typer.Argument(help='Name of the playbook to generate'),
    roles: typing.Optional[str] = typer.Option(
        default='',
        help='List of roles to include in the playbook, delimited by commas',
    )
) -> None:
    """
    Creates a playbook directory with a [bold blue]README.md[/bold blue]
    and [bold blue]main.yml[/bold blue] file.

    If roles are specified, creates a roles directory with a README.md
    and a directory structure for each role.

    [bold green]Example[/bold green]:

    [italic]ansible-wizard playbook my-playbook --roles role1,role2[/italic]
    """
    typer.echo(f'Creating playbook {name}')
    if os.path.exists(name):
        typer.echo(f'ERROR: {name} already exists')
        sys.exit(1)
    os.mkdir(name)
    generate_readme(name, 'playbook', name)
    with open(f'{name}/main.yml', 'w', encoding='utf-8') as main_file:
        main_file.write('---\n')
    typer.echo(f'Generated README.md and main.yml for {name} playbook')
    if roles:
        roles_list = roles.split(',')
        typer.echo(f'Creating roles directory for {name} playbook')
        for role_name in roles_list:
            role_path = f'{name}/roles/{role_name}'
            os.makedirs(role_path)
            generate_readme(role_name, 'role', role_path)
            typer.echo(f'Generated README.md for {name} role')
            setup_role(role_path)
            typer.echo(f'Generated directory structure for {name} role')


@ansible_wizard.command()
def role(
    name: str = typer.Argument(help='Name of the role to generate'),
) -> None:
    """
        Creates a role directory with a [bold blue]README.md[/bold blue]
        and a directory structure.

        The new role will contain the following directories:

        * [bold blue]tasks[/bold blue]
        * [bold blue]handlers[/bold blue]
        * [bold blue]templates[/bold blue]
        * [bold blue]files[/bold blue]
        * [bold blue]vars[/bold blue]
        * [bold blue]defaults[/bold blue]

        Each directory will contain a [bold blue]main.yml[/bold blue] file.

        [bold green]Example[/bold green]:

        [italic]ansible-wizard role my-role[/italic]
    """
    root_playbook = typer.prompt('Enter root playbook name:')
    if not os.path.exists(root_playbook):
        typer.echo(f'ERROR: {root_playbook} does not exist')
        sys.exit(1)
    typer.echo(f'Creating role {name}')
    if os.path.exists(name):
        typer.echo(f'ERROR: {name} already exists')
        sys.exit(1)
    os.mkdir(name)
    generate_readme(name, 'role', name)
    typer.echo(f'Generated README.md for {name} role')
    setup_role(name)
    typer.echo(f'Generated directory structure for {name} role')


if __name__ == '__main__':
    ansible_wizard()
