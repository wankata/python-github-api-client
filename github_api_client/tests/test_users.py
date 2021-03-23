from unittest import TestCase
from .. import users


class UserModelTests(TestCase):
    def test_initialize_empty_sets_all_attrs_to_none(self):
        u = users.User()
        for attr in u.__slots__:
            self.assertEqual(getattr(u, attr), None)

    def test_initialize_with_invalid_attrs_raises_exception(self):
        with self.assertRaises(AttributeError):
            users.User({'not_valid_attribute': True})

    def test_assign_invalid_attrs_raises_exception(self):
        u = users.User()
        with self.assertRaises(AttributeError):
            u.not_valid_attribute = True

    def test_initialize_with_valid_attrs_sets_them_correct(self):
        u = users.User({'login': 'ivan', 'id': 5})
        self.assertEqual(u.login, 'ivan')
        self.assertEqual(u.id, 5)

    def test_assign_valid_attrs_sets_them_correct(self):
        u = users.User()
        u.login = 'ivan'
        u.id = 5
        self.assertEqual(u.login, 'ivan')
        self.assertEqual(u.id, 5)

    def test_initialize_with_valid_attrs_do_not_touch_the_other_attrs(self):
        user_dict = {'login': 'ivan', 'id': 5}
        u = users.User(user_dict)

        for attr in u.__slots__:
            if attr not in user_dict.keys():
                with self.subTest(attr=attr):
                    self.assertEqual(getattr(u, attr), None)

    def test_assign_valid_attrs_do_not_touch_the_other_attrs(self):
        u = users.User()
        u.login = 'ivan'
        u.id = 5

        for attr in u.__slots__:
            if attr not in ['login', 'id']:
                with self.subTest(attr=attr):
                    self.assertEqual(getattr(u, attr), None)
