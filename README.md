# djx
Common utilities and dependencies for the modern Django project.

## environment

Helpers for pulling in environment variables.

### get_string(key, default=None)

Return an environment variable as a string, defaulting to the given
value if the environment variable is undefined.

### get_boolean(key, default)

Return an environment variable as a boolean, defaulting to the given
value if the environment variable is undefined.

### get_int(key)

Return an environment variable as an integer, defaulting to the given
value if the environment variable is undefined.

## static

Helpers for working with static files. Uses `dj-static`.

### Cling

Wrap a WSGI application to support static file serving:

```
    from djx.static import Cling
    application = Cling(get_wsgi_application())
```

## urls

Helpers for dynamically loading urls.

### load_urls(file, namespace=True)

Find submodules of the given file with valid url patterns and concatenate them into a list of patterns.
Only submodules with a `urls` module that contains a `urlpatterns` symbol will be considered.
If the `urls` module exists but cannot be imported, an exception is raised.

If `namespace` is set to `True` (the default), the urls will be exposed under the prefix of the submodule name.
If `namespace` is set to a function, this function will be called with the submodule name,
and the output will be used as the prefix.
If `namespace` is set to a string, this string will be used as the prefix.
If `namespace` is set to `False`, the urls will not be namespaced.

For example, if your project includes an "api" submodule with a `urls.py` file that defines url patterns
for your API and a separate "admin" submodule with a `urls.py` file that defines url patterns for admins,
you can automatically import these patterns with the following one-liner in the project `urls.py` file:

```
    from djx.urls import load_urls
    urlpatterns = load_urls(__file__)
```

Assuming admin/urls.py includes the urls "users" and "groups" and api/urls.py includes the urls "users" and "events",
the above call would produce the following urlpatterns:

```
    /admin/groups/
    /admin/users/
    /api/events/
    /api/users/
```

If you were to pass `namespace=lambda x: '/foo/' + x`, you would get the following patterns:

```
    /foo/admin/events/
    /foo/admin/groups/
    /foo/api/events/
    /foo/api/users/
```

However, if you were to pass `namespace='foo'`, you would get the following patterns:

```
    /foo/events/
    /foo/groups/
    /foo/users/
```

Note that "/foo/users/" becomes ambiguous in this scenario; for this reason,
passing in string or False values to `namespace` should be done with caution.

### get_host(url)

Returns the network host for a given URL.
