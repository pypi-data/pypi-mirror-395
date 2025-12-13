from typing_extensions import assert_type

from sink.api.sdk import Sink, Stream
from sink.api.sdk.types import StreamingBasicResponse


def ensure_accurate_overloads(client: Sink, unknown_bool: bool) -> None:
    # no discriminator
    assert_type(
        client.streaming.basic(model="foo", prompt="bar"),
        StreamingBasicResponse,
    )
    # discriminator=True
    assert_type(
        client.streaming.basic(model="foo", prompt="bar", stream=True),
        Stream[StreamingBasicResponse],
    )
    # discriminator=False
    assert_type(
        client.streaming.basic(model="foo", prompt="bar", stream=False),
        StreamingBasicResponse,
    )
    # unknown discriminator
    assert_type(
        client.streaming.basic(model="foo", prompt="bar", stream=unknown_bool),
        "StreamingBasicResponse | Stream[StreamingBasicResponse]",
    )
