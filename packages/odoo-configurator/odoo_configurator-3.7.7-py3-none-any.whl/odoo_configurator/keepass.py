# Copyright (C) 2023 - Scalizer (<https://www.scalizer.fr>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

import cryptocode
import os
import getpass
from .logging import get_logger
from pykeepass import PyKeePass

logger = get_logger(__name__)


class KeepassCli:
    _name = "Keepass"

    def __init__(self, configurator, keepass_password=''):
        self.configurator = configurator
        self.init_keepass(keepass_password)

    def get_keepass_params(self):
        bitwarden_params = ['keepass_path', 'keepass_group']
        return {param: self.configurator.config.get(param) for param in bitwarden_params}

    def init_keepass(self, keepass_password):
        password = keepass_password or os.environ.get('KEEPASS_PASSWORD', '')
        self._keepass_password = password
        params = self.get_keepass_params()
        self.keepass_path = keepass_password or params.get('keepass_path', '')
        self.keepass_group = keepass_password or params.get('keepass_group', '')

    def get_keepass(self, filename):
        return PyKeePass(os.getenv("HOME") + "/" + filename, password=self._keepass_password)

    def get_keepass_entry(self, filename, group, entry):
        if not self._keepass_password:
            self._keepass_password = getpass.getpass('Keepass Password: ')
        kp = self.get_keepass(filename)
        kgroup = kp.find_groups(name=group, first=True)
        if kgroup:
            kentry = kp.find_entries(title=entry, group=kgroup, recursive=False, first=True)
            if kentry:
                return kentry
            else:
                logger.error("Cannot find %s in %s" % (entry, group))
                raise Exception("Cannot find %s in %s" % (entry, group))
        else:
            logger.error("Cannot find %s" % group)
            raise Exception("Cannot find %s" % group)

    def get_keepass_entry_value(self, filename, group, entry, field, default='admin'):
        try:
            if filename and group and entry:
                entry = self.get_keepass_entry(filename, group, entry)
            elif filename and group and not entry:
                entry = self.get_keepass_entry(self.keepass_path, filename, group)
            elif filename and not group and not entry:
                entry = self.get_keepass_entry(self.keepass_path, self.keepass_group, filename)
            else:
                raise ValueError('No keepass entry found')
        except Exception as err:
            logger.error(type(err).__name__)
            return False
        if entry:
            return eval('entry.' + field)
        return default

    def get_keepass_password(self, filename='', group='', entry=''):
        return self.get_keepass_entry_value(filename, group, entry, 'password')

    def get_keepass_password_crypt(self, filename='', group='', entry='', key=''):
        return cryptocode.encrypt(self.get_keepass_entry_value(filename, group, entry, 'password'), key)

    def get_keepass_user(self, filename='', group='', entry=''):
        return self.get_keepass_entry_value(filename, group, entry, 'username')

    def get_keepass_url(self, filename='', group='', entry=''):
        kp_url = self.get_keepass_entry_value(filename, group, entry, 'url')
        if kp_url and kp_url[-1] == '/':
            kp_url = kp_url[:-1]
        return kp_url
