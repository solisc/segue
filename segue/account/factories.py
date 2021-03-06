from segue.factory import Factory

from models import Account, ResetPassword

import schema

class AccountFactory(Factory):
    model = Account

    UPDATE_WHITELIST = schema.signup["properties"].keys()

    @classmethod
    def clean_for_insert(cls, data):
        data = { c:v for c,v in data.items() if c in AccountFactory.UPDATE_WHITELIST }
        data['document'] = data.pop('cpf', None) or data.pop('passport', None) or data.pop('document', None)
        return data;

    @classmethod
    def clean_for_update(cls, data):
        update_whitelist = AccountFactory.UPDATE_WHITELIST[:]
        update_whitelist.remove('email')
        data = { c:v for c,v in data.items() if c in update_whitelist }
        data['document'] = data.pop('cpf', None) or data.pop('passport', None) or data.pop('document', None)
        return data;


class ResetPasswordFactory(Factory):
    model = ResetPassword

    @classmethod
    def create(cls, account, hash_code):
        reset = cls.model()
        reset.account = account
        reset.hash    = hash_code
        return reset
