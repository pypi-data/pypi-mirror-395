import typer

app = typer.Typer(add_completion=False)


@app.command()
def clear():
    from ..font.manager.default import font_manager
    font_manager.clear()
