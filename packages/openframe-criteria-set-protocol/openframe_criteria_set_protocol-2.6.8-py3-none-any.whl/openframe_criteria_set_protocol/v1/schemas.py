from marshmallow import Schema, fields

criteria_set_id = r'^[a-zA-Z0-9.\-_]+$'
version = r'^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$'


class TreeBodySchema(Schema):
    values = fields.Dict(required=False, dump_default=dict())
    parameters = fields.Dict(required=False, dump_default=dict())


class MatrixBodySchema(Schema):
    values = fields.Dict(required=False, dump_default=dict())
    parameters = fields.Dict(required=False, dump_default=dict())
    additional = fields.Raw(required=False, dump_default=None)
