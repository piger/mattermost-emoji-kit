#!/usr/bin/env python3

import os
import sys
import click
from mattermostdriver import Driver


def read_config(fd):
    """Read a simple "key = value" config file."""

    config = {}

    for line in fd:
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip()
        config[key] = value
    return config


@click.command()
@click.option('--config', 'config_fd', default='importer.cfg', type=click.File())
@click.option('--debug', is_flag=True, help="Enable debug mode")
@click.argument('emojis_dir', type=click.Path(file_okay=False, dir_okay=True, resolve_path=True),
                required=True)
def main(config_fd, debug, emojis_dir):
    """Import emojis into a Mattermost instance."""

    config = read_config(config_fd)
    if 'url' not in config or 'login_id' not in config or 'password' not in config:
        print("Missing values in config; you need to specify 'url', 'login_id', 'password'.")
        sys.exit(1)

    filenames = []
    for root, _, files in os.walk(emojis_dir):
        filenames.extend(os.path.join(root, name) for name in files)

    if not filenames:
        print(f"No emojis were found in {emojis_dir}.")
        sys.exit(1)

    driver = Driver({
        'url': config['url'],
        'login_id': config['login_id'],
        'password': config['password'],
        'port': 443,
        'debug': debug,
    })

    _ = driver.login()

    for filename in filenames:
        emoji_name = os.path.splitext(
            os.path.basename(filename))[0]
        if not emoji_name:
            print(f"Cannot identify the name for {filename}.")
            sys.exit(1)

        emoji_name = emoji_name.replace('_', '-')

        print(f"importing: {emoji_name}")
        try:
            driver.emoji.create_custom_emoji(emoji_name, { 'image': (filename, open(filename, 'rb')) })
        except Exception as ex:
            print(f"got error: {ex}")


if __name__ == '__main__':
    main()
