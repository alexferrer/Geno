# Django settings for myproject project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'          
DATABASE_NAME = '/home/alex/Desktop/geno_latest/dbase/db'     
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http:/en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http:/www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/home/alex/Desktop/geno_latest/media/home/alex/Desktop/geno_latest/media.lawrence.com/"
MEDIA_ROOT = '/home/alex/Desktop/geno_latest/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http:/home/alex/Desktop/geno_latest/media.lawrence.com", "http:/example.com/home/alex/Desktop/geno_latest/media/"
MEDIA_URL = '/home/alex/Desktop/geno_latest/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http:/foo.com/home/alex/Desktop/geno_latest/media/", "/home/alex/Desktop/geno_latest/media/".
ADMIN_MEDIA_PREFIX = '/home/alex/Desktop/geno_latest/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'lc)47thqlgb5dzq+k0gj^@fd!*8fi!!s4u*15je-k@$)lm_p1b'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'myproject.urls'

TEMPLATE_DIRS = (
    '/home/alex/Desktop/geno_latest/templates',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'myproject.geno',
    
    'django.contrib.databrowse',
)


