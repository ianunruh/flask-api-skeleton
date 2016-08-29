from marshmallow import Schema, fields


class SessionSchema(Schema):
    id = fields.Int()

    user = fields.Nested('UserSchema')

    token = fields.Method('get_token')

    user_agent = fields.Str()
    ip_address = fields.Str()
    platform = fields.Str()
    browser = fields.Str()

    created_at = fields.DateTime()
    last_active_at = fields.DateTime()

    def get_token(self, session):
        if self.context.get('on_create'):
            return session.token


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()
    password = fields.Str(load_only=True)
