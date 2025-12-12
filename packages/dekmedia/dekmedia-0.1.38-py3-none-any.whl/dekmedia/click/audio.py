import typer

app = typer.Typer(add_completion=False)


@app.command()
def play(path):
    from ..audio.core import play_file
    play_file(path)


@app.command()
def notify(name, path=None):
    from ..audio.core import play_res
    play_res(name, path)
