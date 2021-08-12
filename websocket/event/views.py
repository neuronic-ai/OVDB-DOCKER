from rest_framework.decorators import api_view
from rest_framework import status
from django.http import JsonResponse
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from module import error


@api_view(['POST'])
def notify_event(request):
    if isinstance(request.body, bytes):
        message = request.body.decode()
    elif isinstance(request.body, str):
        message = request.body
    else:
        message = str(request.body)

    message = json.loads(message)

    if message['type'] == 'on_message':
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            message['data']['group_name'],
            message['data']['content']
        )

    return JsonResponse({
        'status_code': status.HTTP_200_OK,
        'text': error.SUCCESS
    }, status=status.HTTP_200_OK)
