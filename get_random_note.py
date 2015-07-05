#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import random

sys.path.insert(0, os.path.expanduser('~/.virtualenvs/kindle/src/enml-py'))
#sys.path.insert(0, os.path.expanduser('~/venv-kindle/src/enml-py'))
from enml import PlainTextOfENML, HTMLOfENML

from evernote.api.client import EvernoteClient
from evernote.api.client import NoteStore
import evernote.edam.type.ttypes as Types
import evernote.edam.limits.constants as LimitConstants
from evernote.edam.error.ttypes import EDAMSystemException
from evernote.edam.error.ttypes import EDAMUserException

client = note_store = None

def get_note(token, note_guid):
    global client, note_store
    
    if not client:
        client = EvernoteClient(token=token, sandbox=False)
        note_store = client.get_note_store()
        
    note = note_store.getNote(token,
                              note_guid,
                              True,
                              True,
                              False,
                              False)
                              #withContent=True,
                              #withResourcesData=False,
                              #withResourcesRecognition=False,
                              #withResourcesAlternateData=False)
    note.tagNames = note_store.getNoteTagNames(token, note_guid)
    return note

def get_random_note(token, notebook_guid=None, debug=False, verbose=False):
    global client, note_store
    
    if not client:
        client = EvernoteClient(token=token, sandbox=False)
        note_store = client.get_note_store()

    if not notebook_guid:
        notebooks = note_store.listNotebooks()
        notebook = random.choice(notebooks)
        notebook_guid = notebook.guid

    filter = NoteStore.NoteFilter()
    filter.notebookGuid = notebook_guid
    spec = NoteStore.NotesMetadataResultSpec()
    spec.includeCreated = True
    spec.includeTitle = True
    note_infos = note_store.findNotesMetadata(filter,
                    0,
                    LimitConstants.EDAM_USER_NOTES_MAX,
                    spec)
    #filter=filter,
    #offset=0,
    #maxNotes=LimitConstants.EDAM_USER_NOTES_MAX,
    #resultSpec=spec)
    
    #print note_infos.totalNotes, len(note_infos.notes)

    note_guid = random.choice(note_infos.notes).guid

    return get_note(token, note_guid)

def main():
    import sys
    from optparse import OptionParser

    usage="""
Usage: $ ./get_random_note.py EVERNOTE_TOKEN [ NOTEBOOK_GUID ]
  """[1:-3]
    
    parser = OptionParser(usage=usage)
    parser.add_option('--debug',
                      help='ne rien faire vraiment',
                      default=False,
                      action='store_true',
                      dest='debug')
    parser.add_option('--verbose',
                      help='verbose',
                      default=False,
                      action='store_true',
                      dest='verbose')
    parser.add_option('--log',
                      help='log errors to file',
                      default=False,
                      action='store_true',
                      dest='log')
                                                                    
    options, args = parser.parse_args()
    
    if len(args) == 0:
        print usage
        return -1

    if options.log:
        sys.stderr = codecs.open(os.path.join(options.output_dir, 'err.log'), 'w', 'utf-8')
        
    note = get_random_note(token=args[0],
                            notebook_guid=len(args) == 2 and args[1] or None,
                            debug=options.debug,
                            verbose=options.verbose)

    print note.title
    print note.content
    print PlainTextOfENML(note.content)    
        
if __name__ == '__main__':
    sys.exit(main())
