# Setting up the environment
***
1. #### Install [Docker](https://www.docker.com/get-started) or [Memurai](https://www.memurai.com/get-memurai)
   1. if using Docker install c++ build tools [Link](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019)
   2. Run This Command in terminal: `docker run -p 6379:6379 -d redis:5`
   
2. #### Download and install postgres SQL [Link](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
3. #### Initializing Postgress SQL:
   1. #### Run `psql postgres postgres` to access postgress SQL
   2. #### Create the database`CREATE DATABASE chatapp;`
   3. #### Create a user`CREATE USER django WITH PASSWORD 'django-password';`
   4. #### Grant the user privileges`GRANT ALL PRIVILEGES ON DATABASE chatapp TO django;`
4. #### setup a virtual environment `virutalenv venv`
5. #### install the required libraries using `pip install -r requirements.txt`
6. #### create a superuser using `python manage.py createsuperuser`

***
**Make Sure You have a later version of Python e.g. 3.9 or higher**