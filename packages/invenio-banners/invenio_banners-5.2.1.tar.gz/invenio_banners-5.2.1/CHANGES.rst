..
    Copyright (C) 2020-2024 CERN.
    Copyright (C) 2024-2025 Graz University of Technology.
    Copyright (C) 2025      KTH Royal Institute of Technology.

    Invenio-Banners is free software; you can redistribute it and/or modify
    it under the terms of the MIT License; see LICENSE file for more details.

Changes
=======

Version v5.2.1 (released 2025-12-08)

- i18n: pulled translations Turkish language
- fix: partially initialized module
- compatibility(312): distutils removed
- i18n: pulled translations finnish language
- chore: remove unused variable `request_extra_args`

Version v5.2.0 (released 2025-08-06)

- search: add query params active and url_path for search, add None as default value for filters
- global: replace deprecated datetime utcnow() with now(timezone.utc)

Version v5.1.1 (released 2025-07-22)

- fix: mo files not included into build

Version v5.1.0 (released 2025-07-17)

- i18n: pulled translations
- i18n: force pull langs

Version v5.0.0 (released 2025-06-03)

- setup: bump major dependencies
- fix(tests): add configuration
- i18n: add translation entry point (#48)
- fix: setuptools moved from dash to underscore
- i18n: removed deprecated messages

Version v4.1.1 (released 2025-03-26)

- i18n: mark missing strings for translation and push translations

Version v4.1.0 (released 2025-01-22)

- templates: pass ui classes through macro parameters

Version v4.0.0 (released 2024-12-10)

- setup: change to reusable workflows
- setup: bump major dependencies

Version v3.2.0 (released 2024-11-05)

- feat(administration): use html editor for message
- global: change the code to be compatible with sqlalchemy >= 2.0
- global: add compatibility layer to move to flask >= 3.0

Version v3.1.0 (released 2024-08-07)

- http headers: use and adjust vnd.inveniordm.v1+json http accept header

Version 3.0.2 (released 2024-07-17)

- errors: implement REST validation error for banner loader

Version 3.0.1 (released 2024-02-21)

- Moved admin menu item for banners to site administration category

Version 3.0.0 (released 2024-01-31)

- installation: bump invenio-administration

Version 2.1.1 (released 2023-07-24)

- ui: remove bottom margin

Version 2.1.0 (released 2023-03-02)

- remove deprecated flask-babelex imports
- install invenio-i18n explicitly

Version 2.0.0 (released 2023-02-15)

- global: refactor into resource/service pattern
- global: implement CRUD operations
- global: implement best practices for packaging (declarative cfg), code
  linting (black) and testing
- search: improve banners search by query params
- administration: integrate banners view module


Version 1.0.0a1 (release 2020-10-25)
------------------------------------

- Initial public release.
