import os
from .base import PluginUniapp
from dektools.dict import assign


# def get_easy_com_dict(prefix, names):
#     if not names:
#         return {}
#     name = names[0]
#     if len(names) == 1:
#         return {name: f'{prefix}/{name}/{name}.vue'}
#     cursor = 0
#     while True:
#         cursor_char = name[cursor:cursor + 1]
#         for x in names:
#             xx = x[cursor:cursor + 1]
#             if xx != cursor_char or '' in [xx, cursor_char]:
#                 start = name[:cursor]
#                 if not start:
#                     raise Exception(f'empty error for: {prefix} {names}')
#                 return {f'^{start}(.*)': f'{prefix}/{start}$1/{start}$1.vue'}
#         cursor += 1

def get_easy_com_dict(prefix, names):
    return {f'^{name}$': f'{prefix}/{name}/{name}.vue' for name in names}


class PluginUniappVars(PluginUniapp):
    def variables__easy_com(self):
        def pkg_args(fn, base):
            return [
                fn[len(base) + 1:].replace('\\', '/'),
                [f for f in os.listdir(fn) if os.path.isdir(os.path.join(fn, f))]
            ]

        variables = {}
        for root, dirs, _ in os.walk(self.node_modules_dir):
            for name in dirs:
                rn = os.path.join(root, name)
                if name == 'components' and os.path.basename(os.path.dirname(os.path.dirname(rn))) == 'uni_modules':
                    variables.update(get_easy_com_dict(*pkg_args(rn, self.node_modules_dir)))

        # dir_components = os.path.join(self.project_dir, 'components')
        # if os.path.exists(dir_components):
        #     variables.update(get_easy_com_dict(*pkg_args(dir_components, self.project_dir)))

        return {
            'uniapp': {
                'easycom': variables or '{}'
            }
        }

    def run(self):
        self.share_data['variables'] = assign(
            self.share_data.get('variables') or {},
            # self.variables__easy_com()
        )
