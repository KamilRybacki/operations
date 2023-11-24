#!/usr/bin/env python3
"""
This module contains the Ansible Wizard CLI.

The Ansible Wizard CLI is a tool for generating Ansible playbooks and roles.
"""


import os
import sys
import typing

import jinja2
import rich.progress
import typer

ANSIBLE = typer.Typer(
    rich_markup_mode="rich",
    help='Ansible Wizard CLI',
)

# This goes up 4 directories from the current file,
# looks horrible but it works
# TODO: Find a better way to do this

ANSIBLE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )
    )
) + '/ansible'

TEMPLATING_ENGINE = jinja2.Environment(
    loader=jinja2.FileSystemLoader(searchpath='./utils/templates/')
)

ANSIBLE_ROLE_DIRECTORIES = [
    'tasks',
    'handlers',
    'templates',
    'files',
    'vars',
    'defaults',
    'meta',
]

ANSIBLE_PLAYBOOK_SECTIONS = {
    'general': 'General purpose playbooks',
    'net': 'Networking playbooks',
    'vm': 'Virtualization playbooks',
    'k8s': 'Kubernetes playbooks',
}


def generate_readme(
    name: str,
    kind: str,
    directory: str,
) -> None:
    """
        Generates a README.md file for a playbook or role.
    """
    if not os.path.exists(ANSIBLE_DIR):
        typer.echo(f'ERROR: {ANSIBLE_DIR} does not exist')
        typer.Abort()
    typer.echo('Please complete the following description')
    description = typer.prompt(f'{name} is a {kind} that')
    readme_path = f'{directory}/README.md'
    typer.echo(f'Creating {readme_path}')
    template = TEMPLATING_ENGINE.get_template('README.md.j2')
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
    for directory in ANSIBLE_ROLE_DIRECTORIES:
        os.mkdir(f'{role_path}/{directory}')
        main_file_path = f'{role_path}/{directory}/main.yml'
        with open(main_file_path, 'w', encoding='utf-8') as main_file:
            main_file.write('---\n')


@ANSIBLE.command()
def playbook(
    playbook_section: str = typer.Argument(
        help=f"""
            Name of the playbook section to generate the playbook in.

            Valid options are:

            {os.linesep.join([
                f'{os.linesep}* [bold blue]{section}[/bold blue] - {description}'
                for section, description in ANSIBLE_PLAYBOOK_SECTIONS.items()
            ])}
        """,
    ),
    playbook_name: str = typer.Argument(help='Name of the playbook to generate'),
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

    [italic]ansible-wizard playbook my-playbook-section my-playbook-name --roles role1,role2[/italic]
    """
    if playbook_section not in ANSIBLE_PLAYBOOK_SECTIONS:
        typer.echo(f'ERROR: {playbook_section} is not a valid playbook section')
        typer.echo('Type ansible-wizard playbook --help for more information')
        sys.exit(1)
    typer.echo(
        f'Creating playbook {playbook_name} in {playbook_section} section'
    )
    playbook_path = f'{ANSIBLE_DIR}/{playbook_section}/{playbook_name}'
    if os.path.exists(playbook_path):
        typer.echo(f'ERROR: {playbook_name} already exists')
        sys.exit(1)
    os.makedirs(playbook_path, exist_ok=True)
    generate_readme(playbook_name, 'playbook', playbook_path)
    with open(f'{playbook_path}/main.yml', 'w', encoding='utf-8') as main_file:
        main_file.write('---\n')
    typer.echo(
        f'Generated README.md and main.yml for {playbook_name} playbook'
    )
    if roles:
        roles_list = roles.split(',')
        for role_name in roles_list:
            role_path = f'{playbook_path}/roles/{role_name}'
            os.makedirs(role_path)
            generate_readme(role_name, 'role', role_path)
            typer.echo(f'Generated README.md for {role_name} role')
            setup_role(role_path)
            typer.echo(f'Generated directory structure for {role_name} role')


@ANSIBLE.command()
def role(
    role_name: str = typer.Argument(help='Name of the role to generate'),
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
    relative_path = typer.prompt(
        f'Enter playbook path (relative to ${ANSIBLE_DIR}):'
    ).rstrip('/')
    root_playbook = f"{ANSIBLE_DIR}/{relative_path}"
    if not os.path.exists(root_playbook):
        typer.echo(f'ERROR: {root_playbook} does not exist')
        sys.exit(1)
    typer.echo(f'Creating role {role_name}')
    role_path = f'{root_playbook}/roles/{role_name}'
    if os.path.exists(role_path):
        typer.echo(f'ERROR: role {role_name} already exists')
        sys.exit(1)
    os.makedirs(role_path, exist_ok=True)
    generate_readme(role_name, 'role', role_path)
    typer.echo(f'Generated README.md for {role_name} role')
    setup_role(role_path)
    typer.echo(f'Generated directory structure for {role_name} role')


if __name__ == '__main__':
    ANSIBLE()
