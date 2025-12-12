"""
Default parameters, distributions, and seed configuration
"""

DEFAULT_CONFIG = {
    'locale': 'en_US',
    'default_rows': 100,
    'default_seed': None,
    'csv_index': False,
    'json_orient': 'records',
    'json_indent': 4,
}


def get_config(key, default=None):
    """Get configuration value"""
    return DEFAULT_CONFIG.get(key, default)


def set_config(key, value):
    """Set configuration value"""
    DEFAULT_CONFIG[key] = value
