import requests

from urllib.parse import urljoin

from . import settings


def get(endpoint: str, auth: bool = True) -> requests.Response:
    url = urljoin(settings.API_URL, endpoint)
    headers = {'Authorization': f'token {settings.AUTH_TOKEN}'} if auth else {}

    response = requests.get(url, headers=headers)

    response.raise_for_status()

    return response
