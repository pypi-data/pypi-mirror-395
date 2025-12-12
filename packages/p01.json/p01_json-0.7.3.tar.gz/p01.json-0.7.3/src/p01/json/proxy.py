##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
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
$Id:$
"""
from __future__ import absolute_import

from future import standard_library

standard_library.install_aliases()
from builtins import str
from builtins import object

import copy
import logging
import socket
import urllib.request, urllib.parse, urllib.error

import p01.json.exceptions

import p01.json.transport

logger = logging.getLogger(__name__)

JSON_RPC_VERSION = '2.0'


class _Method(object):
    """Proxy callable method"""

    def __init__(self, call, name, jsonId, jsonVersion, jsonWriter):
        self.call = call
        self.name = name
        self.jsonId = jsonId
        self.jsonVersion = jsonVersion
        self.jsonWriter = jsonWriter

    def __call__(self, *args, **kwargs):
        """Process incoming request data"""
        request = {}
        # add our version
        if self.jsonVersion == '1.0':
            pass
        elif self.jsonVersion == '1.1':
            request['version'] = self.jsonVersion
        else:
            request['jsonrpc'] = self.jsonVersion
        request['method'] = self.name

        # There is not support for postional and named parameters in one
        # call. We propably will add support for this within a extension
        # in a later version. Till then, we will raise an exception if
        # we will get both paramters.
        if len(args) > 0 and len(kwargs) > 0:
            raise ValueError(
                'Mixing positional and named parameters in one call is not possible')

        if self.jsonVersion in ['1.0', '1.1']:
            if len(args) > 0:
                params = args
            elif len(kwargs) > 0:
                params = copy.copy(kwargs)
                index = 0
                for arg in args:
                    params[str(index)] = arg
                    index += 1
            else:
                params = []
        else:
            if len(args) > 0:
                params = args
            elif len(kwargs) > 0:
                params = kwargs
            else:
                params = []

        # set params and write json
        request['params'] = params
        # add our json id
        request['id'] = self.jsonId
        data = self.jsonWriter(request)
        try:
            return self.call(data)
        except socket.error as msg:
            logger.exception(msg)
            raise p01.json.exceptions.ResponseError(
                "JSONRPC server connection error.")

    def __getattr__(self, name):
        """Wrap callable method"""
        return _Method(self.call, "%s.%s" % (self.name, name), self.jsonId,
            self.jsonVersion, self.jsonWriter)


class JSONRPCProxy(object):
    """JSON-RPC server proxy."""

    def __init__(self, uri, transport=None, encoding=None, verbose=None,
        jsonId=None, jsonVersion=JSON_RPC_VERSION,
        contentType='application/json-rpc', jsonReader=None, jsonWriter=None,
        username=None, password=None):
        if verbose is None:
            verbose = 0
        self.contentType = contentType
        utype, _uri = urllib.parse.splittype(uri)
        if utype not in ("http", "https"):
            raise IOError("Unsupported JSONRPC protocol")
        self.__host, self.__handler = urllib.parse.splithost(_uri)
        if not self.__handler:
            self.__handler = ""
        if transport is None:
            transport = p01.json.transport.getTransport(uri, username, password,
                contentType=contentType, jsonReader=jsonReader, verbose=verbose)
        self.__transport = transport
        self.__encoding = encoding
        self.__verbose = verbose
        self.jsonId = jsonId or u'jsonrpc'
        self.jsonVersion = jsonVersion
        if jsonWriter is None:
            jsonWriter = p01.json.api.jsonWriter
        self.jsonWriter = jsonWriter
        self.error = None

    def __request(self, request):
        """call a method on the remote server.

        This will raise a ResponseError or return the JSON result dict
        """
        # apply encoding if any
        if self.__encoding:
            request = request.encode(self.__encoding)
        # start the call
        try:
            response = self.__transport.request(self.__host, self.__handler,
                request, verbose=self.__verbose)
            self.error = None
        except p01.json.exceptions.ResponseError as e:
            # catch error message
            self.error = str(e)
            raise e

        if isinstance(response, int):
            # that's just a status code response with no result
            logger.error('Received status code %s' % response)
        elif len(response) == 3:
            # that's a valid response format
            if (self.jsonId is not None and
                response.get('id') is not None and
                self.jsonId != response.get('id')):
                # different request id returned
                raise p01.json.exceptions.ResponseError(
                    "Invalid request id returned")
            if response.get('error'):
                # error mesage in response
                self.error = response['error']
                raise p01.json.exceptions.ResponseError(
                    "Received error from server: %s" % self.error)
            else:
                # only return the result if everything is fine
                return response['result']

        return response

    @property
    def _cookies(self):
        """REturns the cookies fir future requests"""
        return self.__transport.cookies

    def __getattr__(self, name):
        """This let us call methods on remote server."""
        return _Method(self.__request, name, self.jsonId, self.jsonVersion,
            self.jsonWriter)

    def __repr__(self):
        return "<JSONProxy for %s%s>" % (self.__host, self.__handler)

    __str__ = __repr__
