from .version import app as version_app
from .generate import app as generate_app
from .doctor import app as doctor_app
from .config import app as config_app
from .unspine import app as unspine_app
from .parse import app as parse_app
from .explain import app as explain_app

__all__ = [ 'version_app',
            'generate_app',
            'doctor_app',
            'parse_app',
            'unspine_app',
            'config_app',
            'explain_app']
