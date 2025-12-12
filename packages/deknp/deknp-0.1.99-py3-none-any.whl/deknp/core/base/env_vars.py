import json
import base64
from dektools.file import read_text, write_file


class EnvVars:
    marker_begin = '<meta name="{key}"'
    marker_end = '\n'

    def __init__(self, path):
        self.path = path

    def update(self, key, value):
        text = read_text(self.path)
        marker_begin = self.marker_begin.format(key=key)
        marker_end = self.marker_end.format(key=key)
        index_begin = text.find(marker_begin)
        if index_begin == -1:
            raise ValueError(f"Can't find begin marker: {marker_begin}")
        index_end = text.find(marker_end, index_begin)
        if index_end == -1:
            raise ValueError(f"Can't find end marker: {marker_end}")
        if value:
            content = base64.b64encode(json.dumps(value).encode('utf-8')).decode('ascii')
        else:
            content = ""
        text_new = text[:index_begin] + f'{marker_begin} content="{content}">' + text[index_end:]
        write_file(self.path, s=text_new)
