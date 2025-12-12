from .config_manager import get_active_model


def get_model():
    active_config = get_active_model()
    return active_config
