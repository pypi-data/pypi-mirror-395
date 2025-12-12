import os
import json
from .base import PluginVue, PluginUniapp


class PluginVueConfig(PluginVue, PluginUniapp):
    dek_key_vue_config = 'vue.config.js'
    vue_config_marker = '//@marker-config-add'

    @property
    def transpile_dependencies(self):
        result = []

        for dir_dek in self.dek_dir_list:
            package_name = dir_dek[len(self.node_modules_dir) + 1:].replace('\\', '/')
            if package_name:
                result.append(package_name)

        for data_dek in self.dek_info_list_final:
            items = (data_dek.get(self.dek_key_vue_config) or {}).get('transpileDependencies') or []
            result.extend(items)

        return result

    def run(self):
        version = self.get_vue_version()
        if (not version or version[0] != 2) and not self.is_uniapp_project():
            return
        if not os.path.isfile(self.vue_config_standard_filepath):
            return
        s = self.load_text(self.vue_config_standard_filepath)
        str_list = []
        for item in sorted(set(self.transpile_dependencies)):
            mk = f'marker--addTranspileDependencies--{self.get_data_uid(item)}'
            if mk not in s:
                str_list.append(f'vueConfig.addTranspileDependencies({json.dumps(mk)}, {json.dumps(item)})')
        index = s.find(self.vue_config_marker)
        ss = s[:index] + '\n' + '\n'.join(str_list) + '\n' + s[index:]
        self.save_text(self.vue_config_standard_filepath, ss)

    @property
    def vue_config_standard_filepath(self):
        return os.path.join(self.project_dir, self.dek_key_vue_config)
