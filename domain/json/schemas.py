from marshmallow import Schema, fields


class PlayerSchema(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    score = fields.Float()

class CardSchema(Schema):
    id=fields.Int(required=True)
    name=fields.Str(required=True)
    attack=fields.Int(required=True)
    defense=fields.Int(required=True)
