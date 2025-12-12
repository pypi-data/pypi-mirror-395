"""
Generic application runner for imery
"""

import click
import sys
from pathlib import Path
from imgui_bundle import imgui, implot, immapp
from imery.lang import Lang
from imery.frontend.widget_factory import WidgetFactory
from imery.backend.kernel import Kernel
from imery.backend.data_tree import DataTree
from imery.dispatcher import Dispatcher
from imery.types import DataPath
from imery.result import Result

import time

init_time = time.time()

# Global state
main_widget = None
factory = None
dispatcher = None
kernel = None
data_tree = None


def main_loop():
    """Main rendering loop"""
    global main_widget

    if False and time.time() - init_time > 5:
        sys.exit(1)

    if main_widget:
        try:
            res = main_widget.render()
        except Exception as e:
            print("main widget render failed", e)
            sys.exit(1)
        if not res:
            imgui.text_colored(imgui.ImVec4(1.0, 0.0, 0.0, 1.0), f"Render Error: {res}")


@click.command()
@click.option('--imery-path', '-p',
              envvar='IMERY_LAYOUTS_PATH',
              type=str,
              help='Colon-separated list of directories to search for layout modules')
@click.option('--main', '-m',
              required=True,
              type=str,
              help='Name of the main module to load')

def main(imery_path, main):
    """Imery application runner"""
    global main_widget, factory, dispatcher, kernel, data_tree

    # Parse search paths
    if imery_path:
        search_paths = imery_path.split(':')
    else:
        search_paths = ['.']

    # Initialize ImPlot context
    if not implot.get_current_context():
        implot.create_context()

    # Create Lang and load modules
    lang_res = Lang.create(search_paths=search_paths)
    if not lang_res:
        click.echo(f"Error creating Lang: {lang_res}", err=True)
        return 1

    lang = lang_res.unwrapped

    load_res = lang.load_main_module(main)
    if not load_res:
        click.echo(f"Error loading main module '{main}': {load_res}", err=True)
        return 1

    # Create Dispatcher
    dispatcher_res = Dispatcher.create()
    if not dispatcher_res:
        click.echo(f"Error creating Dispatcher: {dispatcher_res}", err=True)
        return 1
    dispatcher = dispatcher_res.unwrapped

    # Create Kernel
    kernel_res = Kernel.create(dispatcher=dispatcher)
    if not kernel_res:
        click.echo(f"Error creating Kernel: {kernel_res}", err=True)
        return 1
    kernel = kernel_res.unwrapped

    # Create WidgetFactory
    factory_res = WidgetFactory.create(widget_definitions=lang.widget_definitions)
    if not factory_res:
        click.echo(f"Error creating WidgetFactory: {factory_res}", err=True)
        return 1
    factory = factory_res.unwrapped

    # Get app config
    app_config = lang.app_config
    if not app_config:
        click.echo("Error: No app configuration found", err=True)
        return 1

    widget_name = app_config.get('widget')
    data_name = app_config.get('data')

    if not widget_name:
        click.echo("Error: app.widget not specified", err=True)
        return 1

    if not data_name:
        click.echo("Error: app.data not specified", err=True)
        return 1

    # Get data definition
    data_definitions = lang.data_definitions
    if data_name not in data_definitions:
        click.echo(f"Error: data '{data_name}' not found", err=True)
        return 1

    data_def = data_definitions[data_name]

    # Substitute builtins in children
    if 'children' in data_def:
        children = data_def['children']
        for key, value in children.items():
            if isinstance(value, str) and value == '$kernel':
                children[key] = kernel

    # Create DataTree
    data_tree = DataTree(data_def)

    # Create main widget
    widget_res = factory.create_widget(widget_name, data_tree, DataPath("/"))
    if not widget_res:
        click.echo(f"Error creating widget '{widget_name}': {widget_res}", err=True)
        return 1

    main_widget = widget_res.unwrapped

    # Run application
    immapp.run(
        gui_function=main_loop,
        window_title="Imery App",
        window_size=(1200, 800),
        fps_idle=0
    )

    return 0


if __name__ == '__main__':
    main()
