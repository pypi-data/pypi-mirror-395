###############################################################################
#
# Copyright (c) 2017 Projekt01 GmbH.
# All Rights Reserved.
#
###############################################################################
"""
$Id: util.py 5222 2025-04-09 08:48:29Z rodrigo.ristow $
"""
from __future__ import absolute_import
from __future__ import unicode_literals

import bleach

ALLOWED_TAGS = [
    'a',
    'abbr',
    'acronym',
    'b',
    'br',
    'blockquote',
    'code',
    'div',
    'em',
    'i',
    'li',
    'ol',
    'p',
    'span',
    'strong',
    'ul',
]

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'target', 'id', 'class', 'name'],
    'abbr': ['id', 'class', 'title'],
    'acronym': ['id', 'class', 'title'],
    'b': ['id', 'class', 'title'],
    'br': [],
    'blockquote': ['id', 'class', 'title'],
    'code': ['id', 'class', 'title'],
    'div': ['id', 'class', 'title'],
    'em': ['id', 'class', 'title'],
    'i': ['id', 'class', 'title'],
    'li': ['id', 'class', 'title'],
    'ol': ['id', 'class', 'title'],
    'p': ['id', 'class', 'title'],
    'span': ['id', 'class', 'title'],
    'strong': ['id', 'class', 'title'],
    'ul': ['id', 'class', 'title'],
}

ALLOWED_STYLES = []


def fixBR(html):
    # note, IE 8 could return upper case tags
    return html.replace('<br>', '<br />').replace('<BR>', '<br />')


def boldAsStrong(html):
    # note, IE 8 could return upper case tags
    html = html.replace('<b>', '<strong>')
    html = html.replace('<B>', '<strong>')
    html = html.replace('</b>', '</strong>')
    html = html.replace('</B>', '</strong>')
    return html


def clean(text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES,
          styles=ALLOWED_STYLES, strip=True, strip_comments=True,
          skipFixBR=False, skipBoldAsStrong=False):
    html = bleach.clean(text, tags=tags, attributes=attributes, styles=styles,
        strip=strip, strip_comments=strip_comments)
    if not skipFixBR:
        html = fixBR(html)
    if not skipBoldAsStrong:
        html = boldAsStrong(html)
    return html


def simpleHTML(html):
    """Cleanup with default whitelist data"""
    return boldAsStrong(clean(html))