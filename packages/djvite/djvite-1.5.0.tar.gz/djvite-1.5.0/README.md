DjVite
======

<div align="center"><img src="./djvite.svg" alt="djvite logo" width="30%"/></div>

Integrates [Vite](https://vite.dev/) resources into a [Django](https://www.djangoproject.com/) web site.

Web requests are first served through **vite** dev server, then either proxified to **django** dev server or served directly.

This simulates a **nginx** proxy and **wsgi** server.

How to use
----------

### Django side

- Add `djvite` to your `INSTALLED_APPS` django config and define your static directories.

```python
# settings.py
INSTALLED_APPS = [
    ...
    'djvite',
]
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = ['dist']
```

- Load the `djvite` plugin into your templates.
- Inject any *script* or *link* from *vite* into your template:
  - `{% vite hotreload %}` enables vite hot module reload in dev mode
  - `{% vite '/src/main.js' %}` for module
  - `{% vite '/src/style.css' %}` for asset
  - Add any attributes to the `vite` tag and it will be added to the final tags.
  - Specifiy multiple sources within one `vite` tag, separate them with spaces.

```html
<!-- myapp/templates/index.html -->
<html>{% load djvite %}
  <heead>
    <title>My title</title>
    {% vite hotreload '/src/main.js' %}
  </head>
  ...
</html>
```

Notes:

You can use the `get_nginx_config` command to generate a working nginx static configuration.

### Vite side

- Add `DjVitePlugin` to your `vite.config.js` file:

```javascript
// vite.config.js
import { defineConfig } from 'vite'
import DjVitePlugin from 'djvite'
export default defineConfig({
  plugins: [
    DjVitePlugin({verbose: true}),
  ],
})
```

Configuration
-------------

In **django** settings:

- `DJVITE` dict, with the following keys:
  - `DEV_MODE` (boolean, default `True`)  
  When `False`, resources are resolved using the `vite-manifest.json` file that list bundle files. This file is generated using `vite build`.
  - `MODULE_EXTS` (extension list, default ot `['.js']`)  
  Use this to provide other extensions to be served as module, for instance `['.js', '.ts', '.jsx', '.tsx']` in Typescript React application.
  - `VITE_MANIFEST_PATH` (`Path | str`, default to `vite.manifest.json`)  
  Location to search for the Vite manifest. Used when `DEV_MODE` is `False`.

In **vite** config plugin:

- `options` object for `DjVitePlugin`.
  - `verbose` default to `false`.
  - `djangoPort` default to `DJANGO_PORT` environment variable or `8000` if not defined.
  - `djangoTemplatesGlob` default to the globbing pattern `**/templates`.
  - `manifestPath` default to `vite.manifest.json`.
