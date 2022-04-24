import pytest

from channels.generic.websocket import (
    AsyncJsonWebsocketConsumer,
    JsonWebsocketConsumer, )

from channels.generic.websocket import (
    WebsocketConsumer, AsyncWebsocketConsumer,
)
from channels.testing import WebsocketCommunicator

data = {}


class WebSocketConsumer(WebsocketConsumer):
    def connect(self):
        data["connected"] = True
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        data["received"] = (text_data, bytes_data)
        self.send(text_data=text_data, bytes_data=bytes_data)

    def disconnect(self, code):
        data["disconnected"] = code


# Create your tests here.
@pytest.mark.django_db()
@pytest.mark.asyncio
async def test_websocket_consumer():
    """
    Tests that WebsocketConsumer is implemented correctly.
    """
    app = WebSocketConsumer()

    # Test a normal connection
    communicator = WebsocketCommunicator(app, "/testws/")
    connected, _ = await communicator.connect()
    assert connected
    assert "connected" in data
    # Test sending text
    await communicator.send_to(text_data="hello")
    response = await communicator.receive_from()
    assert response == "hello"
    assert data["received"] == ("hello", None)
    # Test sending bytes
    await communicator.send_to(bytes_data=b"w\0\0\0")
    response = await communicator.receive_from()
    assert response == b"w\0\0\0"
    assert data["received"] == (None, b"w\0\0\0")
    # Close out
    await communicator.disconnect()
    assert "disconnected" in data


@pytest.mark.asyncio
async def test_async_websocket_consumer():
    """
    Tests that AsyncWebsocketConsumer is implemented correctly.
    """
    results = {}

    class TestAsyncWebsocketConsumer(AsyncWebsocketConsumer):
        async def connect(self):
            results["connected"] = True
            await self.accept()

        async def receive(self, text_data=None, bytes_data=None):
            results["received"] = (text_data, bytes_data)
            await self.send(text_data=text_data, bytes_data=bytes_data)

        async def disconnect(self, code):
            results["disconnected"] = code

    app = TestAsyncWebsocketConsumer()

    # Test a normal connection
    communicator = WebsocketCommunicator(app, "/testws/")
    connected, _ = await communicator.connect()
    assert connected
    assert "connected" in results
    # Test sending text
    await communicator.send_to(text_data="hello")
    response = await communicator.receive_from()
    assert response == "hello"
    assert results["received"] == ("hello", None)
    # Test sending bytes
    await communicator.send_to(bytes_data=b"w\0\0\0")
    response = await communicator.receive_from()
    assert response == b"w\0\0\0"
    assert results["received"] == (None, b"w\0\0\0")
    # Close out
    await communicator.disconnect()
    assert "disconnected" in results


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_json_websocket_consumer():
    """
    Tests that JsonWebsocketConsumer is implemented correctly.
    """
    results = {}

    class TestJsonWebsocketConsumer(JsonWebsocketConsumer):
        def connect(self):
            self.accept()

        def receive_json(self, data=None):
            results["received"] = data
            self.send_json(data)

    app = TestJsonWebsocketConsumer()

    # Open a connection
    communicator = WebsocketCommunicator(app, "/testws/")
    connected, _ = await communicator.connect()
    assert connected
    # Test sending
    await communicator.send_json_to({"hello": "world"})
    response = await communicator.receive_json_from()
    assert response == {"hello": "world"}
    assert results["received"] == {"hello": "world"}
    # Test sending bytes breaks it
    await communicator.send_to(bytes_data=b"w\0\0\0")
    with pytest.raises(ValueError):
        await communicator.wait()


@pytest.mark.asyncio
async def test_async_json_websocket_consumer():
    """
    Tests that AsyncJsonWebsocketConsumer is implemented correctly.
    """
    results = {}

    class TestAsyncJsonWebsocketConsumer(AsyncJsonWebsocketConsumer):
        async def connect(self):
            await self.accept()

        async def receive_json(self, data=None):
            results["received"] = data
            await self.send_json(data)

    app = TestAsyncJsonWebsocketConsumer()

    # Open a connection
    communicator = WebsocketCommunicator(app, "/testws/")
    connected, _ = await communicator.connect()
    assert connected
    # Test sending
    await communicator.send_json_to({"hello": "world"})
    response = await communicator.receive_json_from()
    assert response == {"hello": "world"}
    assert results["received"] == {"hello": "world"}
    # Test sending bytes breaks it
    await communicator.send_to(bytes_data=b"w\0\0\0")
    with pytest.raises(ValueError):
        await communicator.wait()
