##############################################################################
#
# Copyright (c) 2016 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
$Id: api.py 5242 2025-04-28 09:16:12Z rodrigo.ristow $
"""
from __future__ import absolute_import

import json

import six


def jsonReader(data, *args, **kwargs):
    """Returns a json data reader.

    By default we use a method pointer to json.loads
    """
    return json.loads(data, *args, **kwargs)


def jsonWriter(data, encoding='utf-8', separators=(',', ':'), **kwargs):
    """Returns a json data reader.

    By default we use a method pointer to json.dumps
    """
    if six.PY2:
        return json.dumps(data, encoding=encoding, separators=separators, **kwargs)
    else:
        return json.dumps(data, separators=separators, **kwargs)
