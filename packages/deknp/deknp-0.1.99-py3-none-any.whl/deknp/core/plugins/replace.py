import pathlib
from dektools.file import read_text, write_file
from .base import Plugin


class PluginReplace(Plugin):
    dek_key_replace = 'replace'

    def run(self):
        replace_info = self.merge_from_key(self.dek_key_replace)
        for glob_rule, replace_list in replace_info.items():
            for item in replace_list:
                if len(item) == 3:
                    marker, append, merge = item
                else:
                    marker, append = item
                    merge = True
                if merge:
                    out = append + marker
                else:
                    out = append
                for p in pathlib.Path(self.node_modules_dir).glob(glob_rule):
                    text = read_text(p)
                    if marker in text and out not in text:
                        text = text.replace(marker, out)
                        write_file(p, s=text)
