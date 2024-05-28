# Launch the project

## Run CLI tool
> **NOTE**
>
> You'll need to setup the environment before you'll be able to run the CLI tool

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
