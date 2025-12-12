import sys, os
from subprocess import call
from jdatetime import datetime
import click
from pathlib import Path

EDITOR = "vim"
BASE_PATH = Path("~/daily") 
@click.group()
def cli():
    ...
    
@click.command()
@click.option("--message", type=str)
def new(message: str):
    date = datetime.now().date()
    file_name = f"{BASE_PATH.expanduser().as_posix()}/{date.year}.{date.month}.{date.day}.md"
    with open(file_name, "w") as file:
        if message is None: 
            message = str(date)
        file.write(message)
        file.flush()
        call([EDITOR, file.name])

cli.add_command(new)