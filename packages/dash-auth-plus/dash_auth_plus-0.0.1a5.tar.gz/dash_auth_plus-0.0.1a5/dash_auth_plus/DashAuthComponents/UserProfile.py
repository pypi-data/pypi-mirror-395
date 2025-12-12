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


class UserProfile(Component):
    """An UserProfile component.


    Keyword arguments:

    - children (a list of or a singular dash component, string or number; optional)"""

    _children_props: typing.List[str] = []
    _base_nodes = ["children"]
    _namespace = "dash_auth_plus_components"
    _type = "UserProfile"

    def __init__(self, children: typing.Optional[ComponentType] = None, **kwargs):
        self._prop_names = ["children"]
        self._valid_wildcard_attributes = []
        self.available_properties = ["children"]
        self.available_wildcard_properties = []
        _explicit_args = kwargs.pop("_explicit_args")
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != "children"}

        super(UserProfile, self).__init__(children=children, **args)


setattr(UserProfile, "__init__", _explicitize_args(UserProfile.__init__))
