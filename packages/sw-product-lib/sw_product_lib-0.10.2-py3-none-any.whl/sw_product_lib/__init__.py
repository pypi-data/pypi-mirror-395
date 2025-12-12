import importlib.metadata

from strangeworks_core.config.config import Config


__version__ = importlib.metadata.version("sw_product_lib")


DEFAULT_PLATFORM_BASE_URL = "https://api.strangeworks.com"
# initialize common common objects
cfg = Config()


def in_dev_mode():
    return cfg.get_bool("dev_mode")


def is_service_disabled() -> bool:
    """Returns Boolean Indicating Whether Service is Disabled."""
    return cfg.get_bool("service_disabled")
