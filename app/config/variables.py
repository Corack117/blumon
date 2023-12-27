import os

SECRET_KEY = os.environ.get('SECRET_KEY', None)
REFRESH_SECRET_KEY = os.environ.get('REFRESH_SECRET_KEY', None)
ALGORITHM = os.environ.get('ALGORITHM', None)