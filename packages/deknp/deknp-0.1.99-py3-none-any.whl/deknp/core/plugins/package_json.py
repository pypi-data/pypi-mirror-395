import os
from collections import OrderedDict
from dektools.dict import assign
from .base import Plugin


class PluginPackageJson(Plugin):
    package_dependencies_key = 'dependencies'
    package_data_name = 'package.data.json'
    package_data_baned_keys = {'keywords', 'scripts', 'dependencies', 'devDependencies', 'main', '.pnpm'}

    def run(self):
        dependencies = self.merge_from_key(self.package_dependencies_key, True)
        package_data = OrderedDict()
        for data in self.dek_info_list_final:
            package_data = assign(package_data, data.get(self.package_data_name) or {})
        for data in self.dek_info_list_final:
            package_json = data.get(self.package_standard_name) or {}
            if package_json:
                d = self.load_package_standard()
                d = assign(d, package_json)
                d.pop(self.dek_key_root, None)
                self.transform_dependencies(d, dependencies)
                self.save_json(self.package_standard_filepath, d)
                self.save_to_package_data_json(d, package_data)

    @staticmethod
    def transform_dependencies(data, dependencies):
        if dependencies is not None:
            values = {**(data.get('dependencies') or {}), **(data.get('devDependencies') or {})}
            value_dependencies = {}
            value_dev_dependencies = {}
            for k, v in values.items():
                if dependencies.get(k):
                    value_dependencies[k] = v
                else:
                    value_dev_dependencies[k] = v
            data['dependencies'] = value_dependencies
            data['devDependencies'] = value_dev_dependencies

    def save_to_package_data_json(self, data, package_data):
        result = assign(package_data)
        for key, value in data.items():
            if key not in self.package_data_baned_keys:
                result[key] = value
        self.save_json(os.path.join(self.project_dir, self.package_data_name), result)
