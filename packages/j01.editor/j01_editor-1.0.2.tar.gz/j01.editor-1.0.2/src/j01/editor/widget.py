###############################################################################
#
# Copyright (c) 2014 Projekt01 GmbH.
# All Rights Reserved.
#
###############################################################################
"""Widgt mixin classes shared in form and jsform

$Id: widget.py 5752 2025-12-04 00:15:11Z roger.ineichen $
"""
from __future__ import absolute_import

import six

import json

import zope.interface

import z3c.form.interfaces
import z3c.form.widget

import j01.form.widget.textarea
import j01.editor.util
from j01.editor import interfaces


################################################################################
#
# ensure unicode used for javascript

def ensure_unicode(value):
    """Return unicode value on Python 2 and Python 3.
    Converts bytes to unicode using UTF-8.
    Any non-string is converted using str() or unicode().
    """
    if value is None:
        return u""

    # Already unicode on both Python 2 and 3
    if isinstance(value, six.text_type):
        return value

    # Handle bytes on Python 2/3
    if isinstance(value, six.binary_type):
        try:
            return value.decode('utf-8')
        except Exception:
            # Fallback: decode with latin-1 to avoid crashes
            return value.decode('latin-1')

    # Everything else - convert with unicode()
    try:
        return six.text_type(value)
    except Exception:
        # Absolute fallback
        return u"%s" % value



################################################################################
# Templates must be unicode strings in Python 2 to avoid implicit ascii decode
################################################################################

WIDGET = u"""<div id="%(id)sEditorWrapper" class="j01EditorWrapper">
  <textarea style="display:none" id="%(id)sWidget" name="%(name)s">%(content)s</textarea>
  <div id="%(id)sEditor" class="j01Editor">%(html)s</div>
</div>
"""

JAVASCRIPT = u"""<script>
var %(id)sWidget = $('#%(id)sWidget');
var %(id)sEditor = new Quill('#%(id)sEditor', {%(options)s
});
%(id)sEditor.on('text-change', function() {
    var check = %(id)sEditor.root.innerHTML;
    check = check.replace(new RegExp("<p>", "g"), "");
    check = check.replace(new RegExp("</p>", "g"), "");
    check = check.replace(new RegExp("<br>", "g"), "");
    check = check.replace(new RegExp("<br />", "g"), "");
    if (check) {
        %(id)sWidget.val(%(id)sEditor.root.innerHTML);
    } else {
        %(id)sWidget.val('');
    }
});
</script>
"""


################################################################################
# Helper to build Quill modules config (must return unicode)
################################################################################

def getModules(data):
    lines = []
    append = lines.append

    for key, value in list(data.items()):

        if key == 'toolbar':
            grps = []
            for grp in value:
                btns = []
                for btn in grp:
                    if isinstance(btn, six.string_types):
                        btns.append(btn)
                    elif isinstance(btn, dict):
                        for k, v in list(btn.items()):
                            if isinstance(v, six.string_types):
                                v = u"%s" % v
                            elif v is True:
                                v = u"true"
                            elif v is False:
                                v = u"false"
                            btns.append({k: v})
                grps.append(btns)
            # append(u"\n    %s: %s" % (key, grps))
            # append(u"\n    %s: %s" % (key, json.dumps(grps)))
            append(u"\n    %s: %s" % (key, json.dumps(grps,
                ensure_ascii=False).decode('utf-8')))

        elif value is True:
            append(u"\n    %s: true" % key)

        elif value is False:
            append(u"\n    %s: false" % key)

        elif value is None:
            append(u"\n    %s: null" % key)

        elif isinstance(value, int):
            append(u"\n    %s: %s" % (key, value))

        elif isinstance(value, six.string_types):
            if value.startswith('$'):
                append(u"\n    %s: %s" % (key, value))
            else:
                append(u"\n    %s: '%s'" % (key, value))

        else:
            append(u"\n    %s: %s" % (key, value))

    return u','.join(lines)


################################################################################
# JavaScript generator for widget (must return unicode)
################################################################################

def getJavaScript(data):
    try:
        id = data.pop('id')
    except KeyError:
        id = 'j01Editor'

    lines = []
    append = lines.append

    for key, value in list(data.items()):

        if key == 'modules':
            if value is None:
                continue
            append(u"\n        %s: {%s}" % (key, getModules(value)))

        elif value is True:
            append(u"\n    %s: true" % key)

        elif value is False:
            append(u"\n    %s: false" % key)

        elif value is None:
            append(u"\n    %s: null" % key)

        elif isinstance(value, int):
            append(u"\n    %s: %s" % (key, value))

        elif isinstance(value, six.string_types):
            if value.startswith('$'):
                append(u"\n    %s: %s" % (key, value))
            else:
                append(u"\n    %s: '%s'" % (key, value))

        else:
            append(u"\n    %s: %s" % (key, value))

    code = u','.join(lines)

    return JAVASCRIPT % {
        'id': id,
        'options': code,
    }


################################################################################
# Editor Widget
################################################################################

@zope.interface.implementer_only(interfaces.IEditorWidget)
class EditorWidget(j01.form.widget.textarea.TextAreaWidget):

    """Editor widget"""

    value = u''

    theme = 'snow'
    toolbar = [
        ['bold', 'italic'],
        [{'list': 'ordered'}, {'list': 'bullet'}],
        ['clean'],
    ]
    placeholder = None

    def cleanup(self, value):
        """Cleanup removes invalid HTML attributes and tags."""
        return j01.editor.util.simpleHTML(value)

    def extract(self, default=z3c.form.interfaces.NO_VALUE):
        """Support cleanup of returned value."""
        value = super(EditorWidget, self).extract(default)
        if value is not z3c.form.interfaces.NO_VALUE:
            value = self.cleanup(value)
        return value

    @property
    def modules(self):
        data = {}
        if self.toolbar is not None:
            data['toolbar'] = self.toolbar
        return data

    @property
    def javascript(self):
        return getJavaScript({
            'id': self.__name__,
            'theme': self.theme,
            'modules': self.modules,
            'placeholder': self.placeholder,
        })

    def update(self):
        # Marker for loading the widget JS
        self.request.annotations['j01.editor.widget.EditorWidget'] = True
        super(EditorWidget, self).update()

    def render(self):
        """Return HTML including editor javascript."""
        value = self.value or u''
        widget = WIDGET % {
            'id': self.__name__,
            'name': self.name,
            'content': j01.editor.escape(value),
            'html': value,
        }
        # Protection: ensure both values are unicode
        widget = ensure_unicode(widget)
        js = ensure_unicode(self.javascript)
        return widget + u"\n" + js


################################################################################
# Field widget factory
################################################################################

def getEditorWidget(field, request):
    return z3c.form.widget.FieldWidget(field, EditorWidget(request))
