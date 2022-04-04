from django.core.serializers.python import Serializer


class LazyAccountEncoder(Serializer):
    def get_dump_object(self, obj):
        dump_object = {}
        dump_object.update({'id': str(obj.id)})
        dump_object.update({'email': str(obj.email)})
        dump_object.update({'username': str(obj.username)})
        dump_object.update({'first_name': str(obj.first_name)})
        dump_object.update({'last_name': str(obj.last_name)})
        dump_object.update({'bio': str(obj.bio)})
        dump_object.update({'birth_date': str(obj.birth_date)})
        dump_object.update({'profile_image': str(obj.profile_image.url)})
        return dump_object
