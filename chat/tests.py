import pytest
from channels.generic.websocket import WebsocketConsumer
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.urls import path

from .consumers import ChatConsumer


# Create your tests here.
@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_websocket_consumer():
    """
    Tests that WebsocketConsumer is implemented correctly.
    """
    json = {}

    class TestConsumer(WebsocketConsumer):
        def connect(self):
            json["connected"] = True
            self.accept()

        def receive(self, text_data=None, bytes_data=None):
            json["received"] = (text_data, bytes_data)
            self.send(text_data=text_data, bytes_data=bytes_data)

        def disconnect(self, code):
            json["disconnected"] = code

    app = TestConsumer()

    # Test a normal connection
    communicator = WebsocketCommunicator(app, "/testws/")
    connected, _ = await communicator.connect()
    assert connected
    assert "connected" in json
    # Test sending text
    await communicator.send_to(text_data="hello")
    response = await communicator.receive_from()
    assert response == "hello"
    assert json["received"] == ("hello", None)
    # Test sending bytes
    await communicator.send_to(bytes_data=b"w\0\0\0")
    response = await communicator.receive_from()
    assert response == b"w\0\0\0"
    assert json["received"] == (None, b"w\0\0\0")
    # Close out
    await communicator.disconnect()
    assert "disconnected" in json