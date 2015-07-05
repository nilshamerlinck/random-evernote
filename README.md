# Send a random Evernote by email

This script will randomly choose one note from the given Notebook and send it by email.

## Prerequisites

The script uses the [official Evernote SDK](https://github.com/evernote/evernote-sdk-python) to retrieve the random note, my fork of [enml-py](https://github.com/nilshamerlinck/enml-py) to convert ENML to HTML and [pyzmail](http://www.magiksys.net/pyzmail) to send the email.

	$ mkvirtualenv random-evernote
	$ pip install evernote pyzmail
	$ cd ~/.virtualenvs/kindle/src
	$ git clone https://github.com/nilshamerlinck/enml-py

You need to get a developer token from https://www.evernote.com/api/DeveloperToken.action

You also need to get the GUID of the target notebook. The easiest way to do so is to extract it from its URL in the Evernote webapp : `https://www.evernote.com/Home.action#b=f9cb26c5-1a01-4y53-a05a-3231e1efe9f0&st=p` for example.

## Usage

	$ ./get_random_note.py EVERNOTE_TOKEN NOTEBOOK_GUID

