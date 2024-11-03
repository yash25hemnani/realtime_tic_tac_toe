import json
from channels.consumer import SyncConsumer, async_to_sync
from channels.exceptions import StopConsumer

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print('Websocket Connected...', event)
        self.send({
            'type':'websocket.accept'
        })

        # Adding the player inside the group
        self.room_code = self.scope['url_route']['kwargs']['roomCode']
        user_name = self.scope['url_route']

        async_to_sync(self.channel_layer.group_add)(self.room_code, self.channel_name)

    def websocket_receive(self, event):
        print('Websocket Received...', event)
        string = event['text']
        try:
            data = json.loads(string)
            print('Data with type - ', data, type(data))

            if 'User' in data.keys():
                async_to_sync(self.channel_layer.group_send)(self.room_code, {
                    'type':'user.message',
                    'message': json.dumps(data)
                })

            if 'cubeId' in data.keys():
                async_to_sync(self.channel_layer.group_send)(self.room_code, {
                    'type':'game.message',
                    'message': json.dumps(data)
                })

            if 'Winner' in data.keys():
                async_to_sync(self.channel_layer.group_send)(self.room_code, {
                    'type':'winner.message',
                    'message': json.dumps(data)
                })

        except Exception as e:
            print(e)
        

    def user_message(self, event):
        print('User Message: ', event)
        print(type(event))
        self.send({
            'type':'websocket.send',
            'text': event['message']
        })

    def game_message(self, event):
        print('Game Message: ', event)
        self.send({
            'type':'websocket.send',
            'text': event['message']
        })
    
    def winner_message(self, event):
        print('Winner Message: ', event)
        self.send({
            'type':'websocket.send',
            'text': event['message']
        })

    def websocket_disconnect(self, event):
        print('Websocket Disconnected...')