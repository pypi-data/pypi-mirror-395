import typer
from typing_extensions import Annotated
from dektools.shell import shell_wrapper
from dektools.web.url import Url
from dektools.output import print_data_or_value
from ..core import execute_install, execute_build, execute_package_sure, execute_server, run_plugin_dv3_yaml, \
    clear_pkg_cache, plugin_base
from ..gen.tmpl import ShellGenerator

app = typer.Typer(add_completion=False)


@app.command()
def install():
    execute_install()


@app.command()
def build():
    execute_build()


@app.command()
def sure(force: Annotated[bool, typer.Option("--force/--no-force")] = False):
    execute_package_sure(force)


@app.command()
def prepare_for_publish():
    if plugin_base.is_dek_package:
        execute_package_sure(True)
    else:
        execute_install()
        execute_build()


@app.command()
def server():
    execute_server(False)


@app.command()
def serverfull():
    execute_server(True)


@app.command()
def clearcache():
    clear_pkg_cache()


@app.command()
def yaml():
    run_plugin_dv3_yaml()


@app.command()
def shell(path: Annotated[str, typer.Argument()] = "."):
    ShellGenerator(path, None).render()


@app.command()
def login(url):
    url = Url.new(url)
    uncertified = url.uncertified
    shell_wrapper(f"npm config set {url.username}:registry {uncertified.value}")
    shell_wrapper(f"""npm config set -- "{uncertified.replace(scheme='').value}:_authToken" "{url.password}" """)


@app.command()
def logout(url):
    url = Url.new(url)
    shell_wrapper(f"""npm config delete "{url.username}:registry" """)
    shell_wrapper(f"""npm config delete "{url.uncertified.replace(scheme='').value}:_authToken" """)


@app.command()
def meta(path, expression: Annotated[str, typer.Argument()] = ""):
    print_data_or_value(plugin_base.get_package_json(path), expression)
