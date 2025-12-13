import typer
from dhruv.main import hello

app = typer.Typer()

@app.callback()
def callback():
    """
    Dhruv CLI
    """
    pass

@app.command(name="hello")
def hello_cmd():
    """
    Prints a hello message.
    """
    print(hello())

if __name__ == "__main__":
    app()
