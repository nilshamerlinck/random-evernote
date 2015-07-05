#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs, locale, os, sys

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
#sys.stdout = codecs.getwriter('utf-8')(sys.stderr)

os.chdir(os.path.realpath(os.path.dirname(__file__)))

from datetime import datetime
import mimetypes

import pyzmail

from get_random_note import get_note, get_random_note, PlainTextOfENML, HTMLOfENML

def send_mail_from_note(note, smtp_host, smtp_port, smtp_login, smtp_password, smtp_mode, sender, to, debug=False, verbose=False):

    counter = 1
    resources = {}
    images = []
    if note.resources:
        for r in note.resources:
            k = r.data.bodyHash.encode('hex')
            fn = '%.2i.%s' % (counter, mimetypes.guess_extension(r.mime)[1:])
            resources[k] = 'cid:' + fn
            a, b = r.mime.split('/')
            images.append((r.data.body, a, b, fn, None))
            counter += 1

    text_content = PlainTextOfENML(note.content)
    html_content = HTMLOfENML(note.content, resources)
    title = note.title
    #title = 'La note de %sh' % datetime.now().strftime('%H')

    try:
        payload, mail_from, rcpt_to, msg_id = pyzmail.compose_mail(
            sender=sender,
            recipients=to,
            subject=title,
            default_charset='utf-8',
            text=(text_content, 'utf-8'),
            html=(html_content, 'utf-8'),
            attachments=None,
            embeddeds=images,)
            #headers=(('Reply-To', '%s@catch.niouls.net' % str(note.guid)), ))

        ret = pyzmail.send_mail(payload=payload,
                                mail_from=mail_from,
                                rcpt_to=rcpt_to,
                                smtp_host=smtp_host,
                                smtp_port=smtp_port,
                                smtp_mode=smtp_mode,
                                smtp_login=smtp_login,
                                smtp_password=smtp_password)
            
        if isinstance(ret, dict):
            if ret:
                if verbose:
                    print >> sys.stderr, 'failed recipients:', ', '.join(ret.keys())
            else:
                if verbose:
                    print >> sys.stderr, 'success'
        else:
            if verbose:
                print >> sys.stderr, 'error:', ret

    except Exception, e:
        raise
        return 1

    return 0

def main():
    import sys
    from optparse import OptionParser

    usage="""
%prog [ options ]

Exemples:
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

    # inspired by pyzsendmail
    parser.add_option("-f",
                      "--from",
                      dest="sender",
                      help="sender address",
                      metavar="sender",
                      type='string')
    parser.add_option("-t",
                      "--to",
                      action="append",
                      dest="to",
                      help="add one recipient address",
                      metavar="recipient",
                      type='string',
                      default=[])
    parser.add_option("-H",
                      "--smtp-host",
                      dest="smtp_host",
                      help="SMTP host relay",
                      metavar="name_or_ip",
                      default='localhost')
    parser.add_option("-p",
                      "--smtp-port",
                      dest="smtp_port",
                      help="SMTP port (default=25)",
                      metavar="port",
                      type='int',
                      default='25')
    parser.add_option("-L",
                      "--smtp-login",
                      dest="smtp_login",
                      help="SMTP login (if authentication is required)",
                      metavar="login",
                      type='string')
    parser.add_option("-P",
                      "--smtp-password",
                      dest="smtp_password",
                      help="SMTP password (if authentication is required)",
                      metavar="password",
                      type='string')
    parser.add_option("-m",
                      "--smtp-mode",
                      dest="smtp_mode",
                      help="smtp mode in 'normal', 'ssl', 'tls'. (default='normal')",
                      metavar="mode",
                      type='choice',
                      default='normal',
                      choices=('normal', 'ssl', 'tls'))

    options, args = parser.parse_args()

    if len(args) == 0:
        print usage
        return -1

    token = args[0]
    
    note = get_random_note(token)
    if options.verbose:
        print >> sys.stderr, note.content
    
    return send_mail_from_note(note,
                               smtp_host=options.smtp_host,
                               smtp_port=options.smtp_port,
                               smtp_login=options.smtp_login,
                               smtp_password=options.smtp_password,
                               smtp_mode=options.smtp_mode,
                               sender=options.sender,
                               to=options.to,
                               debug=options.debug,
                               verbose=options.verbose)

if __name__ == '__main__':
    sys.exit(main())
