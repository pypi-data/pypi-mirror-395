import typer

from pydevman.echo import app as echo_app
from pydevman.file.__main__ import app as file_app
from pydevman.json.__main__ import app as json_app

app = typer.Typer()


def main():
    app.add_typer(echo_app, name="echo", help="echo 工具")
    app.add_typer(json_app, name="json", help="json 工具")
    app.add_typer(file_app, name="file", help="file 工具")
    app()


if __name__ == "__main__":
    main()
