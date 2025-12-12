from toon.encoder import encode
from typing import Any, Dict, Optional


class BascicResponse:
    """
    A lightweight custom response serializer that encodes
    Python dictionaries into the TOON format.

    This class does not directly integrate with ASGI frameworks but provides
    a simple interface for preparing encoded response bodies. It is designed
    to be used together with a proper ASGI Response class (e.g. StarletteResponse)
    to return TOON-encoded data from endpoints.

    Attributes:
        data (dict):
            The Python dictionary to be serialized into TOON format.
        status_code (int):
            HTTP status code for the response (default: 200).
        content_type (str):
            The MIME type for the response (default: "text/toon").

    Methods:
        encode_body() -> bytes:
            Serializes the dictionary into TOON format and returns the encoded
            byte string to be used as an HTTP response body.

        __str__() -> str:
            Returns the TOON-encoded representation as a regular string,
            primarily for debugging or logging purposes.
    """

    def __init__(
        self,
        data: Dict[str, Any],
        status_code: int = 200,
        content_type: Optional[str] = "text/toon",
    ):
        self.data = data
        self.status_code = status_code
        self.content_type = content_type

    def encode_body(self) -> bytes:
        return encode(self.data).encode("utf-8")

    def __str__(self):
        return encode(self.data)
