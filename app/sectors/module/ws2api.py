import os
import websocket
import _thread as thread
from django.core.cache import cache
import time
import json
from datetime import datetime
import requests

from . import log

from sectors.common import admin_config, error


class Bridge:
    """
    WebSocket to API Data Bridge
    """

    def __init__(self, bridge_info):
        if admin_config.TRACE_MODE:
            websocket.enableTrace(True)

        self.bridge_info = bridge_info

        self.ws = None
        self.connection_status = None
        self.connection_text = 'Waiting for connect'
        self.dumper_status = True
        self.log = log.BridgeLog(bridge_info)
        self.cache = self.log.get_last_log()

        self.REDIS_CACHE_ID = f"{admin_config.BRIDGE_REDIS_CACHE_PREFIX}_{self.bridge_info['id']}"
        self.REDIS_QUEUE = []
        self.REDIS_CACHE_TTL = self.bridge_info['frequency']

        self.WS_HOST = os.getenv('WS_HOST', admin_config.WS_HOST_URL)

    def send_command(self, message_type, data=None):
        res = requests.post(f'{self.WS_HOST}/wsocket/send_command', json={
            'type': message_type,
            'bridge_info': {
                'id': self.bridge_info['id'],
                'src_address': self.bridge_info['src_address']
            },
            'data': data
        })

        return res.json()

    def notify_event(self, event):
        data = event['data']
        if event['type'] == 'on_open':
            self.on_open(None)
        elif event['type'] == 'on_close':
            self.on_close(None, data['close_status_code'], data['close_msg'])
        elif event['type'] == 'on_message':
            self.on_message(None, data['message'])
        elif event['type'] == 'on_error':
            self.on_error(None, data['error'])

    def run_forever(self):
        self.ws.run_forever()

    def dumper(self):
        count = 0
        while True:
            if not self.dumper_status:
                break

            if count >= self.REDIS_CACHE_TTL:
                try:
                    cache.set(self.REDIS_CACHE_ID, self.REDIS_QUEUE, timeout=self.REDIS_CACHE_TTL + 1)
                    self.add_cache(f'REDIS QUEUE:Update - {self.REDIS_QUEUE}')
                    self.REDIS_QUEUE = []
                    count = 0
                except Exception as e:
                    self.add_cache(f'REDIS QUEUE:Update - Exception - {e}')

            time.sleep(1)
            count += 1

    def open(self):
        # if self.ws is None:
        #     self.ws = websocket.WebSocketApp(self.bridge_info['src_address'],
        #                                      on_open=self.on_open,
        #                                      on_message=self.on_message,
        #                                      on_error=self.on_error,
        #                                      on_close=self.on_close)
        # if not self.connection_status:
        #     thread.start_new_thread(self.run_forever, ())
        self.send_command('open')

        self.dumper_status = True
        thread.start_new_thread(self.dumper, ())

    def close_log(self):
        self.log.close()

    def close(self):
        self.connection_status = False
        self.dumper_status = False
        # self.ws.close()
        self.send_command('close')

    def is_connected(self):
        while self.connection_status is None:
            time.sleep(0.1)

        return self.connection_status

    def on_open(self, ws):
        self.connection_status = True
        self.connection_text = 'WS:Open - Connected'
        self.add_cache(self.connection_text)

    def send_message(self, message):
        if self.connection_status:
            self.add_cache(f'WS:Send - {message}')
            # try:
            #     self.ws.send(message)
            # except Exception as e:
            #     self.add_cache(f'WS:Send - Exception - {e}')
            res = self.send_command('send_message', {
                'message': message
            })
            if res['text'] != error.SUCCESS:
                self.add_cache(f"WS:Send - Exception - {res['text']}")

    def on_message(self, ws, message):
        if self.connection_status:
            self.add_cache(f'WS:Recv - {message}')
            self.set_redis_cache(message)

    def on_error(self, ws, error):
        self.connection_status = False
        self.dumper_status = False
        self.connection_text = f'WS:Error - {error}'
        self.add_cache(self.connection_text)

    def on_close(self, ws, close_status_code, close_msg):
        self.connection_status = False
        self.dumper_status = False
        self.connection_text = f'WS:Closed - {close_status_code} - {close_msg}'
        self.add_cache(self.connection_text)

    def set_redis_cache(self, message):
        try:
            self.REDIS_QUEUE.append({
                'date': datetime.now().strftime('%m/%d/%Y, %H:%M:%S'),
                'data': message
            })
            self.add_cache(f'REDIS QUEUE:Append - {message}')
        except Exception as e:
            self.add_cache(f'REDIS QUEUE:Append - Exception - {e}')

    def add_cache(self, data):
        self.trace(data)

        if len(self.cache) > admin_config.LOCAL_CACHE_LIMIT:
            self.cache.pop(0)

        cache_data = {
            'date': datetime.now().strftime('%m/%d/%Y, %H:%M:%S'),
            'data': data
        }

        self.cache.append(cache_data)

        self.log.write_log(json.dumps(cache_data))

    def get_cache(self):
        return self.cache

    def trace(self, trace_log):
        if admin_config.TRACE_MODE:
            print(f"{datetime.now()}: {self.bridge_info['name']}_{self.bridge_info['user_id']}: {trace_log}")
