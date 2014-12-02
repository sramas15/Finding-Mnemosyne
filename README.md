Set up
======
Make sure Python 2.7, pip, easy_install, and virtualenv are installed.
Also make sure you created your Heroku account from my invitation.

Install the Heroku toolbelt from https://toolbelt.heroku.com/
This should give you the commands "heroku" and "foreman"

Get the most recent version of the repo:

    cd ~/path/to/Finding-Mnemosyne
    git pull

Create the virtualenv and install dependencies in the new environment.

    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

Add the heroku repo as a remote.

    heroku git:remote --app rocky-fortress-6883

Try running the app locally:

    foreman start

The app should run, and you should be able to access it at localhost:5000, but it won't work completely
yet because the database is not set up. You need to install PostgreSQL next. The easiest option might be
to download the native Mac app: http://postgresapp.com/
I'm not sure what the details are on this, but mainly you'll just need to have a a PostgreSQL database
running locally on your machine, and also to have the command line util "psql" to play around in case
you want to see the tables.

After installing postgres, create the tables:

    python manage.py migrate

Also create your superuser (gives you access to admin panel at /admin)

    python manage.py createsuperuser

Now the app should work.

    foreman start

In the future, to push changes to the heroku repo, just run:

    git push heroku master

To push to our main Github repo, do what we've always done:

    git push

Upload cards
============
You won't be able to do much on the app without flash cards. Download some flashcards from the Mnemosyne website,
in the *.cards format. Then, while the app is running, navigate to localhost:5000/upload to upload a card set.
If it works successfully, it should redirect you to the same upload page with no positive feedback (sorry this is
a bug). Navigate to the Home page to see if the card set was successfully uploaded. Now you can study them from
the Study page!


Running the analysis scripts
============================

I wrote a little script in scripts/main.py to run each of the analysis steps sequentially.
First make sure that the data directory is inside the scripts directory. (Git didn't handle this because
I made it ignore the data directory for space.)

    mv data scripts/

Rebuild the filtered logs from the main script. (If you don't want to do this, you need to at least rerun
filter_db.create_discretizeddb() since I added a column there to discrete_log).

    cd scripts
    python main.py 0
    python main.py 1
    python main.py 2

See the source code to see what it's actually doing.


Upload user logs
================
Currently, you can upload the discrete_log entries as a CSV file to the app, where it will load those
log entries into the database as your user's own logs (I haven't done any fancy stuff with creating a
special/separate user to associate these "prior" entries with yet).

Create the CSV file. Make sure filtered_logs.db is created already, and that discrete_log has been
rebuilt using the new code.

    sqlite3 scripts/data/filtered_logs.db
    sqlite> .mode csv
    sqlite> .output logs.csv
    sqlite> select * from discrete_log where user_id="<THE_CHOSEN_ONE>";
    sqlite> .exit

You should now have a file at "logs.csv" with the rows you selected. You can upload this file at:
localhost:5000/upload_user_logs
It should have the same (stupid) form behavior as the card upload form (it will look like nothing has
happened if you succeeded.)

To double check the rows are there now, query the postgres tables:

    psql
    <sheila>=# select * from scheduling_repintervallog;

