from marshmallow import Schema, fields


class PlayerSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    score = fields.Float()




