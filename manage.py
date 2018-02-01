#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # 当你使用Django时，你必须告诉它你要使用哪个配置文件来启动服务。也就是给环境变量DJANGO_SETTINGS_MODULE赋值。
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
