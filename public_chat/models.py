from django.conf import settings
from django.db import models


# Create your models here.

def get_group_image_filepath(self, filename):
    return 'group_images/' + str(self.pk) + '/group_image.png'


def get_default_group_image():
    return 'img/dummy_image.png'


class PublicChatRoom(models.Model):
    title = models.CharField(max_length=255, unique=True, blank=False, )
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                   help_text="users who are connected to chat room.")
    about = models.TextField(max_length=150, blank=True)
    group_image = models.ImageField(upload_to=get_group_image_filepath, blank=True, null=True, max_length=255,
                                    default=get_default_group_image)

    class Meta:
        verbose_name = 'Room'

    def __str__(self):
        return self.title

    def connect_user(self, user):
        # return true if user is added to the users list
        is_user_added = False
        if not user in self.users.all():
            self.users.add(user)
            self.save()
            is_user_added = True
        elif user in self.users.all():
            is_user_added = True
        return is_user_added

    def disconnect_user(self, user):
        # return true if user is removed from the users list
        is_user_removed = False
        if user in self.users.all():
            self.users.remove(user)
            self.save()
            is_user_removed = True
        return is_user_removed

    @property
    def group_name(self):
        # Returns the Channels Group name that sockets should subscribe to get sent messages as they are generated.
        return f"PublicChatRoom-{self.id}"


class PublicRoomChatMessageManager(models.Manager):
    def by_room(self, room):
        qs = PublicRoomChatMessage.objects.filter(room=room).order_by("-timestamp")
        return qs


class PublicRoomChatMessage(models.Model):
    # Chat message created by a user inside a PublicChatRoom
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(PublicChatRoom, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(unique=False, blank=False, )

    objects = PublicRoomChatMessageManager()

    class Meta:
        verbose_name = 'message'

    def __str__(self):
        return self.content
