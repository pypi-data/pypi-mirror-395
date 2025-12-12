import os
import shutil
from .base import Plugin


class PluginDv3(Plugin):
    path_generated_dv3 = 'dv3'

    def run(self):
        path_root = self.get_dek_path_generated(self.path_generated_dv3)
        if os.path.exists(path_root):
            shutil.rmtree(path_root)
