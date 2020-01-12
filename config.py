import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Secret key for session management. You can generate random strings here:
# https://randomkeygen.com/
SECRET_KEY = 'my precious'

# Connect to the database
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:5ea6b9fc8971@localhost/hotel?charset=utf8"

SQLALCHEMY_TRACK_MODIFICATIONS = True