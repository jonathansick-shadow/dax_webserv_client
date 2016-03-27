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
Exception classes for RESTful APIs
@author  Brian Van Klaveren, SLAC
"""


class WebservException(Exception):
    """
    The base exception class for the webserv client (this module)
    when there is a general error interacting with the API.
    """

    pass


class WebservRequestException(WebservException):
    """
    Base exception class for all http exceptions.
    This class just wraps the thrown requests.exceptions.RequestException
    exception to something a bit simpler and friendly.
    """

    def __init__(self, httpError):
        self.url = httpError.request.url
        response = httpError.response or {}
        self.status_code = getattr(response, "status_code", None)
        self.headers = getattr(response, "headers", None)
        self.content = getattr(response, "content", None)
        super(WebservRequestException, self).__init__(httpError.message)

    def __str__(self):
        return "(HTTP Error: %s): %s" % (self.status_code, self.content)


class WebservClientException(WebservException):
    """
    The base exception class for all webserv client exceptions.
    """

    def __init__(self, exception, message=None, cause=None, metadata=None, **kwargs):
        self.exception = exception
        self.message = message
        self.cause = cause
        self.metadata = metadata
        super(WebservClientException, self).__init__(str(self))

    def __str__(self):
        return "Webserv Sent Exception %s with message: %s" % (self.exception, self.message)


def checkedError(requestException):
    """ Check error and return WebservClientException when we can
    @param requestException: Exception from requests library
    :return: WebservClientException if it's from the REST API, otherwise WebservRequestException
    """
    response = requestException.response
    if response and response.headers['content-type'] == 'application/json':
        data = response.json()
        data = {}
        if 'exception' in data:
            return WebservClientException(
                exception=data["exception"], message=data.get("message", None),
                cause=data.get("cause", None), metadata=data.get("metadata", None))
    return WebservRequestException(requestException)
