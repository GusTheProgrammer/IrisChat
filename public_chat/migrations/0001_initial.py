# Generated by Django 4.0.1 on 2022-02-26 22:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


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
                ('users', models.ManyToManyField(help_text='users who are connected to chat room.', to=settings.AUTH_USER_MODEL)),
            ],
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
        ),
    ]
