#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_zfiles.api main module

"""

import json

from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden, HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config

from pyams_file.skin.view import FileView
from pyams_utils.registry import query_utility
from pyams_utils.rest import http_error
from pyams_zfiles.interfaces import IDocumentContainer, READ_DOCUMENT_PERMISSION, REST_DOCUMENT_DATA_ROUTE, STATE

__docformat__ = 'restructuredtext'


@view_config(route_name=REST_DOCUMENT_DATA_ROUTE)
def document_data(request):
    """Document data endpoint"""
    oid = request.matchdict.get('oid')
    if not oid:
        return Response(json.dumps(http_error(request, HTTPBadRequest)),
                        status=HTTPBadRequest.code,
                        content_type='application/json',
                        charset='utf-8')
    container = query_utility(IDocumentContainer)
    if container is None:
        return Response(json.dumps(http_error(request, HTTPNotFound)),
                        status=HTTPNotFound.code,
                        content_type='application/json',
                        charset='utf-8')
    document = container.get_document(oid, status=STATE.PUBLISHED.value)
    if document is None:
        return Response(json.dumps(http_error(request, HTTPNotFound)),
                        status=HTTPNotFound.code,
                        content_type='application/json',
                        charset='utf-8')
    if not request.has_permission(READ_DOCUMENT_PERMISSION, context=document):
        return Response(json.dumps(http_error(request, HTTPForbidden)),
                        status=HTTPForbidden.code,
                        content_type='application/json',
                        charset='utf-8')
    request.context = document.data
    return FileView(request)
