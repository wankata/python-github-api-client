import itertools
import requests

from .exceptions import UnsupportedResponseStatus
from .helpers import get


class User:
    """
    User model

    Container for all GitHub user attributes *except plan* information
    """

    __slots__ = frozenset(('login', 'id', 'node_id', 'avatar_url', 'gravatar_id', 'url', 'html_url',
                           'followers_url', 'following_url', 'gists_url', 'starred_url',
                           'subscriptions_url', 'organizations_url', 'repos_url', 'events_url',
                           'received_events_url', 'type', 'site_admin', 'name', 'company', 'blog',
                           'location', 'email', 'hireable', 'bio', 'twitter_username',
                           'public_repos', 'public_gists', 'followers', 'following', 'created_at',
                           'updated_at'))

    def __init__(self, initial: dict = None):
        """
        All not provided user attributes will be set to None.
        Non-allowed attributes raise AttributeError with list of the incorrect attrs provided.
        """

        if initial is None:
            initial = {}

        dict_keys = set(initial)

        # Get all slots of the class and it's parents
        slots = frozenset(
            itertools.chain.from_iterable(
                getattr(cls, '__slots__', frozenset()) for cls in type(self).__mro__
            ),
        )

        if not dict_keys.issubset(slots):
            raise AttributeError(*(dict_keys - slots))

        for attr in slots:
            setattr(self, attr, initial.get(attr, None))


class AuthenticatedUser(User):
    __slots__ = frozenset(('private_gists', 'total_private_repos', 'owned_private_repos',
                           'disk_usage', 'collaborators', 'two_factor_authentication', 'plan'))


def get_authenticated_user() -> AuthenticatedUser:
    """
    https://docs.github.com/en/rest/reference/users#get-the-authenticated-user
    """

    url = '/user'

    response: requests.Response = get(url)

    if response.status_code == 200:
        return AuthenticatedUser(response.json())
    else:
        raise UnsupportedResponseStatus(response.status_code)


def get_user(user: str) -> User:
    """
    https://docs.github.com/en/rest/reference/users#get-a-user
    """

    url = f'/users/{user}'

    response: requests.Response = get(url)

    if response.status_code == 200:
        return AuthenticatedUser(response.json())
    else:
        raise UnsupportedResponseStatus(response.status_code)
