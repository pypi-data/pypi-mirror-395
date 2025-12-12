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


class UserProfilePage(Component):
    """An UserProfilePage component.


    Keyword arguments:

    - children (a list of or a singular dash component, string or number; required)

    - label (string; required)

    - labelIcon (a list of or a singular dash component, string or number; required)

    - url (string; required)"""

    _children_props: typing.List[str] = ["labelIcon"]
    _base_nodes = ["labelIcon", "children"]
    _namespace = "dash_auth_plus_components"
    _type = "UserProfilePage"

    def __init__(
        self,
        children: typing.Optional[ComponentType] = None,
        label: typing.Optional[str] = None,
        url: typing.Optional[str] = None,
        labelIcon: typing.Optional[ComponentType] = None,
        **kwargs
    ):
        self._prop_names = ["children", "label", "labelIcon", "url"]
        self._valid_wildcard_attributes = []
        self.available_properties = ["children", "label", "labelIcon", "url"]
        self.available_wildcard_properties = []
        _explicit_args = kwargs.pop("_explicit_args")
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != "children"}

        for k in ["label", "labelIcon", "url"]:
            if k not in args:
                raise TypeError("Required argument `" + k + "` was not specified.")

        if "children" not in _explicit_args:
            raise TypeError("Required argument children was not specified.")

        super(UserProfilePage, self).__init__(children=children, **args)


setattr(UserProfilePage, "__init__", _explicitize_args(UserProfilePage.__init__))
