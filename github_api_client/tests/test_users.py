import itertools
import requests_mock

from requests.exceptions import HTTPError
from unittest import TestCase
from urllib.parse import urljoin

from .. import exceptions as e
from .. import settings
from ..users import User, AuthenticatedUser, get_authenticated_user, get_user


class UserModelTests(TestCase):
    def setUp(self):
        self.slots = _calculate_slots(User)

    def test_slots_are_calculated_ok(self):
        self.assertEqual(self.slots, User.__slots__)

    def test_initialize_empty_sets_all_attrs_to_none(self):
        u = User()
        for attr in self.slots:
            self.assertEqual(getattr(u, attr), None)

    def test_initialize_with_invalid_attrs_raises_exception(self):
        with self.assertRaises(AttributeError):
            User({'not_valid_attribute': True})

    def test_assign_invalid_attrs_raises_exception(self):
        u = User()
        with self.assertRaises(AttributeError):
            u.not_valid_attribute = True

    def test_initialize_with_valid_attrs_sets_them_ok(self):
        u = User({'login': 'ivan', 'id': 5})
        self.assertEqual(u.login, 'ivan')
        self.assertEqual(u.id, 5)

    def test_assign_valid_attrs_sets_them_ok(self):
        u = User()
        u.login = 'ivan'
        u.id = 5
        self.assertEqual(u.login, 'ivan')
        self.assertEqual(u.id, 5)

    def test_initialize_with_valid_attrs_do_not_touch_the_other_attrs(self):
        user_dict = {'login': 'ivan', 'id': 5}
        u = User(user_dict)

        for attr in self.slots:
            if attr not in user_dict.keys():
                with self.subTest(attr=attr):
                    self.assertEqual(getattr(u, attr), None)

    def test_assign_valid_attrs_do_not_touch_the_other_attrs(self):
        u = User()
        u.login = 'ivan'
        u.id = 5

        for attr in self.slots:
            if attr not in ['login', 'id']:
                with self.subTest(attr=attr):
                    self.assertEqual(getattr(u, attr), None)


class AuthenticatedUserModelTests(TestCase):
    def setUp(self):
        self.slots = _calculate_slots(AuthenticatedUser)

    def test_slots_are_calculated_ok(self):
        correct_slots = User.__slots__ | AuthenticatedUser.__slots__
        self.assertEqual(self.slots, correct_slots)

    def test_initialize_empty_sets_all_attrs_to_none(self):
        u = AuthenticatedUser()
        for attr in self.slots:
            self.assertEqual(getattr(u, attr), None)

    def test_initialize_with_invalid_attrs_raises_exception(self):
        with self.assertRaises(AttributeError):
            AuthenticatedUser({'not_valid_attribute': True})

    def test_assign_invalid_attrs_raises_exception(self):
        u = AuthenticatedUser()
        with self.assertRaises(AttributeError):
            u.not_valid_attribute = True

    def test_initialize_with_valid_attrs_sets_them_ok(self):
        u = AuthenticatedUser({
            'login': 'ivan', 'id': 5,
            'total_private_repos': 10, 'two_factor_authentication': False,
            })

        self.assertEqual(u.login, 'ivan')
        self.assertEqual(u.id, 5)
        self.assertEqual(u.total_private_repos, 10)
        self.assertEqual(u.two_factor_authentication, False)

    def test_assign_valid_attrs_sets_them_ok(self):
        u = AuthenticatedUser()
        u.login = 'ivan'
        u.id = 5
        u.total_private_repos = 10
        u.two_factor_authentication = False

        self.assertEqual(u.login, 'ivan')
        self.assertEqual(u.id, 5)
        self.assertEqual(u.total_private_repos, 10)
        self.assertEqual(u.two_factor_authentication, False)

    def test_initialize_with_valid_attrs_do_not_touch_the_other_attrs(self):
        user_dict = {
            'login': 'ivan', 'id': 5,
            'total_private_repos': 10, 'two_factor_authentication': False,
            }
        u = AuthenticatedUser(user_dict)

        for attr in self.slots:
            if attr not in user_dict.keys():
                with self.subTest(attr=attr):
                    self.assertEqual(getattr(u, attr), None)

    def test_assign_valid_attrs_do_not_touch_the_other_attrs(self):
        u = AuthenticatedUser()
        u.login = 'ivan'
        u.id = 5
        u.total_private_repos = 10
        u.two_factor_authentication = False

        for attr in self.slots:
            if attr not in ['login', 'id', 'total_private_repos', 'two_factor_authentication']:
                with self.subTest(attr=attr):
                    self.assertEqual(getattr(u, attr), None)


@requests_mock.Mocker()
class GetAuthenticatedUserTests(TestCase):
    def test_get_authenticated_user_returns_correct_instance_and_data(self, mock):
        mock.get(urljoin(settings.API_URL, '/user'), json=_AUTHENTICATED_USER_JSON)
        user = get_authenticated_user()

        self.assertIsInstance(user, AuthenticatedUser)
        self.assertEqual(user.name, 'The Mocked Octocat')

    def test_get_authenticated_user_raises_unsupported_status_exception_on_302(self, mock):
        mock.get(urljoin(settings.API_URL, '/user'), status_code=302)

        with self.assertRaises(e.UnsupportedResponseStatus):
            get_authenticated_user()

    def test_get_authenticated_user_raises_http_error_on_500(self, mock):
        mock.get(urljoin(settings.API_URL, '/user'), status_code=500)

        with self.assertRaises(HTTPError):
            get_authenticated_user()


@requests_mock.Mocker()
class GetUserTests(TestCase):
    def test_get_user_returns_correct_instance_and_data(self, mock):
        mock.get(urljoin(settings.API_URL, '/users/octocat'), json=_USER_JSON)
        user = get_user('octocat')

        self.assertIsInstance(user, User)
        self.assertEqual(user.name, 'The Mocked Octocat')

    def test_get_user_raises_unsupported_status_exception_on_302(self, mock):
        mock.get(urljoin(settings.API_URL, '/users/octocat'), status_code=302)

        with self.assertRaises(e.UnsupportedResponseStatus):
            get_user('octocat')

    def test_get_user_raises_http_error_on_500(self, mock):
        mock.get(urljoin(settings.API_URL, '/users/octocat'), status_code=500)

        with self.assertRaises(HTTPError):
            get_user('octocat')


def _calculate_slots(_class):
    return frozenset(
        itertools.chain.from_iterable(
            getattr(cls, '__slots__', frozenset()) for cls in _class.__mro__
        ),
    )


_USER_JSON = {
    'login': 'octocat', 'id': 583231, 'node_id': 'MDQ6VXNlcjU4MzIzMQ==',
    'avatar_url': 'https://avatars.githubusercontent.com/u/583231?v=4', 'gravatar_id': '',
    'url': 'https://api.github.com/users/octocat', 'html_url': 'https://github.com/octocat',
    'followers_url': 'https://api.github.com/users/octocat/followers',
    'following_url': 'https://api.github.com/users/octocat/following{/other_user}',
    'gists_url': 'https://api.github.com/users/octocat/gists{/gist_id}',
    'starred_url': 'https://api.github.com/users/octocat/starred{/owner}{/repo}',
    'subscriptions_url': 'https://api.github.com/users/octocat/subscriptions',
    'organizations_url': 'https://api.github.com/users/octocat/orgs',
    'repos_url': 'https://api.github.com/users/octocat/repos',
    'events_url': 'https://api.github.com/users/octocat/events{/privacy}',
    'received_events_url': 'https://api.github.com/users/octocat/received_events',
    'type': 'User', 'site_admin': False, 'name': 'The Mocked Octocat', 'company': '@github',
    'blog': 'https://github.blog', 'location': 'San Francisco', 'email': None,
    'hireable': None, 'bio': None, 'twitter_username': None, 'public_repos': 8,
    'public_gists': 8, 'followers': 3605, 'following': 9,
    'created_at': '2011-01-25T18:44:36Z', 'updated_at': '2021-03-22T14:27:47Z',
}

_USER_PRIVATE_FIELDS = {
    'private_gists': 0, 'total_private_repos': 0, 'owned_private_repos': 0,
    'disk_usage': 54, 'collaborators': 0, 'two_factor_authentication': False,
    'plan': {
        'name': 'free', 'space': 976562499, 'collaborators': 0, 'private_repos': 10000,
    },
}

_AUTHENTICATED_USER_JSON = _USER_JSON | _USER_PRIVATE_FIELDS
