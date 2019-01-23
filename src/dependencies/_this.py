from . import _markers
from .exceptions import DependencyError


class This(object):
    """Declare attribute and item access during dependency injection."""

    def __init__(self, expression):

        self.__expression__ = expression

    def __getattr__(self, attrname):

        return This(self.__expression__ + ((".", attrname),))

    def __getitem__(self, item):

        # TODO: Do we protect against `this['foo']` expression?
        return This(self.__expression__ + (("[]", item),))

    def __lshift__(self, num):

        # TODO: Do we protect against `(this.foo << 2)` expression?
        if not isinstance(num, int) or num <= 0:
            raise ValueError("Positive integer argument is required")
        else:
            return This(((".", "__parent__"),) * num)


this = This(tuple())


def make_this_spec(dependency):

    check_expression(dependency)
    return _markers.this, ThisSpec(dependency), ["__self__"], 0


class ThisSpec(object):
    def __init__(self, dependency):

        self.dependency = dependency

    def __call__(self, **kwargs):

        result = kwargs["__self__"]

        for kind, symbol in self.dependency.__expression__:
            if kind == ".":
                try:
                    result = getattr(result, symbol)
                except DependencyError:
                    message = (
                        "You tries to shift this more times that Injector has levels"
                    )
                    if symbol == "__parent__":
                        raise DependencyError(message)
                    else:
                        raise
            elif kind == "[]":
                result = result[symbol]

        return result

    @property
    def __expression__(self):

        return self.dependency.__expression__


def check_expression(dependency):

    if not any(
        symbol
        for kind, symbol in dependency.__expression__
        if kind == "." and symbol != "__parent__"
    ):
        raise DependencyError("You can not use 'this' directly in the 'Injector'")
