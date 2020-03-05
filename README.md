# Mattermost emoji kit

A couple of simple scripts to download emojis from [slackmojis.com](https://slackmojis.com) and
import them into a [Mattermost](https://mattermost.com/) instance.

Tested on: Mattermost 5.20.x.

## Requirements

It's easier to execute these scripts with [poetry](https://github.com/python-poetry/poetry).

## Usage

### Downloader

    poetry run ./slackmojis-downloader.py <slackmojis url>

Example:

    poetry run ./slackmojis-downloader --destdir blobs-emojis https://slackmojis.com/categories/17-hangouts-blob-emojis

### Importer

Create a configuration file, `importer.cfg`:

    url = my-mattermost-instance.example.com
    login_id = my-login-id
    password = my-precious-password

**NOTE** I didn't find a way to import emojis into Mattermost by using an access token; you'll have
to use your Mattermost login and password.

Then launch `importer.py` passing a directory containing emoji files; the emoji file names should be
in the following format: `blob_thinking_down.png`, so that the custom emoji will be created as
`blob-thinking-down` and used by writing `:blob-thinking-down:`.

    poetry run ./importer.py blobs-emojis
