from starlette.responses import Response as StarletteResponse
from toonio.core.basic_response import BascicResponse
from typing import Any, Dict, Optional


class Response(StarletteResponse, BascicResponse):
    """
    A custom HTTP response class that outputs TOON-encoded content.

    This class combines the TOON serialization logic provided by
    `BascicResponse` with Starlette's native `Response` implementation to
    generate a complete ASGI-compatible HTTP response.

    The input dictionary is encoded into TOON format and wrapped inside a
    fully-formed HTTP response, including the correct status code and
    `Content-Type` header. The response body sent to the client is the
    raw, TOON-encoded byte sequence.

    In short, this class behaves like a standard StarletteResponse,
    but automatically converts Python dictionaries into TOON.

    Attributes:
        data (dict):
            The Python dictionary to be serialized into TOON format.
        status_code (int):
            HTTP status code returned to the client.
        content_type (str):
            MIME type of the response body. Defaults to "text/toon".

    Methods:
        encode_body() -> bytes:
            Inherited from BascicResponse. Converts the input dictionary
            into a TOON-encoded UTF-8 byte string.

    Usage:
        response = Response({"message": "hello"}, status_code=200)

    Notes:
        - The content provided to the underlying StarletteResponse is
          already TOON-encoded.
        - Browsers may trigger a file download when receiving unknown or
          custom MIME types. This is expected behavior when returning
          nonstandard formats.
    """

    def __init__(
        self,
        data: Dict[str, Any],
        status_code: int = 200,
        content_type: Optional[str] = "text/toon",
    ):

        BascicResponse.__init__(self, data, status_code, content_type)

        body = self.encode_body()

        StarletteResponse.__init__(
            self,
            content=body,
            status_code=status_code,
            media_type=content_type,
        )
