# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio admin extension."""

from invenio_base.utils import entry_points

from . import config
from .admin import Administration
from .views.base import AdminResourceBaseView, AdminView


class InvenioAdministration:
    """Invenio extension."""

    def __init__(self, app=None, entry_point_group="invenio_administration.views"):
        """Extension initialization."""
        self.entry_point_group = entry_point_group

        self.administration = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize application."""
        self.view_classes = []
        self.init_config(app)
        self.administration = Administration(
            app,
            name=app.config["ADMINISTRATION_APPNAME"],
            base_template=app.config["ADMINISTRATION_BASE_TEMPLATE"],
        )
        if self.entry_point_group:
            self.load_entry_point_group(app)
        app.extensions["invenio-administration"] = self

    def load_entry_point_group(self, app):
        """Load admin interface views from entry point group."""
        entrypoints = entry_points(group=self.entry_point_group)
        for ep in entrypoints:
            entry_point = self._load_entry_point(ep)
            entrypoint_path = ep.value

            extension_name_from_path = self._extract_extension_name(entrypoint_path)
            extension_name_from_view = entry_point.extension_name
            # fallback to extracted extension_name if property not set on view
            extension_name = extension_name_from_view or extension_name_from_path

            self.register_view(entry_point, extension_name, app)
        app.register_blueprint(self.administration.blueprint)

    def _load_entry_point(self, entry_point):
        """Loads one entry point. Validates whether its view is an AdminView."""
        ep = entry_point.load()
        if not issubclass(ep, AdminView):
            raise TypeError(f"View class must be of type {AdminView.__name__}")
        return ep

    def register_view(self, view_class, extension_name, app, *args, **kwargs):
        """Register an admin view on this admin instance.

        :param view_class: The view class name passed to the view factory.
        :param extension_name: The name of the extension associated with the view.
        :param args: Positional arguments for view class.
        :param kwargs: Keyword arguments to view class.
        """
        view_instance = view_class(
            extension_name=extension_name, admin=self.administration, *args, **kwargs
        )
        view = view_class.as_view(
            view_class.name,
            extension_name=extension_name,
            admin=self.administration,
            *args,
            **kwargs,
        )
        self.administration.add_view(view, view_instance, *args, **kwargs)
        if issubclass(view_class, AdminResourceBaseView):
            self.register_resource(app, view_class, extension_name)

    def register_resource(self, app, view_class, extension_name):
        """Set views schema."""
        self.view_classes.append((view_class, extension_name))

    @staticmethod
    def _extract_extension_name(entrypoint_path):
        name = entrypoint_path.split(".")[0]
        normalized_name = name.replace("_", "-")
        return normalized_name

    @staticmethod
    def init_config(app):
        """Initialize configuration.

        :param app: The Flask application.
        """
        # Set default configuration
        for k in dir(config):
            if k.startswith("ADMINISTRATION_"):
                app.config.setdefault(k, getattr(config, k))


def finalize_app(app):
    """Finalize the app."""
    view_classes = app.extensions["invenio-administration"].view_classes

    for view_class, extension_name in view_classes:
        if view_class.resource_config:
            view_class.set_resource(extension_name=extension_name)
        if view_class.schema:
            view_class.set_schema(extension_name=extension_name)

    app.extensions["invenio-administration"].administration.init_menu()
