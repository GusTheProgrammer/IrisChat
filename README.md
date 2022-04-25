# Iris Chat

***

#### Usage :desktop_computer:

Visit our final version [IrisChat.me](https://irischat.me/)

or

The Built-in Development Server using `python manage.py runserver`

# Setting up the environment

***

2. #### Install [Docker](https://www.docker.com/get-started) or [Memurai](https://www.memurai.com/get-memurai)
    1. if using Docker install c++ build
       tools [Link](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019)
    2. Run This Command in terminal: `docker run -p 6379:6379 -d redis:5`

3. #### Download and install postgres SQL [Link](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
4. #### Initializing Postgress SQL:
    1. #### Run `psql postgres postgres` to access postgress SQL
    2. #### Create the database`CREATE DATABASE chatapp;`
    3. #### Create a user`CREATE USER django WITH PASSWORD 'django-password';`
    4. #### Grant the user privileges`GRANT ALL PRIVILEGES ON DATABASE chatapp TO django;`
5. #### setup a virtual environment `virutalenv venv`
6. #### install the required libraries using `pip install -r requirements.txt`
7. #### create a superuser using `python manage.py createsuperuser`
8. #### Go to `/admin` and create a room for the public chat
9. #### Run `django manage.py shell` then copy the script (press enter twice after copying it)

```python
from friend.models import FriendList
from chat.utils import find_or_create_private_chat

friend_lists = FriendList.objects.all()
for f in friend_lists:
    for friend in f.friends.all():
        chat = find_or_create_private_chat(f.user, friend)
        chat.is_active = True
        chat.save()
```

8. #### type `quit()` to exit the shell

***
**Make Sure You have a later version of Python e.g. 3.9 or higher**