# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# InvenioAdministration is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio-Administration Permissions Generators."""

from invenio_records_permissions.generators import Generator

from invenio_administration.permissions import administration_access_action


class Administration(Generator):
    """Allows administration-access."""

    def __init__(self):
        """Constructor."""
        super(Administration, self).__init__()

    def needs(self, **kwargs):
        """Enabling Needs."""
        return [administration_access_action]
