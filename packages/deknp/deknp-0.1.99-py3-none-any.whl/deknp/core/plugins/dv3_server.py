import os
import glob
from dektools.file import write_file
from .base import Plugin


class PluginDv3Server(Plugin):
    path_generated_servers = 'dv3/servers'
    glob_server_yaml = '/**/dv3/servers/**/*.yaml'
    glob_prefix_path = '/dv3/servers/'.replace('/', os.sep).replace('\\', os.sep)

    def run(self):
        if not self.share_data.get('packages'):
            return
        packages = {v: k for k, v in self.share_data['packages'].items()}
        packages_dir = sorted(packages.keys(), reverse=True, key=lambda x: len(x))
        for dir_scan in self.dek_dir_list_for_scan:
            server_yaml_dir = None
            package_name = None
            for filepath in glob.glob(dir_scan + self.glob_server_yaml, recursive=True):
                filepath = os.path.normpath(filepath)
                for p in packages_dir:
                    if filepath.startswith(p):
                        package_name = packages[p]
                        break
                if package_name is None:
                    raise Exception(f'filepath not in {packages_dir}')
                index_sep = filepath.rfind(self.glob_prefix_path) + len(self.glob_prefix_path) - 1
                server_yaml_dir = filepath[:index_sep]
                break
            if server_yaml_dir:
                write_file(self.get_dek_path_generated(self.path_generated_servers, package_name), c=server_yaml_dir)
