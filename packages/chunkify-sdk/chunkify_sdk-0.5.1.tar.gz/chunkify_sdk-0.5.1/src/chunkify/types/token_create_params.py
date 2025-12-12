# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["TokenCreateParams"]


class TokenCreateParams(TypedDict, total=False):
    scope: Required[Literal["project", "team"]]
    """
    Scope specifies the scope of the token, which must be either "team" or
    "project".
    """

    name: str
    """Name is the name of the token, which can be up to 64 characters long."""

    project_id: str
    """ProjectId is required if the scope is set to "project"."""
