# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal  # noqa: F401
from dash.development.base_component import Component, _explicitize_args

ComponentType = typing.Union[
    str,
    int,
    float,
    Component,
    None,
    typing.Sequence[typing.Union[str, int, float, Component, None]],
]

NumberType = typing.Union[
    typing.SupportsFloat, typing.SupportsInt, typing.SupportsComplex
]


class ClerkProvider(Component):
    """A ClerkProvider component.


    Keyword arguments:

    - children (a list of or a singular dash component, string or number; required)

    - id (string; optional)

    - PUBLISHABLE_KEY (string; required)

    - afterSignOutUrl (string; optional)

    - themeName (string; optional)"""

    _children_props: typing.List[str] = []
    _base_nodes = ["children"]
    _namespace = "dash_auth_plus_components"
    _type = "ClerkProvider"

    def __init__(
        self,
        children: typing.Optional[ComponentType] = None,
        PUBLISHABLE_KEY: typing.Optional[str] = None,
        afterSignOutUrl: typing.Optional[str] = None,
        themeName: typing.Optional[str] = None,
        id: typing.Optional[typing.Union[str, dict]] = None,
        **kwargs
    ):
        self._prop_names = [
            "children",
            "id",
            "PUBLISHABLE_KEY",
            "afterSignOutUrl",
            "themeName",
        ]
        self._valid_wildcard_attributes = []
        self.available_properties = [
            "children",
            "id",
            "PUBLISHABLE_KEY",
            "afterSignOutUrl",
            "themeName",
        ]
        self.available_wildcard_properties = []
        _explicit_args = kwargs.pop("_explicit_args")
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != "children"}

        for k in ["PUBLISHABLE_KEY"]:
            if k not in args:
                raise TypeError("Required argument `" + k + "` was not specified.")

        if "children" not in _explicit_args:
            raise TypeError("Required argument children was not specified.")

        super(ClerkProvider, self).__init__(children=children, **args)


setattr(ClerkProvider, "__init__", _explicitize_args(ClerkProvider.__init__))
