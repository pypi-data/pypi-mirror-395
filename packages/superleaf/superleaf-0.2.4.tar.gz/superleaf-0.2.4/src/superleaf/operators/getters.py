from superleaf.operators.base import Operator, operator

_NotSpecified = object()


def attr_getter(name: str, default=_NotSpecified) -> Operator:
    def get(obj):
        if default is _NotSpecified:
            return getattr(obj, name)
        else:
            return getattr(obj, name, default)
    return operator(get)


def index_getter(index, default=_NotSpecified) -> Operator:
    def get(obj):
        try:
            return obj[index]
        except KeyError:
            if default is _NotSpecified:
                raise
            return default
    return operator(get)
