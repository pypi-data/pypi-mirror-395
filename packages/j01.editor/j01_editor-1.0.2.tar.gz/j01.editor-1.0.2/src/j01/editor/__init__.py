###############################################################################
#
# Copyright (c) 2014 Projekt01 GmbH.
# All Rights Reserved.
#
###############################################################################
"""Widgt mixin classes shared in form and jsform

$Id: __init__.py 5752 2025-12-04 00:15:11Z roger.ineichen $
"""
from __future__ import absolute_import

from xml.sax import saxutils

import six


def escape(value):
    """Escape the given value.

    Always return unicode, never bytes. Converts bytes to unicode using UTF-8.
    """
    if isinstance(value, bytes):
        # Decode using UTF-8, since J01/Zope environment is UTF-8 everywhere.
        value = value.decode('utf-8')
    if isinstance(value, six.string_types):
        # Now value is guaranteed unicode
        return saxutils.escape(value)
    return value
