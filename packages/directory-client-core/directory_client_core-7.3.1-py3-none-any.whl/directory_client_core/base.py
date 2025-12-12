import abc
import json
import logging
import urllib.parse as urlparse

from monotonic import monotonic
import requests

from sigauth.helpers import RequestSigner


logger = logging.getLogger(__name__)


class AbstractAPIClient(abc.ABC):

    @property
    @abc.abstractmethod
    def version():
        pass

    def __init__(self, base_url, api_key, sender_id, timeout):
        self.base_url = base_url
        self.request_signer = RequestSigner(
            secret=api_key, sender_id=sender_id
        )
        self.timeout = timeout

    def put(self, url, data, authenticator=None):
        return self.request(
            url=url,
            method="PUT",
            content_type="application/json",
            data=json.dumps(data),
            authenticator=authenticator,
        )

    def patch(self, url, data, files=None, authenticator=None):
        if files:
            response = self.request(
                url=url,
                method="PATCH",
                data=data,
                files=files,
                authenticator=authenticator
            )
        else:
            response = self.request(
                url=url,
                method="PATCH",
                content_type="application/json",
                data=json.dumps(data),
                authenticator=authenticator,
            )
        return response

    def get(self, url, params=None, authenticator=None, cache_control=None):
        return self.request(
            url=url,
            method="GET",
            params=params,
            authenticator=authenticator,
            cache_control=cache_control,
        )

    def post(self, url, data={}, files=None, authenticator=None, csrf_token=None, cookies=None, convert_data_to_json=True, content_type='application/json', allow_redirects=True, header_origin=None, header_referer=None):  # noqa:E501
        data = json.dumps(data) if convert_data_to_json else data
        if files:
            response = self.request(
                url=url,
                method="POST",
                data=data,
                files=files,
                authenticator=authenticator,
                csrf_token=csrf_token,
                cookies=cookies,
                content_type=content_type,
                allow_redirects=allow_redirects,
                header_origin=header_origin,
                header_referer=header_referer
            )
        else:
            response = self.request(
                url=url,
                method="POST",
                content_type=content_type,
                data=data,
                authenticator=authenticator,
                csrf_token=csrf_token,
                cookies=cookies,
                allow_redirects=allow_redirects,
                header_origin=header_origin,
                header_referer=header_referer
            )
        return response

    def delete(self, url, data=None, authenticator=None):
        return self.request(
            url=url,
            method="DELETE",
            authenticator=authenticator,
            data=data,
        )

    @staticmethod
    def build_url(base_url, partial_url):
        """
        Makes sure the URL is built properly.

        >>> urllib.parse.urljoin('https://test.com/1/', '2/3')
        https://test.com/1/2/3
        >>> urllib.parse.urljoin('https://test.com/1/', '/2/3')
        https://test.com/2/3
        >>> urllib.parse.urljoin('https://test.com/1', '2/3')
        https://test.com/2/3'
        """
        if not base_url.endswith('/'):
            base_url += '/'
        if partial_url.startswith('/'):
            partial_url = partial_url[1:]

        return urlparse.urljoin(base_url, partial_url)

    def request(
        self, method, url, content_type=None, data=None, params=None,
        files=None, authenticator=None, cache_control=None, csrf_token=None, cookies=None, allow_redirects=True,
        header_origin=None, header_referer=None
    ):

        logger.debug("API request {} {}".format(method, url))
        headers = {
            "User-agent": "EXPORT-DIRECTORY-API-CLIENT/{}".format(self.version)
        }

        if authenticator:
            headers.update(authenticator.headers)

        if cache_control:
            headers.update(cache_control.headers)

        if content_type:
            headers["Content-type"] = content_type

        if csrf_token:
            headers['X-CSRFToken'] = csrf_token

        if header_origin:
            headers["Origin"] = header_origin

        if header_referer:
            headers["Referer"] = header_referer

        url = self.build_url(self.base_url, url)

        start_time = monotonic()

        try:
            return self.send(
                method=method,
                url=url,
                headers=headers,
                data=data,
                params=params,
                files=files,
                cookies=cookies,
                allow_redirects=allow_redirects
            )
        finally:
            elapsed_time = monotonic() - start_time
            logger.debug(
                "API {} request on {} finished in {}".format(
                    method, url, elapsed_time
                )
            )

    def sign_request(self, prepared_request):
        headers = self.request_signer.get_signature_headers(
            url=prepared_request.path_url,
            body=prepared_request.body,
            method=prepared_request.method,
            content_type=prepared_request.headers.get('Content-Type'),
        )
        prepared_request.headers.update(headers)
        return prepared_request

    def send(self, method, url, request=None, allow_redirects=True, *args, **kwargs):

        prepared_request = requests.Request(
            method, url, *args, **kwargs
        ).prepare()

        signed_request = self.sign_request(prepared_request=prepared_request)
        return requests.Session().send(signed_request, timeout=self.timeout, allow_redirects=allow_redirects)
