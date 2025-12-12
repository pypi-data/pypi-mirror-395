"""
Helper functions for data generation
"""

import random
from faker import Faker


def set_seed(seed):
    """Set random seed for reproducibility"""
    if seed is not None:
        Faker.seed(seed)
        random.seed(seed)


def validate_template(template):
    """Validate template structure"""
    required_keys = ["template_name", "subcategories"]
    for key in required_keys:
        if key not in template:
            raise ValueError(f"Template missing required key: {key}")
    return True
