# -*- coding: utf-8 -*-
"""
This extension is search Japanese-English Dictionary File (tab separated).

Synopsis: je <word>
"""
import os
import subprocess as sp
from shutil import which
from albertv0 import iconLookup, Item, ClipAction


__iid__ = "PythonInterface/v0.1"
__prettyname__ = "J-E Dictionary"
__version__ = "1.0"
__trigger__ = "je "
__author__ = "Tetsutaro Maruyama"
__dependencies__ = ["ag"]
__dictionary_file__ = "/usr/local/share/dict/je-jmdict.txt"
__max_candidate__ = 5

if which("ag") is None:
    raise Exception("'ag' is not in $PATH.")
if not os.path.exists(__dictionary_file__):
    raise Exception("dictionary_file is not exists")

icon = iconLookup('accessories-dictionary')


def _compose_ag_command(query):
    if query.startswith('"') and query.endswith('"'):
        kwd = query[1:-1]
        pad = "\t"
    elif query.startswith("'") and query.endswith("'"):
        kwd = query[1:-1]
        pad = "\t"
    else:
        kwd = query
        pad = ''
    return ' '.join([
        'ag',
        '-S',
        '--nocolor',
        '--nonumber',
        '-m',
        '%d' % __max_candidate__,
        '"^%s%s"' % (kwd, pad),
        __dictionary_file__
    ])


def _invoke_ag(args, raws):
    items = list()
    texts = sp.run(
        _compose_ag_command(args),
        shell=True,
        check=False,
        stdout=sp.PIPE,
        stderr=sp.PIPE,
        universal_newlines=True
    ).stdout.splitlines()
    if len(texts) == 0:
        item = Item(
            id='%s no hit' % __prettyname__,
            icon=icon,
            completion=raws,
            subtext='No Translation Candidate found for "%s"' % args
        )
        items.append(item)
    elif len(texts) == 1:
        key, values = texts[0].split("\t")[:2]
        for i, value in enumerate(values.split(',')):
            text = key + "\t" + value.strip()
            item = Item(
                id='%s hit %d' % (__prettyname__, i),
                icon=icon,
                completion=raws,
                text=text,
                subtext='Translation Candidate for "%s"' % args,
                actions=[
                    ClipAction(
                        "Copy translated words to Clipboard",
                        value.strip()
                    )
                ]
            )
            items.append(item)
    else:
        for i, text in enumerate(texts):
            if i >= __max_candidate__:
                break
            item = Item(
                id='%s hit %d' % (__prettyname__, i),
                icon=icon,
                completion=raws,
                text=text,
                subtext='Translation Candidate for "%s"' % args,
                actions=[
                    ClipAction(
                        "Copy translated words to Clipboard",
                        text.split("\t")[1]
                    )
                ]
            )
            items.append(item)
    return items


def handleQuery(query):
    if query.isTriggered:
        args = query.string.strip()
        raws = query.rawString
        if len(args) > 0:
            try:
                return _invoke_ag(args, raws)
            except sp.CalledProcessError as e:
                return Item(
                    id='%s error' % __prettyname__,
                    icon=icon,
                    completion=raws,
                    text=str(e),
                    subtext='Error occurs in Translation for "%s"' % args
                )
        else:
            return Item(
                id='%s no hit' % __prettyname__,
                icon=icon,
                completion=raws,
                text="Empty input",
                subtext='Enter a Japanese word to translate into English'
            )
