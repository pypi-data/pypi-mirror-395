# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Schemas for parameter parsing."""

from typing import Any, ClassVar

from flask_resources.parsers import MultiDictSchema
from marshmallow import fields
from marshmallow.decorators import post_load
from werkzeug.datastructures import ImmutableMultiDict

class SearchRequestArgsSchema(MultiDictSchema):
    """Request URL query string arguments."""

    q: ClassVar[fields.String]
    suggest: ClassVar[fields.String]
    sort: ClassVar[fields.String]
    page: ClassVar[fields.Int]
    size: ClassVar[fields.Int]

    @post_load(pass_original=True)
    def facets(
        self,
        data: dict[str, Any],
        original_data: ImmutableMultiDict[str, str] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]: ...
