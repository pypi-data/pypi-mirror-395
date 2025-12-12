import os
import json
from dektools.file import write_file
from .base import Plugin
from ..base.env_vars import EnvVars


class PluginDv3EnvVars(Plugin):
    dek_key_env = 'vars.env'
    env_path_data = 'deknp.env.log'
    env_path_src = 'index.html'

    def run(self):
        result = self.merge_from_key(self.dek_key_env)
        write_file(
            os.path.join(self.project_dir, self.env_path_data),
            json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True)
        )
        path_src = os.path.join(self.project_dir, self.env_path_src)
        if os.path.isfile(path_src):
            ev = EnvVars(path_src)
            ev.update('envBase', result.get('base'))
            ev.update('envEnv', result.get('dev'))
