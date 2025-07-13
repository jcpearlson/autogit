import json
import os
from pathlib import Path

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
  # TODO: check if this .get checks model and defaults to gpt-4 or what it is doing
  return config.get('model', 'gpt-4')


def set_config(api_key, model):
  save_config({'api_key': api_key, 'model': model})
