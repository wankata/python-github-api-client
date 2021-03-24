import requests_mock

from requests.exceptions import HTTPError
from unittest import TestCase

from .. import helpers
from .. import settings


@requests_mock.Mocker()
class HelpersTests(TestCase):
    def test_get_helper_raises_exception_on_400(self, mock):
        mock.get(settings.API_URL, status_code=400)
        with self.assertRaises(HTTPError):
            helpers.get('')

    def test_get_helper_raises_exception_on_404(self, mock):
        mock.get(settings.API_URL, status_code=404)
        with self.assertRaises(HTTPError):
            helpers.get('')

    def test_get_helper_raises_exception_on_500(self, mock):
        mock.get(settings.API_URL, status_code=500)
        with self.assertRaises(HTTPError):
            helpers.get('')
