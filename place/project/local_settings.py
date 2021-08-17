DEBUG = True

ALLOWED_HOSTS = []


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'place',
        'USER': 'place',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4', 
            'init_command': 'ALTER DATABASE place CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci',
        },
    },
}