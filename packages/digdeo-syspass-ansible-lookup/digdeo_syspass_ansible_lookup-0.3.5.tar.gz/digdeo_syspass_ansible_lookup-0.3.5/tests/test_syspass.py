# This file is part of Ansible Lookup SysPass
#
# Copyright (C) 2020  DigDeo SAS
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
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import unittest
import random
import string
import uuid
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../ansible/plugins/lookup'))

from syspass import LookupModule
from syspassclient.syspassclient import SyspassClient
from syspassclient.config import Config

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def random_string(choice=string.ascii_lowercase, length=40, prefix=None):
    """
    Generate a random string of fixed length

    :param choice:
    :param length: the length of the returned string
    :type length: int
    :param prefix: use a prefix
    :type prefix: str or None
    :return: a string build with random function
    :rtype: str
    """
    if prefix is None:
        prefix = ""
    if type(prefix) != str:
        raise TypeError("'prefix' parameter must be a str type")

    return "{0}{1}".format(
        prefix,
        "".join(random.choice(choice) for _ in range(length))
    )


class TestSyspass(unittest.TestCase):
    def setUp(self):
        self.lookup_module = LookupModule()
        self.lookup_module.syspass_api_url = 'https://vaultprep.cust.digdeo.fr/api.php'
        self.lookup_module.syspass_api_version = '3.1'
        self.lookup_module.syspass_auth_token = '1f43f5473165e0b37d33e8a992e935bc95d1172f97c3fd73a3ba660f85b65eda'
        self.lookup_module.syspass_debug = True
        self.lookup_module.syspass_debug_level = 3
        self.lookup_module.syspass_verbose = True
        self.lookup_module.syspass_verbose_level = 3
        self.lookup_module.syspass_verify_ssl = True
        self.lookup_module.syspass_token_pass = r'_>Zas)?$kO8ThmhlFpZf<\*&\}YInJT~8jP@ec{wt8XSMAn;?_'

        self.lookup_module.import_DD_SYSPASS_vars()
        self.lookup_module.syspass_client = SyspassClient(
            use_by_lookup=True,
            debug=True,
            debug_level=3,
            verbose=True,
            verbose_level=3
        )
        self.lookup_module.impose_DD_SYSPASS_vars()

    def test_ascii_letters(self):
        self.assertEqual('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', self.lookup_module.ascii_letters)

    def test_digits(self):
        self.assertEqual('0123456789', self.lookup_module.digits)

    def test_allowed_punctuation(self):
        self.assertEqual('-_|./?=+()[]~*{}#', self.lookup_module.allowed_punctuation)

    def test_verbose(self):
        self.lookup_module.verbose = False
        self.assertFalse(self.lookup_module.verbose)
        self.lookup_module.verbose = True
        self.assertTrue(self.lookup_module.verbose)
        self.lookup_module.verbose = False
        self.assertFalse(self.lookup_module.verbose)
        self.assertRaises(TypeError, setattr, self.lookup_module, 'verbose', 42)

    def test_verbose_level(self):
        self.lookup_module.verbose_level = 0
        self.assertEqual(0, self.lookup_module.verbose_level)
        self.lookup_module.verbose_level = 42
        self.assertEqual(42, self.lookup_module.verbose_level)
        self.lookup_module.verbose_level = 0
        self.assertEqual(0, self.lookup_module.verbose_level)
        self.assertRaises(TypeError, setattr, self.lookup_module, 'verbose_level', 'Hello')

    def test_debug(self):
        self.lookup_module.debug = False
        self.assertFalse(self.lookup_module.debug)
        self.lookup_module.debug = True
        self.assertTrue(self.lookup_module.debug)
        self.lookup_module.debug = False
        self.assertFalse(self.lookup_module.debug)
        self.assertRaises(TypeError, setattr, self.lookup_module, 'debug', 42)

    def test_debug_level(self):
        self.lookup_module.debug_level = 0
        self.assertEqual(0, self.lookup_module.debug_level)
        self.lookup_module.debug_level = 42
        self.assertEqual(42, self.lookup_module.debug_level)
        self.lookup_module.debug_level = 0
        self.assertEqual(0, self.lookup_module.debug_level)
        self.assertRaises(TypeError, setattr, self.lookup_module, 'debug_level', 'Hello')

    def test_property_syspass_client(self):
        syspass_client = SyspassClient()
        self.assertTrue(isinstance(syspass_client, SyspassClient))

        self.lookup_module.syspass_client = syspass_client
        self.assertTrue(isinstance(self.lookup_module.syspass_client, SyspassClient))
        self.assertEqual(syspass_client, self.lookup_module.syspass_client)

        self.assertRaises(TypeError, setattr, self.lookup_module, 'syspass_client', 42)

    def test_gen_password(self):
        self.assertIsNone(getattr(self.lookup_module, 'password'))
        # self.assertEqual(40, len(self.lookup_module.password))

        self.lookup_module.params = {"password": None}
        self.lookup_module.gen_password()

        self.assertEqual(len(self.lookup_module.password), 40)
        for char in self.lookup_module.password:
            self.assertTrue(char in str(self.lookup_module.chars))

        self.assertNotEqual("42", self.lookup_module.password)
        params = {
            "password": "42424242",
            "psswd_length": 40
        }
        self.lookup_module.params = params
        self.lookup_module.gen_password()
        self.assertEqual(self.lookup_module.password_length, len(self.lookup_module.password))

        params = {
            "psswd_length": 40
        }
        self.lookup_module.params = params
        self.lookup_module.gen_password()
        self.assertEqual(params['psswd_length'], len(self.lookup_module.password))

        params = {
            "password": None,
        }
        self.lookup_module.params = params
        self.assertEqual(self.lookup_module.password_length, len(self.lookup_module.password))
        self.assertEqual(self.lookup_module.password_length_max, 100)
        self.assertEqual(self.lookup_module.password_length_min, 8)

    def test__gen_candidate_chars(self):
        self.assertEqual(self.lookup_module._gen_candidate_chars(["digits", "?|"]), "0123456789")
        self.assertEqual(
            self.lookup_module._gen_candidate_chars(characters=["ascii_letters", 'Hello.42']),
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        )
        self.assertEqual(
            self.lookup_module._gen_candidate_chars(characters=["allowed_punctuation", 'Hello.42']),
            "-_|./?=+()[]~*{}#"
        )
        self.assertEqual(
            self.lookup_module._gen_candidate_chars(characters=["allowed_punctuation", 'digits']),
            "0123456789-_|./?=+()[]~*{}#"
        )
        self.assertEqual(
            self.lookup_module._gen_candidate_chars(characters=["ascii_letters", "allowed_punctuation", 'digits']),
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_|./?=+()[]~*{}#"
        )

        self.assertRaises(TypeError, self.lookup_module._gen_candidate_chars, characters=None)
        self.assertRaises(TypeError, self.lookup_module._gen_candidate_chars)
        self.assertRaises(ValueError, self.lookup_module._gen_candidate_chars, characters=['Hello.42'])

    def test__account_exist(self):
        self.assertIsNone(self.lookup_module._account_exist(text="Pikadois Pauluffe"))

    def test__account_create(self):
        conf = Config()

        # prepare a category
        category_random_name = random_string(length=20, prefix="category_test_")
        req = self.lookup_module.syspass_client.category_create(
            name=category_random_name,
            description='a category for tests'
        )

        actual_category_id = req

        req = self.lookup_module.syspass_client.category_search(
            text=category_random_name
        )

        found_category_id = req
        self.assertEqual(actual_category_id, found_category_id)

        # prepare a customer
        # create a client
        client_random_name = random_string()
        actual_client_id = self.lookup_module.syspass_client.client_create(
            name=client_random_name,
            description='a Client for tests'
        )

        req = self.lookup_module.syspass_client.client_search(
            text=client_random_name
        )

        found_client_id = req

        self.assertEqual(actual_client_id, found_client_id)
        self.lookup_module.term = 'SUPER'
        self.lookup_module.variables = {
            'ansible_hostname': 'hostname.42.ici'
        }

        uniq_random = f'{uuid.uuid4().hex[:6]}'

        self.lookup_module.kwargs = {
            "account": f'Account_{uniq_random}',
            "privategroup": None,
            "expireDate": 0,
            "login": f'Login_{uniq_random}',
            "category": category_random_name,
            "customer": f'Customer_{uniq_random}',
            "customer_desc": 'Test is a good customer',
            "tags": ['Prod', 'MySQL'],
            "url": 'mysite.com',
            "notes": 'ToTP required for this account',
            "chars": ['ascii_letters', 'digits'],
            "psswd_length": 20,
            "private": False,
            "state": 'present',
            "categoryId": actual_category_id

        }
        self.lookup_module._ensure_params()
        # returned_dict = self.lookup_module._account_create()

        # clean up
        self.lookup_module.syspass_client.client_delete(
            cid=actual_client_id
        )
        req = self.lookup_module.syspass_client.client_search(
            authToken=conf.authToken,
            text=client_random_name
        )
        self.assertIsNone(req)

        # Last line
        random_term = random_string()
        random_hostname = random_string()
        random_login = random_string()

        self.lookup_module.term = '{0}'.format(random_term)
        self.lookup_module.variables = {
            'ansible_hostname': '{0}.42.ici'.format(random_hostname)
        }
        random_category_id = random.randint(42, 424242)
        self.lookup_module.term = random_term
        self.lookup_module.variables = {
            'ansible_hostname': 'hostname.42.ici'
        }
        self.lookup_module.kwargs = {
            "account": f'Account_{uniq_random}',
            "privategroup": None,
            "expireDate": 0,
            "login": f'Login_{uniq_random}',
            "category": category_random_name,
            "customer": f'Customer_{uniq_random}',
            "customer_desc": 'Test is a good customer',
            "tags": ['Prod', 'MySQL'],
            "url": 'mysite.com',
            "notes": 'ToTP required for this account',
            "chars": ['ascii_letters', 'digits'],
            "psswd_length": 20,
            "private": False,
            "state": 'present',
            "categoryId": random_category_id

        }
        self.lookup_module._ensure_params()
        self.lookup_module._account_create()

    def test__account_exist_or_create(self):
        conf = Config()

        uniq_random = f'{uuid.uuid4().hex[:6]}'

        # prepare a category
        category_random_name = random_string(length=20, prefix="category_test_")
        req = self.lookup_module.syspass_client.category_create(
            authToken=conf.authToken,
            name=category_random_name,
            description='a category for tests'
        )

        actual_category_id = req

        req = self.lookup_module.syspass_client.category_search(
            authToken=conf.authToken,
            text=category_random_name
        )

        found_category_id = req
        self.assertEqual(actual_category_id, found_category_id)
        self.lookup_module.variables = {
            "ansible_hostname": "hostname.42"
        }
        self.lookup_module.term = 'Account Name minimal'
        self.lookup_module.kwargs = {
            "privategroup": None,
            "expireDate": 0,
            "login": f'Login_{uniq_random}',
            "category": category_random_name,
            "customer": f'Customer_{uniq_random}',
            "customer_desc": 'Test is a good customer',
            "tags": ['Prod', 'MySQL'],
            "url": 'mysite.com',
            "notes": 'ToTP required for this account',
            "chars": ['ascii_letters', 'digits'],
            "psswd_length": 20,
            "private": False,
            "state": 'present',
            "categoryId": actual_category_id,

        }
        self.lookup_module._ensure_params()
        self.lookup_module._account_exist_or_create()

        self.lookup_module.variables = {
            "ansible_hostname": "hostname.42"
        }
        self.lookup_module.term = 'Account Name minimal'
        self.lookup_module.kwargs = {
            "privategroup": None,
            "expireDate": 0,
            "login": f'Login_{uniq_random}',
            "category": category_random_name,
            "customer": f'Customer_{uniq_random}',
            "customer_desc": 'Test is a good customer',
            "tags": ['Prod', 'MySQL'],
            "url": 'mysite.com',
            "notes": 'ToTP required for this account',
            "chars": ['ascii_letters', 'digits'],
            "psswd_length": 20,
            "private": False,
            "state": 'absent',
            "categoryId": actual_category_id

        }
        self.lookup_module.state = 'absent'
        self.lookup_module._ensure_params()
        self.lookup_module._account_exist_or_create()

    def test__ensure_params(self):

        uniq_random = f'{uuid.uuid4().hex[:6]}'
        category_random_name = random_string(length=20, prefix="category_test_")

        self.lookup_module.kwargs = {
            "account": f'Account_{uniq_random}',
            "privategroup": False,
            "expireDate": 0,
            "login": f'Login_{uniq_random}',
            "category": category_random_name,
            "customer": f'Customer_{uniq_random}',
            "customer_desc": 'Test is a good customer',
            "tags": ['Prod', 'MySQL'],
            "url": 'mysite.com',
            "notes": 'ToTP required for this account',
            "chars": ['ascii_letters', 'digits'],
            "psswd_length": 20,
            "private": False,
            "state": 'present',
            "categoryId": 42
        }
        self.lookup_module.variables = {
            "ansible_hostname": "hostname.42"
        }
        self.lookup_module.term = 'Account Name minimal'
        self.lookup_module._ensure_params()

        self.assertEqual('Account Name minimal', self.lookup_module.account)
        self.assertEqual(0, self.lookup_module.privategroup)
        self.assertEqual(0, self.lookup_module.expireDate)
        self.assertEqual(f'Login_{uniq_random}', self.lookup_module.login)
        self.assertEqual(category_random_name, self.lookup_module.category)
        self.assertEqual(f'Customer_{uniq_random}', self.lookup_module.customer)
        self.assertEqual('ToTP required for this account', self.lookup_module.notes)
        self.assertEqual('hostname', self.lookup_module.hostname)

        self.lookup_module.kwargs = {
            "account": f'Account_{uniq_random}',
            "privategroup": False,
            "expireDate": 0,
            "login": 'login.42',
            "category": category_random_name,
            "customer": f'Customer_{uniq_random}',
            "customer_desc": 'Test is a good customer',
            "tags": ['Prod', 'MySQL'],
            "url": 'mysite.com',
            "notes": 'ToTP required for this account',
            "chars": ['ascii_letters', 'digits'],
            "psswd_length": 20,
            "private": False,
            "state": 'present',
            "categoryId": 42
        }
        self.lookup_module.variables = {
            "ansible_hostname": "hostname.42"
        }
        self.lookup_module.term = {
            'env': 'tests',
            'url_listen': 'hostname.42.ici',
            'login': 'login.42',
            'category': 'category.42',
            'app': 'tests'

        }
        self.lookup_module._ensure_params()
        self.assertEqual(f'hostname login.42 {category_random_name}', self.lookup_module.account)
        self.assertEqual(0, self.lookup_module.privategroup)
        self.assertEqual(0, self.lookup_module.expireDate)
        self.assertEqual('login.42', self.lookup_module.login)
        self.assertEqual(category_random_name, self.lookup_module.category)
        self.assertEqual(f'Customer_{uniq_random}', self.lookup_module.customer)
        self.assertEqual('ToTP required for this account', self.lookup_module.notes)
        self.assertEqual('hostname', self.lookup_module.hostname)

        # Test 3
        self.lookup_module.kwargs = {
            "account": f'Account_{uuid.uuid4().hex[:6]}',
            "privategroup": False,
            "expireDate": 0,
            "login": 'mylogin',
            "category": 'category.42',
            "customer": 'DDPREP',
            "customer_desc": 'Test is a good customer',
            "tags": ['Prod', 'MySQL'],
            "url": 'mysite.com',
            "notes": 'ToTP required for this account',
            "chars": ['ascii_letters', 'digits'],
            "psswd_length": 20,
            "private": False,
            "state": 'present',
            "categoryId": 42
        }
        self.lookup_module.variables = {
            "ansible_hostname": "hostname.42"
        }
        self.lookup_module.term = {
            'url_listen': 'hostname.42.ici',
            'login': 'login.42',
            'category': 'category.42',
            'app': 'tests',
            'state': 'present',
            'password': 'ithavenotpassword'

        }
        self.lookup_module._ensure_params()
        self.assertEqual(f'hostname tests category.42', self.lookup_module.account)
        self.assertEqual(0, self.lookup_module.privategroup)
        self.assertEqual(0, self.lookup_module.expireDate)
        self.assertEqual('mylogin', self.lookup_module.login)
        self.assertEqual('category.42', self.lookup_module.category)
        self.assertEqual('DDPREP', self.lookup_module.customer)
        self.assertEqual('ToTP required for this account', self.lookup_module.notes)
        self.assertEqual('hostname', self.lookup_module.hostname)
        self.assertEqual(['Prod', 'MySQL', 'APP'], self.lookup_module.tags)

    def test__ensure_everything_is_right(self):
        self.lookup_module.gen_password()
        self.lookup_module.hostname = "hello.42.hostname"
        self.lookup_module.account = "hello.42.account"
        self.lookup_module.login = "hello.42.login"
        self.lookup_module.category = "hello.42.category"
        self.lookup_module.customer = "hello.42.customer"
        self.lookup_module._ensure_everything_is_right()

        self.lookup_module = LookupModule()

        self.assertRaises(ValueError, self.lookup_module._ensure_everything_is_right)

    def test__ensure_category_id_exist(self):
        self.lookup_module.category = 'category_{0}'.format(random_string())
        return_1 = self.lookup_module._ensure_category_id_exist()
        self.lookup_module.category = 'category_{0}'.format(random_string())
        return_2 = self.lookup_module._ensure_category_id_exist()
        self.assertNotEqual(return_1, return_2)

        self.assertRaises(TypeError, self.lookup_module._ensure_category_id_exist, category=42)
        self.assertRaises(ValueError, self.lookup_module._ensure_category_id_exist, category="")

    def test__ensure_customer_id_exist(self):
        self.lookup_module.customer = 'customer_{0}'.format(random_string())
        return_1 = self.lookup_module._ensure_customer_id_exist()
        self.lookup_module.customer = 'customer_{0}'.format(random_string())
        return_2 = self.lookup_module._ensure_customer_id_exist()
        self.assertNotEqual(return_1, return_2)

        self.assertRaises(TypeError, self.lookup_module._ensure_customer_id_exist, customer=42)
        self.assertRaises(ValueError, self.lookup_module._ensure_customer_id_exist, customer="")

    def test__ensure_user_group_id_exist(self):
        self.lookup_module.__customer_desc = None
        return_1 = self.lookup_module._ensure_user_group_id_exist(
            customer='customer_{0}'.format(random_string()),
            customer_desc=None
        )

        self.lookup_module.customer = 'customer_{0}'.format(random_string())
        self.lookup_module.customer_desc = 'description_{0}'.format(random_string())
        return_2 = self.lookup_module._ensure_user_group_id_exist()

        self.assertNotEqual(return_1, return_2)

        self.assertRaises(
            TypeError,
            self.lookup_module._ensure_user_group_id_exist,
            customer='customer_{0}'.format(random_string()),
            customer_desc=42
        )
        self.assertRaises(
            TypeError,
            self.lookup_module._ensure_user_group_id_exist,
            customer=42,
            customer_desc='description_{0}'.format(random_string())
        )
        self.assertRaises(
            ValueError,
            self.lookup_module._ensure_user_group_id_exist,
            customer="",
            customer_desc='description_{0}'.format(random_string())
        )

    def test__ensure_tags_id_exist(self):
        return_1 = self.lookup_module._ensure_tags_id_exist(tags=[random_string(), random_string(), random_string()])

        self.assertTrue(type(return_1) == list)
        self.assertTrue(type(return_1[0]) == int)
        self.assertTrue(type(return_1[1]) == int)
        self.assertTrue(type(return_1[2]) == int)

        self.lookup_module.tags = [random_string(), random_string(), random_string()]

        return_2 = self.lookup_module._ensure_tags_id_exist()
        self.assertTrue(type(return_2) == list)
        self.assertTrue(type(return_2[0]) == int)
        self.assertTrue(type(return_2[1]) == int)
        self.assertTrue(type(return_2[2]) == int)

        self.assertRaises(
            TypeError,
            self.lookup_module._ensure_tags_id_exist,
            tags=42
        )

    def test_term_property(self):
        self.lookup_module.term = {'hello': 42}
        self.assertEqual(42, self.lookup_module.term['hello'])

        setattr(self.lookup_module, 'term', None)
        self.assertIsNone(self.lookup_module.term)

        self.lookup_module.term = 'Hello'
        self.assertEqual('Hello', self.lookup_module.term)

        self.lookup_module.term = ['Hello']
        self.assertEqual('Hello', self.lookup_module.term)

        self.assertRaises(TypeError, setattr, self.lookup_module, 'term', 42)

    def test_variables_property(self):
        self.lookup_module.variables = {'Hello': 42}
        self.assertEqual({'Hello': 42}, self.lookup_module.variables)

        self.lookup_module.variables = None
        self.assertEqual({}, self.lookup_module.variables)

        self.assertRaises(TypeError, setattr, self.lookup_module, 'variables', 42)

    def test_kwargs_property(self):
        self.lookup_module.kwargs = {'Hello': 42}
        self.assertEqual(42, self.lookup_module.kwargs['Hello'])
        # self.lookup_module.kwargs = None
        # self.assertIsNone(self.lookup_module.kwargs)

        self.assertRaises(TypeError, setattr, self.lookup_module, 'kwargs', 42)

    def test_params_property(self):
        self.lookup_module.params = 42
        self.assertEqual(42, self.lookup_module.params)
        self.lookup_module.params = 'Hello'
        self.assertEqual('Hello', self.lookup_module.params)

    def test_syspass_auth_token(self):
        self.lookup_module.syspass_auth_token = "Hello.42"
        self.assertEqual("Hello.42", self.lookup_module.syspass_auth_token)
        self.lookup_module.syspass_auth_token = None
        self.assertIsNone(self.lookup_module.syspass_auth_token)

        self.assertRaises(TypeError, setattr, self.lookup_module, 'syspass_auth_token', 42)

    def test_syspass_token_pass(self):
        self.lookup_module.syspass_token_pass = "Hello.42"
        self.assertEqual("Hello.42", self.lookup_module.syspass_token_pass)
        self.lookup_module.syspass_token_pass = None
        self.assertIsNone(self.lookup_module.syspass_token_pass)

        self.assertRaises(TypeError, setattr, self.lookup_module, 'syspass_token_pass', 42)

    def test_syspass_verify_ssl(self):
        self.lookup_module.syspass_verify_ssl = True
        self.assertTrue(self.lookup_module.syspass_verify_ssl)

        self.lookup_module.syspass_verify_ssl = None
        self.assertFalse(self.lookup_module.syspass_verify_ssl)

        self.assertRaises(TypeError, setattr, self.lookup_module, 'syspass_verify_ssl', 42)

    def test_syspass_api_url(self):
        self.lookup_module.syspass_api_url = "Hello.42"
        self.assertEqual("Hello.42", self.lookup_module.syspass_api_url)
        self.lookup_module.syspass_api_url = None
        self.assertIsNone(self.lookup_module.syspass_api_url)

        self.assertRaises(TypeError, setattr, self.lookup_module, 'syspass_api_url', 42)

    def test_syspass_api_version(self):
        self.lookup_module.syspass_api_version = "3.0"
        self.assertEqual("3.0", self.lookup_module.syspass_api_version)
        self.lookup_module.syspass_api_version = None
        self.assertIsNone(self.lookup_module.syspass_api_version)

        self.assertRaises(TypeError, setattr, self.lookup_module, 'syspass_api_version', 42)

    def test_syspass_debug(self):
        self.lookup_module.syspass_debug = True
        self.assertTrue(self.lookup_module.syspass_debug)

        self.lookup_module.syspass_debug = None
        self.assertFalse(self.lookup_module.syspass_debug)

        self.assertRaises(TypeError, setattr, self.lookup_module, 'syspass_debug', 42)

    def test_syspass_debug_level(self):
        self.lookup_module.syspass_debug_level = 3
        self.assertEqual(3, self.lookup_module.syspass_debug_level)
        self.lookup_module.syspass_debug_level = None
        self.assertEqual(0, self.lookup_module.syspass_debug_level)

        self.assertRaises(TypeError, setattr, self.lookup_module, 'syspass_debug_level', 'Hello.42')

    def test_syspass_verbose(self):
        self.lookup_module.syspass_verbose = True
        self.assertTrue(self.lookup_module.syspass_verbose)

        self.lookup_module.syspass_verbose = None
        self.assertFalse(self.lookup_module.syspass_verbose)

        self.assertRaises(TypeError, setattr, self.lookup_module, 'syspass_verbose', 42)

    def test_syspass_verbose_level(self):
        self.lookup_module.syspass_verbose_level = 3
        self.assertEqual(3, self.lookup_module.syspass_verbose_level)
        self.lookup_module.syspass_verbose_level = None
        self.assertEqual(0, self.lookup_module.syspass_verbose_level)

        self.assertRaises(TypeError, setattr, self.lookup_module, 'syspass_verbose_level', 'Hello.42')

    def test_syspass_default_length(self):
        self.assertEqual(40, self.lookup_module.syspass_default_length)
        self.lookup_module.syspass_default_length = 8
        self.assertEqual(8, self.lookup_module.syspass_default_length)
        self.lookup_module.syspass_default_length = 40
        self.assertEqual(40, self.lookup_module.syspass_default_length)
        self.assertRaises(TypeError, setattr, self.lookup_module, 'syspass_default_length', 'Hello')
        self.assertRaises(ValueError, setattr, self.lookup_module, 'syspass_default_length', 0)
        self.assertRaises(ValueError, setattr, self.lookup_module, 'syspass_default_length', 101)

    def test_account(self):
        self.assertEqual(None, self.lookup_module.account)
        self.lookup_module.account = "Toto"
        self.assertEqual("Toto", self.lookup_module.account)
        self.assertRaises(TypeError, setattr, self.lookup_module, 'account', None)

    def test_password_length(self):
        self.assertEqual(self.lookup_module.password_length, self.lookup_module.syspass_default_length)
        self.lookup_module.password_length = 8
        self.assertEqual(8, self.lookup_module.password_length)
        self.lookup_module.password_length = 40
        self.assertEqual(40, self.lookup_module.password_length)
        self.assertRaises(TypeError, setattr, self.lookup_module, 'password_length', 'Hello')
        self.assertRaises(ValueError, setattr, self.lookup_module, 'password_length', 0)
        self.assertRaises(ValueError, setattr, self.lookup_module, 'password_length', 101)

    def test_password_length_min(self):
        # default value
        self.assertEqual(8, self.lookup_module.password_length_min)
        # set value
        self.lookup_module.password_length_min = 17
        self.assertEqual(17, self.lookup_module.password_length_min)
        # test clamp
        self.lookup_module.password_length_min = 0
        self.assertEqual(1, self.lookup_module.password_length_min)

        self.lookup_module.password_length_min = -1
        self.assertEqual(1, self.lookup_module.password_length_min)

        self.lookup_module.password_length_max = 8
        self.lookup_module.password_length_min = 8
        self.assertEqual(7, self.lookup_module.password_length_min)

        self.lookup_module.password_length_max = 4000
        self.lookup_module.password_length_min = 200
        self.assertEqual(199, self.lookup_module.password_length_min)

        self.assertRaises(TypeError, setattr, self.lookup_module, 'password_length_min', 'Hello')

    def test_password_length_max(self):
        # test default value
        self.assertEqual(100, self.lookup_module.password_length_max)
        # test test value
        self.lookup_module.password_length_max = 10
        self.assertEqual(10, self.lookup_module.password_length_max)
        # # test clamp
        self.lookup_module.password_length_max = 201
        self.assertEqual(200, self.lookup_module.password_length_max)

        self.lookup_module.password_length_max = -1
        self.assertEqual(self.lookup_module.password_length_min + 1, self.lookup_module.password_length_max)

        self.lookup_module.password_length_min = 8
        self.lookup_module.password_length_max = 8
        self.assertEqual(9, self.lookup_module.password_length_max)

        self.lookup_module.password_length_max = 4000
        self.lookup_module.password_length_min = 200
        self.assertEqual(199, self.lookup_module.password_length_min)

        self.assertRaises(TypeError, setattr, self.lookup_module, 'password_length_max', 'Hello')

    def test_password(self):
        self.lookup_module.password = "Hello42422"
        self.assertEqual('Hello42422', self.lookup_module.password)

        self.lookup_module.password = None
        self.assertEqual(self.lookup_module.syspass_default_length, len(self.lookup_module.password))

        self.assertRaises(ValueError, setattr, self.lookup_module, 'password', 'ToShort')
        self.assertRaises(ValueError, setattr, self.lookup_module, 'password',
                          'That_Is_Really_To_Long_For_A_Password_That_Is_Really_To_Long_For_A_Password_That_Is_Really_'
                          'To_Long_For_A_Password_That_Is_Really_To_Long_For_A_Password_That_Is_Really_To_Long_'
                          'For_A_Password_')

    def test_hostname(self):
        self.assertIsNone(self.lookup_module.hostname)
        self.lookup_module.hostname = 'hostname.42'
        self.assertEqual('hostname.42', self.lookup_module.hostname)
        self.lookup_module.hostname = None
        self.assertIsNone(self.lookup_module.hostname)
        self.assertRaises(TypeError, setattr, self.lookup_module, 'hostname', 42)

    def test_login(self):
        self.assertIsNone(getattr(self.lookup_module, 'login'))
        self.lookup_module.login = 'login.42'
        self.assertEqual('login.42', getattr(self.lookup_module, 'login'))
        self.lookup_module.login = None
        self.assertIsNone(getattr(self.lookup_module, 'login'))
        self.assertRaises(TypeError, setattr, self.lookup_module, 'login', 42)

    def test_category(self):
        self.assertIsNone(self.lookup_module.category)
        self.lookup_module.category = 'category.42'
        self.assertEqual('category.42', self.lookup_module.category)
        self.lookup_module.category = None
        self.assertIsNone(self.lookup_module.category)
        self.assertRaises(TypeError, setattr, self.lookup_module, 'category', 42)

    def test_customer(self):
        self.assertIsNone(self.lookup_module.customer)
        self.lookup_module.customer = 'customer.42'
        self.assertEqual('customer.42', self.lookup_module.customer)
        self.lookup_module.customer = None
        self.assertIsNone(self.lookup_module.customer)
        self.assertRaises(TypeError, setattr, self.lookup_module, 'customer', 42)

    def test_customer_desc(self):
        self.assertEqual("", self.lookup_module.customer_desc)
        self.lookup_module.customer_desc = 'customer_desc.42'
        self.assertEqual('customer_desc.42', self.lookup_module.customer_desc)
        self.lookup_module.customer_desc = None
        self.assertEqual("", self.lookup_module.customer_desc)
        self.assertRaises(TypeError, setattr, self.lookup_module, 'customer_desc', 42)

    def test_tags(self):
        self.assertEqual([], self.lookup_module.tags)
        self.lookup_module.tags = ['tags.42']
        self.assertEqual(['tags.42'], self.lookup_module.tags)
        self.lookup_module.tags = None
        self.assertEqual([], self.lookup_module.tags)
        self.assertRaises(TypeError, setattr, self.lookup_module, 'tags', 42)

    def test_notes(self):
        self.assertEqual("", self.lookup_module.notes)
        self.lookup_module.notes = 'notes.42'
        self.assertEqual('notes.42', self.lookup_module.notes)
        self.lookup_module.notes = None
        self.assertEqual("", self.lookup_module.notes)
        self.assertRaises(TypeError, setattr, self.lookup_module, 'notes', 42)

    def test_state(self):
        self.assertEqual('present', getattr(self.lookup_module, 'state'))
        self.lookup_module.state = 'absent'
        self.assertEqual('absent', getattr(self.lookup_module, 'state'))
        self.lookup_module.state = None
        self.assertEqual('present', getattr(self.lookup_module, 'state'))
        self.assertRaises(TypeError, setattr, self.lookup_module, 'state', 42)
        self.assertRaises(ValueError, setattr, self.lookup_module, 'state', '42')

    def test_private(self):
        self.assertEqual(0, self.lookup_module.private)
        self.lookup_module.private = 1
        self.assertEqual(1, self.lookup_module.private)
        self.lookup_module.private = 0
        self.assertEqual(0, self.lookup_module.private)
        self.lookup_module.private = -42
        self.assertEqual(0, self.lookup_module.private)
        self.lookup_module.private = 42
        self.assertEqual(1, self.lookup_module.private)
        self.lookup_module.private = None
        self.assertEqual(0, self.lookup_module.private)
        self.assertRaises(TypeError, setattr, self.lookup_module, 'private', 'Hello.42')

    def test_privategroup(self):
        self.assertEqual(0, self.lookup_module.privategroup)
        self.lookup_module.privategroup = 1
        self.assertEqual(1, self.lookup_module.privategroup)
        self.lookup_module.privategroup = 0
        self.assertEqual(0, self.lookup_module.privategroup)
        self.lookup_module.privategroup = -42
        self.assertEqual(0, self.lookup_module.privategroup)
        self.lookup_module.privategroup = 42
        self.assertEqual(1, self.lookup_module.privategroup)
        self.assertRaises(TypeError, setattr, self.lookup_module, 'privategroup', 'Hello.42')

    def test_expireDate(self):
        self.assertEqual(0, self.lookup_module.expireDate)
        self.lookup_module.expireDate = 1581589151
        self.assertEqual(1581589151, self.lookup_module.expireDate)
        self.lookup_module.expireDate = None
        self.assertEqual(0, self.lookup_module.expireDate)
        self.assertRaises(TypeError, setattr, self.lookup_module, 'expireDate', '42')

    def test__ensure_chars(self):
        self.assertEqual('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_|./?=+()[]~*{}#',
                         self.lookup_module.chars)
        self.lookup_module.kwargs = {'chars': ['ascii_letters']}
        self.lookup_module._ensure_chars()
        self.assertEqual('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', self.lookup_module.chars)

    def test__ensure_password_length(self):
        self.assertEqual(40, self.lookup_module.password_length)
        self.lookup_module._templar = {'_available_variables': {'syspass_default_length': 9}}
        self.lookup_module._ensure_password_length()
        self.assertEqual(9, self.lookup_module.password_length)

        self.lookup_module.kwargs = {'psswd_length': 24}
        self.lookup_module._ensure_password_length()
        self.assertEqual(24, self.lookup_module.password_length)

    def test__ensure_password(self):
        # Reset everything
        self.lookup_module.params = None
        self.lookup_module.kwargs = None
        self.lookup_module.variables = None
        self.lookup_module.password = None
        self.lookup_module._templar = None
        reset_password = self.lookup_module.password
        # Test params
        self.lookup_module.params = {'password': 'password.params.42'}
        self.lookup_module._ensure_password()
        self.assertNotEqual(reset_password, self.lookup_module.password)
        self.assertEqual('password.params.42', self.lookup_module.password)

        # Reset everything
        self.lookup_module.params = None
        self.lookup_module.kwargs = None
        self.lookup_module.variables = None
        self.lookup_module.password = None
        self.lookup_module._templar = None
        reset_password = self.lookup_module.password
        # Test _templar _available_variables
        self.lookup_module._templar = {
            '_available_variables': {'password': 'password._available_variables.42'}
        }
        self.lookup_module._ensure_password()
        self.assertNotEqual(reset_password, self.lookup_module.password)
        self.assertEqual('password._available_variables.42', self.lookup_module.password)

        # Reset everything
        self.lookup_module.params = None
        self.lookup_module.kwargs = None
        self.lookup_module.variables = None
        self.lookup_module.password = None
        self.lookup_module._templar = None
        reset_password = self.lookup_module.password
        # Test kwargs
        self.lookup_module.kwargs = {'password': 'password.kwargs.42'}
        self.lookup_module._ensure_password()
        self.assertNotEqual(reset_password, self.lookup_module.password)
        self.assertEqual('password.kwargs.42', self.lookup_module.password)

        # Reset everything
        self.lookup_module.params = None
        self.lookup_module.kwargs = None
        self.lookup_module.variables = None
        self.lookup_module.password = None
        self.lookup_module._templar = None
        reset_password = self.lookup_module.password
        # Test variables
        self.lookup_module.variables = {'password': 'password.variables.42'}
        self.lookup_module._ensure_password()
        self.assertNotEqual(reset_password, self.lookup_module.password)
        self.assertEqual('password.variables.42', self.lookup_module.password)

        # Reset everything
        self.lookup_module.params = None
        self.lookup_module.kwargs = None
        self.lookup_module.variables = None
        self.lookup_module.password = None
        self.lookup_module._templar = None
        reset_password = self.lookup_module.password
        # Test variables
        self.lookup_module._ensure_password()
        self.assertNotEqual(reset_password, self.lookup_module.password)

    def test__ensure_hostname(self):
        self.lookup_module.variables = {'ansible_hostname': 'hostname.42'}
        self.lookup_module._ensure_hostname()
        self.assertEqual('hostname', getattr(self.lookup_module, 'hostname'))

        self.lookup_module.variables = {'ansible_hostname': 'hostname.42',
                                        'host_override': 'host_override.42'}
        self.lookup_module._ensure_hostname()
        self.assertEqual('host_override.42', getattr(self.lookup_module, 'hostname'))

    def test__ensure_login(self):
        self.assertIsNone(getattr(self.lookup_module, 'login'))

        self.lookup_module._ensure_login()
        self.assertIsNone(self.lookup_module.login)
        self.lookup_module.term = {}
        self.lookup_module._ensure_login()
        self.assertEqual('', getattr(self.lookup_module, 'login'))
        self.lookup_module.kwargs = {'login': 'login.42'}
        self.lookup_module._ensure_login()
        self.assertEqual('login.42', getattr(self.lookup_module, 'login'))

    def test__ensure_category(self):
        self.assertIsNone(getattr(self.lookup_module, 'category'))
        self.lookup_module._ensure_category()
        self.assertIsNone(getattr(self.lookup_module, 'category'))

        self.lookup_module.kwargs = {'category': 'category.42'}
        self.lookup_module._ensure_category()
        self.assertEqual('category.42', getattr(self.lookup_module, 'category'))

    def test__ensure_customer(self):
        self.assertIsNone(getattr(self.lookup_module, 'customer'))

        self.lookup_module._ensure_customer()
        self.assertIsNone(getattr(self.lookup_module, 'customer'))

        self.lookup_module.kwargs = {'customer': 'customer.42'}
        self.lookup_module._ensure_customer()
        self.assertEqual('customer.42', getattr(self.lookup_module, 'customer'))

    def test__ensure_customer_desc(self):
        self.assertEqual('', getattr(self.lookup_module, 'customer_desc'))

        self.lookup_module._ensure_customer_desc()
        self.assertEqual('', getattr(self.lookup_module, 'customer_desc'))

        self.lookup_module.kwargs = {'customer_desc': 'customer_desc.42'}
        self.lookup_module._ensure_customer_desc()
        self.assertEqual('customer_desc.42', getattr(self.lookup_module, 'customer_desc'))

    def test__ensure_tags(self):
        self.assertEqual([], getattr(self.lookup_module, 'tags'))

        self.lookup_module._ensure_tags()
        self.assertEqual([], getattr(self.lookup_module, 'tags'))

        self.lookup_module.kwargs = {'tags': ['tags.42']}
        self.lookup_module._ensure_tags()
        self.assertEqual(['tags.42'], getattr(self.lookup_module, 'tags'))

    def test_url(self):
        self.assertIsNone(self.lookup_module.url)

        self.lookup_module.url = 'url.42'
        self.assertEqual('url.42', getattr(self.lookup_module, 'url'))

        self.lookup_module.url = None
        self.assertIsNone(self.lookup_module.url)

        self.lookup_module.term = {'url_listen': ['super.com']}
        self.lookup_module._ensure_url()
        self.assertEqual('super.com', getattr(self.lookup_module, 'url'))

        self.assertRaises(TypeError, setattr, self.lookup_module, 'url', 42)

    def test__ensure_url(self):
        self.assertEqual(None, getattr(self.lookup_module, 'url'))

        self.lookup_module._ensure_url()
        self.assertEqual(None, getattr(self.lookup_module, 'url'))

        self.lookup_module.kwargs = {'url': 'url.42'}
        self.lookup_module._ensure_url()
        self.assertEqual('url.42', getattr(self.lookup_module, 'url'))

    def test__ensure_notes(self):
        self.assertEqual('', getattr(self.lookup_module, 'notes'))

        self.lookup_module._ensure_notes()
        self.assertEqual('', getattr(self.lookup_module, 'notes'))

        self.lookup_module.kwargs = {'notes': 'notes.42'}
        self.lookup_module._ensure_notes()
        self.assertEqual('notes.42', getattr(self.lookup_module, 'notes'))

    def test__ensure_private(self):
        self.assertEqual(0, getattr(self.lookup_module, 'private'))

        self.lookup_module._ensure_private()
        self.assertEqual(0, getattr(self.lookup_module, 'private'))

        self.lookup_module.kwargs = {'private': True}
        self.lookup_module._ensure_private()
        self.assertEqual(1, getattr(self.lookup_module, 'private'))

        self.lookup_module.kwargs = {'private': False}
        self.lookup_module._ensure_private()
        self.assertEqual(0, getattr(self.lookup_module, 'private'))

        self.lookup_module.kwargs = {'private': 1}
        self.lookup_module._ensure_private()
        self.assertEqual(0, getattr(self.lookup_module, 'private'))

        self.lookup_module.kwargs = {'private': True}
        self.lookup_module._ensure_private()
        self.lookup_module.kwargs = {'private': 1}
        self.lookup_module._ensure_private()
        self.assertEqual(0, getattr(self.lookup_module, 'private'))

    def test__ensure_private_group(self):
        self.assertEqual(0, getattr(self.lookup_module, 'privategroup'))

        self.lookup_module._ensure_private()
        self.assertEqual(0, getattr(self.lookup_module, 'privategroup'))

        self.lookup_module.kwargs = {'privategroup': True}
        self.lookup_module._ensure_private_group()
        self.assertEqual(1, getattr(self.lookup_module, 'privategroup'))

        self.lookup_module.kwargs = {'privategroup': False}
        self.lookup_module._ensure_private_group()
        self.assertEqual(0, getattr(self.lookup_module, 'privategroup'))

        self.lookup_module.kwargs = {'privategroup': 1}
        self.lookup_module._ensure_private_group()
        self.assertEqual(0, getattr(self.lookup_module, 'privategroup'))

        self.lookup_module.kwargs = {'privategroup': True}
        self.lookup_module._ensure_private_group()
        self.lookup_module.kwargs = {'privategroup': 1}
        self.lookup_module._ensure_private_group()
        self.assertEqual(0, getattr(self.lookup_module, 'privategroup'))

    def test__ensure_expiration_date(self):
        self.assertEqual(0, getattr(self.lookup_module, 'expireDate'))

        self.lookup_module._ensure_expiration_date()
        self.assertEqual(0, getattr(self.lookup_module, 'expireDate'))

        self.lookup_module.kwargs = {'expireDate': 42}
        self.lookup_module._ensure_expiration_date()
        self.assertEqual(42, getattr(self.lookup_module, 'expireDate'))

    def test__ensure_state(self):
        self.assertEqual('present', getattr(self.lookup_module, 'state'))

        self.lookup_module._ensure_state()
        self.assertEqual('present', getattr(self.lookup_module, 'state'))

        self.lookup_module.kwargs = {'state': 'absent'}
        self.lookup_module._ensure_state()
        self.assertEqual('absent', getattr(self.lookup_module, 'state'))

        self.lookup_module.kwargs = {'state': 'absent'}
        self.lookup_module.term = {'state': 'present'}
        self.lookup_module._ensure_state()
        self.assertEqual('present', getattr(self.lookup_module, 'state'))

        self.lookup_module.kwargs = {'state': 'absent'}
        self.lookup_module.term = None
        self.lookup_module._ensure_state()
        self.assertEqual('absent', getattr(self.lookup_module, 'state'))

        self.lookup_module.kwargs = None
        self.lookup_module.term = None
        self.lookup_module._ensure_state()
        self.assertEqual('present', getattr(self.lookup_module, 'state'))

    def test__ensure_syspass_auth_token(self):
        self.lookup_module.syspass_auth_token = None
        self.assertIsNone(self.lookup_module.syspass_auth_token)

        self.lookup_module.variables = None
        self.lookup_module.kwargs = None
        self.lookup_module._templar = {
            '_available_variables': {'syspass_auth_token': 'syspass_auth_token.42'}}
        self.lookup_module._ensure_syspass_auth_token()
        self.assertEqual('syspass_auth_token.42', self.lookup_module.syspass_auth_token)

        self.lookup_module.syspass_auth_token = None
        self.assertIsNone(self.lookup_module.syspass_auth_token)

        self.lookup_module.variables = None
        self.lookup_module._templar = None
        self.lookup_module.kwargs = {'syspass_auth_token': 'syspass_auth_token.42'}
        self.lookup_module._ensure_syspass_auth_token()
        self.assertEqual('syspass_auth_token.42', self.lookup_module.syspass_auth_token)

        self.lookup_module.syspass_auth_token = None
        self.assertIsNone(self.lookup_module.syspass_auth_token)

        self.lookup_module.variables = {'syspass_auth_token': 'syspass_auth_token.42'}
        self.lookup_module._templar = None
        self.lookup_module.kwargs = None
        self.lookup_module._ensure_syspass_auth_token()
        self.assertEqual('syspass_auth_token.42', self.lookup_module.syspass_auth_token)

    def test__ensure_syspass_token_pass(self):
        self.lookup_module.syspass_token_pass = None
        self.assertIsNone(self.lookup_module.syspass_token_pass)

        self.lookup_module.variables = None
        self.lookup_module.kwargs = None
        self.lookup_module._templar = {
            '_available_variables': {'syspass_token_pass': 'syspass_token_pass.42'}
        }
        self.lookup_module._ensure_syspass_token_pass()
        self.assertEqual('syspass_token_pass.42', self.lookup_module.syspass_token_pass)

        self.lookup_module.syspass_token_pass = None
        self.assertIsNone(self.lookup_module.syspass_token_pass)

        self.lookup_module.variables = None
        self.lookup_module._templar = None
        self.lookup_module.kwargs = {'syspass_token_pass': 'syspass_token_pass.42'}
        self.lookup_module._ensure_syspass_token_pass()
        self.assertEqual('syspass_token_pass.42', self.lookup_module.syspass_token_pass)

        self.lookup_module.syspass_token_pass = None
        self.assertIsNone(self.lookup_module.syspass_token_pass)

        self.lookup_module.variables = {'syspass_token_pass': 'syspass_token_pass.42'}
        self.lookup_module._templar = None
        self.lookup_module.kwargs = None
        self.lookup_module._ensure_syspass_token_pass()
        self.assertEqual('syspass_token_pass.42', self.lookup_module.syspass_token_pass)

    def test__ensure_syspass_verify_ssl(self):
        self.lookup_module.syspass_verify_ssl = None
        self.assertFalse(self.lookup_module.syspass_verify_ssl)

        self.lookup_module.variables = None
        self.lookup_module.kwargs = None

        self.lookup_module._templar = {
            '_available_variables': {'syspass_verify_ssl': 'True'}
        }
        self.lookup_module._ensure_syspass_verify_ssl()
        self.assertTrue(self.lookup_module.syspass_verify_ssl)
        self.lookup_module._templar = {
            '_available_variables': {'syspass_verify_ssl': 'False'}
        }
        self.lookup_module._ensure_syspass_verify_ssl()
        self.assertFalse(self.lookup_module.syspass_verify_ssl)

        self.lookup_module.syspass_verify_ssl = None
        self.assertFalse(self.lookup_module.syspass_verify_ssl)

        self.lookup_module.variables = None
        self.lookup_module._templar = None

        self.lookup_module.kwargs = {'syspass_verify_ssl': 'True'}
        self.lookup_module._ensure_syspass_verify_ssl()
        self.assertTrue(self.lookup_module.syspass_verify_ssl)

        self.lookup_module.kwargs = {'syspass_verify_ssl': 'False'}
        self.lookup_module._ensure_syspass_verify_ssl()
        self.assertFalse(self.lookup_module.syspass_verify_ssl)

        self.lookup_module.syspass_verify_ssl = None
        self.assertFalse(self.lookup_module.syspass_verify_ssl)

        self.lookup_module._templar = None
        self.lookup_module.kwargs = None

        self.lookup_module.variables = {'syspass_verify_ssl': 'True'}
        self.lookup_module._ensure_syspass_verify_ssl()
        self.assertTrue(self.lookup_module.syspass_verify_ssl)

        self.lookup_module.variables = {'syspass_verify_ssl': 'False'}
        self.lookup_module._ensure_syspass_verify_ssl()
        self.assertFalse(self.lookup_module.syspass_verify_ssl)

    def test__ensure_syspass_api_url(self):
        self.lookup_module.syspass_api_url = None
        self.assertIsNone(self.lookup_module.syspass_api_url)

        self.lookup_module.variables = None
        self.lookup_module.kwargs = None
        self.lookup_module._templar = {
            '_available_variables': {'syspass_api_url': 'syspass_api_url.42'}}
        self.lookup_module._ensure_syspass_api_url()
        self.assertEqual('syspass_api_url.42', self.lookup_module.syspass_api_url)

        self.lookup_module.syspass_api_url = None
        self.assertIsNone(self.lookup_module.syspass_api_url)

        self.lookup_module.variables = None
        self.lookup_module._templar = None
        self.lookup_module.kwargs = {'syspass_api_url': 'syspass_api_url.42'}
        self.lookup_module._ensure_syspass_api_url()
        self.assertEqual('syspass_api_url.42', self.lookup_module.syspass_api_url)

        self.lookup_module.syspass_api_url = None
        self.assertIsNone(self.lookup_module.syspass_api_url)

        self.lookup_module.variables = {'syspass_api_url': 'syspass_api_url.42'}
        self.lookup_module._templar = None
        self.lookup_module.kwargs = None
        self.lookup_module._ensure_syspass_api_url()
        self.assertEqual('syspass_api_url.42', self.lookup_module.syspass_api_url)

    def test__ensure_syspass_api_version(self):
        self.lookup_module.syspass_api_version = None
        self.assertIsNone(self.lookup_module.syspass_api_version)

        self.lookup_module.variables = None
        self.lookup_module.kwargs = None
        self.lookup_module._templar = {
            '_available_variables': {'syspass_api_version': 'syspass_api_version.42'}
        }
        self.lookup_module._ensure_syspass_api_version()
        self.assertEqual('syspass_api_version.42', self.lookup_module.syspass_api_version)

        self.lookup_module.syspass_api_version = None
        self.assertIsNone(self.lookup_module.syspass_api_version)

        self.lookup_module.variables = None
        self.lookup_module._templar = None
        self.lookup_module.kwargs = {'syspass_api_version': 'syspass_api_version.42'}
        self.lookup_module._ensure_syspass_api_version()
        self.assertEqual('syspass_api_version.42', self.lookup_module.syspass_api_version)

        self.lookup_module.syspass_api_version = None
        self.assertIsNone(self.lookup_module.syspass_api_version)

        self.lookup_module.variables = {'syspass_api_version': 'syspass_api_version.42'}
        self.lookup_module._templar = None
        self.lookup_module.kwargs = None
        self.lookup_module._ensure_syspass_api_version()
        self.assertEqual('syspass_api_version.42', self.lookup_module.syspass_api_version)

    def test__ensure_syspass_debug(self):
        self.lookup_module.syspass_debug = None
        self.assertFalse(self.lookup_module.syspass_debug)

        self.lookup_module.variables = None
        self.lookup_module.kwargs = None
        self.lookup_module._templar = {
            '_available_variables': {'syspass_debug': 'True'}
        }
        self.lookup_module._ensure_syspass_debug()
        self.assertTrue(self.lookup_module.syspass_debug)

        self.lookup_module._templar = {
            '_available_variables': {'syspass_debug': 'False'}
        }
        self.lookup_module._ensure_syspass_debug()
        self.assertFalse(self.lookup_module.syspass_debug)

        self.lookup_module.syspass_debug = None
        self.assertFalse(self.lookup_module.syspass_debug)

        self.lookup_module.variables = None
        self.lookup_module._templar = None
        self.lookup_module.kwargs = {'syspass_debug': 'True'}
        self.lookup_module._ensure_syspass_debug()
        self.assertTrue(self.lookup_module.syspass_debug)

        self.lookup_module.kwargs = {'syspass_debug': 'False'}
        self.lookup_module._ensure_syspass_debug()
        self.assertFalse(self.lookup_module.syspass_debug)

        self.lookup_module.syspass_debug = None
        self.assertFalse(self.lookup_module.syspass_debug)

        self.lookup_module._templar = None
        self.lookup_module.kwargs = None
        self.lookup_module.variables = {'syspass_debug': 'True'}
        self.lookup_module._ensure_syspass_debug()
        self.assertTrue(self.lookup_module.syspass_debug)

        self.lookup_module.variables = {'syspass_debug': 'False'}
        self.lookup_module._ensure_syspass_debug()
        self.assertFalse(self.lookup_module.syspass_debug)

    def test__ensure_syspass_debug_level(self):
        self.lookup_module.syspass_debug_level = None
        self.assertEqual(0, self.lookup_module.syspass_debug_level)

        self.lookup_module.variables = None
        self.lookup_module.kwargs = None
        self.lookup_module._templar = {'_available_variables': {'syspass_debug_level': '42'}}
        self.lookup_module._ensure_syspass_debug_level()
        self.assertEqual(42, self.lookup_module.syspass_debug_level)

        self.lookup_module.syspass_debug_level = None
        self.assertEqual(0, self.lookup_module.syspass_debug_level)

        self.lookup_module.variables = None
        self.lookup_module._templar = None
        self.lookup_module.kwargs = {'syspass_debug_level': '42'}
        self.lookup_module._ensure_syspass_debug_level()
        self.assertEqual(42, self.lookup_module.syspass_debug_level)

        self.lookup_module.syspass_debug_level = None
        self.assertEqual(0, self.lookup_module.syspass_debug_level)

        self.lookup_module.variables = {'syspass_debug_level': '42'}
        self.lookup_module._templar = None
        self.lookup_module.kwargs = None
        self.lookup_module._ensure_syspass_debug_level()
        self.assertEqual(42, self.lookup_module.syspass_debug_level)

    def test__ensure_syspass_verbose(self):
        self.lookup_module.syspass_verbose = None
        self.assertFalse(self.lookup_module.syspass_verbose)

        self.lookup_module.variables = None
        self.lookup_module.kwargs = None
        self.lookup_module._templar = {
            '_available_variables': {'syspass_verbose': 'True'}
        }
        self.lookup_module._ensure_syspass_verbose()
        self.assertTrue(self.lookup_module.syspass_verbose)
        self.lookup_module._templar = {
            '_available_variables': {'syspass_verbose': 'False'}
        }
        self.lookup_module._ensure_syspass_verbose()
        self.assertFalse(self.lookup_module.syspass_verbose)

        self.lookup_module.syspass_verbose = None
        self.assertFalse(self.lookup_module.syspass_verbose)

        self.lookup_module.variables = None
        self.lookup_module._templar = None
        self.lookup_module.kwargs = {'syspass_verbose': 'True'}
        self.lookup_module._ensure_syspass_verbose()
        self.assertTrue(self.lookup_module.syspass_verbose)
        self.lookup_module.kwargs = {'syspass_verbose': 'False'}
        self.lookup_module._ensure_syspass_verbose()
        self.assertFalse(self.lookup_module.syspass_verbose)

        self.lookup_module.syspass_verbose = None
        self.assertFalse(self.lookup_module.syspass_verbose)

        self.lookup_module._templar = None
        self.lookup_module.kwargs = None
        self.lookup_module.variables = {'syspass_verbose': 'True'}
        self.lookup_module._ensure_syspass_verbose()
        self.assertTrue(self.lookup_module.syspass_verbose)
        self.lookup_module.variables = {'syspass_verbose': 'False'}
        self.lookup_module._ensure_syspass_verbose()
        self.assertFalse(self.lookup_module.syspass_verbose)

    def test__ensure_syspass_verbose_level(self):
        self.lookup_module.syspass_verbose_level = None
        self.assertEqual(0, self.lookup_module.syspass_verbose_level)

        self.lookup_module.variables = None
        self.lookup_module.kwargs = None
        self.lookup_module._templar = {'_available_variables': {'syspass_verbose_level': '42'}}
        self.lookup_module._ensure_syspass_verbose_level()
        self.assertEqual(42, self.lookup_module.syspass_verbose_level)

        self.lookup_module.syspass_verbose_level = None
        self.assertEqual(0, self.lookup_module.syspass_verbose_level)

        self.lookup_module.variables = None
        self.lookup_module._templar = None
        self.lookup_module.kwargs = {'syspass_verbose_level': '42'}
        self.lookup_module._ensure_syspass_verbose_level()
        self.assertEqual(42, self.lookup_module.syspass_verbose_level)

        self.lookup_module.syspass_verbose_level = None
        self.assertEqual(0, self.lookup_module.syspass_verbose_level)

        self.lookup_module.variables = {'syspass_verbose_level': '42'}
        self.lookup_module._templar = None
        self.lookup_module.kwargs = None
        self.lookup_module._ensure_syspass_verbose_level()
        self.assertEqual(42, self.lookup_module.syspass_verbose_level)

    def test_run(self):
        kwargs = {
            "account": f'Account_{uuid.uuid4().hex[:6]}',
            "privategroup": False,
            "expireDate": 0,
            "login": f'Account_{uuid.uuid4().hex[:6]}' ,
            "category": f'Category_{uuid.uuid4().hex[:6]}',
            "customer": f'Customer_{uuid.uuid4().hex[:6]}',
            "customer_desc": 'Test is a good customer',
            "tags": ['Prod', 'MySQL'],
            "url": f'site-{uuid.uuid4().hex[:6]}.com',
            "notes": 'ToTP required for this account',
            "chars": ['ascii_letters', 'digits'],
            "psswd_length": 20,
            "private": False,
            "state": 'present',
            "categoryId": 42,
            "action": "get"
        }
        variables = {
            'ansible_hostname': 'hostname.42',
            'syspass_auth_token': '1f43f5473165e0b37d33e8a992e935bc95d1172f97c3fd73a3ba660f85b65eda',
            'syspass_token_pass': r'_>Zas)?$kO8ThmhlFpZf<\*&\}YInJT~8jP@ec{wt8XSMAn;?_',
            'syspass_verify_ssl': 'True',
            'syspass_api_url': 'https://vaultprep.cust.digdeo.fr/api.php',
            'syspass_api_version': '3.1',
            'syspass_debug': 'True',
            'syspass_debug_level': '3',
            'syspass_verbose': 'True',
            'syspass_verbose_level': '3'
        }
        # term = 'Account Name minimal'
        self.lookup_module.login = 'Toto'
        self.lookup_module.category = 'TotoCategory'
        self.lookup_module.customer = 'TotoCustomer'
        self.lookup_module.run('term', variables=variables, kwargs=kwargs)


if __name__ == "__main__":
    unittest.main()
