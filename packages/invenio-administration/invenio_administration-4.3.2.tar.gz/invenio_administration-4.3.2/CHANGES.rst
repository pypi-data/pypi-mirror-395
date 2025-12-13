..
    Copyright (C) 2022-2024 CERN.
    Copyright (C) 2024-2025 Graz University of Technology.
    Copyright (C) 2024-2025 KTH Royal Institute of Technology.

    invenio-administration is free software; you can redistribute it and/or
    modify it under the terms of the MIT License; see LICENSE file for more
    details.

Changes
=======

Version v4.3.2 (released 2025-12-08)

- i18n: pulled translations
- tests: add option to keep services in `run-tests.sh`
- webpack: respect `COLLECT_STATIC_ROOT` when copying tinymce
- fix: typo in search empty resources message

Version v4.3.1 (released 2025-10-07)

- i18n: pulled translations
- index: change welcome message to be non RDM-specific

Version v4.3.0 (released 2025-08-06)

- theme: move TinyMCE from invenio-app-rdm to invenio-administration

- ui: fix recursive import of header_login.html

Version v4.2.0 (released 2025-07-17)

- i18n: pulled translations

Version v4.1.0 (released 2025-07-14)

- chores: replaced importlib_xyz with importlib
- i18n: run js compile_catalog
- i18n: run js extract msgs
- i18n: DeleteModal replace Trans component with i18next
- i18n: DeleteModalTrigger replace Trans component with i18next
- i18n: update ResultsPerPage label to use i18next for translation
- i18n: refactor compile catalog
- i18n: force pull translations
- i18n: extract msgs
- fix: include invenio-i18n dependency

Version v4.0.0 (released 2025-06-03)

- setup: bump major dependencies

Version v3.1.2 (released 2025-03-10)

- forms: handle date type in form generation

Version v3.1.1 (released 2025-03-10)

- ui: improve UX of modal button triggers

Version v3.1.0 (released 2025-01-24)

- modal: add support for custom modal SUI props

Version v3.0.0 (released 2024-12-10)

- tests: remove invenio-admin dependency
- setup: change to reusable workflows
- setup: bump major dependencies

Version v2.9.0 (released 2024-11-11)

- admin: change default # of results from 10 to 20
- fix: make tooltip required
- bug: fix type for BoolFormatter value

Version v2.8.2 (released 2024-10-10)

- webpack: bump react-searchkit to v3.0.0 due to axios upgrade

Version v2.8.1 (released 2024-10-10)

- setup: bump invenio-search-ui to fix dependency installation

Version v2.8.0 (released 2024-10-10)

- deps: update axios major version (needed only to run js tests)

Version v2.7.2 (released 2024-10-02)

- views: add callback hook on search results rendered

Version v2.7.1 (released 2024-10-02)

- details: remove parsing for name field

Version v2.7.0 (released 2024-09-26)

- feature: add display packages version badges in the sidebar

Version v2.6.0 (released 2024-09-26)

- actions: add actions properties (icon)
- actions: add possibility of pre-filling the action form
- form: add hidden field, lazy field
- form: refactor fields generation to improve readability and modular approach
- form: add overridable components

Version v2.5.0 (released 2024-08-22)

- package: bump react-invenio-forms
- ui: add comma separator to admin result count

Version v2.4.1 (released 2024-07-15)

- global: remove dependency on invenio-vocabularies
    * Delegates administration UI schema type definition to the mashmallow
      class.

Version 2.4.0 (released 2024-06-20)

- form: added support for json fields

Version 2.3.0 (released 2024-06-04)

- installation: upgrade invenio-records-resources and invenio-vocabularies
- marshmallow_utils: add enum to mapping
- ui: remove required restriction on fieldSchema

Version 2.2.3 (released 2024-05-24)

- views: accept kwars to be passed to get_api_endpoint

Version 2.2.2 (released 2024-05-23)

- views: allow list view to receive a pid_value

Version 2.2.1 (released 2024-05-15)

- remove implicit dependency on oai_pmh view

Version 2.2.0 (released 2024-03-22)

- fix: before_first_request deprecation (move to finalize app entry point)
- installation: upgrade invenio-app and invenio-base

Version 2.1.1 (released 2024-03-04)

- bump react-invenio-forms

Version 2.1.0 (released 2024-02-27)

- actions: add explicit prop for dropdown display
- form: updated mapping and added RichInput

Version 2.0.1 (released 2024-02-19)

- Add default bool value for BooleanField

Version 2.0.0 (released 2024-01-29)

- installation: bump invenio-accounts

Version 1.10.1 (2023-12-07)

- format: enforce code formatting using black
- marshmallow_utils: enhance marshmallow utility functions to traverse type inheritance
- i18n-global: add fuzzy search in compile-catalog

Version 1.10.0 (2023-11-30)

- marshmallw_utils: add EDTFDateTimeString mapping

Version 1.9.3 (2023-10-30)

- marshmallow_utils: add ``URL`` field type mapping

Version 1.9.2 (2023-10-19)

- accessibility: add tooltips to icons

Version 1.9.1 (2023-09-25)

- assets: improve error handling on details page
- styling: minor improvements

Version 1.9.0 (2023-09-18)

- views: adapt actions creation

Version 1.8.0 (2023-09-14)

- setup: bump to invenio-vocabularies v2.0.0

Version 1.7.0 (2023-09-08)

- chore: expose admin api
- assets: overridable search result item layout
- utils: process date field in schema

Version 1.6.1 (2023-07-07)

- skip `fields.Method` from jsonify

Version 1.6.0 (2023-07-03)

- Adding a mapping for the fields.Method

Version 1.5.0 (2023-06-15)

- setup: upgrade invenio dependencies

Version 1.4.1 (2023-05-25)

- fix action form creation

Version 1.4.0 (2023-04-25)

- upgrade invenio-records-resources

Version 1.3.0 (2023-04-20)

- upgrade invenio-records-resources

Version 1.2.0 (2023-03-24)

- bump invenio-records-resources to v2.0.0

Version 1.1.1 (released 2023-03-09)

- assets: add html formatting to display components

Version 1.1.0 (released 2023-03-02)

- remove deprecated flask-babelex dependency and imports
- upgrade invenio-theme, invenio-vocabularies
- fix form field sorting order

Version 1.0.6 (released 2023-02-15)

- forms: add support for checkbox, dropdown and textarea fields
- forms: add support for default value (prefill)
- forms: add support for specific table column width (search view)

Version 1.0.5 (released 2023-01-26)

- assets: fix button help popup

Version 1.0.4 (released 2023-01-24)

- menu: add disable view hook method

Version 1.0.3 (released 2023-01-20)

- forms: add tooltip to field when passed from fieldSchema
- modal: fix styling

Version 1.0.2 (released 2022-11-25)

- use centralized axios configuration
- add i18n translations
- refactor actions buttons

Version 1.0.1 (released 2022-11-04)

- upgrade invenio-records-resources
- upgrade invenio-vocabublaries

Version 1.0.0

- Initial public release.
