from .base import*
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'djangowebapp-gbgneucag0ccahgv.canadacentral-01.azurewebsites.net',
    'localhost',  # opcional para desarrollo local
]

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS=[BASE_DIR /'static']




MEDIA_URLS='media/'
MEDIA_ROOT=[BASE_DIR /'media']
