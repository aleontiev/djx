from django.utils import six
from django.template import Template, Context


def resolve_path(path, context):
    """Resolve a value given a path and a deeply-nested object

    Arguments:
        path: a dot-separated string
        context: any object, list, dictionary,
            or single-argument callable

    Returns:
        value at the end of the path, or None

    Examples:

        T = namedtuple('T', ['x'])
        context = {"a": [T('y')]}
        resolve_path("a.0.x", context) == 'y'
    """
    parts = path.split('.')
    for part in parts:
        if context is None:
            break
        if callable(context):
            # try to "call" into the context
            try:
                try:
                    # 1. assume it is a method that takes no arguments
                    # and returns a nested object
                    context = context()
                except TypeError:
                    # 2. assume its a method that takes the next part
                    # as the argument
                    context = context(part)
                    continue
            except Exception:
                # fallback: assume this is a special object
                # that we should not call into
                # e.g. a django ManyRelatedManager
                pass

        if isinstance(context, dict):
            context = context.get(part, None)
        elif isinstance(context, list):
            # throws ValueError if part is NaN
            part = int(part)
            try:
                context = context[part]
            except IndexError:
                context = None
                break
        else:
            context = getattr(context, part, None)
    if context and callable(context):
        # if the result is a callable,
        # try to resolve it
        context = context()
    return context


def resolve_template(template, context):
    template = Template(template)
    context = Context(context)
    return template.render(context)


def humanize(value, sep=u', '):
    if value is None:
        value = u'null'
    elif type(value) == bool:
        value = unicode(value).lower()
    elif isinstance(value, six.string_types):
        pass
    elif isinstance(value, list):
        value = sep.join([humanize(v, sep=sep) for v in value])
    elif isinstance(value, dict):
        value = sep.join(
            ['%s=%s' % (str(k), humanize(v, sep=sep))
                for k, v in six.iteritems(value)]
        )
    else:
        value = unicode(value)
    return value
