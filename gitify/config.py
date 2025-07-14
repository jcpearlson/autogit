import json
import os
from pathlib import Path

from gitify.__init__ import DEFAULT_MODEL

CONFIG_FILE = Path.home() / '.gitifyconfig'


def get_config():
  if CONFIG_FILE.exists():
    with open(CONFIG_FILE) as f:
      return json.load(f)
  return {}


def save_config(config):
  with open(CONFIG_FILE, 'w') as f:
    json.dump(config, f)


def get_api_key():
  config = get_config()
  if 'api_key' not in config:
    raise ValueError("No API key found. Please run `gitify config` to set it.")
  return config['api_key']


def get_model():
  config = get_config()
  return config.get('model', DEFAULT_MODEL)


def set_config(api_key, model):
  save_config({'api_key': api_key, 'model': model})
