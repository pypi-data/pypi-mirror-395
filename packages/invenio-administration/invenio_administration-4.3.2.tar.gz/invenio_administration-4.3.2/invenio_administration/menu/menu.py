# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022-2024 CERN.
# Copyright (C) 2023 Graz University of Technology.
# Copyright (C) 2024 KTH Royal Institute of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Administration menu module."""

import urllib.parse

from flask import request
from invenio_i18n import lazy_gettext as _
from invenio_theme.proxies import current_theme_icons
from speaklater import make_lazy_string

from invenio_administration.permissions import administration_permission


class AdminMenu:
    """Main class for the admin menu."""

    def __init__(self):
        """Constructor."""
        self._menu_items = []

    @property
    def items(self):
        """Return all raw menu items."""
        return self._menu_items

    def register_menu_entries(self, flask_menu_instance, menu_key="admin_navigation"):
        """Register all menu items to a flask menu instance."""
        main_menu = flask_menu_instance.submenu(menu_key)

        # items without category go first and the rest are sorted alphabetically
        ordered_menu_items = sorted(
            self._menu_items,
            key=lambda menu_item: (menu_item.category is not None, menu_item.category),
        )

        for menu_entry in ordered_menu_items:
            category = menu_entry.category
            name = menu_entry.name
            endpoint = menu_entry.endpoint
            order = menu_entry.order
            active_when = menu_entry.active_when
            label = menu_entry.label
            icon = menu_entry.icon
            disabled = menu_entry.disabled

            if disabled():
                continue

            if category:
                category_menu = main_menu.submenu(category)
                category_menu.register(text=category)
                category_menu.submenu(name).register(
                    endpoint=endpoint,
                    text=label,
                    order=order,
                    active_when=active_when or self.sub_content_active_when,
                    icon=icon,
                )
            else:
                main_menu.submenu(name).register(
                    endpoint=endpoint,
                    text=label,
                    order=order,
                    active_when=active_when or self.default_active_when,
                    icon=icon,
                )

    def register_admin_entry(self, current_menu, endpoint):
        """Register administration entry as the last one."""
        current_menu.submenu("profile-admin.administration").register(
            f"{endpoint}.dashboard",
            _(
                "%(icon)s Administration",
                icon=make_lazy_string(
                    lambda: f'<i class="{current_theme_icons.cogs}"></i>'
                ),
            ),
            order=1,
            visible_when=lambda: administration_permission.can(),
        )

    def add_menu_item(self, item, index=None):
        """Add menu item."""
        if not isinstance(item, MenuItem):
            return TypeError(_("Item should be MenuItem instance."))

        if index:
            self._menu_items[index] = item
            return

        self._menu_items.append(item)

    def add_view_to_menu(self, view, index=None):
        """Add menu item from view."""
        menu_item = MenuItem(
            endpoint=view.endpoint,
            name=view.name,
            category=view.category,
            label=view.menu_label,
            order=view.order,
            icon_key=view.icon,
            disabled=view.disabled,
        )

        self.add_menu_item(menu_item, index)

    @staticmethod
    def default_active_when(self):
        """Default condition for the menu item active state."""
        return request.endpoint == self._endpoint

    @staticmethod
    def sub_content_active_when(self):
        """Condition for menu items with sub content.

        Makes all pages with derivative URL highlight the parent menu.
        """
        menu_url = urllib.parse.urlparse(self.url)
        request_url = urllib.parse.urlparse(request.url_rule.rule)

        return request_url.path == menu_url.path or request_url.path.startswith(
            f"{menu_url.path}/"
        )


class MenuItem:
    """Class for menu item."""

    def __init__(
        self,
        name="",
        endpoint="",
        category="",
        order=0,
        icon_key=None,
        active_when=None,
        label="",
        disabled=lambda x: False,
    ):
        """Constructor."""
        self.name = name
        self.endpoint = endpoint
        self.category = category
        self.order = order
        self.active_when = active_when
        self.icon_key = icon_key
        self.label = label
        self.disabled = disabled

    @property
    def icon(self):
        """Return corresponding template path for icon."""
        if not self.icon_key:
            return None

        return current_theme_icons[self.icon_key]
