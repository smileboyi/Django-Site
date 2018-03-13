"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import pymysql   # 如果要使用其他数据库，先导入相关数据库模块
pymysql.install_as_MySQLdb()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jw1fsxyg6a(zmun&iv$^rma09wfoc*ao=2=qb@(fy9@^x$1il^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # 每个应用都有数据库表，使用前先创建表python manage.py migrate
    'django.contrib.admin',  # admin管理后台站点
    'django.contrib.auth', # 身份认证系统
    'django.contrib.contenttypes', # 内容类型框架
    'django.contrib.sessions', # 会话框架
    'django.contrib.messages', # 消息框架
    'django.contrib.staticfiles', # 静态文件管理框架
    'django.contrib.admindocs', # admindocs应用可以从模型、视图、模板标签等地方获得文档内容
    'django.contrib.sitemaps', # 网站地图，不需要建立数据表

    #注册app,数据库就会对它创建表
    'cmdb',
    'polls',
    'upload',
    'login',

    'captcha',  #　图片验证码，需要建立自己的数据库表

    # 使用rest框架
    'rest_framework',
    'snippets.apps.SnippetsConfig', # 如果使用的django版本低于1.9，直接使用snippets来代替snippets.apps.SnippetsConfig即可
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # Django的messages框架默认使用的存储后端为sessions。所以Session中间件必须被启用，并出现在Message中间件之前。
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

# Django可以配置一个或多个模板引擎（语言），也可以不用引擎。
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # render时要指定html文件的地址(DIRS是一个元祖，后面逗号不能省略)
        # 模板的搜索路径。当加载Django模板时，会在DIRS中进行查找。
        # 建议在每个APP的的模版子目录下都建立一个子目录来唯一对应这个APP，
        # 这样做可以增强你的APP的可用性。 将所有的模版文件放在根模版目录下会引发混淆。
        'DIRS': [os.path.join(BASE_DIR,'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    # 默认使用django自带的sqlite数据库
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }

    # 使用mysql数据库
    # 百度把if version < (1, 3, 3)语句注释掉
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     # 要先创建好数据库,值是创建好的数据库名称
    #     'NAME': 'mysite',  
    #     'HOST': 'localhost',
    #     'USER': 'root',
    #     'PASSWORD': '',
    #     'PORT': '3306',
    #     'OPTIONS': {
    #         'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    #         'charset': 'utf8mb4',
    #     },
    # }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

# 这个指的是引用指针，不是具体的目录，可以改成你想要的任何名字。但是在html文件中，必须和他对应。
STATIC_URL = '/static/'

# 新建一行（将值赋值给一个元祖，后面逗号不能省略）
STATICFILES_DIRS = (
    # 第二个参数和静态资源文件对应
    os.path.join(BASE_DIR, 'static'),
)



# 邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sina.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'xxxxx@sina.com'
EMAIL_HOST_PASSWORD = 'xxxxxx'

# 注册有效期天数
CONFIRM_DAYS = 7


# 分页（snippets应用）
# REST框架中的设置都命名为单个字典设置，名为“REST_FRAMEWORK”，这有助于保持它们与其他项目设置分离
# 分页设置: http://www.django-rest-framework.org/api-guide/pagination/
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination', # 使用全局分页变量
    'PAGE_SIZE': 10
}
