import json
from pathlib import Path
from typing import Optional

import toml
import typer
from quick_zip.core.settings import console, settings
from rich.syntax import Syntax

app = typer.Typer()


@app.callback(invoke_without_command=True)
def config(
    config_file: Optional[str] = typer.Argument(settings.config_file),
    filter: Optional[str] = typer.Option(None, "-f"),
):
    """📄 displays the configuration file"""

    if isinstance(config_file, str):
        config_file = Path(config_file)

    with open(config_file, "r") as f:
        content = f.read()

    if filter:
        temp_dict = toml.loads(content).get(filter)

        if temp_dict == None:
            console.print(
                f"Error! Could not find key '{filter}' in {config_file}",
                style="red",
            )

            raise typer.Exit()

        content = json.dumps(temp_dict, indent=4)

    console.print("Config File Path", settings.config_file)

    if settings.verbose:
        syntax = Syntax(content, "toml", theme="material", line_numbers=True)
        console.print(syntax)
