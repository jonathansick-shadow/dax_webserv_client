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
Low level clients for HTTP interaction.
@author  Brian Van Klaveren, SLAC
"""

import requests
from urllib import quote as _qt


class BaseHttpClient:
    """Request/Response Helper class for all HTTP endpoint clients"""

    def __init__(self, url, authStrategy=None):
        """
        Initialize Base HTTP client
        @param url: HTTP endpoint of root web application.
        @param authStrategy: A requests.auth.AuthBase to handle authentication
        @return: Configured BaseHttpClient
        """
        self.baseUrl = url
        self.authStrategy = authStrategy

    def _target(self, endpoint, path):
        def _resolve(_path, part):
            """Sanitize all the slashes!"""
            _path = _path.rstrip("/")
            part = part.lstrip("/")
            return "/".join((_path, part)) if len(part) else _path
        newBaseUrl = _resolve(self.baseUrl, endpoint)
        return _resolve(newBaseUrl, path)

    def doRequest(self, httpMethod, endpoint, target, params=None, data=None, **kwargs):
        """If necessary, target should have been quoted"""
        target = self._target(endpoint, target)
        headers = kwargs["headers"] if "headers" in kwargs else None
        requests_method = getattr(requests, httpMethod)
        resp = requests_method(target, params=params, headers=headers, data=data, auth=self.authStrategy)
        resp.raise_for_status()
        return resp


class MetaHttpClient(BaseHttpClient):
    """
    MetaServ HTTP Client.
    This client deals only with requests.Response objects.
    """
    ENDPOINT = "/meta"

    def getRoot(self, **kwargs):
        path = ""
        return self.doRequest("get", self.ENDPOINT, path)

    def getTypes(self, **kwargs):
        """
        List the instances, with lsstLevel in ('DC', 'L1', 'L2', 'L3', 'dev'),
        which have at least one database for the 'db' repo type.
        @param kwargs: kwargs to pass through to requests library.
        """
        path = "/db"
        return self.doRequest("get", self.ENDPOINT, path)

    def getDbNames(self, lsstLevel, **kwargs):
        """
        List available databases
        @param: lsstLevel: Given instance to check
        @param kwargs: kwargs to pass through to requests library.
        """
        path = "/db/{lsstLevel}".format(lsstLevel=_qt(lsstLevel))
        return self.doRequest("get", self.ENDPOINT, path)

    def getDbInfo(self, lsstLevel, dbName, **kwargs):
        """
        Retrieves information about a database
        @param lsstLevel: Given instance
        @param dbName: Database in the given instance to query
        @param kwargs: kwargs to pass through to requests library.
        """
        path = "/db/{lsstLevel}/{dbName}".format(lsstLevel=_qt(lsstLevel), dbName=_qt(dbName))
        return self.doRequest("get", self.ENDPOINT, path)

    def getTableNames(self, lsstLevel, dbName, **kwargs):
        """
        List available table names
        @param lsstLevel: Given instance
        @param dbName: Database in the given instance to query
        @param kwargs: kwargs to pass through to requests library.
        """
        path = "/db/{lsstLevel}/{dbName}/tables".format(lsstLevel=_qt(lsstLevel), dbName=_qt(dbName))
        return self.doRequest("get", self.ENDPOINT, path)

    def getTableInfo(self, lsstLevel, dbName, tableName, **kwargs):
        """
        Get a table's information
        @param lsstLevel: Given instance
        @param dbName: Database in the given instance
        @param tableName: The table's name
        @param kwargs: kwargs to pass through to requests library.
        """
        path = "/db/{lsstLevel}/{dbName}/tables/{tableName}".format(
            lsstLevel=_qt(lsstLevel), dbName=_qt(dbName), tableName=_qt(tableName))
        return self.doRequest("get", self.ENDPOINT, path)

    def getTableSchema(self, lsstLevel, dbName, tableName, **kwargs):
        """
        Get a table's schema
        @param lsstLevel: Given instance
        @param dbName: Database in the given instance
        @param tableName: The table's name
        @param kwargs: kwargs to pass through to requests library.
        """
        path = "/db/{lsstLevel}/{dbName}/tables/{tableName}/schema".format(
            lsstLevel=_qt(lsstLevel), dbName=_qt(dbName), tableName=_qt(tableName))
        return self.doRequest("get", self.ENDPOINT, path)
