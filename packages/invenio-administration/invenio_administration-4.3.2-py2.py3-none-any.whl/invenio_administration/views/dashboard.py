# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
# Copyright (C) 2024 KTH Royal Institute of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Administration dashboard view."""

from invenio_i18n import lazy_gettext as _

from invenio_administration.views.base import AdminView


class AdminDashboardView(AdminView):
    """Admin dashboard view."""

    template = "invenio_administration/index.html"
    name = "dashboard"
    url = "/"
    icon = "home"
    title = _("Dashboard")
    menu_label = _("Dashboard")
