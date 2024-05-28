#!/usr/bin/env python
import subprocess
import click

BASE_DOCKER_COMPOSE_COMMAND = [
    "docker-compose",
    "-f",
    "docker-compose.yaml",
    "--profile=backend",
    "--env-file=envs/.env",
]


def run_verbose(command):
    print(f"Running: \n{' '.join(command)}")
    subprocess.run(
        command,
    )


def container_up(rebuild):
    command = BASE_DOCKER_COMPOSE_COMMAND.copy()

    command.extend(
        [
            "up",
            "-d",
        ]
    )

    if rebuild:
        command.append("--build")

    run_verbose(command)


def container_down():
    command = BASE_DOCKER_COMPOSE_COMMAND.copy()
    command.append("down")

    run_verbose(command)


@click.group()
def project_runner():
    """A simple project runner CLI tool."""
    pass


@project_runner.command()
@click.option("--rebuild", "-r", is_flag=True, help="Rebuild the container")
def up(rebuild: bool):
    """Up the project containers using docker-compose"""
    container_up(rebuild)


@project_runner.command()
def down():
    """Stop the project containers using docker-compose"""
    container_down()


@project_runner.command()
@click.option("--rebuild", "-r", is_flag=True, help="Rebuild the container")
def restart(rebuild: bool):
    "Restart the project containers using docker-compose"
    container_down()
    container_up(rebuild)


if __name__ == "__main__":
    project_runner()
