###############################################################################
#
# Copyright (c) 2017 Projekt01 GmbH.
# All Rights Reserved.
#
###############################################################################
"""Interfaces

$Id: interfaces.py 5752 2025-12-04 00:15:11Z roger.ineichen $
"""
from __future__ import absolute_import

import j01.form.interfaces


# editor text
class IEditorWidget(j01.form.interfaces.ITextAreaWidget):
    """Editor widget"""
