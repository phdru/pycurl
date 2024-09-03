#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4:et

from . import localhost
import pycurl
import unittest

from . import appmanager
from . import util

setup_module_1, teardown_module_1 = appmanager.setup(('app', 8380))
setup_module_2, teardown_module_2 = appmanager.setup(('app', 8381))
setup_module_3, teardown_module_3 = appmanager.setup(('app', 8382))

def setup_module(mod):
    setup_module_1(mod)
    setup_module_2(mod)
    setup_module_3(mod)

def teardown_module(mod):
    teardown_module_3(mod)
    teardown_module_2(mod)
    teardown_module_1(mod)

class MultiWaitTest(unittest.TestCase):
    def test_multi_wait_extra_param(self):
        m = pycurl.CurlMulti()
        self.assertRaises(ValueError, m.wait, [], 0)

    def test_multi_wait(self):
        urls = [
            'http://%s:8380/success' % localhost,
            'http://%s:8381/success' % localhost,
            'http://%s:8382/success' % localhost,
        ]

        # init
        m = pycurl.CurlMulti()
        m.handles = []
        for url in urls:
            c = util.DefaultCurl()
            # save info in standard Python attributes
            c.url = url
            c.body = util.BytesIO()
            c.http_code = -1
            m.handles.append(c)
            # pycurl API calls
            c.setopt(c.URL, c.url)
            c.setopt(c.WRITEFUNCTION, c.body.write)
            m.add_handle(c)

        # get data
        num_handles = len(m.handles)
        while True:
            while True:
                m.wait(None, 1000)
                ret, num_handles = m.perform()
                if ret != pycurl.E_CALL_MULTI_PERFORM:
                    break
            if num_handles == 0:
                break

        # close handles
        for c in m.handles:
            # pycurl API calls
            m.remove_handle(c)
            c.close()
        m.close()

        for c in m.handles:
            self.assertEqual('success', c.body.getvalue().decode())
