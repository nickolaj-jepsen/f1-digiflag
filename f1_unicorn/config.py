import json

_cache = {}


def load_config():
    global _cache
    if _cache:
        return _cache
    with open("config.json", "r") as f:
        config = json.load(f)
        _cache = config
        return config


def save_config(config):
    global _cache
    with open("config.json", "w") as f:
        json.dump(config, f)
        _cache = config
