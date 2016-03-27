# LSST Data Management System
# Copyright 2015 AURA/LSST.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.

"""
High level python client for Webserv interaction
@author  Brian Van Klaveren, SLAC
"""

# standard library
import unittest
from lsst.dax.webserv.client import MetaClient


def wrappedMockDoRequest(obj):
    def mockDoRequest(httpMethod, endpoint, target, params=None, data=None, **kwargs):
        target = obj._target(endpoint, target)
        resp = lambda: None
        resp.json = lambda: "{method} {target}".format(method=httpMethod, target=target)
        return resp
    return mockDoRequest


class TestMetaserv(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestMetaserv, self).__init__(*args, **kwargs)
        self.client = MetaClient.createClientFromUrl("http://example.com")
        # patch the doRequest method
        self.client.httpClient.doRequest = wrappedMockDoRequest(self.client.httpClient)

    def testClient(self):
        expected = 'get http://example.com/meta'
        expected = "/".join((expected, "db"))
        self.assertEqual(expected, self.client.getTypes())
        expected = "/".join((expected, "DC"))
        self.assertEqual(expected, self.client.getDbNames("DC"))
        expected = "/".join((expected, "sources"))
        self.assertEqual(expected, self.client.getDbInfo("DC", "sources"))
        expected = "/".join((expected, "tables"))
        self.assertEqual(expected, self.client.getTableNames("DC", "sources"))
        expected = "/".join((expected, "galaxies"))
        self.assertEqual(expected, self.client.getTableInfo("DC", "sources", "galaxies"))
        expected = "/".join((expected, "schema"))
        self.assertEqual(expected, self.client.getTableSchema("DC", "sources", "galaxies"))
