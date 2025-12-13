# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2025 CERN.
# Copyright (C) 2019-2022 Northwestern University.
# Copyright (C)      2022 TU Wien.
# Copyright (C)      2022 Graz University of Technology.
#
# Invenio App RDM is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JS/CSS Webpack bundles for theme."""

import os

from flask import current_app
from invenio_assets.webpack import WebpackThemeBundle
from werkzeug.local import LocalProxy


def build_static_path(subpath):
    """Return a lazy loaded path under `COLLECT_STATIC_ROOT`."""
    return LocalProxy(
        lambda: os.path.join(current_app.config["COLLECT_STATIC_ROOT"], subpath)
    )


theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "invenio-administration-search": "./js/invenio_administration/src/search/search.js",
                "invenio-administration-edit": "./js/invenio_administration/src/edit/edit.js",
                "invenio-administration-create": "./js/invenio_administration/src/create/create.js",
                "base-admin-theme": "./js/invenio_administration/src/theme.js",
                "invenio-administration-details": "./js/invenio_administration/src/details/details.js",
            },
            dependencies={
                "@babel/runtime": "^7.9.0",
                "@tinymce/tinymce-react": "^4.3.0",
                "tinymce": "^6.7.2",
                "i18next": "^20.3.0",
                "i18next-browser-languagedetector": "^6.1.0",
                "luxon": "^1.23.0",
                "path": "^0.12.7",
                "prop-types": "^15.7.2",
                "react-copy-to-clipboard": "^5.0.0",
                "react-i18next": "^11.11.0",
                "react-invenio-forms": "^4.0.0",
                "react-searchkit": "^3.0.0",
                "yup": "^0.32.0",
                "formik": "^2.2.9",
            },
            aliases={
                # Define Semantic-UI theme configuration needed by
                # Invenio-Theme in order to build Semantic UI (in theme.js
                # entry point). theme.config itself is provided by
                # cookiecutter-invenio-rdm.
                "@js/invenio_administration": "js/invenio_administration",
                "@translations/invenio_administration": "translations/invenio_administration",
            },
            copy=[
                # Copy some assets into "static/dist", as TinyMCE requires that
                # Note that the base path for all entries is the `config.json` directory
                {
                    "from": "../node_modules/tinymce/skins/content/default/content.css",
                    "to": build_static_path("dist/js/skins/content/default"),
                },
                {
                    "from": "../node_modules/tinymce/skins/ui/oxide/skin.min.css",
                    "to": build_static_path("dist/js/skins/ui/oxide"),
                },
                {
                    "from": "../node_modules/tinymce/skins/ui/oxide/content.min.css",
                    "to": build_static_path("dist/js/skins/ui/oxide"),
                },
            ],
        ),
    },
)
