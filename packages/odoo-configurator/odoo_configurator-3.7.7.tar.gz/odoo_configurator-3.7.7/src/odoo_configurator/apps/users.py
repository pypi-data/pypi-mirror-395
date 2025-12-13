# Copyright (C) 2023 - Teclib'ERP (<https://www.teclib-erp.com>).
# Copyright (C) 2024 - Scalizer (<https://www.scalizer.fr>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from . import base


class OdooUsers(base.OdooModule):
    _name = "Users"
    _key = "users"

    def apply(self):
        if self._key in self._datas:
            super(OdooUsers, self).apply()
            self.execute()


    def execute(self, datas=None):
        if not datas:
            datas = self._datas
        sections = datas.get(self._key, {})
        for section in sections:
            users = sections.get(section)
            self.logger.info("\t- %s" % section)
            for user in users:
                self.logger.info("\t\t- User %s" % user)
                self.update_user(users[user])
        if self._key in self._datas:
            self._datas.pop(self._key)
        if self._key in datas:
            datas.pop(self._key)

    def update_user(self, user_values):
        groups_id = []
        context = dict(user_values.get('context', {}))
        context.update(self._context)
        for group in user_values.get("groups_id", []):
            if group == "unlink all":
                groups_id.append((5,))
            else:
                groups_id.append(
                    (4, self._connection.get_ref(group)))

        login = user_values.get('login')
        if user_values.get('force_id', False):
            user_id = self.get_id_from_xml_id(user_values.get('force_id'))
        else:
            user_id = self.search('res.users', [('login', '=', login)], order='id', context=context)

        vals = dict(user_values.get('values', {}))
        if login:
            vals['login'] = login
        if groups_id:
            vals['groups_id'] = groups_id
        context['active_test'] = False
        if not user_id:
            self.execute_odoo('res.users', 'create', [vals], {'context': context})
            self.create_xml_id('external_config', 'res.users', login, user_id)
        else:
            self.execute_odoo('res.users', 'write', [user_id, vals], {'context': context})