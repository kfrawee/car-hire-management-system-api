from marshmallow import (
    Schema,
    ValidationError,
    fields,
    post_dump,
    validate,
    validates_schema,
)

DEFAULT_STRING_KWARGS = {
    "validate": [validate.Predicate("isascii"), validate.Length(min=1)]
}


class CreateCustomer(Schema):
    """For create customer request validation and response dump/order"""

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


class UpdateCustomer(Schema):
    """For update customer request validation"""

    first_name = fields.String(**DEFAULT_STRING_KWARGS)
    last_name = fields.String(**DEFAULT_STRING_KWARGS)
    email = fields.Email()
    phone_number = fields.String(
        validate=validate.Length(max=11, error="Please enter a valid phone number."),
    )
    address = fields.String(**DEFAULT_STRING_KWARGS)

    @validates_schema
    def validate_data_input(self, data, **kwargs):
        fields_to_update = any(
            [
                data.get("first_name"),
                data.get("last_name"),
                data.get("email"),
                data.get("phone_number"),
                data.get("address"),
            ]
        )

        if not fields_to_update:
            raise ValidationError("No fields to update.")

    class Meta:
        ordered = True

    @post_dump
    def return_dict(self, data, **kwargs):
        """Post dump hook: Convert OrderedDict to Dict"""
        return dict(data)
