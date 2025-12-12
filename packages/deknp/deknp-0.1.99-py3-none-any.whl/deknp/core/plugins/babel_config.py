import os
import json
from .base import Plugin


class PluginBabelConfig(Plugin):
    dek_key_babel_config = 'babel.config.js'
    babel_config_marker = '//@marker-config-add'

    def run(self):
        if not os.path.isfile(self.babel_config_standard_filepath):
            return
        for data in self.dek_info_list_final:
            config_info = data.get(self.dek_key_babel_config) or {}
            if config_info:
                s = self.load_text(self.babel_config_standard_filepath)
                str_list = []
                for k, v in config_info.get('presets', {}).items():
                    mk = f'marker-preset---{k}'
                    if mk not in s:
                        str_list.append(f'babelConfig.addPreset({json.dumps(mk)}, {json.dumps(v)})')
                for k, v in config_info.get('plugins', {}).items():
                    mk = f'marker-plugin---{k}'
                    if mk not in s:
                        str_list.append(f'babelConfig.addPlugin({json.dumps(mk)}, {json.dumps(v)})')
                index = s.find(self.babel_config_marker)
                ss = s[:index] + '\n' + '\n'.join(str_list) + '\n' + s[index:]
                self.save_text(self.babel_config_standard_filepath, ss)

    @property
    def babel_config_standard_filepath(self):
        return os.path.join(self.project_dir, self.dek_key_babel_config)
