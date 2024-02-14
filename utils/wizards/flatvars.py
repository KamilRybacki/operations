#!/usr/bin/env python3
"""
This module allows to quickly flatten Helm Values YAML so that
the nested structure is removed and the variables are all at the top
and enerates a Jinja2 template with the flattened variables.
"""

import os
import sys
import typing
import yaml  # type: ignore

import typer

FLATVARS = typer.Typer(
    rich_markup_mode="rich",
    help='Flat Helm values generator',
)


DEFAULT_DEPTH = 2
BARRIER_KEYS = [
    'annotations',
]


@FLATVARS.command()
def flatten(
    input_file: str = typer.Argument(
        help="""
            Path to the Helm Values YAML file to flatten
        """,
    ),
    output_file: typing.Optional[str] = typer.Option(
        default='',
        help="""
            Path to the output file with flattened Helm Values
        """,
    ),
    depth: typing.Optional[int] = typer.Option(
        default=DEFAULT_DEPTH,
        help='How many levels of nesting to flatten',
    ),
    prefix: typing.Optional[str] = typer.Option(
        default='',
        help='Prefix to add to the flattened variables',
    )
) -> None:
    if not os.path.exists(input_file):
        typer.secho(f"File {input_file} does not exist", fg=typer.colors.RED)
        sys.exit(1)
    with open(input_file, 'r', encoding='utf-8') as helm_chart:
        helm_values = [
            line
            for line in helm_chart.read().strip().splitlines()
            if not line.strip().startswith('#')
            and line.strip()
        ]
        flat_values = flatten_helm_values(
            yaml.safe_load('\n'.join(helm_values)),
            depth or DEFAULT_DEPTH,
            prefix or ''
        )
        flattened_yaml = yaml.dump(flat_values, default_flow_style=False)
        output_file_path = output_file \
            or input_file.replace('.yaml', '_flat.yaml').replace('.yml', '_flat.yml')
        with open(output_file_path, 'w', encoding='utf-8') as output:
            output.write(flattened_yaml)
    typer.secho(
        f"Flattened Helm Values have been written to {output_file_path}",
        fg=typer.colors.GREEN
    )


def flatten_helm_values(values: dict, depth: int, prefix: str) -> dict:
    """
    Flatten the nested dictionary values
    """
    flat_values: dict[str, str | int | dict | list] = {}
    depth_counter = 0
    for key, value in values.items():
        if isinstance(value, dict):
            if depth_counter < depth:
                flat_values.update(
                    flatten_helm_values(
                        value,
                        depth,
                        format_key(f"{prefix}_{key}")
                    )
                )
                depth_counter += 1
                continue
            if key.split('_')[-1] in BARRIER_KEYS or '/' in key:
                flat_values[
                    format_key(f"{prefix}_{key}")
                ] = value
                continue
            for k, v in value.items():
                flat_values[
                    format_key(f"{prefix}_{key}_{k}")
                ] = v
        else:
            flat_values[
                format_key(f"{prefix}_{key}")
            ] = value
    return flat_values


def format_key(key: str) -> str:
    """
    Format the key to be used in the flattened dictionary.
    For each section separated by underscores, split snake case
    and join individual words with underscores.
    """
    formatted_sections = []
    for section in key.split('_'):
        split_snake_case_words = []
        first_pointer = 0
        second_pointer = 1
        while second_pointer < len(section):
            if section[second_pointer].isupper():
                split_snake_case_words.append(
                    section[first_pointer:second_pointer].lower()
                )
                first_pointer = second_pointer
            second_pointer += 1
        split_snake_case_words.append(
            section[first_pointer:second_pointer].lower()
        )
        formatted_sections.append(
            '_'.join(split_snake_case_words)
        )
    return '_'.join(formatted_sections)
