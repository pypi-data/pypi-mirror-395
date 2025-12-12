import os
import json
import hashlib
from .base import Plugin
from dektools.file import write_file
from dekgen.resloader import ResLoader


class PluginDv3Yaml(Plugin):
    yaml_prefix = '.yaml'
    yaml_suffix = yaml_prefix + '.json'
    yaml_group_mark = '.'

    path_generated_dv3 = 'dv3'

    def run(self):
        js_glob_list = self.get_js_glob_list()
        groups = {}
        for glob_item in js_glob_list:
            if glob_item.endswith(self.yaml_suffix):
                basename = os.path.basename(glob_item)
                group = basename[: -len(self.yaml_suffix)].rsplit(self.yaml_group_mark, 1)[-1]
                array = groups.setdefault(group, [])
                end = -(len(self.yaml_group_mark) + len(group) + len(self.yaml_suffix))
                real_glob_item = glob_item[:end] + self.yaml_prefix
                for filepath in self.list_glob_filepath(real_glob_item):
                    array.append(filepath)
        for group, paths in groups.items():
            res_loader = ResLoader.from_template_file(*(dict(filepath=filepath) for filepath in paths))
            for data in res_loader.data_list:
                data.pop('__context__', None)
                filepath = data.pop('__file__')
                index = filepath.rfind(self.path_generated_dv3)
                uid = hashlib.sha256(filepath.encode('utf-8')).hexdigest()
                filepath_new = self.get_dek_path_generated(
                    os.path.splitext(filepath[index:])[0] + '.' + uid + self.yaml_group_mark + group + self.yaml_suffix)
                write_file(filepath_new, s=json.dumps(data, indent=2, ensure_ascii=False, sort_keys=False))
