## Personal blog hosted on xhalford.com.

# Setup:

`git clone git@github.com:rsHalford/xhalford-blog.git`

`python3 -m venv /path/to/new/virtual/environment`

`pip install -r requirements.txt`

## Settings.py
```python

from decouple import config, Csv
import dj_database_url

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)

```

## Create a .env at root, and add the following:

### Local Environment
```

SECRET_KEY=
DEBUG=True
ALLOWED_HOSTS=.localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

```

### Production Environment
```

SECRET_KEY=
ALLOWED_HOSTS=
DATABASE_URL=postgres://{ db_user }:{ db_password }@{ db_host }:{ db_port }/{ db_name }
EMAIL_HOST=smtp.domain.xyz
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

```
