#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

# https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html
# Make coding more python3-ish, this is required for contributions to Ansible

from __future__ import absolute_import, division, print_function
from ansible.parsing.yaml.objects import AnsibleUnicode
from ansible.utils.unsafe_proxy import AnsibleUnsafeText
from colorama import init, Fore, Style

init(autoreset=True)
__metaclass__ = type
__version__ = "0.3.5"

DOCUMENTATION = """
        DISCLAIMER: This module has been heavily inspired by https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/lookup/password.py for password generation and term handling and thus is under GPL.

        lookup: syspass
        author: Gousseaud Gaëtan <gousseaud.gaetan.pro@gmail.com>, Pierre-Henry Muller <pierre-henry.muller@digdeo.fr>, Tuxa <tuxa@rtnp.org>
        short_description: get syspass user password and syspass API client
        description:
            - This lookup returns the contents from Syspass database, a user's password more specifically. Other functions are also implemented for further use.
        ansible_version: ansible 10.4 with mitogen
        python_version: 3.7
        syspass_version: 3.2
        params:
            -term: the account name (required and must be unique)
            -login: login given to created account
            -category: category given to created account
            -customer: client given to created account
            -state: like in Ansible absent to remove the password, present in default to create (Optional)
            -pass_length: generated password length (Optional)
            -chars: type of chars used in generated (Optional)
            -url: url given to created account (Optional)
            -notes: notes given to created account (Optional)
            -private: is this password private for users who have access or public for all users in acl (default false)
            -privategroup: is private only for users in same group (default false)
            -expirationDate: expiration date given to created account (Optional) and not tested (no entry in webui)
        notes:
            - Account is only created if exact name has no match.
            - A different field passed to an already existing account wont modify it.
            - Utility of tokenPass: https://github.com/nuxsmin/sysPass/issues/994#issuecomment-409050974
            - Rudimentary list of API accesses (Deprecated): https://github.com/nuxsmin/sysPass/blob/d0056d74a8a2845fb3841b02f4af5eac3e4975ed/lib/SP/Services/Api/ApiService.php#L175
            - Usage of ansible vars: https://github.com/ansible/ansible/issues/33738#issuecomment-350819222
        syspass function list:
            SyspassClient:
                Account:
                    -AccountSearch
                    -AccountViewpass
                    -AccountCreate
                    -AccountDelete
                    -AccountView
                Category:
                    -CategorySearch
                    -CategoryCreate
                    -CategoryDelete
                Client:
                    -ClientSearch
                    -ClientCreate
                    -ClientDelete
                Tag:
                    -TagCreate
                    -TagSearch
                    -TagDelete
                UserGroup:
                    - UserGroupCreate
                    - UserGroupSearch
                    - UserGroupDelete
                Others:
                    -Backup
"""
EXAMPLES = """
### IN HOST VARS ###

syspass_API_URL: http://syspass-server.net/api.php
syspass_API_KEY: 'API_KEY' #Found in Users & Accesses -> API AUTHORIZATION -> User token
syspass_API_ACC_TOKPWD: Password for API_KEY for Account create / view / delete password account permission in API
syspass_default_length: number of chars in password

### IN PLAYBOOK ###

NOTE: Default values are handled

##### USAGE 1 #####

- name: Minimum declaration to get / create password
  local_action: debug msg="{{ lookup('syspass', 'Server 1 test account', login=test, category='MySQL', customer='Customer 1') }}"

- name: All details for password declaration
  local_action: debug msg="{{ lookup('syspass', 'Server 1 test account', login=test, category='MySQL', customer='Customer 1',
    url='https://exemp.le', notes='Additional information', private=True, privategroupe=True) }}"

- name: Minimum declaration to delete password
  local_action: debug msg="{{ lookup('syspass', 'Server 1 test account', state=absent) }}"


"""
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

# from ansible.module_utils._text import to_native, to_text

display = Display()

import random
import warnings
from urllib3.exceptions import HTTPWarning, InsecureRequestWarning

warnings.simplefilter("ignore", HTTPWarning)
warnings.simplefilter("ignore", InsecureRequestWarning)

import syspassclient
import threading

lock = threading.Lock()


class LookupModule(LookupBase):
    def __init__(self, loader=None, templar=None, **kwargs):
        LookupBase.__init__(self, loader=loader, templar=templar, kwargs=kwargs)

        # Private property's

        self.__verbose = None
        self.__verbose_level = None
        self.__debug = None
        self.__debug_level = None
        self.debug = False
        self.debug_level = 0
        self.verbose = False
        self.verbose_level = 0

        self.__syspass_client = None
        self.__term = None
        self.__variables = None
        self.__kwargs = None
        self.__params = None
        # Property Mess
        self.__account = None
        self.__chars = None
        self.__syspass_default_length = None
        # Default DigDeo Client vars
        self.__syspass_config_dir = None
        self.__syspass_auth_token = None
        self.__syspass_token_pass = None
        self.__syspass_verify_ssl = None
        self.__syspass_api_url = None
        self.__syspass_api_version = None
        self.__syspass_debug = None
        self.__syspass_debug_level = None
        self.__syspass_verbose = None
        self.__syspass_verbose_level = None
        self.__password_length = None
        self.__password_length_min = 8
        self.__password_length_max = 100
        self.__password = None
        self.__hostname = None
        self.__login = None
        self.__category = None
        self.__customer = None
        self.__customer_desc = None
        self.__tags = None
        self.__url = None
        self.__notes = None
        self.__state = None
        self.__private = None
        self.__privategroup = None
        self.__expireDate = None

        # First init
        self.params = None
        # self.term = None

        # self.syspass_client = None

        # Default DigDeo Client vars
        self.syspass_config_dir = None
        self.syspass_auth_token = None
        self.syspass_token_pass = None
        self.syspass_verify_ssl = None
        self.syspass_api_url = None
        self.syspass_api_version = None
        self.syspass_debug = None
        self.syspass_debug_level = None
        self.syspass_verbose = None
        self.syspass_verbose_level = None

        self.syspass_default_length = 40
        self.password_length = self.syspass_default_length
        self.chars = self._gen_candidate_chars(
            ["ascii_letters",
             "digits",
             "allowed_punctuation"]
        )
        # self.gen_password()
        # self.password = None
        # self.account = None
        self.hostname = None
        self.login = None
        self.category = None
        self.customer = None
        self.customer_desc = None
        self.tags = None
        self.url = None
        self.notes = None
        self.state = None
        self.private = 0
        self.privategroup = None
        self.expireDate = None

    @property
    def verbose(self):
        """
        Get if the verbose information's is display to the screen.

        :return: True if verbose mode is enable, False for disable it.
        :rtype: bool
        """
        return bool(self.__verbose)

    @verbose.setter
    def verbose(self, verbose):
        """
        Set if the verbose information's display on the screen.

        Generally it highly stress the console and is here for future maintenance of that Application.

        Enjoy future dev it found it function ;)

        :param verbose: True is verbose mode is enable, False for disable it.
        :type verbose: bool
        :raise TypeError: when "verbose" argument is not a :py:data:`bool`
        """
        # Exit as soon of possible
        if type(verbose) != bool:
            raise TypeError("'verbose' must be a bool type")

        # make the job in case
        if self.verbose != bool(verbose):
            self.__verbose = bool(verbose)

    @property
    def verbose_level(self):
        """
        Get the verbose information's level to display on the screen.

        Range: 0 to 3

        See: Object.set_verbose_level() for more information's about effect of ``debug_level``

        :return: The verbose_level property
        :rtype: int
        """
        return self.__verbose_level

    @verbose_level.setter
    def verbose_level(self, verbose_level):
        """
        Set the verbose level of information's display on the screen.

        Generally it highly stress the console and is here for future maintenance of that Application.

        Enjoy future dev it found it function ;)

        :param verbose_level: The Debug level to set
        :type verbose_level: int
        :raise TypeError: when "verbose_level" argument is not a :py:data:`int`
        """
        # Exit as soon of possible
        if type(verbose_level) != int:
            raise TypeError("'verbose_level' must be a int type")

        # make the job in case
        if self.verbose_level != verbose_level:
            self.__verbose_level = verbose_level

    @property
    def debug(self):
        """
        Get the debugging information's level to display on the screen.

        :return: True if debugging mode is enable, False for disable it.
        :rtype: bool
        """
        return bool(self.__debug)

    @debug.setter
    def debug(self, debug):
        """
        Set the debugging level of information's display on the screen.

        Generally it highly stress the console and is here for future maintenance of that Application.

        Enjoy future dev it found it function ;)

        :param debug: True is debugging mode is enable, False for disable it.
        :type debug: bool
        :raise TypeError: when "debug" argument is not a :py:data:`bool`
        """
        # Exit as soon of possible
        if type(debug) != bool:
            raise TypeError("'debug' must be a bool type")

        # make the job in case
        if self.debug != bool(debug):
            self.__debug = bool(debug)

    @property
    def debug_level(self):
        """
        Get the debugging information's level to display on the screen.

        Range: 0 to 3

        See: MorseDecoder.set_debug_level() for more information's about effect of ``debug_level``

        :return: The debug_level property
        :rtype: int
        """
        return self.__debug_level

    @debug_level.setter
    def debug_level(self, debug_level):
        """
        Set the debugging level of information's display on the screen.

        Generally it highly stress the console and is here for future maintenance of that Application.

        Enjoy future dev it found it function ;)

        :param debug_level: The Debug level to set
        :type debug_level: int
        :raise TypeError: when "debug_level" argument is not a :py:data:`int`
        """
        # Exit as soon of possible
        if type(debug_level) != int:
            raise TypeError("'debug_level' must be a int type")

        # make the job in case
        if self.debug_level != debug_level:
            self.__debug_level = debug_level

    @property
    def syspass_client(self):
        """
        Property it store the internal syspassClient object

        That is the only one point where store a syspass instance.
        That property flush a first init of SyspassLookup, and can be reset via it property.

        :return: a SyspassClient object instance
        :rtype: SyspassClient
        """
        return self.__syspass_client

    @syspass_client.setter
    def syspass_client(self, syspass_client=None):
        """
        Set the syspass_client property.

        :param syspass_client: a SyspassClient object instance
        :type syspass_client: SyspassClient
        :raise TypeError: when syspass_client is not a SyspassClient object instance
        """
        if not isinstance(syspass_client, syspassclient.SyspassClient):
            raise TypeError(
                "'syspass_client' parameter, must be a SyspassClient instance object"
            )

        if self.syspass_client != syspass_client:
            self.__syspass_client = syspass_client

    @property
    def syspass_auth_token(self):
        """
        Return the **syspass_auth_token** property value

        It ``property`` is use as **authToken** for **syspass**

        :return: the **syspass_auth_token** property value
        :rtype: str or None
        """
        return self.__syspass_auth_token

    @syspass_auth_token.setter
    def syspass_auth_token(self, syspass_auth_token=None):
        """
        Set the ``syspass_auth_token`` property value

        :param syspass_auth_token:
        :type: str ot None
        :raise TypeError: when ``syspass_auth_token`` is not a str type or None
        """
        if (
                syspass_auth_token is not None
                and not isinstance(syspass_auth_token, str)
        ):
            raise TypeError(
                "'syspass_auth_token' parameter, must be a str type or None"
            )

        if self.syspass_auth_token != syspass_auth_token:
            self.__syspass_auth_token = syspass_auth_token

    @property
    def syspass_token_pass(self):
        """
        Return the ``syspass_token_pass`` property value

        It ``property`` is use as **TokenPass** for **syspass**

        :return: the ``syspass_token_pass`` property value
        :rtype: str or None
        """
        return self.__syspass_token_pass

    @syspass_token_pass.setter
    def syspass_token_pass(self, syspass_token_pass=None):
        """
        Set the ``syspass_token_pass`` property value

        :param syspass_token_pass: the ``syspass_token_pass`` property value
        :type: str ot None
        :raise TypeError: when ``syspass_token_pass`` is not a str type or None
        """
        if (
                syspass_token_pass is not None
                and not isinstance(syspass_token_pass, str)
        ):
            raise TypeError(
                "'syspass_token_pass' parameter, must be a str type or None"
            )

        if self.syspass_token_pass != syspass_token_pass:
            self.__syspass_token_pass = syspass_token_pass

    @property
    def syspass_verify_ssl(self):
        """
        Return the ``syspass_verify_ssl`` property value

        It ``property`` is use for inform liburl to verify SSL certificate

        :return: the ``syspass_verify_ssl`` property value
        :rtype: str or None
        """
        return self.__syspass_verify_ssl

    @syspass_verify_ssl.setter
    def syspass_verify_ssl(self, syspass_verify_ssl=None):
        """
        Set the ``syspass_verify_ssl`` property value

        :param syspass_verify_ssl: the ``syspass_verify_ssl`` property value
        :type: bool ot None
        :raise TypeError: when ``syspass_verify_ssl`` is not a bool type or None
        """
        if syspass_verify_ssl is None:
            syspass_verify_ssl = False

        if (
                syspass_verify_ssl is not None
                and type(syspass_verify_ssl) != bool
        ):
            raise TypeError(
                "'syspass_verify_ssl' parameter, must be a bool type or None"
            )

        if self.syspass_verify_ssl != syspass_verify_ssl:
            self.__syspass_verify_ssl = syspass_verify_ssl

    @property
    def syspass_api_url(self):
        return self.__syspass_api_url

    @syspass_api_url.setter
    def syspass_api_url(self, syspass_api_url=None):
        if (
                syspass_api_url is not None
                and not isinstance(syspass_api_url, str)
        ):
            raise TypeError(
                "'syspass_api_url' parameter, must be a str type or None"
            )

        if self.syspass_api_url != syspass_api_url:
            self.__syspass_api_url = syspass_api_url

    @property
    def syspass_api_version(self):
        return self.__syspass_api_version

    @syspass_api_version.setter
    def syspass_api_version(self, syspass_api_version=None):
        if (
                syspass_api_version is not None
                and not isinstance(syspass_api_version, str)
        ):
            raise TypeError(
                "'syspass_api_version' parameter, must be a str type or None"
            )

        if self.syspass_api_version != syspass_api_version:
            self.__syspass_api_version = syspass_api_version

    @property
    def syspass_debug(self):
        return self.__syspass_debug

    @syspass_debug.setter
    def syspass_debug(self, syspass_debug=None):
        if syspass_debug is None:
            syspass_debug = False

        if (
                syspass_debug is not None
                and type(syspass_debug) != bool
        ):
            raise TypeError(
                "'syspass_debug' parameter, must be a bool type or None"
            )

        if self.syspass_debug != syspass_debug:
            self.__syspass_debug = syspass_debug

    @property
    def syspass_debug_level(self):
        return self.__syspass_debug_level

    @syspass_debug_level.setter
    def syspass_debug_level(self, syspass_debug_level=None):
        if syspass_debug_level is None:
            syspass_debug_level = 0

        if (
                syspass_debug_level is not None
                and type(syspass_debug_level) != int
        ):
            raise TypeError(
                "'syspass_debug_level' parameter, must be a int type or None"
            )

        if self.syspass_debug_level != syspass_debug_level:
            self.__syspass_debug_level = syspass_debug_level

    @property
    def syspass_verbose(self):
        return self.__syspass_verbose

    @syspass_verbose.setter
    def syspass_verbose(self, syspass_verbose=None):
        if syspass_verbose is None:
            syspass_verbose = False

        if (
                syspass_verbose is not None
                and type(syspass_verbose) != bool
        ):
            raise TypeError(
                "'syspass_verbose' parameter, must be a bool type or None"
            )

        if self.syspass_verbose != syspass_verbose:
            self.__syspass_verbose = syspass_verbose
            if self.syspass_client:
                self.syspass_client.verbose = self.syspass_verbose

    @property
    def syspass_verbose_level(self):
        return self.__syspass_verbose_level

    @syspass_verbose_level.setter
    def syspass_verbose_level(self, syspass_verbose_level=None):
        if syspass_verbose_level is None:
            syspass_verbose_level = 0

        if (
                syspass_verbose_level is not None
                and type(syspass_verbose_level) != int
        ):
            raise TypeError(
                "'syspass_debug_level' parameter, must be a int type or None"
            )

        if self.syspass_verbose_level != syspass_verbose_level:
            self.__syspass_verbose_level = syspass_verbose_level

    @property
    def syspass_default_length(self):
        """
        The default password length use for generate password, use when password_length parameter is not set

        :return: The default password length
        :rtype: int
        """
        return self.__syspass_default_length

    @syspass_default_length.setter
    def syspass_default_length(self, value):
        """
        Set the default syspass_default_length in range [8..40]

        :param value: The default password length use for generate password
        :type value: int
        :raise TypeError: When  syspass_default_length is not in range 8 to 40
        """
        if type(value) != int:
            raise TypeError('"syspass_default_length" must be a int type')

        if value not in range(self.password_length_min, self.password_length_max + 1):
            raise ValueError(
                '"syspass_default_length" must be contain in range {0} to {1}'.format(
                    self.password_length_min, self.password_length_max
                )
            )

        if self.syspass_default_length != value:
            self.__syspass_default_length = value

    @property
    def account(self):
        return self.__account

    @account.setter
    def account(self, account=None):
        """
        :param account: a account name
        :return: str or None
        """
        if account is None:
            raise TypeError('"Account" can not be none at all')

        if self.account != account:
            self.__account = account

    @property
    def password_length_min(self):
        return self.__password_length_min

    @password_length_min.setter
    def password_length_min(self, value):
        if type(value) != int:
            raise TypeError('"password_length_min" must be a int type')

        # Clamp value to 1
        if value < 1:
            value = 1
        # Fix a hard limit to 200, that the syspass 3.1 max
        if value >= 200:
            value = 199
        # Clamp value to max - 1
        if value >= self.password_length_max:
            value = self.password_length_max - 1

        if self.password_length_min != value:
            self.__password_length_min = value

    @property
    def password_length_max(self):
        return self.__password_length_max

    @password_length_max.setter
    def password_length_max(self, value):
        if type(value) != int:
            raise TypeError('"password_length_max" must be a int type')

        # Clamp value to 1
        if value < 1:
            value = 1
        # Clamp value to max - 1
        if value <= self.password_length_min:
            value = self.password_length_min + 1
        # Fix a hard limit to 200, that the syspass 3.1 max
        if value > 200:
            value = 200

        if self.password_length_max != value:
            self.__password_length_max = value

    @property
    def password_length(self):
        """
        The password length use to generate password.

        :return: The default password length
        :rtype: int
        """
        return self.__password_length

    @password_length.setter
    def password_length(self, value):
        """
        Set the password_length in range [8..40]

        :param value: The password length use to generate password
        :type value: int
        :raise TypeError: When  password_length is not in range 8 to 40
        """
        if type(value) != int:
            raise TypeError('"password_length" must be a int type')
        if value not in range(self.password_length_min, self.password_length_max + 1):
            raise ValueError(
                '"password_length" must be contain in range {0} to {1}'.format(
                    self.password_length_min, self.password_length_max
                )
            )

        if self.password_length != value:
            self.__password_length = value

    @property
    def chars(self):
        return self.__chars

    @chars.setter
    def chars(self, chars):
        if self.chars != chars:
            self.__chars = chars

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password=None):
        if password is None:
            self.gen_password()
            password = self.password

        if len(password) not in range(
                self.password_length_min, self.password_length_max + 1
        ):
            raise ValueError(
                '"password" must be contain in range {0} to {1}'.format(
                    self.password_length_min, self.password_length_max
                )
            )

        if self.password != password:
            self.__password = password

    @property
    def hostname(self):
        """
        hostname property

        :return:the hostname or None if haven't
        :rtype: str or None
        """
        return self.__hostname

    @hostname.setter
    def hostname(self, hostname):
        """
        Set the hostname property

        :param hostname: the hostname to set
        :type: or None
        """
        if (
                hostname is not None
                and not isinstance(hostname, str)
        ):
            raise TypeError('"hostname" must be a str or None')
        if self.hostname != hostname:
            self.__hostname = hostname

    @property
    def login(self):
        return self.__login

    @login.setter
    def login(self, login=None):
        if (
                login is not None
                and not isinstance(login, str)
        ):
            raise TypeError('"login" must be a str or None')
        if self.login != login:
            self.__login = login

    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, category=None):
        if (
                category is not None
                and not isinstance(category, str)
        ):
            raise TypeError('"category" must be a str or None')
        if self.category != category:
            self.__category = category

    @property
    def customer(self):
        return self.__customer

    @customer.setter
    def customer(self, customer=None):
        if (
                customer is not None
                and not isinstance(customer, str)
        ):
            raise TypeError('"customer" must be a str or None')

        if self.customer != customer:
            self.__customer = customer

    @property
    def customer_desc(self):
        return self.__customer_desc

    @customer_desc.setter
    def customer_desc(self, customer_desc=None):
        if (
                customer_desc is not None
                and not isinstance(customer_desc, str)
        ):
            raise TypeError('"customer" must be a str or None')
        if customer_desc is None:
            customer_desc = ""
        if self.customer_desc != customer_desc:
            self.__customer_desc = customer_desc

    @property
    def tags(self):
        return self.__tags

    @tags.setter
    def tags(self, tags=None):
        # Support both list and list-like objects (AnsibleUnsafeList, etc.) for Ansible 2.20+
        if tags is not None and not isinstance(tags, (list, tuple)) and not hasattr(tags, '__iter__'):
            raise TypeError('"tags" must be a list or None')
        if tags is None:
            tags = []
        # Convert to list if it's a list-like object
        if tags is not None and not isinstance(tags, list):
            tags = list(tags)
        if self.tags != tags:
            self.__tags = tags

    @property
    def url(self):
        """
        Url from where access to the account

        :return: Account’s access URL or IP
        :rtype: str
        """
        return self.__url

    @url.setter
    def url(self, url=None):
        """
        Url from where access to the account

        if set to None url will be set to ""

        :param url: Account’s access URL or IP
        :type url: string or None
        """
        # if url is None:
        #     url = ""
        # print('URL')
        # Support both str and str-like objects (AnsibleUnicode, AnsibleUnsafeText, etc.) for Ansible 2.20+
        if url is not None and not isinstance(url, str):
            raise TypeError('"url" must be a str or None')

        if self.url != url:
            self.__url = url

    @property
    def notes(self):
        return self.__notes

    @notes.setter
    def notes(self, notes=None):
        if (
                notes is not None
                and not isinstance(notes, str)
        ):
            raise TypeError('"notes" must be a str or None')
        if notes is None:
            notes = ""
        if self.notes != notes:
            self.__notes = notes

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state=None):
        if state is None:
            state = "present"
        # Support both str and str-like objects (AnsibleUnicode, AnsibleUnsafeText, etc.) for Ansible 2.20+
        if not isinstance(state, str):
            raise TypeError('"state" must be a str or None')
        if str(state).lower() not in ["absent", "present"]:
            raise ValueError('"state" must be a "absent" or "present"')
        if self.state != str(state).lower():
            self.__state = str(state).lower()

    @property
    def private(self):
        """
        Set account as private. It can be either 0 or 1

        :return: 0 or 1
        :rtype: int
        """
        return self.__private

    @private.setter
    def private(self, private=None):
        if private is None:
            private = 0
        if type(private) != int:
            raise TypeError('"notes" private be a int or None')
        if private <= 0:
            private = 0
        if private >= 1:
            private = 1
        if self.private != private:
            self.__private = private

    @property
    def privategroup(self):
        """
        Set account as private for group. It can be either 0 or 1

        :return: 0 or 1
        :rtype: int
        """
        return self.__privategroup

    @privategroup.setter
    def privategroup(self, privategroup=None):
        if privategroup is not None and type(privategroup) != int:
            raise TypeError('"privategroup" private be a int or None')
        if privategroup is None:
            privategroup = 0
        if privategroup <= 0:
            privategroup = 0
        if privategroup >= 1:
            privategroup = 1
        if self.privategroup != privategroup:
            self.__privategroup = privategroup

    @property
    def expireDate(self):
        return self.__expireDate

    @expireDate.setter
    def expireDate(self, expireDate=None):
        if expireDate is None:
            expireDate = 0
        if type(expireDate) != int:
            raise TypeError('"expireDate" private be a int or None')

        if self.expireDate != expireDate:
            self.__expireDate = expireDate

    @property
    def ascii_letters(self):
        """
        Return **abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ**

        :return: allowed letters
        :rtype: str
        """
        return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    @property
    def digits(self):
        """
        Return **0123456789**

        :return: allow digit
        :rtype: str
        """
        return "0123456789"

    @property
    def allowed_punctuation(self):
        """
        Return **-_|./?=+()[]~*{}#**

        :return: allowed punctuation
        :rtype: str
        """
        return "-_|./?=+()[]~*{}#"

    def _gen_candidate_chars(self, characters=None):
        """
        Generate a string containing all valid chars as defined by ``characters``

        The values of each char spec can be:
        * a name of an attribute in the 'strings' module ('digits' for example).
        The value of the attribute will be added to the candidate chars.
        * a string of characters. If the string isn't an attribute in 'string'
        module, the string will be directly added to the candidate chars.

        By example::
        characters=['digits', '?|']``
        will match ``string.digits`` and add all ascii digits.  ``'?|'`` will add
        the question mark and pipe characters directly. Return will be the string::
        u'0123456789?|'

        :param characters: A list of character specs. The character specs are shorthand names for sets of characters \
        like 'digits', 'ascii_letters', or 'punctuation' or a string to be included verbatim.
        :type characters: list
        :return: str
        :rtype: str
        :raise TypeError: when ``characters``  is not a list
        """
        # Support both list and list-like objects (AnsibleUnsafeList, etc.) for Ansible 2.20+
        if not isinstance(characters, (list, tuple)) and not hasattr(characters, '__iter__'):
            raise TypeError("'characters' must be a list type")

        chars = ""
        if "ascii_letters" in characters:
            chars += self.ascii_letters
        if "digits" in characters:
            chars += self.digits
        if "allowed_punctuation" in characters:
            chars += self.allowed_punctuation

        if chars == "":
            raise ValueError("The password can not be generate with empty characters")

        return chars

    def _account_exist(self, text=None, matchall=None):
        """
        Test if a account exist

        :param text:
        :return: None if not exist else the JSon return of the syspassclient
        :rtype: None or dict
        """
        account_id = self.syspass_client.account_search(
            authToken=self.syspass_client.authToken, text=text, matchall=matchall
        )

        if account_id is not None and type(account_id) == int:
            return account_id
        else:
            return None

    def _account_create(self):
        """
        Internal function it create account without test if the account exist

        :return: the password of the account if it exist
        :rtype: str
        """

        # Following handlers verify existence of fields
        # creating them in case of absence.
        categoryId = self._ensure_category_id_exist()
        customerId = self._ensure_customer_id_exist()
        userGroupId = self._ensure_user_group_id_exist()
        tagsId = self._ensure_tags_id_exist()

        # if self.password is None:
        #     self.gen_password()

        self.syspass_client.account_create(
            authToken=self.syspass_client.authToken,
            tokenPass=self.syspass_client.tokenPass,
            name=self.account,
            categoryId=int(categoryId),
            clientId=int(customerId),
            userGroupId=int(userGroupId),
            password=self.password,
            login=self.login,
            url=self.url,
            tagsId=tagsId,
            notes=self.notes,
            privateGroup=self.privategroup,
            private=int(self.private),
            expireDate=self.expireDate,
            parentId=None,
        )

        return self.password

    def _account_exist_or_create(self):
        values = []

        account = self._account_exist(self.account)

        # if account is not None and isinstance(account, dict) and account["id"]:
        if account is not None and isinstance(account, int):
            if self.state == "absent":
                self.syspass_client.account_delete(
                    authToken=self.syspass_client.authToken, account_id=account
                )
                values_to_return = "Deleted Account"

            else:
                values_to_return = self.syspass_client.account_viewpass(
                    authToken=self.syspass_client.authToken, account_id=account
                )

        else:
            values_to_return = self._account_create()

        values.append(values_to_return)
        return values

    def _ensure_tags_id_exist(self, tags=None):
        if tags is None:
            tags = self.tags
        # Support both list and list-like objects (AnsibleUnsafeList, etc.) for Ansible 2.20+
        if not isinstance(tags, (list, tuple)) and not hasattr(tags, '__iter__'):
            raise TypeError('"tags" property and parameter can not be None')
        # Convert to list if it's a list-like object
        if not isinstance(tags, list):
            tags = list(tags)

        tagsId = []
        for tag in tags:
            returned_value = self.syspass_client.tag_search(
                authToken=self.syspass_client.authToken, text=tag
            )
            if returned_value is not None:
                tagsId.append(returned_value)
            else:
                tagsId.append(
                    self.syspass_client.tag_create(
                        authToken=self.syspass_client.authToken, name=tag
                    )
                )

        return tagsId

    def _ensure_user_group_id_exist(self, customer=None, customer_desc=None):
        if customer is None:
            customer = self.customer
        if (
                customer is not None
                and not isinstance(customer, str)
        ):
            raise TypeError('"customer" property and parameter can not be None')
        if customer == "":
            raise ValueError('"customer" property and parameter can not be empty')

        if customer_desc is None:
            customer_desc = self.customer_desc
        if (
                customer_desc is not None
                and not isinstance(customer_desc, str)
        ):
            raise TypeError('"customer_desc" property and parameter can not be None')

        userGroupId = self.syspass_client.user_group_search(
            authToken=self.syspass_client.authToken, text=customer, count=1
        )
        if userGroupId is None:
            if customer_desc is not None:
                userGroupId = self.syspass_client.user_group_create(
                    authToken=self.syspass_client.authToken,
                    name=customer,
                    description=customer_desc,
                )

            # #########################################################################################
            # #########################################################################################
            # ## Code impossible to touch, impossible to force, never that code is touch in any case ##
            # #########################################################################################
            # #########################################################################################
            # else:
            #     userGroupId = self.syspass_client.user_group_create(
            #         name=customer
            #     )
        return userGroupId

    def _ensure_customer_id_exist(self, customer=None):
        if customer is None:
            customer = self.customer
        if (
                type(customer) != str
                and type(customer) != AnsibleUnicode
                and type(customer) != AnsibleUnsafeText
        ):
            raise TypeError('"customer" property can not be None')
        if customer == "":
            raise ValueError('"customer" property can not be empty')

        customerId = self.syspass_client.client_search(
            authToken=self.syspass_client.authToken, text=customer
        )

        if customerId is None:
            customerId = self.syspass_client.client_create(
                authToken=self.syspass_client.authToken, name=customer
            )
        return customerId

    def _ensure_category_id_exist(self, category=None):
        if category is None:
            category = self.category
        if (
                category is not None
                and not isinstance(category, str)
        ):
            raise TypeError('"category" property can not be None')
        if category == "":
            raise ValueError('"category" property can not be empty')

        categoryId = self.syspass_client.category_search(
            authToken=self.syspass_client.authToken, text=category
        )
        if categoryId is None:
            categoryId = self.syspass_client.category_create(
                authToken=self.syspass_client.authToken, name=category
            )
            if categoryId is None:
                raise ValueError(f'Failed to create category "{category}", categoryId is None')
        return categoryId

    def gen_password(self):
        """
        Function it generate a password

        :return: a password
        :rtype: str
        """

        password = " "
        if isinstance(self.params, dict) and "psswd_length" in self.params:
            self.password_length = self.params["psswd_length"]
        while " " in password:
            password = "{0}".format(
                "".join(
                    random.choice(str(self.chars)) for _ in range(self.password_length)
                )
            )

        self.password = password

    def _ensure_params(self):
        # global
        self._ensure_terms()
        self._ensure_variables()

        # specific parameters
        self._ensure_account()
        self._ensure_chars()
        self._ensure_password_length()
        self._ensure_password()
        self._ensure_hostname()
        self._ensure_login()
        self._ensure_category()
        self._ensure_customer()
        self._ensure_customer_desc()
        self._ensure_tags()
        self._ensure_url()
        self._ensure_notes()
        self._ensure_state()
        self._ensure_private()
        self._ensure_private_group()
        self._ensure_expiration_date()

        # Final
        self._ensure_everything_is_right()

        # In case term is a dict and not a string
        if isinstance(self.term, dict):
            if self.term.get("env", None) is not None:
                env = self.term.get("env")
                if env in ["prod", "prep", "rec", "dev", "tests"]:
                    if env.upper() not in self.tags:
                        self.tags.append(env.upper())

                self.url = self.term.get("url_listen")[0]
                self.login = self.term.get("login")
                self.account = "{0} {1} {2}".format(
                    self.hostname, self.login, self.category
                )
                ###############################
                #  WAS Comment   originally   #
                ###############################
                # self.customer = env.upper() #
                ###############################

            # elif self.term.get("app", None) is not None:
            elif "app" in self.term:
                if "APP" not in self.tags:
                    self.tags.append("APP")

                self.url = self.term.get("url_listen")[0]
                self.account = "{0} {1} {2}".format(
                    self.hostname, self.term["app"], self.category
                )

            if "state" in self.term:
                # if self.term.get("state", None) is not None:
                self.state = self.term.get("state")
                if "password" in self.term:
                    self.password = self.term.get("password")

    def import_DD_SYSPASS_vars(self):

        self._ensure_syspass_api_url()
        self._ensure_syspass_api_version()
        self._ensure_syspass_auth_token()
        self._ensure_syspass_debug()
        self._ensure_syspass_debug_level()
        self._ensure_syspass_verbose()
        self._ensure_syspass_verbose_level()
        self._ensure_syspass_verify_ssl()
        self._ensure_syspass_token_pass()

        self.debug = self.syspass_debug
        self.debug_level = self.syspass_debug_level
        self.verbose = self.syspass_verbose
        self.verbose_level = self.syspass_verbose_level

        if self.debug and self.debug_level > 1:
            # TITLE
            print(Fore.YELLOW + Style.BRIGHT + "{0}: ".format(self.__class__.__name__.upper()), end="", )
            print(Fore.WHITE + Style.BRIGHT + "{0}".format("Import DD_SYSPASS_CLIENT vars"))

            # syspass_api_url
            print(Fore.CYAN + Style.BRIGHT + "< " + Fore.WHITE + "syspass_api_url: ", end="", )
            print(Fore.GREEN + Style.BRIGHT + "{0}".format(self.syspass_api_url))

            # syspass_api_version
            print(Fore.CYAN + Style.BRIGHT + "< " + Fore.WHITE + "syspass_api_version: ", end="", )
            print(Fore.GREEN + Style.BRIGHT + "{0}".format(self.syspass_api_version))

            # syspass_auth_token
            print(Fore.CYAN + Style.BRIGHT + "< " + Fore.WHITE + "syspass_auth_token: ", end="", )
            print(Fore.GREEN + Style.BRIGHT + "{0}".format(self.syspass_auth_token))

            # syspass_debug
            print(Fore.CYAN + Style.BRIGHT + "< " + Fore.WHITE + "syspass_debug: ", end="", )
            print(Fore.GREEN + Style.BRIGHT + "{0}".format(self.syspass_debug))

            # syspass_debug_level
            print(Fore.CYAN + Style.BRIGHT + "< " + Fore.WHITE + "syspass_debug_level: ", end="", )
            print(Fore.GREEN + Style.BRIGHT + "{0}".format(self.syspass_debug_level))

            # syspass_verbose
            print(Fore.CYAN + Style.BRIGHT + "< " + Fore.WHITE + "syspass_verbose: ", end="", )
            print(Fore.GREEN + Style.BRIGHT + "{0}".format(self.syspass_verbose))

            # syspass_verbose_level
            print(Fore.CYAN + Style.BRIGHT + "< " + Fore.WHITE + "syspass_verbose_level: ", end="", )
            print(Fore.GREEN + Style.BRIGHT + "{0}".format(self.syspass_verbose_level))

            # syspass_verify_ssl
            print(Fore.CYAN + Style.BRIGHT + "< " + Fore.WHITE + "syspass_verify_ssl: ", end="", )
            print(Fore.GREEN + Style.BRIGHT + "{0}".format(self.syspass_verify_ssl))

            # syspass_token_pass
            print(Fore.CYAN + Style.BRIGHT + "< " + Fore.WHITE + "syspass_token_pass: ", end="", )
            print(Fore.GREEN + Style.BRIGHT + "{0}".format(self.syspass_token_pass))

    def impose_DD_SYSPASS_vars(self):

        if self.syspass_client:
            if self.debug and self.debug_level > 1:
                # Title
                print(
                    Fore.YELLOW
                    + Style.BRIGHT
                    + "{0}: ".format(self.__class__.__name__.upper()),
                    end="",
                )
                print(
                    Fore.WHITE
                    + Style.BRIGHT
                    + "{0} {1}".format("Impose setting to", self.syspass_client)
                )

            # syspass_api_url
            self.syspass_client.api_url = self.syspass_api_url
            if self.debug and self.debug_level > 2:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "> "
                    + Fore.WHITE
                    + "syspass_api_url:",
                    end="",
                )
                if self.syspass_api_url == self.syspass_client.api_url:
                    print(Fore.GREEN + Style.BRIGHT + " {0}".format("OK"))
                else:  # pragma: no cover
                    print(Fore.RED + Style.BRIGHT + " {0}".format("FAILED"))

            # syspass_api_version
            self.syspass_client.api_version = self.syspass_api_version
            if self.debug and self.debug_level > 2:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "> "
                    + Fore.WHITE
                    + "syspass_api_version:",
                    end="",
                )
                if (
                        self.syspass_api_version
                        == self.syspass_client.api_version
                ):
                    print(Fore.GREEN + Style.BRIGHT + " {0}".format("OK"))
                else:  # pragma: no cover
                    print(Fore.RED + Style.BRIGHT + " {0}".format("FAILED"))

            # syspass_auth_token
            self.syspass_client.authToken = self.syspass_auth_token
            if self.debug and self.debug_level > 2:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "> "
                    + Fore.WHITE
                    + "syspass_auth_token:",
                    end="",
                )
                if self.syspass_auth_token == self.syspass_client.authToken:
                    print(Fore.GREEN + Style.BRIGHT + " {0}".format("OK"))
                else:  # pragma: no cover
                    print(Fore.RED + Style.BRIGHT + " {0}".format("FAILED"))

            # syspass_debug
            self.syspass_client.debug = self.syspass_debug
            if self.debug and self.debug_level > 2:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "> "
                    + Fore.WHITE
                    + "syspass_debug:",
                    end="",
                )
                if self.syspass_debug == self.syspass_client.debug:
                    print(Fore.GREEN + Style.BRIGHT + " {0}".format("OK"))
                else:  # pragma: no cover
                    print(Fore.RED + Style.BRIGHT + " {0}".format("FAILED"))

            # syspass_debug_level
            self.syspass_client.debug_level = self.syspass_debug_level
            if self.debug and self.debug_level > 2:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "> "
                    + Fore.WHITE
                    + "syspass_debug_level:",
                    end="",
                )
                if (
                        self.syspass_debug_level
                        == self.syspass_client.debug_level
                ):
                    print(Fore.GREEN + Style.BRIGHT + " {0}".format("OK"))
                else:  # pragma: no cover
                    print(Fore.RED + Style.BRIGHT + " {0}".format("FAILED"))

            # syspass_verbose
            self.syspass_client.verbose = self.syspass_verbose
            if self.debug and self.debug_level > 2:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "> "
                    + Fore.WHITE
                    + "syspass_verbose:",
                    end="",
                )
                if self.syspass_verbose == self.syspass_client.verbose:
                    print(Fore.GREEN + Style.BRIGHT + " {0}".format("OK"))
                else:  # pragma: no cover
                    print(Fore.RED + Style.BRIGHT + " {0}".format("FAILED"))

            # syspass_verbose_level
            self.syspass_client.verbose_level = self.syspass_verbose_level
            if self.debug and self.debug_level > 2:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "> "
                    + Fore.WHITE
                    + "syspass_verbose_level:",
                    end="",
                )
                if (
                        self.syspass_verbose_level
                        == self.syspass_client.verbose_level
                ):
                    print(Fore.GREEN + Style.BRIGHT + " {0}".format("OK"))
                else:  # pragma: no cover
                    print(Fore.RED + Style.BRIGHT + " {0}".format("FAILED"))

            # syspass_verify_ssl
            self.syspass_client.verify_ssl = self.syspass_verify_ssl
            if self.debug and self.debug_level > 2:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "> "
                    + Fore.WHITE
                    + "syspass_verify_ssl:",
                    end="",
                )
                if self.syspass_verify_ssl == self.syspass_client.verify_ssl:
                    print(Fore.GREEN + Style.BRIGHT + " {0}".format("OK"))
                else:  # pragma: no cover
                    print(Fore.RED + Style.BRIGHT + " {0}".format("FAILED"))

            # syspass_token_pass
            self.syspass_client.tokenPass = self.syspass_token_pass
            if self.debug and self.debug_level > 2:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "> "
                    + Fore.WHITE
                    + "syspass_token_pass:",
                    end="",
                )
                if self.syspass_token_pass == self.syspass_client.tokenPass:
                    print(Fore.GREEN + Style.BRIGHT + " {0}".format("OK"))
                else:  # pragma: no cover
                    print(Fore.RED + Style.BRIGHT + " {0}".format("FAILED"))

    def _ensure_everything_is_right(self):
        self.params = {
            "chars": self.chars,
            "psswd_length": self.password_length,
            "password": self.password,
            "hostname": self.hostname,
            "account": self.account,
            "login": self.login,
            "category": self.category,
            "customer": self.customer,
            "customer_desc": self.customer_desc,
            "tags": self.tags,
            "url": self.url,
            "notes": self.notes,
            "state": self.state,
            "private": self.private,
            "privategroup": self.privategroup,
            "expireDate": self.expireDate,
        }
        for k, v in self.params.items():
            if v is None:
                if k == "url":
                    pass
                else:
                    raise ValueError("Error : %s must be defined" % k)

    def _ensure_account(self):
        self.account = self.term

    def _ensure_category(self):
        # category
        if isinstance(self.kwargs, dict) and "category" in self.kwargs:
            self.category = self.kwargs["category"]

    def _ensure_customer(self):
        # customer
        if isinstance(self.kwargs, dict) and "customer" in self.kwargs:
            self.customer = self.kwargs["customer"]

    def _ensure_customer_desc(self):
        # customer_desc
        if isinstance(self.kwargs, dict) and "customer_desc" in self.kwargs:
            self.customer_desc = self.kwargs["customer_desc"]

    def _ensure_chars(self):
        # chars
        if isinstance(self.kwargs, dict) and "chars" in self.kwargs:
            self.chars = self._gen_candidate_chars(self.kwargs["chars"])

    def _ensure_expiration_date(self):
        # expirationDate
        if isinstance(self.kwargs, dict) and "expireDate" in self.kwargs:
            self.expireDate = self.kwargs["expireDate"]

    def _ensure_hostname(self):
        # hostname
        if self.variables is not None:
            if isinstance(self.variables, dict) and "host_override" in self.variables:
                self.hostname = str(self.variables["host_override"])
            elif (
                    isinstance(self.variables, dict)
                    and "ansible_hostname" in self.variables
            ):
                self.hostname = str(self.variables["ansible_hostname"].split(".")[0])

    def _ensure_login(self):
        # login
        if isinstance(self.kwargs, dict) and "login" in self.kwargs:
            self.login = self.kwargs["login"]
        elif isinstance(self.term, dict):
            self.login = ""

    def _ensure_notes(self):
        # notes
        if isinstance(self.kwargs, dict) and "notes" in self.kwargs:
            self.notes = self.kwargs["notes"]

    def _ensure_password(self):
        # password
        if (
                isinstance(self.params, dict)
                and "password" in self.params
                and self.params["password"] is not None
                and self.params["password"] != ""
        ):
            self.password = str(self.params["password"])

        elif (
                isinstance(self.kwargs, dict)
                and "password" in self.kwargs
                and self.kwargs["password"] is not None
                and self.kwargs["password"] != ""
        ):
            self.password = str(self.kwargs["password"])

        elif (
                isinstance(self._templar, dict)
                and "_available_variables" in self._templar
                and "password" in self._templar["_available_variables"]
                and self._templar["_available_variables"]["password"] is not None
                and self._templar["_available_variables"]["password"] != ""
        ):
            self.password = str(self._templar["_available_variables"]["password"])
        elif (
                isinstance(self.variables, dict)
                and "password" in self.variables
                and self.variables["password"] is not None
                and self.variables["password"] != ""
        ):
            self.password = str(self.variables["password"])
        else:
            self.gen_password()

    def _ensure_password_length(self):
        # password length
        if isinstance(self.kwargs, dict) and "psswd_length" in self.kwargs:
            self.password_length = self.kwargs["psswd_length"]
        elif (
                isinstance(self._templar, dict) and "_available_variables" in self._templar
        ):
            if "syspass_default_length" in self._templar["_available_variables"]:
                self.password_length = int(
                    self._templar["_available_variables"]["syspass_default_length"]
                )

    def _ensure_private(self):
        # private
        if isinstance(self.kwargs, dict) and "private" in self.kwargs:
            if type(self.kwargs["private"]) == bool:
                if self.kwargs["private"] is True:
                    self.private = 1
                else:
                    self.private = 0
            else:
                self.private = 0

    def _ensure_private_group(self):
        # privategroup
        if isinstance(self.kwargs, dict) and "privategroup" in self.kwargs:
            if type(self.kwargs["privategroup"]) == bool:
                if self.kwargs["privategroup"] is True:
                    self.privategroup = 1
                else:
                    self.privategroup = 0
            else:
                self.privategroup = 0

    def _ensure_state(self):
        self.state = "present"

        if isinstance(self.kwargs, dict) and "state" in self.kwargs:
            if self.kwargs["state"] is not None:
                self.state = self.kwargs["state"]

        if isinstance(self.term, dict) and "state" in self.term:
            if self.term["state"] is not None:
                self.state = self.term["state"]

    def _ensure_syspass_auth_token(self):
        # syspass_auth_token
        if (
                isinstance(self.kwargs, dict)
                and "syspass_auth_token" in self.kwargs
        ):
            self.syspass_auth_token = str(
                self.kwargs["syspass_auth_token"]
            )

        elif (
                isinstance(self._templar, dict)
                and "_available_variables" in self._templar
                and "syspass_auth_token" in self._templar["_available_variables"]
        ):
            self.syspass_auth_token = str(
                self._templar["_available_variables"]["syspass_auth_token"]
            )
        elif (
                isinstance(self.variables, dict)
                and "syspass_auth_token" in self.variables
        ):
            self.syspass_auth_token = str(
                self.variables["syspass_auth_token"]
            )

    def _ensure_syspass_token_pass(self):
        # syspass_token_pass
        if (
                isinstance(self.kwargs, dict)
                and "syspass_token_pass" in self.kwargs
        ):
            self.syspass_token_pass = str(
                self.kwargs["syspass_token_pass"]
            )
        elif (
                isinstance(self._templar, dict)
                and "_available_variables" in self._templar
                and "syspass_token_pass" in self._templar["_available_variables"]
        ):
            self.syspass_token_pass = str(
                self._templar["_available_variables"]["syspass_token_pass"]
            )
        elif (
                isinstance(self.variables, dict)
                and "syspass_token_pass" in self.variables
        ):
            self.syspass_token_pass = str(
                self.variables["syspass_token_pass"]
            )

    def _ensure_syspass_verify_ssl(self):
        # syspass_verify_ssl
        if (
                isinstance(self.kwargs, dict)
                and "syspass_verify_ssl" in self.kwargs
        ):
            if (
                    str(self.kwargs["syspass_verify_ssl"]).lower() == "true"
                    or str(self.kwargs["syspass_verify_ssl"]).lower() == "yes"
            ):
                self.syspass_verify_ssl = True
            else:
                self.syspass_verify_ssl = False

        elif (
                isinstance(self._templar, dict)
                and "_available_variables" in self._templar
                and "syspass_verify_ssl" in self._templar["_available_variables"]
        ):
            if (
                    str(self._templar["_available_variables"]["syspass_verify_ssl"]).lower() == "true"
                    or str(self._templar["_available_variables"]["syspass_verify_ssl"]).lower() == "yes"
            ):
                self.syspass_verify_ssl = True
            else:
                self.syspass_verify_ssl = False

        elif (
                isinstance(self.variables, dict)
                and "syspass_verify_ssl" in self.variables
        ):
            if (
                    str(self.variables["syspass_verify_ssl"]).lower() == "true"
                    or str(self.variables["syspass_verify_ssl"]).lower() == "yes"
            ):
                self.syspass_verify_ssl = True
            else:
                self.syspass_verify_ssl = False

    def _ensure_syspass_api_url(self):
        # syspass_api_url
        if isinstance(self.kwargs, dict) and "syspass_api_url" in self.kwargs:
            self.syspass_api_url = str(
                self.kwargs["syspass_api_url"]
            )
        elif (
                isinstance(self._templar, dict)
                and "_available_variables" in self._templar
                and "syspass_api_url" in self._templar["_available_variables"]
        ):
            self.syspass_api_url = str(
                self._templar["_available_variables"]["syspass_api_url"]
            )
        elif (
                isinstance(self.variables, dict)
                and "syspass_api_url" in self.variables
        ):
            self.syspass_api_url = str(
                self.variables["syspass_api_url"]
            )

    def _ensure_syspass_api_version(self):
        # syspass_api_version
        if (
                isinstance(self.kwargs, dict)
                and "syspass_api_version" in self.kwargs
        ):
            self.syspass_api_version = str(
                self.kwargs["syspass_api_version"]
            )
        elif (
                isinstance(self._templar, dict)
                and "_available_variables" in self._templar
                and "syspass_api_version" in self._templar["_available_variables"]
        ):
            self.syspass_api_version = str(
                self._templar["_available_variables"]["syspass_api_version"]
            )
        elif (
                isinstance(self.variables, dict)
                and "syspass_api_version" in self.variables
        ):
            self.syspass_api_version = str(
                self.variables["syspass_api_version"]
            )

    def _ensure_syspass_debug(self):
        # syspass_debug
        if isinstance(self.kwargs, dict) and "syspass_debug" in self.kwargs:
            if (
                    str(self.kwargs["syspass_debug"]).lower() == "true"
                    or str(self.kwargs["syspass_debug"]).lower() == "yes"
            ):
                self.syspass_debug = True
            else:
                self.syspass_debug = False
        elif (
                isinstance(self._templar, dict)
                and "_available_variables" in self._templar
                and "syspass_debug" in self._templar["_available_variables"]
        ):
            if (
                    str(self._templar["_available_variables"]["syspass_debug"]).lower() == "true"
                    or str(self._templar["_available_variables"]["syspass_debug"]).lower() == "yes"
            ):
                self.syspass_debug = True
            else:
                self.syspass_debug = False
        elif (
                isinstance(self.variables, dict)
                and "syspass_debug" in self.variables
        ):
            if (
                    str(self.variables["syspass_debug"]).lower() == "true"
                    or str(self.variables["syspass_debug"]).lower() == "yes"
            ):
                self.syspass_debug = True
            else:
                self.syspass_debug = False

    def _ensure_syspass_debug_level(self):
        # syspass_debug_level
        if (
                isinstance(self.kwargs, dict)
                and "syspass_debug_level" in self.kwargs
        ):
            self.syspass_debug_level = int(
                self.kwargs["syspass_debug_level"]
            )
        elif (
                isinstance(self._templar, dict)
                and "_available_variables" in self._templar
                and "syspass_debug_level" in self._templar["_available_variables"]
        ):
            self.syspass_debug_level = int(
                self._templar["_available_variables"]["syspass_debug_level"]
            )
        elif (
                isinstance(self.variables, dict)
                and "syspass_debug_level" in self.variables
        ):
            self.syspass_debug_level = int(
                self.variables["syspass_debug_level"]
            )

    def _ensure_syspass_verbose(self):
        # syspass_verbose
        if isinstance(self.kwargs, dict) and "syspass_verbose" in self.kwargs:
            if (
                    str(self.kwargs["syspass_verbose"]).lower() == "true"
                    or str(self.kwargs["syspass_verbose"]).lower() == "yes"
            ):
                self.syspass_verbose = True
            else:
                self.syspass_verbose = False
        elif (
                isinstance(self._templar, dict)
                and "_available_variables" in self._templar
                and "syspass_verbose" in self._templar["_available_variables"]
        ):
            if (
                    str(self._templar["_available_variables"]["syspass_verbose"]).lower() == "true"
                    or str(self._templar["_available_variables"]["syspass_verbose"]).lower() == "yes"
            ):
                self.syspass_verbose = True
            else:
                self.syspass_verbose = False
        elif (
                isinstance(self.variables, dict)
                and "syspass_verbose" in self.variables
        ):
            if (
                    str(self.variables["syspass_verbose"]).lower() == "true"
                    or str(self.variables["syspass_verbose"]).lower() == "yes"
            ):
                self.syspass_verbose = True
            else:
                self.syspass_verbose = False

    def _ensure_syspass_verbose_level(self):
        # syspass_verbose_level
        if (
                isinstance(self.kwargs, dict)
                and "syspass_verbose_level" in self.kwargs
        ):
            self.syspass_verbose_level = int(
                self.kwargs["syspass_verbose_level"]
            )
        elif (
                isinstance(self._templar, dict)
                and "_available_variables" in self._templar
                and "syspass_verbose_level"
                in self._templar["_available_variables"]
        ):
            self.syspass_verbose_level = int(
                self._templar["_available_variables"]["syspass_verbose_level"]
            )
        elif (
                isinstance(self.variables, dict)
                and "syspass_verbose_level" in self.variables
        ):
            self.syspass_verbose_level = int(
                self.variables["syspass_verbose_level"]
            )

    def _ensure_tags(self):
        # tags
        if isinstance(self.kwargs, dict) and "tags" in self.kwargs:
            self.tags = self.kwargs["tags"]

    def _ensure_url(self):
        # url
        if type(self.kwargs) == dict and "url" in self.kwargs:
            self.url = self.kwargs["url"]

        if type(self.term) == dict and "url_listen" in self.term:
            self.url = self.term["url_listen"][0]

    def _ensure_variables(self):
        # Note: In Ansible 2.19+, _available_variables became read-only.
        # Variables are passed via the 'variables' parameter to run().
        # This function is kept for backward compatibility but does nothing.
        pass

    @property
    def term(self):
        return self.__term

    @term.setter
    def term(self, term=None):
        if (
                term is not None
                and not isinstance(term, str)
                and type(term) != list
                and type(term) != dict
        ):
            raise TypeError('"term" must be a None, str or dict type')

        if isinstance(term, list):
            term = term[0]

        # if term is not None and type(term) != dict and type(term) != list:
        #     term = ''
        # if isinstance(self.term, dict):
        #     self.term = term
        # if isinstance(term, list) and len(term) == 1:
        #     term = dict(term[0])
        # else:
        #     raise AnsibleError("Term is not correct Error : %s" % self.term)
        if term != self.term:
            self.__term = term

    @property
    def variables(self):
        return self.__variables

    @variables.setter
    def variables(self, variables=None):
        if variables is None:
            variables = {}
        if type(variables) != dict:
            raise TypeError("'variables' MUST be a dict type")
        if variables != self.variables:
            self.__variables = variables

    @property
    def kwargs(self):
        return self.__kwargs

    @kwargs.setter
    def kwargs(self, value=None):
        if value is None:
            value = {}
        if type(value) != dict:
            raise TypeError('"kwargs" must be a dict type')
        if "kwargs" in value:
            value = value["kwargs"]
        if value != self.kwargs:
            self.__kwargs = value

    @property
    def params(self):
        return self.__params

    @params.setter
    def params(self, params=None):
        """

        :param params:
        :type params: dict or None
        """
        if params is None:
            self.__params = {}
        if params != self.params:
            self.__params = params

    def run(self, term, variables=None, **kwargs):
        """

        :param term: the first argument is a list containing the terms.
        :type term: list or str
        :param variables:
        :param kwargs:
        :return:
        """
        # Import everything
        self.term = term
        self.variables = variables
        self.kwargs = kwargs

        # Process parameters
        self._ensure_params()
        self.import_DD_SYSPASS_vars()

        if self.debug:
            print(
                Fore.YELLOW
                + Style.BRIGHT
                + "{0}: ".format(self.__class__.__name__.upper()),
                end="",
            )
            print(Fore.WHITE + Style.NORMAL + "version ", end="")
            print(Fore.GREEN + Style.BRIGHT + "{0}".format(__version__))

        self.syspass_client = syspassclient.SyspassClient(
            use_by_lookup=True,
            debug=self.debug,
            debug_level=self.debug_level,
            verbose=self.verbose,
            verbose_level=self.verbose_level
        )

        self.impose_DD_SYSPASS_vars()
        if self.debug:
            self.syspass_client.display_resume()

        # Make the work

        return self._account_exist_or_create()

    def _ensure_terms(self):
        pass
        # Small code for know if the first argument is a string or a list element.

        # if isinstance(self.term, dict):
        #     self.term = dict(self.term)
        # elif len(self.term) == 1:
        #     self.term = self.term[0]
        #
        # if isinstance(self.term, dict):
        #     pass
        # elif isinstance(self.term, str):
        #     pass
        # elif isinstance(self.term, list) and len(self.term) == 1:
        #     self.term = self.term[0]
        # else:
        #     raise AnsibleError("Term is not correct Error : %s" % self.term)

# def main():
#     sys.stdout.write(LookupModule().run(sys.argv[1:], None)[0])
#     sys.stdout.write("\n")
#     sys.stdout.flush()
#     return 0


# if __name__ == "__main__":
#     sys.exit(main())
