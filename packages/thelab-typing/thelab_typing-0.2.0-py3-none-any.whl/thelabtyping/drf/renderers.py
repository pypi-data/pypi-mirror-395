from collections.abc import Mapping
from typing import Any
import json

from pydantic import BaseModel
from rest_framework import renderers
from rest_framework.compat import INDENT_SEPARATORS, LONG_SEPARATORS, SHORT_SEPARATORS


class JSONRenderer(renderers.JSONRenderer):
    """
    Same as the normal JSONRenderer, but knows how to work with Pydantic models.
    """

    def render(
        self,
        data: BaseModel | Any,
        accepted_media_type: str | None = None,
        renderer_context: Mapping[str, Any] | None = None,
    ) -> bytes:
        """
        Render `data` into JSON, returning a bytestring.
        """
        if data is None:
            return b""

        renderer_context = renderer_context or {}
        indent = self.get_indent(accepted_media_type or "", renderer_context or {})
        if indent is None:
            separators = SHORT_SEPARATORS if self.compact else LONG_SEPARATORS
        else:
            separators = INDENT_SEPARATORS

        if isinstance(data, BaseModel):
            ret = data.model_dump_json(
                indent=indent,
            )
        else:
            ret = json.dumps(
                data,
                cls=self.encoder_class,
                indent=indent,
                ensure_ascii=self.ensure_ascii,
                allow_nan=not self.strict,
                separators=separators,
            )

        # We always fully escape \u2028 and \u2029 to ensure we output JSON
        # that is a strict javascript subset.
        # See: https://gist.github.com/damncabbage/623b879af56f850a6ddc
        ret = ret.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
        return ret.encode()


class BrowsableAPIRenderer(renderers.BrowsableAPIRenderer):
    """
    Same as the normal BrowsableAPIRenderer, but knows how to work with Pydantic models.
    """

    def render(
        self,
        data: BaseModel | Any,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Render data for the browsable API, converting Pydantic models to dicts."""
        if isinstance(data, BaseModel):
            data = data.model_dump()
        return super().render(data, *args, **kwargs)
