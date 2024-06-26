from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

include(
    'components/common.py',
    'components/database.py',
    'components/installed_apps.py',
    'components/middleware.py',
    'components/templates.py',
    'components/auth_password_validators.py',
    'components/auth.py',
)
