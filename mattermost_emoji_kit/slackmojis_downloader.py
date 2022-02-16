#!/usr/bin/env python3

import click
import sys
import os
import re
import requests
from urllib.parse import urljoin
from multiprocessing.pool import ThreadPool
from bs4 import BeautifulSoup


def validate_filename(filename):
    """Ensure that a filename only contains alphanumeric characters."""

    m = re.search(r'^(?:[a-zA-Z-_0-9])+\.\w{1,3}$', filename)
    if m is not None:
        return True
    return False


def download_emoji(download):
    """Download a single emoji from slackmojis.com."""

    dest_filename, href = download

    if not os.path.exists(dest_filename):
        response = requests.get(href, stream=True)
        if response.status_code == 200:
            with open(dest_filename, 'wb') as fd:
                for chunk in response:
                    fd.write(chunk)

    return dest_filename


def validate_url(ctx, param, value):
    """Validate the URL parameter for this script."""

    if not value.startswith('https://slackmojis.com'):
        raise click.BadParameter("The URL needs to be a slackmojis.com page")
    return value


@click.command()
@click.option('--destdir', type=click.Path(file_okay=False, dir_okay=True, resolve_path=True),
              default='emojis', help='Destination directory for the downloaded emojis')
@click.argument('slackmojis_url', callback=validate_url)
def main(destdir, slackmojis_url):
    """Download emojis from slackmojis.com.

    Example:

    \b
    slackmojis-downloader https://slackmojis.com/categories/17-hangouts-blob-emojis
    """

    response = requests.get(slackmojis_url)
    if response.status_code != 200:
        print(f"Error fetching the slackmojis page; status code: {response.status_code}.")
        sys.exit(1)

    soup = BeautifulSoup(response.text, 'html.parser')

    ul = soup.find('ul', class_='emojis')
    assert(ul is not None)

    downloads = []
    base_url = 'https://slackmojis.com'
    if not os.path.exists(destdir):
        os.makedirs(destdir)

    for anchor in ul.find_all('a', class_='downloader'):
        filename = anchor['download']
        href = anchor['href']
        assert(validate_filename(filename))
        download_url = urljoin(base_url, href)
        download = (os.path.join(destdir, filename), download_url)
        downloads.append(download)

    results = ThreadPool(10).imap_unordered(download_emoji, downloads)
    with click.progressbar(length=len(downloads), label="Downloading emojis") as bar:
        for result in results:
            bar.update(1)


if __name__ == '__main__':
    main()
