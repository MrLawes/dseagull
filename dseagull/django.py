import os

import django


def setup(value):
    import pymysql
    pymysql.install_as_MySQLdb()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', value)
    django.setup()
