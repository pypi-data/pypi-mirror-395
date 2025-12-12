import json
import sys

from rich.console import Console

console = Console()


def log(*args, **kwargs):
    console.print(*args, **kwargs)


def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False


def is_runserver():
    """
    Checks if the Django application is started as a server.
    We'll also assume it started if manage.py is not used (e.g. when Django is started using wsgi/asgi).
    The main purpose of this check is to not run certain code on other management commands such
    as `migrate`.
    """
    is_manage_cmd = sys.argv[0].endswith("/manage.py")

    return not is_manage_cmd or sys.argv[1] == "runserver"


def flatten(xss):
    return [x for xs in xss for x in xs]
