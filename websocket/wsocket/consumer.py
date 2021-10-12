import requests
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from module import admin_config, common
from db.models import (
    TBLBridge
)


class BridgeConsumer(WebsocketConsumer):
    def connect(self):
        try:
            bridge = TBLBridge.objects.get(dst_address__contains=self.scope['path'], is_active=True)

            self.bridge_id = bridge.id
            # self.group_name = f'{admin_config.BRIDGE_CONSUMER_PREFIX}_{bridge.id}_{common.generate_random_string(6)}'
            self.group_name = f'{admin_config.BRIDGE_CONSUMER_PREFIX}_{bridge.id}'
            async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
            self.accept()

            # res = requests.post(f'http://{admin_config.OV_APP_HOST_URL}/event/notify_event', json={
            #     'type': 'on_add_ws_client',
            #     'bridge_id': bridge.id,
            #     'data': {
            #         'group_name': self.group_name
            #     }
            # })
        except:
            self.close()

    def disconnect(self, code):
        self.close()
        # try:
        #     res = requests.post(f'http://{admin_config.OV_APP_HOST_URL}/event/notify_event', json={
        #         'type': 'on_remove_ws_client',
        #         'bridge_id': self.bridge_id,
        #         'data': {
        #             'group_name': self.group_name
        #         }
        #     })
        # except:
        #     pass

    def notify(self, event):
        # new_event = event.copy
        # del new_event['notify']
        # print(event)
        # print(new_event)
        self.send(text_data=json.dumps(event))

    def receive(self, text_data=None, bytes_data=None):
        pass
