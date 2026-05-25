import dj_database_url
import os
from pathlib import Path
import ssl

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

def _parse_bool(value, default=False):
    if value is None:
        return default
    return str(value).strip().lower() in ("1", "true", "t", "yes", "y", "on")

def _parse_list(value):
    if not value:
        return []
    return [item.strip() for item in str(value).split(",") if item.strip()]

def _load_dotenv(dotenv_path: Path):
    """
    Loader simples de .env sem dependências externas.
    Não sobrescreve variáveis já definidas no ambiente.
    """
    if not dotenv_path.exists():
        return

    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        os.environ.setdefault(key, value)

_load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY não configurada.")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = _parse_bool(os.environ.get("DJANGO_DEBUG"), default=True)

ALLOWED_HOSTS = _parse_list(
    os.environ.get("DJANGO_ALLOWED_HOSTS", "*")
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'core',
    'corsheaders',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'core.auth.APIKeyAuthentication',
        # ✅ OTIMIZADO: Remover SessionAuthentication se não precisa de sessão
        # 'rest_framework.authentication.SessionAuthentication',
    ],
    # ✅ OTIMIZADO: Throttling desativado se não é crítico
    # Throttling usa cache Redis = leituras extras
    # Desative se não é essencial ou use cache em memória
    # 'DEFAULT_THROTTLE_CLASSES': [
    #     'rest_framework.throttling.AnonRateThrottle',
    #     'rest_framework.throttling.UserRateThrottle',
    # ],
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': os.environ.get('DRF_THROTTLE_ANON', '60/min'),
    #     'user': os.environ.get('DRF_THROTTLE_USER', '300/min'),
    # },
}


ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

CORS_ALLOWED_ORIGINS = _parse_list(os.environ.get("CORS_ALLOWED_ORIGINS"))
CSRF_TRUSTED_ORIGINS = _parse_list(os.environ.get("CSRF_TRUSTED_ORIGINS"))

# Celery + Redis - OTIMIZADO para evitar auto-consumo
# Render fornece REDIS_URL; em dev local, use variável de ambiente ou padrão local
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

CELERY_BROKER_URL = REDIS_URL
# ⚠️ REMOVIDO: CELERY_RESULT_BACKEND - Tasks são fire-and-forget (não precisa guardar resultado)
CELERY_RESULT_BACKEND = None  # Não armazena resultados no Redis (evita auto-consumo)

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "America/Sao_Paulo"

# ⚠️ DESATIVADO: CELERY_TASK_TRACK_STARTED - Evita overhead de rastreamento
CELERY_TASK_TRACK_STARTED = False  # Não tracked no Redis

CELERY_TASK_TIME_LIMIT = int(os.environ.get("CELERY_TASK_TIME_LIMIT", "300"))
CELERY_TASK_SOFT_TIME_LIMIT = int(os.environ.get("CELERY_TASK_SOFT_TIME_LIMIT", "270"))

CELERY_BROKER_CONNECTION_TIMEOUT = 5.0  # Reduzido para Render
CELERY_BROKER_HEARTBEAT = 30  # Heartbeat para detectar conexões mortas
CELERY_BROKER_POOL_LIMIT = 10  # Limitar pool de conexões

# Retry settings otimizados
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = _parse_bool(
    os.environ.get("CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP"), default=True
)
CELERY_BROKER_CONNECTION_RETRY = _parse_bool(
    os.environ.get("CELERY_BROKER_CONNECTION_RETRY"), default=True
)
CELERY_BROKER_CONNECTION_MAX_RETRIES = int(os.environ.get("CELERY_BROKER_CONNECTION_MAX_RETRIES", "100"))

# Transport options otimizados
CELERY_BROKER_TRANSPORT_OPTIONS = {
    "socket_connect_timeout": 5.0,
    "socket_timeout": 10.0,
    "visibility_timeout": 3600,  # Task timeout visibility
}

# SSL para Render/produção
CELERY_BROKER_USE_SSL = {
    "ssl_cert_reqs": ssl.CERT_NONE
}

SECURE_SSL_REDIRECT = _parse_bool(
    os.environ.get("SECURE_SSL_REDIRECT"),
    default=not DEBUG
)

SESSION_COOKIE_SECURE = _parse_bool(
    os.environ.get("SESSION_COOKIE_SECURE"),
    default=not DEBUG
)
# ✅ OTIMIZADO: Use banco de dados para sessões (é mais eficiente que Redis)
# Redis é melhor para cache de aplicação, não para sessões de usuário
SESSION_ENGINE = "django.contrib.sessions.backends.db"
# SESSION_CACHE_ALIAS = "default"  # Desativado

CSRF_COOKIE_SECURE = _parse_bool(
    os.environ.get("CSRF_COOKIE_SECURE"),
    default=not DEBUG
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {'format': '%(levelname)s %(name)s: %(message)s'},
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'simple'},
    },
    'root': {
        'handlers': ['console'],
        'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
    },
}


DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SSL_CERT_REQS": None,
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
            # ✅ REMOVIDO: "COMPRESSOR" - ZlibCompressor adiciona overhead de CPU/memória
            # Compressão não vale a pena para dados pequenos (cache típico < 100KB)
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 5,  # ✅ Pool pequeno = menos overhead
            }
        },
        "KEY_PREFIX": "cache",
        "TIMEOUT": 3600,  # ✅ Aumentado de 300s para 1h - dados expiram menos freq
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
