from dotenv import load_dotenv

load_dotenv()

from orion.config.settings import get_settings  # noqa: E402

config = get_settings()
