#!/usr/bin/env python
import json
import os
import subprocess
import sys
from pathlib import Path
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import typer


cli = typer.Typer()


@cli.command()
def gen(
    python_file: str = typer.Argument(
        ..., help="The name of a Python file that describes your API"
    )
):
    name = Path(python_file).with_suffix("")
    uvicorn_process = subprocess.Popen(
        [f"uvicorn {name}:app --log-level critical"],
        shell=True,
        cwd="/data",
        stdout=subprocess.DEVNULL,
    )
    retry = int(os.getenv("RETRY", 3))
    retry_delay = int(os.getenv("BACKOFF_FACTOR", 1))
    r = Retry(connect=retry, backoff_factor=retry_delay)
    s = requests.Session()
    s.mount("http://", HTTPAdapter(max_retries=r))
    response = s.get("http://127.0.0.1:8000/openapi.json")
    if 200 < response.status_code >= 300:
        uvicorn_status = uvicorn_process.poll()
        if uvicorn_status is not None:
            typer.echo(f"Invalid specification:\n{uvicorn_process.stderr}")
            sys.exit(1)
        else:
            typer.echo(
                f"An error occured downloading OpenAPI specification:\n{response.text}"
            )
            uvicorn_process.kill()
            sys.exit(1)
    else:
        uvicorn_process.kill()
    spec = response.json()
    json.dump(spec, sys.stdout, indent=4)


@cli.command()
def doc(
    python_file: str = typer.Argument(
        ..., help="The name of a Python file that describes your API"
    )
):
    name = Path(python_file).with_suffix("")
    uvicorn_process = subprocess.Popen(
        [f"uvicorn {name}:app --host 0.0.0.0 --reload"], shell=True, cwd="/data"
    )
    uvicorn_process.wait()


if __name__ == "__main__":
    cli()
