from __future__ import absolute_import

import pytest


def register(injector):
    """Register Py.test fixture performing injection in it's scope."""

    if "fixture" not in injector:
        injector.fixture

    options = {"name": injector.name}

    for option in ["scope", "params", "autouse", "ids"]:
        if option in injector:
            options[option] = getattr(injector, option)

    @pytest.fixture(**options)
    def __fixture(request):

        return injector.let(request=request).fixture

    __fixture.injector = injector
    return __fixture


def require(fixturename):
    """Mark fixture as a dependency for injection process."""

    return type(Requirement.__name__, (Requirement,), {"fixturename": fixturename})


class Requirement(object):

    fixturename = None

    def __new__(cls, request):

        return request.getfixturevalue(cls.fixturename)

    def __init__(self, request):

        pass
