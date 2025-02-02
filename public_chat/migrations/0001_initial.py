# Generated by Django 4.0.1 on 2022-04-21 14:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import public_chat.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicChatRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('about', models.TextField(blank=True, max_length=150)),
                ('group_image', models.ImageField(blank=True, default=public_chat.models.get_default_group_image, max_length=255, null=True, upload_to=public_chat.models.get_group_image_filepath)),
                ('users', models.ManyToManyField(blank=True, help_text='users who are connected to chat room.', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Room',
            },
        ),
        migrations.CreateModel(
            name='PublicRoomChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public_chat.publicchatroom')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'message',
            },
        ),
    ]
