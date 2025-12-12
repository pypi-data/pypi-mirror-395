import json
import time
import jwt


from pytest_httpserver import HTTPServer
from werkzeug.wrappers import Response, Request


class TokenHandler:
    def __init__(self, url) -> None:
        self.url = url

    def handle_token(self, r: Request) -> Response:
        data = r.form.to_dict()
        if data is None:
            return Response(status=400)

        if data['grant_type'] == 'refresh_token':
            assert 'refresh_token' in data
            assert 'client_id' in data
            acc = jwt.encode({'user': 'test', 'exp': int(time.time()) + 60}, 'test')
            ref = jwt.encode({'exp': int(time.time() + 360)}, 'test')
            return Response(
                response=json.dumps({'access_token': acc, 'refresh_token': ref}),
                status=200,
                content_type='application/json'
            )

        if data['grant_type'] == 'urn:ietf:params:oauth:grant-type:device_code':
            assert 'device_code' in data
            assert 'client_id' in data
            acc = jwt.encode({'user': 'test', 'exp': int(time.time()) + 60}, 'test')
            ref = jwt.encode({'exp': int(time.time() + 480)}, 'test')
            return Response(
                response=json.dumps({'access_token': acc, 'refresh_token': ref}),
                status=200,
                content_type='application/json'
            )

        return Response(status=400)

    def handle_device(self, r: Request) -> Response:
        data = r.form.to_dict()
        if data is None:
            return Response(status=400)
        if 'client_id' not in data:
            return Response('no client_id in body', status=500)
        return Response(
            response=json.dumps({
                'verification_uri_complete': f'{self.url}/verify',
                'device_code': 'ABC-123',
                'expires_in': 61,
                'interval': 1
            }),
            status=200,
            content_type="application/json"
        )


def setup_server_auth_endpoints(httpserver: HTTPServer) -> HTTPServer:

    baseurl = httpserver.url_for('')
    th = TokenHandler(baseurl)

    httpserver.expect_request('/.well-known/openid-configuration').respond_with_json({
        'token_endpoint': f'{baseurl}/token',
        'device_authorization_endpoint': f'{baseurl}/device'
    })

    httpserver.expect_request('/token').respond_with_handler(th.handle_token)

    httpserver.expect_request('/device').respond_with_handler(th.handle_device)

    return httpserver
