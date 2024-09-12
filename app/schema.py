# schemas.py
from marshmallow import Schema, fields, validate, validates_schema, ValidationError

class UserSchema(Schema):
    name = fields.Str(required=True)
    
class GroupSchema(Schema):
    name = fields.Str(required=True)
    members = fields.List(fields.Int(required=True), required=True)

class SettleupSchema(Schema):
    user_id = fields.Int(required=True)
    amount = fields.Float(required=True, validate=validate.Range(min=0))

class ExpenseSchema(Schema):
    reason = fields.Str(required=False)
    expense_by = fields.Int(required=True)
    expense_to = fields.List(fields.Nested(SettleupSchema), required=True)
    amount = fields.Float(required=True, validate=validate.Range(min=0))
    group_id = fields.Int(required=True)

    @validates_schema
    def validate_total_amount(self, data, **kwargs):
        total_settleup_amount = sum(item['amount'] for item in data['expense_to'])
        if total_settleup_amount != data['amount']:
            raise ValidationError('The total of expense_to amounts must equal the expense amount', field_names=['amount'])
        


