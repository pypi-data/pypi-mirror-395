#!/usr/bin/env python3

# setup logging
import logging, os
log_level = os.environ.get('LOGLEVEL', 'WARNING').upper()

logging.basicConfig(
    level=getattr(logging, log_level, 'WARNING'),
    format="%(asctime)s - %(name)s - %(levelname)s: %(filename)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger('markpub-themes')

import argparse
from pathlib import Path
import shutil
from simple_term_menu import TerminalMenu
import sys
import yaml
from . import get_theme_path, list_themes, __version__

# install a theme for custom use
def select_markpub_theme():
    themes = sorted(list_themes())
    """Interactive menu with arrow key navigation."""
    terminal_menu = TerminalMenu(
        themes,
        title="Select a theme:",
        menu_cursor="> ",
        menu_cursor_style=("fg_cyan", "bold"),
        menu_highlight_style=("fg_cyan", "bold")
    )
    choice_idx = terminal_menu.show()
    return themes[choice_idx] if choice_idx is not None else None

def clone_theme(theme_name, destination):
    """Clone a theme to a destination directory."""
    logging.info(f"Installing theme {theme_name} in directory {destination}")

    # Check if directory is initialized
#    markpub_dir = Path(directory).resolve() / ".markpub"
#    if not markpub_dir.exists():
#        logger.error(f"Directory {directory} is not initialized. Run 'markpub init' first.")
#        return

    try:
        source = Path(get_theme_path(theme_name))
        logging.debug(f"source theme dir: {source}")
        dest = Path(destination).expanduser().resolve()

        if dest.exists():
            logger.error(f"Error: Destination '{dest}' already exists", file=sys.stderr)
            return 1

        shutil.copytree(
            source,
            dest,
            ignore=shutil.ignore_patterns('__pycache__','__init__.py'),
            dirs_exist_ok=True)
        logger.info(f"Theme '{theme_name}' local install successful.")
        logger.info(f"Theme '{theme_name}' cloned to {dest}")
        return 0
    except Exception as e:
        logger.error(f"Error cloning theme: {e}", file=sys.stderr)
        return 1

def activate_theme(theme_name, config_file=None):
    """Activate a theme (sets it as the active theme)."""
    try:
        # Verify theme_path exists
        get_theme_path(theme_name)

        if Path(config_file).exists():
            config_path = Path(config_file).expanduser().resolve()
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_file, encoding='utf-8') as f:
                config_doc = yaml.safe_load(f)
                config_doc['theme'] = theme_name
            with open(config_file,'w', encoding='utf-8') as f:
                yaml.safe_dump(config_doc, f, default_flow_style=False, sort_keys=False)
            print(f"Theme '{theme_name}' activated in {config_path}")
            return 0
        else:
            logger.error(f"{config_file} not found; activation canceled.")
            return 1
    except Exception as e:
        print(f"Error activating theme: {e}", file=sys.stderr)
        return 1

def main():
    """Main CLI entry point."""
    # expected destination and config values
    markpub_dir = '.'
    themes_dir = f"{markpub_dir}/themes"
    config_file = f"{markpub_dir}/markpub.yaml"

    parser = argparse.ArgumentParser(
        prog='markpub-themes',
        description='Manage markpub themes'
    )
    parser.add_argument('--version', '-V', action='version', version=f'%(prog)s {__version__}')
    subparsers = parser.add_subparsers(required=True)
    # subparser for "list" command
    list_parser = subparsers.add_parser('list', help='List available themes')
    list_parser.set_defaults(cmd='list')
    # subparser for "clone" command
    clone_parser = subparsers.add_parser('clone', help='Install a theme in ./markpub/themes directory')
    clone_parser.set_defaults(cmd='clone')
    # subparser for "activate" command
    activate_parser = subparsers.add_parser('activate', help='Specify theme to use in config file')
    activate_parser.set_defaults(cmd='activate')

    args = parser.parse_args()
    logger.info(args)

    match args.cmd:
        case 'list':
            themes = sorted(list_themes())
            print("Available themes:")
            for theme in themes:
                print(f"  - {theme}")
        case 'clone':
        # clone installs selected theme in local directory and activates
            theme_selected = select_markpub_theme()
            if theme_selected is None:
                print("Selection canceled.")
                return 1
            clone_theme(theme_selected, f"{themes_dir}/{theme_selected}")
            return activate_theme(theme_selected, config_file)
        case 'activate':
        # activate: updates configuration file "theme" key
            theme_selected = select_markpub_theme()
            if theme_selected is None:
                print("Selection canceled.")
                return 1
            return activate_theme(theme_selected, config_file)
        case _:
            parser.print_help()
            return

if __name__ == '__main__':
    sys.exit(main())
