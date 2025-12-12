import os
from .base import Plugin


class PluginRequests(Plugin):
    path_generated_icons = 'dv3/requests'

    def run(self):
        self.walk(self.dir_server)

    @property
    def dir_server(self):
        return os.path.join(self.project_dir, 'server')

    def walk(self, root):
        if os.path.isdir(root):
            for name in os.listdir(root):
                rn = os.path.join(root, name)
                if os.path.isdir(rn) and name not in ['.venv']:
                    self.walk(rn)
                elif name == 'requests.djcreator.json':
                    if 'dumppredefined__' not in root.split(os.sep):
                        name_root = rn[len(self.dir_server) + 1:].split(os.sep, 1)[0]
                        self.save_json(
                            self.get_dek_path_generated(self.path_generated_icons, f'{name_root}.json'),
                            self.load_json(rn))
