[![coverage report](https://git.digdeo.fr/digdeo-system/dd-ansible-syspass/badges/master/coverage.svg)](https://git.digdeo.fr/digdeo-system/dd-ansible-syspass/commits/master) [![pipeline status](https://git.digdeo.fr/digdeo-system/dd-ansible-syspass/badges/master/pipeline.svg)](https://git.digdeo.fr/digdeo-system/dd-ansible-syspass/commits/master)

# digdeo-ansible-syspass

**Module page**: https://pypi.org/project/digdeo-syspass-ansible-lookup/  
**Documentation**: https://www.readthedoc.io/digdeo-syspass-ansible-lookup  
**Bug Tracker**: https://gitdev.digdeo.fr/digdeo-projets-floss1/digdeo-syspass-ansible-lookup/issues  

## Introduction
**digdeo-ansible-syspass** is a [ansible](https://ansible.com) [lookup](https://docs.ansible.com/ansible/latest/plugins/lookup.html) plugin write in [python](https://www.python.org).

That program is a [ansible](https://ansible.com) plugin interface it use [digdeo-syspass-client](https://pypi.org/project/digdeo-syspass-client/) to dialog with the [syspass](https://www.syspass.org) API. 

It plugin is dedicated to lookup password's from a [syspass](https://www.syspass.org) server.

## Installation

### Normal installation
```shell script
python3 -m venv venv
. venv/bin/activate
pip install digdeo-syspass-ansible-lookup
```

### Force a Ansible version
```shell script
python3 -m venv venv
. venv/bin/activate
pip install wheel "ansible == 2.7.17"
pip install digdeo-syspass-ansible-lookup
```

### Force libxml

On Linux (and most other well-behaved operating systems), pip will manage to build the source distribution as long as ``libxml2`` and ``libxslt`` are properly installed, including development packages, i.e. header files, etc. 

See the requirements section above and use your system package management tool to look for packages like ``libxml2-dev`` or ``libxslt-devel``. If the build fails, make sure they are installed.

Alternatively, setting ``STATIC_DEPS=true`` will download and build both libraries automatically in their latest version, e.g. 

```shell script
STATIC_DEPS=true pip install lxml.
```


Note that module use [digdeo-syspass-client](https://pypi.org/project/digdeo-syspass-client/) python module 
Please pay attention about config.yml file in case you need more information's.


**DISCLAIMER:**<br>
This module has been heavily inspired by https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/lookup/password.py for password generation and term handling and thus is under GPL.

    lookup: syspass
    author: Gousseaud Gaëtan <gousseaud.gaetan.pro@gmail.com>, Pierre-Henry Muller <pierre-henry.muller@digdeo.fr>, Jérôme Ornech <jornech@digdeo.fr>
    short_description: get syspass user password and syspass API client
    description:
    - This lookup returns the contents from Syspass database, a user's password more specificly. Other functions are also implemented for further use.
    ansible_version: ansible 2.7.17 and more with mitogen
    python_version: 3.5 and more
    syspass_version: 3.0, 3.1
 
### Ansible usage:

#### Example 1
**Vars set inside common ansible sub-structure directory**

In case you use the group name `all`.

* Create a sub directory structure `./group_vars/all` and enter inside it directory
* copy paste you variable with right value inside a file name **syspass.yml**
```
syspass_auth_token: ##################################################
syspass_token_pass: ##################################################
syspass_verify_ssl: True
syspass_api_url: ##################################################
syspass_api_version: 3.1
syspass_debug: False
syspass_debug_level: 3
syspass_verbose: True
syspass_verbose_level: 3
```
* start you playbook with ``ansible-playbook playbook.yml``

#### Example 2 
**Vars set inside the playbook file**

In case you use the group name `all` the playbook can look like that:
```
--- # -*- mode: yaml; coding: utf-8 -*-

- hosts: all
  vars:
    syspass_default_length: 42
    syspass_auth_token: ##################################################
    syspass_token_pass: ##################################################
    syspass_verify_ssl: True
    syspass_api_url: ##################################################
    syspass_api_version: 3.1
    syspass_debug: False
    syspass_debug_level: 3
    syspass_verbose: True
    syspass_verbose_level: 3
  tasks:
    - name: SysPass | Force virtual Environement
      set_fact:
        ansible_python_interpreter: "/usr/bin/env python"
    - name: SysPass | Minimal test | get and if not exist insert
      debug:
        msg: "{{ lookup('syspass', 'Account Name minimal', login='mylogin', category='MySQL', customer='PREP') }}"
      register: pass1
      changed_when: false
    - name: SysPass | Minimal test | get and compare
      debug:
        msg: "{{ lookup('syspass', 'Account Name minimal', login='mylogin', category='MySQL', customer='PREP') }}"
      register: pass2
      changed_when: pass1.msg == pass2.msg
      failed_when: pass1.msg != pass2.msg
```

### Ansible Vault usage:

In case you use the group name `all`.

* Create a sub directory structure `./group_vars/all` and enter inside it directory
* use command line interface for create **syspass.yml** file `ansible-vault create syspass.yml`
* edit the **syspass.yml** file `ansible-vault edit syspass.yml`
* copy paste you variable with right value inside **syspass.yml** file
```
syspass_auth_token: ##################################################
syspass_token_pass: ##################################################
syspass_verify_ssl: True
syspass_api_url: ##################################################
syspass_api_version: 3.1
syspass_debug: False
syspass_debug_level: 3
syspass_verbose: True
syspass_verbose_level: 3
```
* create a file to store the vault password ``echo "password1234" > /my_directory/vault_passwd"``
* export env var ``DEFAULT_VAULT_PASSWORD_FILE`` via ``export DEFAULT_VAULT_PASSWORD_FILE="/my_directory/vault_passwd"``
* start you playbook with ``ansible-playbook --vault-password-file=$DEFAULT_VAULT_PASSWORD_FILE playbook.yml``

#### Summary
```
> cd directory_where_is_my_ansible.cfg_file
> mkdir -p group_vars/all
> cd group_vars/all
> ansible-vault create syspass.yml
New Vault password: 
Confirm New Vault password: 
> ansible-vault edit syspass.yml
Vault password:
syspass_auth_token: ##################################################
syspass_token_pass: ##################################################
syspass_verify_ssl: True
syspass_api_url: ##################################################
syspass_api_version: 3.1
syspass_debug: False
syspass_debug_level: 3
syspass_verbose: True
syspass_verbose_level: 3
~                                                                                                                                                                                         
~                                                                                                                                                                                         
~                                                                                                                                                                                         
~                                                                                                                                                                                         
-- INSERTION --    
^Z :wq
> export DEFAULT_VAULT_PASSWORD_FILE="/my_private_directory/vault_passwd"
> echo "password1234" > $DEFAULT_VAULT_PASSWORD_FILE
> cd directory_where_is_my_ansible.cfg_file
> ansible-playbook --vault-password-file=$DEFAULT_VAULT_PASSWORD_FILE playbooks/playbook.yml
```

Parameters:
-----------

- **chars**: (Optional)
     
     Type of chars used during a password generation, 
     
     Allowed value: ``ascii_letters``, ``digits``, ``allowed_punctuation``
     
     Default value: ['ascii_letters','digits','allowed_punctuation']
     
- **psswd_length**: (Optional)

     password length, during a password generation, that value is automatically clamped from ``password_length_min`` and ``password_length_max``

     Default value: 42
    
- **password**: (Optional)

     Directly impose a password, it shortcut the password generation
    
- **hostname**: (Optional is set by Ansible)

     Require by Ansible, it correspond to Ansible host, you can impose a specific host from here

- **account**: 
     
     Match with Syspass API Account https://syspass-doc.readthedocs.io/en/3.1/application/api.html#accounts
     
- **login**:
     
     login given to created account
     
- **category**:

     Match with Syspass API Categories https://syspass-doc.readthedocs.io/en/3.1/application/api.html#categories
     
- **customer**:

     Match with Syspass API Clients https://syspass-doc.readthedocs.io/en/3.1/application/api.html#clients
     
- **customer_desc**: (Optional)

     Match with Syspass API Clients creation/description https://syspass-doc.readthedocs.io/en/3.1/application/api.html#clients

- **tags**:

     Match with Syspass API Tags https://syspass-doc.readthedocs.io/en/3.1/application/api.html#tags
     
- **url**: 

     url given to created account (Optional)
     
- **notes**:

     notes given to created account (Optional)
     
- **state**:

     Default Value: ``present``
     Allowed Value: ``present`` or ``absent``
     
- **private**: self.private,

     is this password private for users who have access or public for all users in acl (default false)
     
- **privategroup**: self.privategroup,

    is private only for users in same group (default false)
    
- **expireDate**: self.expireDate

    expiration date given to created account (Optional)
    
    Allowed Value: Expire date in UNIX timestamp format

    
notes:
-----
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

### IN PLAYBOOK ###

NOTE: Default values are handled 

##### USAGE 1 #####
```yamlex
    - name: SysPass | Minimal test | get and if not exist insert
      debug:
        msg: "{{ lookup('syspass', 'Account Name minimal', login='mylogin', category='MySQL', customer='PREP') }}"
      register: pass1
      changed_when: false

    - name: SysPass | Minimal test | get and compare
      debug:
        msg: "{{ lookup('syspass', 'Account Name minimal', login='mylogin', category='MySQL', customer='PREP') }}"
      register: pass2
      changed_when: pass1.msg == pass2.msg
      failed_when: pass1.msg != pass2.msg
```
**Authors**:
Gousseaud Gaëtan <gousseaud.gaetan.pro@gmail.com>
Pierre-Henry Muller <pierre-henry.muller@digdeo.fr>
Jérôme Ornech <i.dont.share.my.mail@nothing.fr>
