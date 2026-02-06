# config/loader.py

import yaml
import os

BASE_DIR = os.path.dirname(__file__)

def load_user_preferences():
    path = os.path.join(BASE_DIR, 'user_preferences.yaml')
    with open(path, 'r') as f:
        return yaml.safe_load(f)


