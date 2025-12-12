import typer

app = typer.Typer()


@app.command()
def hello(name=None):
    if name:
        print(f"hello {name}")
    else:
        print("hello")


if __name__ == "__main__":
    app()
