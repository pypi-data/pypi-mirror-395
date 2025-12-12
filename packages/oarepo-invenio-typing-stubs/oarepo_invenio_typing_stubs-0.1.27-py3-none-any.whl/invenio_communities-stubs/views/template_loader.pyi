from typing import List

from flask import Flask
from flask.templating import DispatchingJinjaLoader
from invenio_app.helpers import ThemeJinjaLoader
from jinja2 import ChoiceLoader
from werkzeug.utils import cached_property

class CommunityThemeJinjaLoader(ThemeJinjaLoader):
    brand: str
    def __init__(
        self, app: Flask, loader: DispatchingJinjaLoader, brand: str
    ) -> None: ...
    @cached_property
    def prefixes(self) -> List[str]: ...

class CommunityThemeChoiceJinjaLoader(ChoiceLoader):
    app: Flask
    def __init__(self, brand: str) -> None: ...
