import os
from mysecrets import SECRET_KEY as my_secret_key
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or my_secret_key