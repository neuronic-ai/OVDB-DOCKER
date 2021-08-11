from rest_framework.decorators import api_view
from rest_framework import status
from django.http import JsonResponse
import json

from module import admin_config, bridge, error


@api_view(['POST'])
def send_command(request):
    if isinstance(request.body, bytes):
        message = request.body.decode()
    elif isinstance(request.body, str):
        message = request.body
    else:
        message = str(request.body)

    message = json.loads(message)

    if message['type'] == 'init':
        res = init_bridge(request)
    elif message['type'] == 'open':
        res = open_bridge(request, message['bridge_info'])
    elif message['type'] == 'close':
        res = close_bridge(request, message['bridge_info'])
    elif message['type'] == 'send_message':
        res = send_message_bridge(request, message['bridge_info'], message['data'])
    else:
        res = error.UNKNOWN_COMMAND_TYPE

    return JsonResponse({
        'status_code': status.HTTP_200_OK,
        'text': res
    })


def init_bridge(request):
    for b_obj in admin_config.BRIDGES_OBJ:
        b_obj['obj'].close()
        admin_config.BRIDGES_OBJ.remove(b_obj)

    return error.SUCCESS


def open_bridge(request, bridge_info):
    new_bridge = True

    for b_obj in admin_config.BRIDGES_OBJ:
        if b_obj['id'] == bridge_info['id']:
            b_obj['obj'].open()
            new_bridge = False
            break

    if new_bridge:
        obj = bridge.Bridge(bridge_info)
        obj.open()
        admin_config.BRIDGES_OBJ.append({
            'id': bridge_info['id'],
            'obj': obj
        })

    return error.SUCCESS


def close_bridge(request, bridge_info):
    for b_obj in admin_config.BRIDGES_OBJ:
        if b_obj['id'] == bridge_info['id']:
            b_obj['obj'].close()
            return error.SUCCESS

    return error.UNKNOWN_BRIDGE_ID


def send_message_bridge(request, bridge_info, data):
    for b_obj in admin_config.BRIDGES_OBJ:
        if b_obj['id'] == bridge_info['id']:
            return b_obj['obj'].send_message(data['message'])

    return error.UNKNOWN_BRIDGE_ID
