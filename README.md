# Archived

## I have moved to [rshalford.com](https://www.rshalford.com).

Under that domain I will continue my blog posts and consolidate other parts of my online presence.


## Personal blog hosted on xhalford.com


# Production


## Apache setup

/etc/apache2/sites-available/blog.conf

```conf
<VirtualHost *:80>
        ServerName www.blog.com
        ServerAlias blog.com
        ServerAdmin user@blog.com

        DocumentRoot /home/user/blog

        ErrorLog ${APACHE_LOG_DIR}/blog-error.log
        CustomLog ${APACHE_LOG_DIR}/blog-access.log combined

        Alias /static /home/user/blog/static
        <Directory /home/user/blog/static>
                Require all granted
        </Directory>

        Alias /media /home/user/blog/media
        <Directory /home/user/blog/media>
                Require all granted
        </Directory>

        WSGIScriptAlias / /home/user/blog/blog_backend/wsgi.py
        WSGIDaemonProcess blog python-path=/home/user/blog python-home=/home/user/blog/venv
        WSGIProcessGroup blog
        <Directory /home/user/blog/blog_backend>
                <Files wsgi.py>
                        Require all granted
                </Files>
        </Directory>
RewriteEngine on
RewriteCond %{HTTP_HOST} ^www.blog.com$ [OR]
RewriteCond %{HTTP_HOST} ^blog.com$
RewriteRule ^(.*)$ https://www.blog.com$1 [R=301,L]
</VirtualHost>
```

```sh
# enable the virtual host file
$ sudo a2ensite blog.conf
$ sudo systemctl restart apache2
$ sudo apache2ctl configtest
```


## Certbot

```sh
# install certbot, then get and install certificates
$ sudo snap install --classic certbot
$ sudo ln -s /snap/bin/certbot /usr/bin/certbot
$ sudo certbot --apache

# test automatic renewals
$ sudo certbot renew --dry-run
```


## Prevent multiple WSGI processes

/etc/apache2/sites-available/blog.conf

```sh
# comment/remove the following lines
        WSGIScriptAlias / /home/user/blog/blog_backend/wsgi.py
        WSGIDaemonProcess blog python-path=/home/user/blog python-home=/home/user/blog/venv
        WSGIProcessGroup blog
```


## Clone and setup

```sh
# clone the project
$ git clone git@github.com:rsHalford/xhalford-blog.git blog

# change the project ownership to the apache group
$ chown :www-data blog/

$ cd blog/

# create the python virtual environment and activate it
$ python3 -m venv venv
$ source venv/bin/activate

# install the required production dependencies
$ pip install -r requirements-prod.txt

# propagate the model changes into the database schema
$ python3 manage.py migrate

# collect all app static files to be served
$ python3 manage.py collectstatic
```

## Environment variables

.env

```sh
ENCRYPT_KEY={ encrypt_key }
SECRET_KEY={ secret_key }
ALLOWED_HOSTS=.blog.com
DATABASE_URL=postgres://{ db_user }:{ db_password }@{ db_host }:{ db_port }/{ db_name }
EMAIL_HOST="{ smtp.blog.xyz }"
EMAIL_HOST_USER="{ user@blog.com }"
EMAIL_HOST_PASSWORD="{ password123 }"
```


# Development


## Clone and setup

```sh
# clone the project
$ git clone git@github.com:rsHalford/xhalford-blog.git

# install poetry
$ curl -sSL https://install.python-poetry.org | python3 - --git https://github.com/python-poetry/poetry.git@master

$ cd xhalford-blog/

# install the default, development and testing dependencies
$ poetry install --no-root --with=development,testing
```


## Environment variables

.env

```
ENCRYPT_KEY={ encrypt_key }
SECRET_KEY={ secret_key }
DEBUG=True
ALLOWED_HOSTS=.localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_REFERRER_POLICY=""
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```


## Create database

```sh
# enter the poetry shell
$ poetry shell

# propagate the model changes into the database schema
$ python3 manage.py migrate

# collect all app static files to be served
$ python3 manage.py collectstatic
```


## Export requirements-prod.txt

```sh
# poetry-export-plugin is used to export to a requirements-prod.txt for production
$ poetry plugin add poetry-export-plugin
$ poetry export --without=development,testing --format=requirements.txt --output=requirements-prod.txt --without-hashes
```
