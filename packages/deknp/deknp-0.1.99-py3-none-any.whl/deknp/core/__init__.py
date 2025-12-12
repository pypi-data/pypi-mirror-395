import os
import shutil
import json
import sys
from collections import OrderedDict, ChainMap
from copy import deepcopy
from itertools import chain
from dektools.file import write_file, read_text, remove_path
from dektools.serializer.yaml import yaml
from dektools.shell import Cli, shell_wrapper
from dektools.dict import dict_merge
from .plugins.base import PluginBase, Plugin
from .run import run_plugins, PluginDv3Yaml, PluginDv3EnvVars

project_dir = os.getcwd()
plugin_base = PluginBase(project_dir)

path_project_log = os.path.join(project_dir, 'deknp.log')
path_project_tree_log = os.path.join(project_dir, 'deknp.tree.log')

cli = Cli({
    "pnpm": "pnpm-lock.yaml",
    "yarn": "yarn.lock",
    "npm": "package.lock"
}, project_dir).cur


def filter_packages(data):
    def pop(d):
        for k in list(d):
            if os.path.exists(os.path.join(plugin_base.node_modules_dir, k)):
                d.pop(k)

    data = deepcopy(data)
    pop(data.get('dependencies') or {})
    pop(data.get('devDependencies') or {})
    return data


def merge_package(a, b):
    result = deepcopy(a)
    result.update([
        (
            'dependencies',
            OrderedDict(ChainMap(a.get('dependencies', OrderedDict()), b.get('dependencies', OrderedDict())))
        ),
        (
            'devDependencies',
            OrderedDict(ChainMap(a.get('devDependencies', OrderedDict()), b.get('devDependencies', OrderedDict())))
        ),
    ])
    return result


def execute_build():
    if cli == 'yarn':
        shell_wrapper(f'{cli} build')
    else:
        shell_wrapper(f'{cli} run build')


def execute_install():
    def raw_install():
        if cli == 'yarn':
            shell_wrapper(cli)
        else:
            shell_wrapper(f'{cli} install')

    def walk(dir_dek_list):
        dir_dek_list = [x for x in dir_dek_list if x[0] not in handed_set]
        if not dir_dek_list:
            return
        data_total = plugin_base.load_package_standard()
        for dir_dek, is_dev in dir_dek_list:
            handed_set.add(dir_dek)
            fp = plugin_base.get_package_dek_json_path(dir_dek)
            if fp:
                data_dek = plugin_base.load_json(fp)
                dict_merge(data_dek, Plugin.data_dek_default(data_dek))
                if dir_dek == project_dir:
                    data_dek_run = data_dek.get(Plugin.dek_key_root, {}).get(Plugin.dek_key_current_project) or {}
                    if data_dek_run:
                        dict_merge(data_dek, data_dek_run)

                summary[data_dek['name']] = dir_dek, data_dek, is_dev

                data_total = merge_package(plugin_base.load_package_standard(deepcopy(data_total)), data_total)
                data_total = merge_package(data_total, data_dek)

        plugin_base.save_json(plugin_base.package_standard_filepath, data_total)
        raw_install()

        walk(chain(
            (
                (os.path.join(plugin_base.node_modules_dir, k), False)
                for k in reversed(data_total.get('dependencies', {}))),
            (
                (os.path.join(plugin_base.node_modules_dir, k), True)
                for k in reversed(data_total.get('devDependencies', {}))),
        ))

    weight_cache = {}

    def get_weight(name):
        if name in weight_cache:
            return weight_cache[name]
        result = 1
        for target in chain(summary[name][1].get('dependencies', {}), summary[name][1].get('devDependencies', {})):
            if target in summary:
                result += get_weight(target)
        weight_cache[name] = result
        return result

    if not plugin_base.is_dek_package:
        raw_install()
        return

    handed_set = set()
    if plugin_base.is_dek_package:
        dd = plugin_base.load_json(plugin_base.package_dek_filepath)
        dd.update([
            ('dependencies', {}),
            ('devDependencies', {}),
        ])
        plugin_base.save_json(plugin_base.package_standard_filepath, dd)

    summary = {}
    walk([(project_dir, False)])
    sorted_summary = sorted(((name, *x) for name, x in summary.items()), key=lambda x: get_weight(x[0]))

    dek_dir_list = [x[1] for x in sorted_summary]
    dek_dev_dir_list = [x[1] for x in sorted_summary if x[3]]
    data_dek_list = [x[2] for x in sorted_summary]

    # pnpm may install multi wrong version of packages, so clear it and install by the lock file
    remove_path(plugin_base.node_modules_dir)
    raw_install()

    dek_info_list = [x.get(Plugin.dek_key_root) or OrderedDict() for x in data_dek_list]
    write_file(path_project_tree_log, yaml.dumps(data_dek_list))
    write_file(
        path_project_log,
        json.dumps([dek_info_list, dek_dir_list, dek_dev_dir_list], indent=2, ensure_ascii=False))
    run_plugins(project_dir, dek_info_list, dek_dir_list, dek_dev_dir_list)


def execute_package_sure(force=False):
    if plugin_base.is_dek_package and (force or not os.path.exists(plugin_base.package_standard_filepath)):
        data_dek = plugin_base.load_json(plugin_base.package_dek_filepath)
        data_dek.pop(Plugin.dek_key_root, None)
        plugin_base.save_json(plugin_base.package_standard_filepath, data_dek)


def execute_server(begin=False):
    dir_servers = os.path.join(project_dir, 'dek', 'dv3', 'servers')
    project_name = plugin_base.get_package_json(
        project_dir
    )['name'].split('/')[-1].replace('-', '').replace('_', '').lower()
    if os.path.isdir(dir_servers) and os.listdir(dir_servers):
        dir_work = os.path.join(project_dir, 'server')
        if not os.path.isdir(dir_work):
            os.makedirs(dir_work)
        dir_material = os.path.join(dir_work, '.material')
        if not os.path.exists(dir_material):
            shell_wrapper(f'djcreator wrapper clean --project={project_name}')
            shell_wrapper(f'djcreator project {project_name} {dir_work}')
        dir_project = os.path.join(dir_material, f'{project_name}.yaml')
        if os.path.isdir(dir_project):
            shutil.rmtree(dir_project)
        shutil.copytree(dir_servers, dir_project)
        shell_wrapper(f'dekshell rf .shell.initshell.pysh', chdir=dir_work)
        if begin:
            shell_wrapper(f'dekshell rf .shell.generate.{project_name}.pysh', chdir=dir_material)
            shell_wrapper(f'deknp install', chdir=project_dir)


def run_plugin_dv3_yaml():
    run_plugins(project_dir, *json.loads(read_text(path_project_log)), [PluginDv3Yaml])


def run_plugin_dv3_env_vars():
    run_plugins(project_dir, *json.loads(read_text(path_project_log)), [PluginDv3EnvVars])


def get_pnpm_cache_dir():  # https://github.com/pnpm/pnpm/blob/v8.10.5/config/config/src/dirs.ts
    if os.getenv('XDG_CACHE_HOME'):
        return os.path.join(os.getenv('XDG_CACHE_HOME'), 'pnpm')
    if sys.platform == 'darwin':
        return os.path.join(os.path.expanduser('~'), 'Library/Caches/pnpm')
    if sys.platform != 'win32':
        return os.path.join(os.path.expanduser('~'), '.cache/pnpm')
    if os.getenv('LOCALAPPDATA'):
        return os.path.join(os.getenv('LOCALAPPDATA'), 'pnpm-cache')
    return os.path.join(os.path.expanduser('~'), '.pnpm-cache')


def clear_pkg_cache():
    pkg_info = plugin_base.get_package_json(project_dir)
    name, version = pkg_info['name'], pkg_info['version']
    path_meta = os.path.join(get_pnpm_cache_dir(), 'metadata')
    if os.path.isdir(path_meta):
        for host in os.listdir(path_meta):
            path_pkg = os.path.join(path_meta, host, name + '.json')
            if os.path.isfile(path_pkg):
                data = json.loads(read_text(path_pkg))
                versions = data.get('versions') or {}
                exists = versions.pop(version, None)
                if exists is not None:
                    if versions:
                        write_file(path_pkg, json.dumps(data))
                    else:
                        remove_path(path_pkg)
