from django.core.serializers.python import Serializer

from chat.utils import calculate_timestamp
from .constants import *


class LazyRoomChatMessageEncoder(Serializer):
    def get_dump_object(self, obj):
        dump_object = {}
        dump_object.update({'msg_type': MSG_TYPE_MESSAGE})
        dump_object.update({'msg_id': str(obj.id)})
        dump_object.update({'user_id': str(obj.user.id)})
        dump_object.update({'username': str(obj.user.username)})
        dump_object.update({'message': str(obj.content)})
        dump_object.update({'profile_image': str(obj.user.profile_image.url)})
        dump_object.update({'natural_timestamp': calculate_timestamp(obj.timestamp)})

        return dump_object


class LazyGroupInfoEncoder(Serializer):
    def get_dump_object(self, obj):
        dump_object = {}
        dump_object.update({'id': str(obj.id)})
        dump_object.update({'title': str(obj.title)})
        dump_object.update({'about': str(obj.about)})
        dump_object.update({'group_image': str(obj.group_image.url)})

        return dump_object
