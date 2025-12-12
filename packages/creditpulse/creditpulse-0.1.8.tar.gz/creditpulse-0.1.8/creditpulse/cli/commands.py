"""Command line interface."""

import click


@click.command()
@click.option("--name", "-n", help="Name to greet", type=str, default=None, )
@click.version_option()
def main(name: str) -> None:
    """My Project CLI."""
    print(name)
