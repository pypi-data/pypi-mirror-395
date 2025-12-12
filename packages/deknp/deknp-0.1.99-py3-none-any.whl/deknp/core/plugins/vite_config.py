import os
import json
from collections import OrderedDict
from dektools.dict import list_dedup
from .base import PluginVue, PluginUniapp


class PluginViteConfig(PluginVue, PluginUniapp):
    dek_key_vite_config = 'vite.settings.js'
    dek_config_marker = '//@marker-dek-config-add'

    vite_config_items = [
        ['assign', 'global', None, False],
        ['list', 'plugins', None, True],
        ['list', 'scssHeader', None, False],
        ['dict', 'alias', None, False],
        ['dict', 'buildInputs', None, True],
        ['dict', 'define', None, True],
        ['list', 'optimizeDeps', None, False],
    ]

    def get_item_list(self, key, dedup=True):
        result = []
        for data_dek in self.dek_info_list_final:
            data = data_dek.get(self.dek_key_vite_config)
            if data:
                items = data.get(key)
                if items:
                    if not isinstance(items, list):
                        items = [items]
                    for item in items:
                        if dedup:
                            item = json.dumps(item, sort_keys=True)
                        result.append(item)
        return [json.loads(item) for item in list_dedup(result)] if dedup else result

    def get_item_dict(self, key):
        result = OrderedDict()
        for data_dek in self.dek_info_list_final:
            data = data_dek.get(self.dek_key_vite_config)
            if data:
                items = data.get(key)
                if items:
                    result.update(items)
        return result

    def run(self):
        if self.is_uniapp_project():
            if self.get_uniapp_vue_version() != 3:
                return
        else:
            version = self.get_vue_version()
            if not version or version[0] != 3:
                return
        if not os.path.isfile(self.vue_config_standard_filepath):
            return
        s = self.load_text(self.vue_config_standard_filepath)
        str_list = []

        for (typed, name, method, raw) in self.vite_config_items:
            if not method:
                method = "add" + name[0].upper() + name[1:]
            if typed == 'assign':
                for value in self.get_item_list(name):
                    mk = f'marker--{method}--{self.get_data_uid(value)}'
                    if mk not in s:
                        str_list.append(
                            f'dekConfig.{method}({json.dumps(mk)}, {value if raw else json.dumps(value)})')
            elif typed == 'list':
                for key, value in self.get_item_dict(name).items():
                    mk = f'marker--{method}--{self.get_data_uid([key, value])}'
                    if mk not in s:
                        str_list.append(f'dekConfig.{method}({json.dumps(mk)}, {value if raw else json.dumps(value)})')
            elif typed == 'dict':
                for key, value in self.get_item_dict(name).items():
                    mk = f'marker--{method}--{self.get_data_uid([key, value])}'
                    if mk not in s:
                        str_list.append(
                            f'dekConfig.{method}({json.dumps(mk)}, '
                            f'{json.dumps(key)}, {value if raw else json.dumps(value)})'
                        )

        index = s.find(self.dek_config_marker)
        ss = ''.join([
            s[:index], '\n',
            '\n'.join([x for x in self.get_item_dict('imports').values() if x not in s]), '\n',
            '\n'.join(str_list), '\n',
            s[index:]
        ])
        self.save_text(self.vue_config_standard_filepath, ss)

    @property
    def vue_config_standard_filepath(self):
        return os.path.join(self.project_dir, self.dek_key_vite_config)
