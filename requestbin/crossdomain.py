from datetime import timedelta
from functools import update_wrapper

from flask import make_response, request, current_app

accept_headers = [
    'Accept',
    'Accept-CH',
    'Accept-Charset',
    'Accept-Datetime',
    'Accept-Encoding',
    'Accept-Ext',
    'Accept-Features',
    'Accept-Language',
    'Accept-Params',
    'Accept-Ranges',
    'Access-Control-Allow-Credentials',
    'Access-Control-Allow-Headers',
    'Access-Control-Allow-Methods',
    'Access-Control-Allow-Origin',
    'Access-Control-Expose-Headers',
    'Access-Control-Max-Age',
    'Access-Control-Request-Headers',
    'Access-Control-Request-Method',
    'Age',
    'Allow',
    'Alternates',
    'Authentication-Info',
    'Authorization',
    'C-Ext',
    'C-Man',
    'C-Opt',
    'C-PEP',
    'C-PEP-Info',
    'CONNECT',
    'Cache-Control',
    'Compliance',
    'Connection',
    'Content-Base',
    'Content-Disposition',
    'Content-Encoding',
    'Content-ID',
    'Content-Language',
    'Content-Length',
    'Content-Location',
    'Content-MD5',
    'Content-Range',
    'Content-Script-Type',
    'Content-Security-Policy',
    'Content-Style-Type',
    'Content-Transfer-Encoding',
    'Content-Type',
    'Content-Version',
    'Cookie',
    'Cost',
    'DAV',
    'DELETE',
    'DNT',
    'DPR',
    'Date',
    'Default-Style',
    'Delta-Base',
    'Depth',
    'Derived-From',
    'Destination',
    'Differential-ID',
    'Digest',
    'ETag',
    'Expect',
    'Expires',
    'Ext',
    'From',
    'GET',
    'GetProfile',
    'HEAD',
    'HTTP-date',
    'Host',
    'IM',
    'If',
    'If-Match',
    'If-Modified-Since',
    'If-None-Match',
    'If-Range',
    'If-Unmodified-Since',
    'Keep-Alive',
    'Label',
    'Last-Event-ID',
    'Last-Modified',
    'Link',
    'Location',
    'Lock-Token',
    'MIME-Version',
    'Man',
    'Max-Forwards',
    'Media-Range',
    'Message-ID',
    'Meter',
    'Negotiate',
    'Non-Compliance',
    'OPTION',
    'OPTIONS',
    'OWS',
    'Opt',
    'Optional',
    'Ordering-Type',
    'Origin',
    'Overwrite',
    'P3P',
    'PEP',
    'PICS-Label',
    'POST',
    'PUT',
    'Pep-Info',
    'Permanent',
    'Position',
    'Pragma',
    'ProfileObject',
    'Protocol',
    'Protocol-Query',
    'Protocol-Request',
    'Proxy-Authenticate',
    'Proxy-Authentication-Info',
    'Proxy-Authorization',
    'Proxy-Features',
    'Proxy-Instruction',
    'Public',
    'RWS',
    'Range',
    'Referer',
    'Refresh',
    'Resolution-Hint',
    'Resolver-Location',
    'Retry-After',
    'Safe',
    'Sec-Websocket-Extensions',
    'Sec-Websocket-Key',
    'Sec-Websocket-Origin',
    'Sec-Websocket-Protocol',
    'Sec-Websocket-Version',
    'Security-Scheme',
    'Server',
    'Set-Cookie',
    'Set-Cookie2',
    'SetProfile',
    'SoapAction',
    'Status',
    'Status-URI',
    'Strict-Transport-Security',
    'SubOK',
    'Subst',
    'Surrogate-Capability',
    'Surrogate-Control',
    'TCN',
    'TE',
    'TRACE',
    'Timeout',
    'Title',
    'Trailer',
    'Transfer-Encoding',
    'UA-Color',
    'UA-Media',
    'UA-Pixels',
    'UA-Resolution',
    'UA-Windowpixels',
    'URI',
    'Upgrade',
    'User-Agent',
    'Variant-Vary',
    'Vary',
    'Version',
    'Via',
    'Viewport-Width',
    'WWW-Authenticate',
    'Want-Digest',
    'Warning',
    'Width',
    'X-Content-Duration',
    'X-Content-Security-Policy',
    'X-Content-Type-Options',
    'X-CustomHeader',
    'X-DNSPrefetch-Control',
    'X-Forwarded-For',
    'X-Forwarded-Port',
    'X-Forwarded-Proto',
    'X-Frame-Options',
    'X-Modified',
    'X-OTHER',
    'X-PING',
    'X-PINGOTHER',
    'X-Powered-By',
    'X-Requested-With'
]

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            # if headers is not None:
            #     h['Access-Control-Allow-Headers'] = headers
            h['Access-Control-Allow-Headers'] = ','.join(accept_headers)
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)

    return decorator
