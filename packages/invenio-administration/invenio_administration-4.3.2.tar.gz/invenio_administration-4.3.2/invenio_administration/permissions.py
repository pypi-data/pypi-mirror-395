# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# invenio-administration is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Permissions for administration module."""

from invenio_access import action_factory
from invenio_access.permissions import Permission

administration_access_action = action_factory("administration-access")
administration_permission = Permission(administration_access_action)
