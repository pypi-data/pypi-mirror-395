from .plugins import PluginUniappVars, PluginPackageJson, PluginBabelConfig, PluginVueConfig, PluginOverrideRoot, \
    PluginDv3, PluginImages, PluginViteConfig, PluginDv3Svg, PluginDv3Yaml, PluginPackages, PluginRequests, \
    PluginDv3Server, PluginDv3EnvVars, PluginReplace

g_plugin_list = [
    PluginUniappVars,
    PluginOverrideRoot,
    PluginPackageJson,
    PluginBabelConfig,
    PluginVueConfig,
    PluginViteConfig,
    PluginImages,
    PluginDv3,
    PluginDv3Svg,
    PluginDv3Yaml,

    PluginPackages,
    PluginDv3Server,
    PluginRequests,
    PluginDv3EnvVars,
    PluginReplace
]


def run_plugins(project_dir, dek_info_list, dek_dir_list, dek_dev_dir_list, plugin_list=None):
    share_data = {}
    for plugin_cls in plugin_list or g_plugin_list:
        plugin = plugin_cls(project_dir, dek_info_list, dek_dir_list, dek_dev_dir_list, share_data)
        plugin.run()
