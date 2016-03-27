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
High level python clients for Webserv interaction
@author  Brian Van Klaveren, SLAC
"""

from .exceptions import checkedError
from .httpclient import MetaHttpClient
from requests.exceptions import RequestException


class BaseClient:
    """
    Base class for clients.
    """

    def _doRequest(self, httpClientMethod, *args):
        """
        Convenience method to wrap the exceptions.
        @param httpClientMethod: Instance method from httpClient to dispatch
        @param args: httpClientMethod arguments
        @return: Python dict from JSON response, or an appropriate WebservRequestException
        """
        try:
            resp = httpClientMethod(*args)
            return resp.json()
        except RequestException as e:
            raise checkedError(e)


class MetaClient(BaseClient):
    """
    High-level MetaServ Client.
    """

    def __init__(self, metaHttpClient):
        """
        Returns a client configured with the given MetaHttpClient
        @param metaHttpClient: The underlying MetaHttpClient to handle requests
        @return: configured MetaClient
        """
        self.httpClient = metaHttpClient

    def createClientFromUrl(url, authStrategy=None):
        """
        Factory method to reate a new client from url and auth strategy.
        @param url: HTTP endpoint of root web application.
        @param authStrategy: A requests.auth.AuthBase to handle authentication
        @return: Configured BaseHttpClient
        """
        return MetaClient(MetaHttpClient(url, authStrategy))

    createClientFromUrl = staticmethod(createClientFromUrl)

    def getRoot(self):
        return self._doRequest(self.httpClient.getRoot)

    def getTypes(self):
        """
        List the instances, with lsstLevel in ('DC', 'L1', 'L2', 'L3', 'dev'),
        which have at least one database for the 'db' repo type.
        """
        return self._doRequest(self.httpClient.getTypes)

    def getDbNames(self, lsstLevel):
        """
        List available databases
        @param: lsstLevel: Given instance to check
        """
        return self._doRequest(self.httpClient.getDbNames, lsstLevel)

    def getDbInfo(self, lsstLevel, dbName):
        """
        Retrieves information about a database
        @param lsstLevel: Given instance
        @param dbName: Database in the given instance to query
        """
        return self._doRequest(self.httpClient.getDbInfo, lsstLevel, dbName)

    def getTableNames(self, lsstLevel, dbName):
        """
        List available table names
        @param lsstLevel: Given instance
        @param dbName: Database in the given instance to query
        """
        return self._doRequest(self.httpClient.getTableNames, lsstLevel, dbName)

    def getTableInfo(self, lsstLevel, dbName, tableName):
        """
        Get a table's information
        @param lsstLevel: Given instance
        @param dbName: Database in the given instance
        @param tableName: The table's name
        """
        return self._doRequest(self.httpClient.getTableInfo, lsstLevel, dbName, tableName)

    def getTableSchema(self, lsstLevel, dbName, tableName):
        """
        Get a table's schema
        @param lsstLevel: Given instance
        @param dbName: Database in the given instance
        @param tableName: The table's name
        """
        return self._doRequest(self.httpClient.getTableSchema, lsstLevel, dbName, tableName)
