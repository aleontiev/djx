import os
import importlib
import pkgutil
import sys
from django.conf.urls import url, include
from django.utils import six
try:
    # py2
    from urlparse import urlparse
except:
    # py3
    from urllib.parse import urlparse


def load_urls(relative, namespace=True):
    relative = os.path.dirname(relative)
    base = None
    for p in sys.path:
        if relative.startswith(p):
            base = p

    if base is None:
        raise Exception('%s is not in sys.path (%s)' % (relative, sys.path))

    prefix = relative.replace(base, '').replace('/', '.')
    if prefix.startswith('.'):
        prefix = prefix[1:]
    if prefix:
        prefix = prefix + '.'

    urlpatterns = []
    for _, name, package in pkgutil.iter_modules([relative]):
        if package:
            module_name = '%s%s.urls' % (prefix, name)
            try:
                urls = importlib.import_module(module_name)
            except ImportError as e:
                if str(e).startswith('No module named urls'):
                    continue
                else:
                    raise

            patterns = getattr(urls, 'urlpatterns', None)
            if patterns:
                if namespace:
                    if isinstance(namespace, six.string_types):
                        # use the given string as the prefix
                        name = namespace
                    elif callable(namespace):
                        # call the given method with the module name
                        name = namespace(name)
                    else:
                        # only strings, functions, or True are valid
                        # truthy values for `namespace`
                        assert(namespace is True)
                    urlpatterns.append(
                        url('%s/' % name, include(patterns))
                    )
                else:
                    urlpatterns.extend(patterns)

    return urlpatterns


def get_host(url):
    url = urlparse(url)
    return url.netloc.split(':')[0]
