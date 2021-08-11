import os
import requests
import websocket
import _thread as thread
import time

from module import admin_config, error


class Bridge:
    """
    WebSocket to WebHook Data Bridge
    """

    def __init__(self, bridge_info):
        if admin_config.TRACE_MODE:
            websocket.enableTrace(True)

        self.bridge_info = bridge_info

        self.ws = None
        self.connection_status = None
        self.connection_text = 'Waiting for connect'

        self.OV_HOST = os.getenv('OV_HOST', admin_config.OV_HOST_URL)

    def notify_event(self, message_type, data=None):
        res = requests.post(f'{self.OV_HOST}/api/notify_event', json={
            'type': message_type,
            'bridge_id': self.bridge_info['id'],
            'data': data
        })

    def run_forever(self):
        self.ws.run_forever()

    def open(self):
        if self.ws is None:
            self.ws = websocket.WebSocketApp(self.bridge_info['src_address'],
                                             on_open=self.on_open,
                                             on_message=self.on_message,
                                             on_error=self.on_error,
                                             on_close=self.on_close)
        if not self.connection_status:
            thread.start_new_thread(self.run_forever, ())

    def close(self):
        self.connection_status = False
        self.ws.close()

    def is_connected(self):
        while self.connection_status is None:
            time.sleep(0.1)

        return self.connection_status

    def on_open(self, ws):
        self.connection_status = True
        # self.connection_text = 'WS:Open - Connected'
        # self.add_cache(self.connection_text)
        self.notify_event('on_open')

    def send_message(self, message):
        if self.connection_status:
            # self.add_cache(f'WS:Send - {message}')
            try:
                self.ws.send(message)
                return error.SUCCESS
            except Exception as e:
                return str(e)

    def on_message(self, ws, message):
        if self.connection_status:
            # self.add_cache(f'WS:Recv - {message}')
            # self.call_webhook(message)
            self.notify_event('on_message', {
                'message': message
            })

    def on_error(self, ws, error):
        self.connection_status = False
        # self.connection_text = f'WS:Error - {error}'
        # self.add_cache(self.connection_text)
        self.notify_event('on_error', {
            'error': error
        })

    def on_close(self, ws, close_status_code, close_msg):
        self.connection_status = False
        # self.connection_text = f'WS:Closed - {close_status_code} - {close_msg}'
        # self.add_cache(self.connection_text)
        self.notify_event('on_close', {
            'close_status_code': close_status_code,
            'close_msg': close_msg
        })
