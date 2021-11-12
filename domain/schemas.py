"""
This is a python document to work with schemas validation in marshmallow
"""
# ---------------------------------------------------------------------------------------------------------------Imports
from marshmallow import Schema, fields


# --------------------------------------------------------------------------parameters for each request structure needed
class PlayerSchema(Schema):
    IdPlayer = fields.Int(required=True)
    PlayerName = fields.Str(required=True)
    PlayerScore = fields.Float(required=True)


class CardSchema(Schema):
    IdCard = fields.Int(required=True)
    CardName = fields.Str(required=True)
    CardAttack = fields.Int(required=True)
    CardDefense = fields.Int(required=True)
    CardImage = fields.Str(required=True)


class ParameterLoadSchema(Schema):
    attribute = fields.Str(required=True)
    value = fields.Field(required=True)
# ----------------------------------------------------------------------------------------------------------------------
