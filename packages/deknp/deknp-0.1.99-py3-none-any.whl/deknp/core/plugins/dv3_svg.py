import os
from .fix import svgpathtools  # noqa
from svgpathtools import svg2paths2
from .base import Plugin


def get_svg_data(filepath):
    paths, attributes, svg_attributes = svg2paths2(filepath)
    vb = [int(x) for x in svg_attributes['viewBox'].split(' ') if x]
    p_list = []
    result = {
        "w": vb[2],
        "h": vb[3],
        "p": p_list
    }
    for i in range(len(paths)):
        attr = attributes[i]
        d = attr.get('d')
        if not d:
            d = paths[i].d()
        fill = attr.get('fill')
        pd = dict(d=d)
        if fill and fill != 'currentColor':
            pd['c'] = fill
        p_list.append(pd)
    return result


class PluginDv3Svg(Plugin):
    path_generated_icons = 'dv3/icons'
    glob_icon_svg = '/**/dv3/icons/*.svg'

    def run(self):
        for filepath in self.list_glob_filepath(self.glob_icon_svg):
            name = os.path.splitext(os.path.basename(filepath))[0]
            self.save_text(
                self.get_dek_path_generated(self.path_generated_icons, f'{name}.svg'),
                self.load_text(filepath))
            self.save_json(
                self.get_dek_path_generated(self.path_generated_icons, f'{name}.json'),
                get_svg_data(filepath))
