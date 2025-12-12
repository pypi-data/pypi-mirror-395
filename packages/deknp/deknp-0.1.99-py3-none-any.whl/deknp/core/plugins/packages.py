import os
import shutil
from .base import PluginVue


class PluginPackages(PluginVue):
    path_generated_package = '@'
    excludes = [
        "dek-override",
        "LICENSE",
        "package.dek.json",
        "package.dek.json5",
        "package.json",
        "README.md"
    ]

    def run(self):
        version = self.get_vue_version()
        if version and version[0] != 3:
            return
        package_map = {}
        path_root = self.get_dek_path_generated(self.path_generated_package)
        if os.path.exists(path_root):
            shutil.rmtree(path_root)
        for dir_dek in self.dek_dir_list:
            if dir_dek in self.dek_dev_dir_list:
                continue
            package_map[self.get_package_json(dir_dek)['name']] = dir_dek
            if dir_dek == self.project_dir:
                continue
            pkg_path = dir_dek[len(self.node_modules_dir) + 1:]
            for file in os.listdir(dir_dek):
                if file in self.excludes:
                    continue
                filepath = os.path.join(dir_dek, file)
                p = self.get_dek_path_generated(self.path_generated_package, pkg_path)
                if os.path.isfile(filepath):
                    if not os.path.exists(p):
                        os.makedirs(p)
                    shutil.copyfile(filepath, os.path.join(p, file))
                else:
                    shutil.copytree(filepath, os.path.join(p, file))
        self.share_data['packages'] = package_map
