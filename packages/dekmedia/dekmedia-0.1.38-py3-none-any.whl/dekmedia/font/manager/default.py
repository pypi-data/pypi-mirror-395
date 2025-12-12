import os
from .base import Manager

_env_paths = os.getenv(__name__.partition('.')[0].upper() + '_FONT_PATHS') or ''

font_manager = Manager([p for p in _env_paths.split(';') if p])
