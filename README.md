# Mattermost emoji kit

A couple of simple scripts to download emojis from [slackmojis.com](https://slackmojis.com) and
import them into a [Mattermost](https://mattermost.com/) instance.

Tested on: Mattermost 6.x

## Setup

```
$ python3 -m venv venv
$ . ./venv/bin/activate
$ pip3 install .
```

## Usage

### Downloader

    $ slackmojis-downloader <slackmojis url>

Example:

    $ slackmojis-downloader --destdir blobs-emojis https://slackmojis.com/categories/17-hangouts-blob-emojis

### Importer

Create a configuration file, `importer.cfg`:

    url = my-mattermost-instance.example.com (no HTTP or HTTPS prefix is needed)
    login_id = my-login-id (e.g. user@example.com)
    password = my-precious-password

**NOTE** I didn't find a way to import emojis into Mattermost by using an access token; you'll have
to use your Mattermost login and password.

Then launch `mattermost-emoji-importer` passing a directory containing emoji files; the emoji file names should be
in the following format: `blob_thinking_down.png`, so that the custom emoji will be created as
`blob-thinking-down` and used by writing `:blob-thinking-down:`.

    $ git clone https://github.com/seanprashad/slackmoji.gi
    $ mattermost-emoji-importer slackmoji/emoji/blob/
