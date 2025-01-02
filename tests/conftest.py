def pytest_configure(config):  # noqa
    from django.conf import settings

    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            },
        },
        LANGUAGE_CODE='zh-hans',
        TIME_ZONE='Asia/Shanghai',
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'dseagull',
            'tests.models',
            'tests',
        ],
    )
