# Setup Instructions 

After setting up the database and installing all the modules you'll need to run this app, you will need to run the following command in the terminal before you're able to run python manage.py runserver:

For Mac/Linux Users:

***For Mac/Linux Users: export READ_DOT_ENV_FILE=True***

***For Windows Users: set READ_DOT_ENV_FILE=True***

As opposed to how we've coded thus far, the database specifications needn't be changed in settings.py, but in the .env file. This is the path for it from the base directory: 

***crm/.env***

If you cannot find the above file, it's okay! Create a .env file at the aforementioned location and paste the following:

DEBUG=True
SECRET_KEY='django-insecure-1*wp-#d+qexi5qd%-t-61u64s($1jnkvk&6o)r&2l9$%wz+3^a'
DB_NAME=alyousuf
DB_USER=ayadmin
DB_PASSWORD=alyousuf123
DB_HOST=localhost
DB_PORT=

The above will be what you'll be modelling your database on. Remember you'll need to create a database, a user and grant permission to the user.

You may define your own database or set it up according to how I did.

If you face an error like this: ***django.core.exceptions.ImproperlyConfigured: Set the SECRET_KEY environment variable***,
chances are that your error lies in line 26 of settings.py. Uncommenting that line should make your project work.

I do encourage you to fork this project and play around with it to get a feel of it and the various functionalities I have implemented within it.

Feel free to reach out to me in case of any doubts or clarifications :)
