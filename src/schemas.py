from marshmallow import Schema, fields, post_dump, validate

DEFAULT_STRING_KWARGS = {
    "validate": [validate.Predicate("isascii"), validate.Length(min=1)]
}


class CreateOrUpdateCustomer(Schema):
    """For request validation and response dump/order"""

    customer_id = fields.String()  # XXX for dump only

    first_name = fields.String(**DEFAULT_STRING_KWARGS, required=True)
    last_name = fields.String(**DEFAULT_STRING_KWARGS, required=True)
    email = fields.Email(required=True)
    phone_number = fields.String(
        validate=validate.Length(max=11, error="Please enter a valid phone number."),
        required=True,
    )
    address = fields.String(**DEFAULT_STRING_KWARGS, required=True)

    created_on = fields.String()
    updated_on = fields.String(allow_none=True, missing=None)

    class Meta:
        ordered = True

    @post_dump
    def return_dict(self, data, **kwargs):
        """Post dump hook: Convert OrderedDict to Dict"""
        return dict(data)
