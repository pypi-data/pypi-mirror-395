from dektools.typer import command_version
from . import app
from . import audio as audio_command
from . import image as image_command
from . import font as font_command

command_version(app, __name__)

app.add_typer(audio_command.app, name='audio')
app.add_typer(image_command.app, name='image')
app.add_typer(font_command.app, name='font')


def main():
    app()
