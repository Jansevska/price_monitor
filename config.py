import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    USERNAME = os.environ.get('username')
    PASSWORD = os.environ.get('password')