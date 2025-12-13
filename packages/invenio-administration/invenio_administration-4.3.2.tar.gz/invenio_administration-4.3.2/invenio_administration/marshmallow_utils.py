# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022-2024 CERN.
# Copyright (C) 2023-2024 KTH Royal Institute of Technology.
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio administration marshmallow utils module."""
import marshmallow
from invenio_i18n import lazy_gettext as _
from marshmallow import fields
from marshmallow_utils import fields as invenio_fields
from marshmallow_utils.fields import EDTFDateString, EDTFDateTimeString

custom_mapping = {
    # marshmallow
    fields.Str: "string",
    fields.Integer: "integer",
    fields.List: "array",
    fields.Dict: "object",
    fields.Url: "string",
    fields.String: "string",
    fields.DateTime: "datetime",
    fields.Float: "float",
    fields.Boolean: "bool",
    fields.Raw: "dict",
    fields.UUID: "uuid",
    fields.Time: "time",
    fields.Date: "date",
    fields.TimeDelta: "timedelta",
    fields.Decimal: "decimal",
    fields.Enum: "string",
    fields.Method: "function",
    # invenio fields
    invenio_fields.SanitizedUnicode: "string",
    invenio_fields.links.Links: "array",
    invenio_fields.links.Link: "string",
    invenio_fields.tzdatetime.TZDateTime: "datetime",
    invenio_fields.sanitizedhtml.SanitizedHTML: "html",
    invenio_fields.isodate.ISODateString: "date",
    invenio_fields.url.URL: "string",
    EDTFDateString: "date",
    EDTFDateTimeString: "datetime",
}


def find_type_in_mapping(field_type, custom_mapping):
    """
    Find a field type by traversing the inheritance chain.

    Args:
        field_type (Type): The field type to be searched.
        custom_mapping (dict): The mapping of types.

    Returns:
        The mapped value for the found field type.

    Raises:
        KeyError: If the field type is not found in the mapping.
    """
    current_type = field_type
    while current_type:
        if current_type in custom_mapping:
            return custom_mapping[current_type]
        current_type = current_type.__base__

    raise KeyError(_("Unrecognized field type: %(field_type)s", field_type=field_type))


def jsonify_schema(schema):
    """Marshmallow schema to dict."""
    schema_dict = {}
    for field, field_type in schema.fields.items():
        is_links = isinstance(field_type, invenio_fields.links.Links)

        if is_links:
            continue

        is_read_only = field_type.dump_only
        is_create_only = (
            field_type.metadata["create_only"]
            if "create_only" in field_type.metadata
            else False
        )

        field_type_name = field_type.__class__
        is_required = field_type.required

        nested_field = isinstance(field_type, fields.Nested)
        list_field = isinstance(field_type, fields.List)

        dump_default = field_type.dump_default if field_type.dump_default else None
        load_default = field_type.load_default if field_type.load_default else None
        if callable(dump_default):
            dump_default = dump_default()
        if callable(load_default):
            load_default = load_default()

        schema_dict[field] = {
            "required": is_required,
            "readOnly": is_read_only,
            "title": (
                field_type.metadata["title"] if "title" in field_type.metadata else None
            ),
            "createOnly": is_create_only,
            "metadata": field_type.metadata,
            "dump_default": dump_default,
            "load_default": load_default,
        }

        options = field_type.validate
        if options and hasattr(options, "choices"):
            schema_dict[field].update({"enum": list(options.choices)})

        if nested_field:
            schema_type = getattr(
                field_type.schema, "administration_schema_type", "object"
            )
            schema_dict[field].update(
                {
                    "type": schema_type,
                    "properties": jsonify_schema(field_type.schema),
                }
            )
        elif list_field and isinstance(field_type.inner, fields.Nested):
            # list of objects (vocabularies or nested)
            schema_type = getattr(
                field_type.inner.schema, "administration_schema_type", "object"
            )
            schema_dict[field].update(
                {
                    "type": "array",
                    "items": {
                        "type": schema_type,
                        "properties": jsonify_schema(field_type.inner.schema),
                    },
                }
            )
        elif list_field and not isinstance(field_type.inner, fields.Nested):
            # list of plain types
            schema_dict[field].update(
                {
                    "type": "array",
                    "items": {
                        "type": find_type_in_mapping(
                            field_type.inner.__class__, custom_mapping
                        )
                    },
                }
            )
        else:
            try:
                field_type_mapping = find_type_in_mapping(
                    field_type_name, custom_mapping
                )
                schema_dict[field].update(
                    {
                        "type": field_type_mapping,
                    }
                )
            except KeyError:
                raise Exception(
                    _(
                        "Unrecognised schema field %(field)s: %(field_type_name)s",
                        field=field,
                        field_type_name=field_type_name,
                    )
                )

    return schema_dict
