import json

from channels.generic.websocket import AsyncWebsocketConsumer


class DebugChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))


class ComponentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'update_component'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        component_id = text_data_json["component_id"]
        content = text_data_json["content"]

        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat.message",
                "component_id": component_id,
                "content": content
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        component_id = event["component_id"]
        content = event["content"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps({
                "component_id": component_id,
                "content": content
            }))
