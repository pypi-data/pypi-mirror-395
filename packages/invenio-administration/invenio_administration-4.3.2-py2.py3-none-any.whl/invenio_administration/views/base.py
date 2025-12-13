# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022-2024 CERN.
# Copyright (C) 2024 Graz University of Technology.
# Copyright (C) 2024 KTH Royal Institute of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Administration views base module."""
from functools import partial

from flask import current_app, render_template, url_for
from flask.views import MethodView
from invenio_i18n import lazy_gettext as _
from invenio_search_ui.searchconfig import search_app_config

from invenio_administration.errors import (
    InvalidActionsConfiguration,
    InvalidExtensionName,
    InvalidResource,
    MissingDefaultGetView,
    MissingExtensionName,
    MissingResourceConfiguration,
)
from invenio_administration.marshmallow_utils import jsonify_schema
from invenio_administration.permissions import administration_permission


class AdminView(MethodView):
    """Base view for admin views."""

    extension_name = None
    name = None
    category = None
    template = "invenio_administration/index.html"
    url = None
    menu_label = None
    order = None
    icon = None

    decorators = [administration_permission.require(http_exception=403)]

    def __init__(
        self,
        name=__name__,
        category=None,
        url=None,
        extension_name=None,
        admin=None,
        order=0,
        icon=None,
    ):
        """Constructor."""
        if self.extension_name is None:
            self.extension_name = extension_name

        if self.name is None:
            self.name = name

        if self.category is None:
            self.category = category

        if self.menu_label is None:
            self.menu_label = self.name

        self.administration = admin

        if self.order is None:
            self.order = order

        if self.icon is None:
            self.icon = icon

        self.url = url or self._get_view_url(self.url)

        # Default view
        if self.get is None:
            raise MissingDefaultGetView(self.__class__.__name__)

    @staticmethod
    def disabled():
        """Determine if the view should be disabled."""
        return False

    @property
    def endpoint(self):
        """Get name for endpoint location e.g: 'administration.index'."""
        if self.administration is None:
            return self.name
        return f"{self.administration.endpoint}.{self.name}"

    @classmethod
    def _get_view_extension(cls, extension_name=None):
        """Get the flask extension of the view."""
        try:
            if extension_name:
                return current_app.extensions[extension_name]
            return current_app.extensions[cls.extension_name]
        except KeyError:
            raise InvalidExtensionName(extension_name)

    def _get_view_url(self, url):
        """Generate URL for the view. Override to change default behavior."""
        new_url = url
        if new_url is None:
            if isinstance(self, self.administration.dashboard_view_class):
                new_url = "/"
            else:
                new_url = "/%s" % self.name.lower()
        else:
            if not url.startswith("/"):
                new_url = "/%s" % (url)
        # Sanitize url
        new_url = new_url.replace(" ", "_")
        return new_url

    def _get_template(self):
        return self.template

    def render(self, **kwargs):
        """Render template."""
        kwargs["admin_base_template"] = self.administration.base_template
        return render_template(self._get_template(), **kwargs)

    def get(self):
        """GET view method."""
        return self.render()


class AdminResourceBaseView(AdminView):
    """Base view for admin resources."""

    display_edit = False
    display_delete = False
    resource_config = None
    resource = None
    actions = {}
    schema = None
    api_endpoint = None
    pid_path = "pid"
    title = None
    resource_name = None

    create_view_name = None
    list_view_name = None
    request_headers = {"Accept": "application/json"}

    def __init__(
        self,
        name=__name__,
        category=None,
        url=None,
        extension_name=None,
        admin=None,
        order=0,
        icon=None,
    ):
        """Constructor."""
        super().__init__(name, category, url, extension_name, admin, order, icon)

        if self.extension_name is None:
            raise MissingExtensionName(self.__class__.__name__)
        if self.resource_config is None:
            raise MissingResourceConfiguration(self.__class__.__name__)

    @classmethod
    def set_schema(cls):
        """Set schema."""
        cls.schema = cls.get_service_schema()

    @classmethod
    def set_resource(cls, extension_name=None):
        """Set resource."""
        cls.resource = cls._get_resource(extension_name)

    @classmethod
    def _get_resource(cls, extension_name=None):
        extension_name = cls._get_view_extension(extension_name)
        try:
            return getattr(extension_name, cls.resource_config)
        except AttributeError:
            raise InvalidResource(resource=cls.resource_config, view=cls.__name__)

    @classmethod
    def get_service_schema(cls):
        """Get marshmallow schema of the assigned service."""
        # schema.schema due to the schema wrapper imposed,
        # when the actual class needed
        return cls.resource.service.schema.schema()

    def _schema_to_json(self, schema):
        """Translate marshmallow schema to JSON.

        Provides action payload template for the frontend.
        """
        return jsonify_schema(schema)

    def get_api_endpoint(self, **kwargs):
        """Get search API endpoint."""
        api_url_prefix = current_app.config["SITE_API_URL"]
        slash_tpl = "/" if not self.api_endpoint.startswith("/") else ""

        if not self.api_endpoint.startswith(api_url_prefix):
            return f"{api_url_prefix}{slash_tpl}{self.api_endpoint}"

        return f"{slash_tpl}{self.api_endpoint}"

    def get_actions(self):
        """Get actions attribute."""
        return self.actions

    def serialize_actions(self):
        """Serialize actions for the resource frontend view.

        {"action_name":
            {"text": "Action"
             "payload_schema": schema in json
             "order": 1
             }
         }
        """
        serialized_actions = {}
        for key, value in self.get_actions().items():
            if "payload_schema" and "order" not in value:
                raise InvalidActionsConfiguration

            serialized_actions[key] = {**value}

            if value["payload_schema"] is not None:
                serialized_actions[key]["payload_schema"] = self._schema_to_json(
                    value["payload_schema"]()
                )

        return serialized_actions

    def get_list_view_endpoint(self):
        """Returns administration UI list view endpoint."""
        if self.list_view_name:
            return url_for(f"administration.{self.list_view_name}")
        if isinstance(self, AdminResourceListView):
            return url_for(f"administration.{self.name}")

    def get_create_view_endpoint(self):
        """Returns administration UI list view endpoint."""
        if self.create_view_name:
            return url_for(f"administration.{self.create_view_name}")


class AdminResourceDetailView(AdminResourceBaseView):
    """Details view based on given config."""

    display_edit = True
    display_delete = True

    name = None
    item_field_exclude_list = None
    item_field_list = None
    template = "invenio_administration/details.html"
    title = _("Resource details")

    def get_context(self, pid_value=None):
        """Create details view context."""
        name = self.name
        schema = self.get_service_schema()
        serialized_schema = self._schema_to_json(schema)
        fields = self.item_field_list
        return {
            "request_headers": self.request_headers,
            "name": name,
            "resource_schema": serialized_schema,
            "fields": fields,
            "exclude_fields": self.item_field_exclude_list,
            "ui_config": self.item_field_list,
            "pid": pid_value,
            "api_endpoint": self.get_api_endpoint(),
            "title": self.title,
            "list_endpoint": self.get_list_view_endpoint(),
            "actions": self.serialize_actions(),
            "pid_path": self.pid_path,
            "display_edit": self.display_edit,
            "display_delete": self.display_delete,
            "list_ui_endpoint": self.get_list_view_endpoint(),
            "resource_name": (
                self.resource_name if self.resource_name else self.pid_path
            ),
        }

    def get(self, pid_value=None):
        """GET view method."""
        return self.render(**self.get_context(pid_value=pid_value))


class AdminFormView(AdminResourceBaseView):
    """Basic form view."""

    form_fields = None
    display_read_only = True

    def get(self, pid_value=None):
        """GET view method."""
        schema = self.get_service_schema()
        serialized_schema = self._schema_to_json(schema)
        form_fields = self.form_fields
        return self.render(
            **{
                "resource_schema": serialized_schema,
                "form_fields": form_fields,
                "pid": pid_value,
                "api_endpoint": self.get_api_endpoint(),
                "title": self.title,
                "list_endpoint": self.get_list_view_endpoint(),
                "ui_config": self.form_fields,
            }
        )


class AdminResourceEditView(AdminFormView):
    """Admin resource edit view."""

    template = "invenio_administration/edit.html"
    title = _("Edit resource")


class AdminResourceCreateView(AdminFormView):
    """Admin resource edit view."""

    template = "invenio_administration/create.html"
    title = _("Create resource")


class AdminResourceListView(AdminResourceBaseView):
    """List view based on provided resource."""

    template = "invenio_administration/search.html"

    # decides if there is a detail view
    display_read = True
    display_create = True

    # hides searchbar
    display_search = True

    search_config_name = None
    search_facets_config_name = None
    search_sort_config_name = None
    sort_options = {}
    available_facets = {}
    item_field_exclude_list = None
    item_field_list = None
    api_endpoint = None
    item_api_endpoint = None
    title = None

    search_request_headers = {"Accept": "application/json"}

    def get_search_request_headers(self, **kwargs):
        """Get search request headers."""
        return self.search_request_headers

    def get_search_app_name(self, **kwargs):
        """Get search app name."""
        if self.search_config_name is None:
            return f"{self.name.upper()}_SEARCH"
        return self.search_config_name

    def init_search_config(self, **kwargs):
        """Build search view config."""
        return partial(
            search_app_config,
            config_name=self.get_search_app_name(**kwargs),
            available_facets=current_app.config.get(self.search_facets_config_name),
            sort_options=current_app.config[self.search_sort_config_name],
            endpoint=self.get_api_endpoint(**kwargs),
            headers=self.get_search_request_headers(**kwargs),
            pagination_options=(20, 50),
            default_size=20,
        )

    def get_sort_options(self):
        """Get search sort options."""
        if not self.sort_options:
            return self.resource.service.config.search.sort_options
        return self.sort_options

    def get_available_facets(self):
        """Get search available facets."""
        if not self.available_facets:
            return self.resource.service.config.search.facets
        return self.available_facets

    def get_context(self, **kwargs):
        """Create details view context."""
        search_conf = self.init_search_config(**kwargs)
        schema = self.get_service_schema()
        serialized_schema = self._schema_to_json(schema)
        pid_value = kwargs.get("pid_value", "")
        return {
            "search_config": search_conf,
            "title": self.title,
            "name": self.name,
            "resource_schema": serialized_schema,
            "fields": self.item_field_list,
            "display_search": self.display_search,
            "display_create": self.display_create,
            "display_edit": self.display_edit,
            "display_delete": self.display_delete,
            "display_read": self.display_read,
            "actions": self.serialize_actions(),
            "pid_path": self.pid_path,
            "pid_value": pid_value,
            "create_ui_endpoint": self.get_create_view_endpoint(),
            "list_ui_endpoint": self.get_list_view_endpoint(),
            "resource_name": (
                self.resource_name if self.resource_name else self.pid_path
            ),
        }

    def get(self, **kwargs):
        """GET view method."""
        return self.render(**self.get_context(**kwargs))


class AdminResourceViewSet:
    """View set based on resource.

    Provides a list view and a details view given the provided configuration.
    """

    extension_name = None
    name = None
    category = None
    template = "invenio_administration/index.html"
    url = None
    menu_label = None

    resource_config = None
    resource = None

    schema = None
    api_endpoint = None
    pid_path = "pid"
    title = None
    actions = None

    create_view_name = None
    edit_view_name = None
    details_view_name = None
    list_view_name = None

    display_create = False
    display_read = True
    display_edit = False
    display_delete = False

    sort_options = ()
    available_filters = None
    item_field_exclude_list = None
    item_field_list = None

    def list_view(self):
        """List view."""
        pass

    def details_view(self):
        """Details view."""
        pass

    def edit_view(self):
        """Details view."""
        pass

    def create_view(self):
        """Details view."""
        pass
