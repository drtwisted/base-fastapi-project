# Launch the project
## Prerequisites
Make sure you have installed:
 * `docker`
 * `docker-compose`
 * `poetry`
 * (optional) `conda` you may need to install it in order to satisfy the python version

## Setup environment
To setup the dev environemnt you will have to take next steps:
 * Setup a python virtual environment with the tool of your choice
 * Activate your virtual environment and run:
```bash
poetry install --with=dev --no-root
```

## Run CLI tool
> **NOTE**
>
> You'll need to have the virtual environment actiavted before you'll be able to run the CLI tool

Make sure that the CLI tool has run priviledges:
```bash
chmod +x ./run.py
```
Now you can run the tool:
```bash
./run.py

Usage: run.py [OPTIONS] COMMAND [ARGS]...

  A simple project runner CLI tool.

Options:
  --help  Show this message and exit.

Commands:
  down     Stop the project containers using docker-compose
  restart  Restart the project containers using docker-compose
  up       Up the project containers using docker-compose
```
To get more details on each command, run:
```bash
./run.py [command] --help
```
