# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$123_nj8vtcodhz#++j4^htn+66pe5$!hovf0p9prbzc$qo(4s'

TELEGRAM_BOT_TOKEN = "534829617:AAHGPzWecEhC9pjXBuJJx4HsETj0EyJD46U"

# ALLOWED_HOSTS = ['127.0.0.1', '.breathum.herokuapp.com', '.breathum.ml', '46.160.68.56']
ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'breathum',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
