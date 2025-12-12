import os
import tempfile
from dektools.file import write_file, remove_path
from .base import Plugin


class PluginOverrideRootTemplate(Plugin.default_template_cls):
    file_ignore_name = 'dek-override'


class PluginOverrideRoot(Plugin):
    default_template_cls = PluginOverrideRootTemplate
    dek_key_override = 'override'
    dek_overrides_dir_name = 'dek-override'

    def run(self):
        ignore_info = self.merge_from_key(self.dek_key_override)
        dir_temp = tempfile.mkdtemp()
        for dir_dek in self.dek_dir_list:
            src = os.path.join(dir_dek, self.dek_overrides_dir_name)
            if os.path.exists(src):
                write_file(dir_temp, ma=src)
        for filename, info in ignore_info.items():
            write_file(
                os.path.join(dir_temp, self.default_template_cls.get_file_ignore(filename)),
                s="\n".join([x for x, b in info.items() if b])
            )
        self.default_template.render_dir(self.project_dir, dir_temp)
        remove_path(dir_temp)
