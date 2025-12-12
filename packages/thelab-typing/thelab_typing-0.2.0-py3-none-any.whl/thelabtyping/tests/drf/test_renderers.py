from unittest.mock import MagicMock, patch
import re

from django.test import TestCase
import pydantic

from thelabtyping.abc import ListOf
from thelabtyping.drf.renderers import BrowsableAPIRenderer, JSONRenderer


def strip_trailing_whitespace(content: str) -> str:
    return re.sub(" +\n", "\n", content)


class Person(pydantic.BaseModel):
    name: str


class PersonList(ListOf[Person]):
    pass


class JSONRendererTest(TestCase):
    def test_render_normal(self) -> None:
        obj = {"foo": ["bar", "baz"]}
        renderer = JSONRenderer()
        content = renderer.render(obj, "application/json")
        self.assertEqual(content.decode(), '{"foo":["bar","baz"]}')

    def test_render_indented(self) -> None:
        obj = {"foo": ["bar", "baz"]}
        renderer = JSONRenderer()
        content = renderer.render(obj, "application/json; indent=2")
        self.assertEqual(
            strip_trailing_whitespace(content.decode()),
            '{\n  "foo": [\n    "bar",\n    "baz"\n  ]\n}',
        )

    def test_render_null(self) -> None:
        renderer = JSONRenderer()
        content = renderer.render(None, "application/json")
        self.assertEqual(content, b"")

    def test_render_base_model(self) -> None:
        obj = Person(name="Diane")
        renderer = JSONRenderer()
        content = renderer.render(obj)
        self.assertEqual(content.decode(), '{"name":"Diane"}')

    def test_render_base_model_indented(self) -> None:
        obj = Person(name="Diane")
        renderer = JSONRenderer()
        content = renderer.render(obj, "application/json; indent=2")
        self.assertEqual(
            strip_trailing_whitespace(content.decode()),
            '{\n  "name": "Diane"\n}',
        )

    def test_render_root_model(self) -> None:
        obj = PersonList(
            [
                Person(name="Diane"),
            ]
        )
        renderer = JSONRenderer()
        content = renderer.render(obj)
        self.assertEqual(content.decode(), '[{"name":"Diane"}]')


class BrowsableAPIRendererTest(TestCase):
    @patch("rest_framework.renderers.BrowsableAPIRenderer.render")
    def test_render_normal(self, _render: MagicMock) -> None:
        _render.return_value = "rc"

        obj = {"foo": ["bar", "baz"]}
        renderer = BrowsableAPIRenderer()
        resp = renderer.render(obj)

        self.assertEqual(resp, "rc")

        _render.assert_called_once_with({"foo": ["bar", "baz"]})

    @patch("rest_framework.renderers.BrowsableAPIRenderer.render")
    def test_render_model(self, _render: MagicMock) -> None:
        _render.return_value = "rc"

        obj = Person(name="Diane")
        renderer = BrowsableAPIRenderer()
        resp = renderer.render(obj)

        self.assertEqual(resp, "rc")

        _render.assert_called_once_with({"name": "Diane"})
