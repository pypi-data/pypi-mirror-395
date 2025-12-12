import os
import json
from itertools import chain
from dektools.file import write_file, read_file
from dektools.startup.cache import StartupCache
from ...const import weight_dict, font_props_default
from ...type import get_afm_meta, get_ttf_meta
from ...path import iter_all_fonts, iter_dir_fonts


class Manager(StartupCache):
    __version__ = 'v0.1.0'
    done_name = __version__

    def __init__(self, paths=None):
        self.paths = paths if paths else []
        if self._is_done():
            self.font_list = json.loads(read_file(self.path_data))
        else:
            self.font_list = []
        super().__init__()

    @property
    def path_data(self):
        return self.path_index / self.__version__ / 'fonts.json'

    def _cache_handler(self):
        result = []
        for file in chain(iter(iter_all_fonts()), iter(iter_dir_fonts(*self.paths))):
            if os.path.splitext(file)[-1].lower() == ".afm":
                info = get_afm_meta(file)
            else:
                info = get_ttf_meta(file)
            result.append({'path': file, 'props': info})
        self.font_list = result
        write_file(self.path_data, s=json.dumps(self.font_list))

    def find_family(self, family, **kwargs):
        name_list = [name.strip() for name in family.split(',')]
        entries = [{**font_props_default, 'name': name, **kwargs} for name in name_list]
        return self.find(entries)

    def find(self, entries):
        for props in entries:
            props['weight'] = weight_dict.get(props['weight'], props['weight'])
        for item in self.font_list:
            if item['props'] in entries:
                return item['path']
