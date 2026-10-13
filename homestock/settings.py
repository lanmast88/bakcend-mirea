"""Настройки Django-проекта homestock.

Проект создан командой ``django-admin startproject homestock .`` и
добавляет веб-интерфейс к консольному приложению учёта товаров в доме.
Документация настроек: https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path

#: Корень репозитория: homestock/settings.py -> homestock -> корень.
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ проекта. В рабочем окружении хранится вне репозитория.
SECRET_KEY = (
    "django-insecure--k)g(4nfzk@+&o340h-8u@j_u$mq20_^fi(1(&$s=%8*=7qy%y"
)

# Режим отладки. Для проверки собственной страницы 404 временно
# выключается: при DEBUG = True Django показывает служебную страницу.
DEBUG = True

#: Адреса, с которых принимаются запросы при выключенной отладке.
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


# Приложения проекта: встроенные приложения Django и приложения
# веб-интерфейса. Без регистрации Django не обнаружит приложение.
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "homepage",
    "categories",
    "items",
    "operations",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

#: Корневой модуль маршрутизации проекта.
ROOT_URLCONF = "homestock.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "homestock.wsgi.application"


# База данных. Данные предметной области пока хранятся в JSON-файлах
# каталога data/; SQLite используется служебными приложениями Django.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Проверка паролей встроенного приложения django.contrib.auth.
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".NumericPasswordValidator"
        ),
    },
]


# Локализация проекта.
LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True


#: Префикс адресов статических файлов.
STATIC_URL = "static/"

#: Тип первичного ключа по умолчанию для будущих Django-моделей.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
