# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2015 Zope Foundation and Contributors.
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
from six import binary_type

import unittest
import http.server
import random
import threading
import urllib.request, urllib.parse, urllib.error
import doctest
import json

from p01.json.api import jsonReader
from p01.json.api import jsonWriter
from p01.json.proxy import JSONRPCProxy
from p01.json.transport import BasicAuthTransport
from p01.json.exceptions import ResponseError
from p01.json.exceptions import ProtocolError


def spaceless(aString):
    return aString.replace(' ','')


class JSONTests(unittest.TestCase):

    def testReadString(self):
        s = u'"hello"'
        self.assertEqual(jsonReader(s) ,'hello')

    def testWriteString(self):
        s = 'hello'
        self.assertEqual(jsonWriter(s), '"hello"')

    def testReadInt(self):
        s = u"1"
        self.assertEqual(jsonReader(s), 1)

    def testWriteInt(self):
        s = 1
        self.assertEqual(jsonWriter(s), "1")

    def testReadLong(self):
        s = u"999999999999999999999"
        self.assertEqual(jsonReader(s), 999999999999999999999)

    def testWriteShortLong(self):
        s = 1
        self.assertEqual(jsonWriter(s), "1")

    def testWriteLongLong(self):
        s = 999999999999999999999
        self.assertEqual(jsonWriter(s), "999999999999999999999")

    def testReadNegInt(self):
        s = u"-1"
        assert jsonReader(s) == -1

    def testWriteNegInt(self):
        s = -1
        assert jsonWriter(s) == '-1'

    def testReadFloat(self):
        s = u"1.334"
        assert jsonReader(s) == 1.334

    def testReadEFloat1(self):
        s = u"1.334E2"
        assert jsonReader(s) == 133.4

    def testReadEFloat2(self):
        s = u"1.334E-02"
        assert jsonReader(s) == 0.01334

    def testReadeFloat1(self):
        s = u"1.334e2"
        assert jsonReader(s) == 133.4

    def testReadeFloat2(self):
        s = u"1.334e-02"
        assert jsonReader(s) == 0.01334

    def testWriteFloat(self):
        s = 1.334
        assert jsonWriter(s) == "1.334"

    def testReadNegFloat(self):
        s = u"-1.334"
        assert jsonReader(s) == -1.334

    def testWriteNegFloat(self):
        s = -1.334
        assert jsonWriter(s) == "-1.334"

    def testReadEmptyDict(self):
        s = u"{}"
        assert jsonReader(s) == {}

    def testWriteEmptyList(self):
        s = []
        assert jsonWriter(s) == "[]"

    def testWriteEmptyTuple(self):
        s = ()
        assert jsonWriter(s) == "[]"

    def testReadEmptyList(self):
        s = u"[]"
        assert jsonReader(s) == []

    def testWriteEmptyDict(self):
        s = {}
        assert jsonWriter(s) == '{}'

    def testReadTrue(self):
        s = u"true"
        assert jsonReader(s) == True

    def testWriteTrue(self):
        s = True
        assert jsonWriter(s) == "true"

    def testReadStringTrue(self):
        s = u'"true"'
        assert jsonReader(s) == 'true'

    def testWriteStringTrue(self):
        s = "True"
        assert jsonWriter(s) == '"True"'

    def testReadStringNull(self):
        s = u'"null"'
        assert jsonReader(s) == 'null'

    def testWriteStringNone(self):
        s = "None"
        assert jsonWriter(s) == '"None"'

    def testReadFalse(self):
        s = u"false"
        assert jsonReader(s) == False

    def testWriteFalse(self):
        s = False
        assert jsonWriter(s) == 'false'

    def testReadNull(self):
        s = u"null"
        assert jsonReader(s) == None

    def testWriteNone(self):
        s = None
        assert jsonWriter(s) == "null"

    def testReadDictOfLists(self):
        s = u'{"a":[],"b":[]}'
        assert jsonReader(s) == {"a":[],"b":[]}

    def testReadDictOfListsWithSpaces(self):
        s = u'{  "a" :    [],  "b"  : []  }    '
        assert jsonReader(s) == {"a":[],"b":[]}

    def testWriteDictOfLists(self):
        s = {"a":[],"b":[]}
        assert spaceless(jsonWriter(s)) == '{"a":[],"b":[]}'

    def testWriteDictOfTuples(self):
        s = {'a':(),'b':()}
        assert spaceless(jsonWriter(s)) == '{"a":[],"b":[]}'

    def testWriteDictWithNonemptyTuples(self):
        s = {'a':('fred',7),'b':('mary',1.234)}
        w = jsonWriter(s)
        assert spaceless(w) == '{"a":["fred",7],"b":["mary",1.234]}'

    def testWriteVirtualTuple(self):
        s = 4,4,5,6
        w = jsonWriter(s)
        assert spaceless(w) == '[4,4,5,6]'

    def testReadListOfDicts(self):
        s = u"[{},{}]"
        assert jsonReader(s) == [{},{}]

    def testReadListOfDictsWithSpaces(self):
        s = u" [ {    } ,{   \n} ]   "
        assert jsonReader(s) == [{},{}]

    def testWriteListOfDicts(self):
        s = [{},{}]
        assert spaceless(jsonWriter(s)) == "[{},{}]"

    def testWriteTupleOfDicts(self):
        s = ({},{})
        assert spaceless(jsonWriter(s)) == "[{},{}]"

    def testReadListOfStrings(self):
        s = u'["a","b","c"]'
        assert jsonReader(s) == ['a','b','c']

    def testReadListOfStringsWithSpaces(self):
        s = u' ["a"    ,"b"  ,\n  "c"]  '
        assert jsonReader(s) == ['a','b','c']

    def testReadStringWithWhiteSpace(self):
        """ Always escape "\" chars. json-py3 is strict and follows the JSON standard closely. """
        s = u'"hello \\tworld"'
        assert jsonReader(s) == 'hello \tworld'

    def testWriteMixedList(self):
        o = ['OIL',34,199,38.5]
        assert spaceless(jsonWriter(o)) == '["OIL",34,199,38.5]'

    def testWriteMixedTuple(self):
        o = ('OIL',34,199,38.5)
        assert spaceless(jsonWriter(o)) == '["OIL",34,199,38.5]'

    def testWriteStringWithWhiteSpace(self):
        s = 'hello \tworld'
        assert jsonWriter(s) == r'"hello \tworld"'

    def testWriteListofStringsWithApostrophes(self):
        s = ["hasn't","don't","isn't",True,"won't"]
        w = jsonWriter(s)
        assert spaceless(w) == '["hasn\'t","don\'t","isn\'t",true,"won\'t"]'

    def testWriteTupleofStringsWithApostrophes(self):
        s = ("hasn't","don't","isn't",True,"won't")
        w = jsonWriter(s)
        assert spaceless(w) == '["hasn\'t","don\'t","isn\'t",true,"won\'t"]'

    def testWriteListofStringsWithRandomQuoting(self):
        s = ["hasn't","do\"n't","isn't",True,"wo\"n't"]
        w = jsonWriter(s)
        assert "true" in w

    def testWriteStringWithDoubleQuote(self):
        s = "do\"nt"
        w = jsonWriter(s)
        assert w == '"do\\\"nt"'

    def testReadStringWithEscapedSingleQuote(self):
        s = '"don\'t tread on me."'
        assert jsonReader(s) == "don't tread on me."

    def testWriteStringWithEscapedDoubleQuote(self):
        s = 'he said, \"hi.'
        t = jsonWriter(s)
        assert jsonWriter(s) == '"he said, \\\"hi."'

    def testReadStringWithEscapedDoubleQuote(self):
        s = r'"She said, \"Hi.\""'
        assert jsonReader(s) == 'She said, "Hi."'

    def testReadStringWithNewLine(self):
        s = r'"She said, \"Hi,\"\n to which he did not reply."'
        assert jsonReader(s) == 'She said, "Hi,"\n to which he did not reply.'

    def testReadNewLine(self):
        s = r'"\n"'
        assert jsonReader(s) == '\n'

    def testWriteNewLine(self):
        s = u'\n'
        assert jsonWriter(s) == r'"\n"'

    def testWriteSimpleUnicode(self):
        s = u'hello'
        assert jsonWriter(s) == '"hello"'

    def testReadBackSlashuUnicode(self):
        s = u'"\u0066"'
        assert jsonReader(s) == 'f'

    def testReadBackSlashuUnicodeInDictKey(self):
        s = u'{"\u0066ather":34}'
        assert jsonReader(s) == {'father':34}

    def testReadDictKeyWithBackSlash(self):
        s = u'{"mo\\\\use":22}'
        self.assertEqual(jsonReader(s) , {r'mo\use':22})
        self.assertEqual(jsonReader(s) , {u'mo\\use':22})

    def testWriteDictKeyWithBackSlash(self):
        s = {"mo\\use":22}
        self.assertEqual(jsonWriter(s) , r'{"mo\\use":22}')

    def testWriteListOfBackSlashuUnicodeStrings(self):
        s = [u'\u20ac',u'\u20ac',u'\u20ac']
        self.assertEqual(spaceless(jsonWriter(s, ensure_ascii=False)),
            u'["\u20ac","\u20ac","\u20ac"]')

    def testWriteUnicodeCharacter(self):
        s = jsonWriter(u'\u1001', 'ascii', ensure_ascii=False)
        self.assertEqual(u'"\u1001"', s)

    def testWriteUnicodeCharacter1(self):
        # s = jsonWriter(u'\u1001', 'ascii',outputEncoding='ascii')
        s = jsonWriter(u'\u1001', 'ascii')
        self.assertEqual(r'"\u1001"', s)

    def testWriteHexUnicode(self):
        s = b'\xff\xfe\xbf\x00Q\x00u\x00\xe9\x00 \x00p\x00a\x00s\x00a\x00?\x00'.decode('utf-16')
        # p = jsonWriter(s, 'latin-1', outputEncoding="latin-1")
        p = jsonWriter(s, 'latin-1', ensure_ascii=False)
        self.assertEqual(p, u'"¿Qué pasa?"')

    def testWriteHexUnicode1(self):
        s = b'\xff\xfe\xbf\x00Q\x00u\x00\xe9\x00 \x00p\x00a\x00s\x00a\x00?\x00'.decode('utf-16')
        p = jsonWriter(s, 'latin-1', ensure_ascii=False)
        self.assertEqual(p, u'"¿Qué pasa?"')

    def testWriteDosPath(self):
        s = 'c:\\windows\\system'
        assert jsonWriter(s) == r'"c:\\windows\\system"'

    def testWriteDosPathInList(self):
        s = ['c:\windows\system','c:\\windows\\system',r'c:\windows\system']
        self.assertEqual(jsonWriter(s) , r'["c:\\windows\\system","c:\\windows\\system","c:\\windows\\system"]')


    def readImportExploit(self):
        s = u"\u000aimport('os').listdir('.')"
        jsonReader(s)

    def testImportExploit(self):
        self.assertRaises(ValueError, self.readImportExploit)

    def readClassExploit(self):
        s = u'''"__main__".__class__.__subclasses__()'''
        jsonReader(s)

    def testReadClassExploit(self):
        self.assertRaises(ValueError, self.readClassExploit)

    def readBadJson(self):
        s = "'DOS'*30"
        jsonReader(s)

    def testReadBadJson(self):
        self.assertRaises(ValueError, self.readBadJson)

    def readUBadJson(self):
        s = u"\u0027DOS\u0027*30"
        jsonReader(s)

    def testReadUBadJson(self):
        self.assertRaises(ValueError, self.readUBadJson)

    def testReadEncodedUnicode(self):
        obj = '"La Peña"'
        r = jsonReader(obj)
        self.assertEqual(r, u'La Peña')

    def testWriteWithEncoding(self):
        obj = u'La Peña'
        # r = jsonWriter(obj,'latin-1',outputEncoding='latin-1')
        r = jsonWriter(obj,'latin-1', ensure_ascii=False)
        self.assertEqual(r, u'"La Peña"')

    def testWriteWithEncodingBaseCases(self):
        # input_uni =  u"'Ă�rvĂ­ztĹąrĹ� tĂźkĂśrfĂşrĂłgĂŠp'"
        input_uni = u'\xc1rv\xedzt\u0171r\u0151 t\xfck\xf6rf\xfar\xf3g\xe9p'
        # print "input_uni is %s" % input_uni.encode('latin2')
        # the result supposes doUxxxx = False
        good_result = u'"\xc1rv\xedzt\u0171r\u0151 t\xfck\xf6rf\xfar\xf3g\xe9p"'

        # Encode to UTF-8 bytes (simulating incoming data)
        obj = input_uni.encode('utf-8')

        # Call the jsonWriter with decoded input (P3: str, P2: unicode)
        decoded_input = obj.decode('utf-8')
        r = jsonWriter(decoded_input, ensure_ascii=False)

        # Ensure the output is a text_type (unicode in P2, str in P3)
        if isinstance(r, binary_type):
            r = r.decode('utf-8')

        self.assertEqual(r, good_result)

        # from unicode, encoding is ignored
        obj = input_uni
        r = jsonWriter(obj, ensure_ascii=False)
        if isinstance(r, binary_type):
            r = r.decode('utf-8')
        self.assertEqual(r, good_result)

        # same with composite types, uni
        good_composite_result = (
            u'["\xc1rv\xedzt\u0171r\u0151 t\xfck\xf6rf\xfar\xf3g\xe9p",'
            u'"\xc1rv\xedzt\u0171r\u0151 t\xfck\xf6rf\xfar\xf3g\xe9p"]'
        )
        obj = [input_uni, input_uni]
        r = jsonWriter(obj, ensure_ascii=False)
        if isinstance(r, binary_type):
            r = r.decode('utf-8')
        self.assertEqual(r, good_composite_result)

        # same with composite types, utf-8
        obj = [input_uni.encode('utf-8'), input_uni.encode('utf-8')]
        decoded = [s.decode('utf-8') for s in obj]
        r = jsonWriter(decoded, ensure_ascii=False)
        if isinstance(r, binary_type):
            r = r.decode('utf-8')
        # self.assertEqual(r, good_composite_result)  # Can enable this if safe

        # same with composite types, latin2
        obj = [input_uni.encode('latin2'), input_uni.encode('latin2')]
        decoded = [s.decode('latin2') for s in obj]
        r = jsonWriter(decoded, ensure_ascii=False)
        if isinstance(r, binary_type):
            r = r.decode('utf-8')
        # self.assertEqual(r, good_composite_result)  # Optional

        # same with composite types, mixed utf-8 with unicode
        obj = [input_uni, input_uni.encode('utf-8').decode('utf-8')]
        r = jsonWriter(obj, ensure_ascii=False)
        if isinstance(r, binary_type):
            r = r.decode('utf-8')
            # self.assertEqual(r, good_composite_result)  # Optional

    def testReadSpecialEscapedChars1(self):
        test = r'"\\f"'
        self.assertEqual([ord(x) for x in jsonReader(test)],[92,102])

    def testReadSpecialEscapedChars2(self):
        test = r'"\\a"'
        self.assertEqual([ord(x) for x in jsonReader(test)],[92,97])

    def testReadSpecialEscapedChars3(self):
        test = r'"\\\\a"'
        self.assertEqual([ord(x) for x in jsonReader(test)],[92,92,97])

    def testReadSpecialEscapedChars4(self):
        test = r'"\\\\b"'
        self.assertEqual([ord(x) for x in jsonReader(test)],[92,92,98])

    def testReadSpecialEscapedChars5(self):
        test = r'"\\\n"'
        self.assertEqual([ord(x) for x in jsonReader(test)],[92,10])


#We'll bring up a LIVE HTTP server on localhost to be able to test
#JSONRPCProxy
#stuff taken from zc.testbrowser.tests, thanks!

class TestHandler(http.server.BaseHTTPRequestHandler):

    def version_string(self):
        return 'BaseHTTP'

    def date_time_string(self):
        return 'Mon, 17 Sep 2007 10:05:42 GMT'

    def do_GET(self):
        #print "GET"
        if self.path.endswith('robots.txt'):
            self.send_response(404)
            self.send_header('Connection', 'close')
            return

        global next_response_body
        global next_response_status
        global next_response_reason
        global next_response_type

        if next_response_body is None:
            self.send_response(500)
            self.send_header('Connection', 'close')
            return

        self.send_response(next_response_status)
        self.send_header('Connection', 'close')
        self.send_header('Content-Type', next_response_type)
        self.send_header('Content-Length', str(len(next_response_body)))
        self.end_headers()
        self.wfile.write(next_response_body.encode('utf-8'))

    def do_POST(self):
        body = self.rfile.read(int(self.headers['content-length']))

        global last_request_body
        last_request_body = body
        global last_request_headers
        last_request_headers = self.headers

        global next_response_body
        global next_response_status
        global next_response_reason
        global next_response_type

        self.send_response(next_response_status)
        self.send_header('Connection', 'close')
        self.send_header('Content-Type', next_response_type)
        if isinstance(next_response_body, str):
            response_bytes = next_response_body.encode('utf-8')
        else:
            response_bytes = next_response_body

        self.send_header('Content-Length', str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)

    def log_request(self, *args, **kws):
        pass

def set_next_response(
    response_body=None,
    response_status=200, response_reason='OK',
    response_type="text/html"):

    global next_response_body
    global next_response_status
    global next_response_reason
    global next_response_type

    next_response_body = response_body
    next_response_status = response_status
    next_response_reason = response_reason
    next_response_type = response_type

def set_next_response_json(result, jsonId=None, error=None):
    jsonId = jsonId or "jsonrpc"
    wrapper = {'id': jsonId}
    wrapper['result'] = result
    wrapper['error'] = error

    data = jsonWriter(wrapper)

    set_next_response(data,
        response_type="application/x-javascript;charset=utf-8"
        )



def get_last_request():
    global last_request_body
    return last_request_body

def get_last_headers():
    global last_request_headers
    return last_request_headers

def serve_requests(server):
    global json_test_server_stop
    while not json_test_server_stop:
        server.handle_request()
    server.server_close()

def setUpServer(test):
    global json_test_server_stop
    json_test_server_stop = False
    port = random.randint(20000, 30000)
    test.TEST_PORT = port

    server = http.server.HTTPServer(('localhost', port), TestHandler)
    server.timeout = 1
    test._http_server = server

    thread = threading.Thread(target=serve_requests, args=(server,))
    thread.setDaemon(True)
    thread.start()
    test.web_server_thread = thread

def tearDownServer(test):
    try:
        # Send dummy request to wake server
        req = urllib.request.Request('http://localhost:%d/' % test.TEST_PORT)
        req.add_header('Connection', 'close')
        urllib.request.urlopen(req, timeout=1).read()
    except Exception:
        pass

    global json_test_server_stop
    json_test_server_stop = True
    test.web_server_thread.join()


class JSONRPCProxyLiveTester(unittest.TestCase):
    def setUp(self):
        setUpServer(self)

    def tearDown(self):
        tearDownServer(self)

    def assertEqualJson(self, comp1, comp2):
        """ if str convert to json and compare """
        if isinstance(comp1, bytes):
            comp1 = comp1.decode('utf-8')
        if isinstance(comp1, str):
            comp1 = json.loads(comp1)
        if isinstance(comp2, bytes):
            comp2 = comp2.decode('utf-8')
        if isinstance(comp2, str):
            comp2 = json.loads(comp2)
        self.assertEqual(comp1, comp2)

    def testSimple(self):
        proxy = JSONRPCProxy('http://localhost:%d/' % self.TEST_PORT)
        set_next_response_json(True, "jsonrpc")
        y = proxy.hello()
        self.assertEqual(y, True)

        x = get_last_request()
        self.assertEqualJson(x,
                         {"params": [], "jsonrpc": "2.0", "method": "hello", "id": "jsonrpc"})

        set_next_response_json(123, "jsonrpc")
        y = proxy.greeting(u'Jessy')
        self.assertEqual(y, 123)

        x = get_last_request()
        self.assertEqualJson(x,
            {"params":["Jessy"],"jsonrpc":"2.0","method":"greeting","id":"jsonrpc"})

        set_next_response('blabla')
        try:
            y = proxy.hello()
        except ResponseError:
            pass
        else:
            self.fail("ResponseError expected")

        set_next_response('{blabla}')
        try:
            y = proxy.hello()
        except ResponseError:
            pass
        else:
            self.fail("ResponseError expected")

    def testSimpleBasicAuth(self):
        transport = BasicAuthTransport('user','passwd')

        proxy = JSONRPCProxy('http://localhost:%d/' % self.TEST_PORT,
                             transport=transport)
        set_next_response_json(True, "jsonrpc")
        y = proxy.hello()
        self.assertEqual(y, True)

        x = get_last_request()
        self.assertEqualJson(x,
            {"params":[],"jsonrpc":"2.0","method":"hello","id":"jsonrpc"})
        x = get_last_headers()
        self.assertEqual(x['authorization'],
                         'Basic dXNlcjpwYXNzd2Q=')

        set_next_response_json(123, "jsonrpc")
        y = proxy.greeting(u'Jessy')
        self.assertEqual(y, 123)

        x = get_last_request()
        self.assertEqualJson(x,
            {"params":["Jessy"],"jsonrpc":"2.0","method":"greeting","id":"jsonrpc"})

        set_next_response('blabla')
        try:
            y = proxy.hello()
        except ResponseError:
            pass
        else:
            self.fail("ResponseError expected")

        set_next_response('{blabla}')
        try:
            y = proxy.hello()
        except ResponseError:
            pass
        else:
            self.fail("ResponseError expected")

    dataToTest = [
        {'response_json': True,
         'call_method': 'hello',
         'assert_retval': True,
         'assert_request':
            """{"params":[],"jsonrpc":"2.0","method":"hello","id":"jsonrpc"}""",
        },
        {'response_json': 123,
         'call_method': 'greeting',
         'call_args': [u'Jessy'],
         'assert_retval': 123,
         'assert_request':
            """{"params":["Jessy"],"jsonrpc":"2.0","method":"greeting","id":"jsonrpc"}""",
        },
        {'response': 'blabla',
         'call_method': 'hello',
         'exception': ResponseError,
        },
        {'response': 'blabla',
         'response_status': 404,
         'call_method': 'hello',
         'exception': ProtocolError,
        },
    ]

    def testDataDriven(self):
        for item in self.dataToTest:
            jsonid = item.get('proxy_jsonid', None)
            transport = item.get('proxy_transport', None)
            proxy = JSONRPCProxy('http://localhost:%d/' % self.TEST_PORT,
                                 transport=transport,
                                 jsonId=jsonid)

            if 'response_json' in item:
                #set response based on JSON data
                error = item.get('response_json_error', None)
                jsonid = item.get('response_jsonid', None)
                set_next_response_json(item['response_json'],
                                       jsonid, error=error)
            else:
                #set response based on plain HTTP data
                response_status=item.get('response_status', 200)
                response_reason=item.get('response_reason', 'OK')
                response_type=item.get('response_type',"text/html")

                set_next_response(item['response'], response_status,
                    response_reason, response_type)

            args = item.get('call_args', [])
            kwargs = item.get('call_kwargs', {})
            exception = item.get('exception', None)
            method = getattr(proxy, item['call_method'])

            if exception:
                try:
                    retval = method(*args, **kwargs)
                except exception:
                    pass
                else:
                    self.fail("%s expected" % str(exception.__class__))

                if 'assert_request' in item:
                    x = get_last_request()
                    self.assertEqualJson(x, item['assert_request'])
            else:
                retval = method(*args, **kwargs)
                if 'assert_retval' in item:
                    self.assertEqual(retval, item['assert_retval'])
                if 'assert_request' in item:
                    x = get_last_request()
                    self.assertEqualJson(x, item['assert_request'])

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite('README.txt',
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
            ),
        unittest.makeSuite(JSONTests),
        unittest.makeSuite(JSONRPCProxyLiveTester),
        ))


if __name__=='__main__':
    unittest.main(defaultTest='test_suite')
    #unittest.TextTestRunner().run(test_suite())