import requests
import flask
from atlas_consortia_commons.string import trim_dict_or_list
from atlas_consortia_commons.file import ensure_trailing_slash_url
import json

ubkg_cache = dict()
_config_key = 'UBKG'


class Ubkg:
    def __init__(self, config: dict, config_key: str = _config_key):
        self.error = None
        self.config = config
        self.config_key = config_key

    def get_cache(self):
        return ubkg_cache

    def get_ubkg_valueset(self, node):
        return self.get_ubkg(node)

    def get_ubkg_by_key(self, node):
        key = get_from_node(node, 'key')
        return self.get_ubkg(node, key)

    def get_ubkg_by_endpoint(self, node):
        key = get_from_node(node, 'key')
        endpoint = get_from_node(node, 'endpoint')
        return self.get_ubkg(node, key, endpoint)

    def get_ubkg(self, node, key: str = 'VALUESET', endpoint: str = None):
        code = get_from_node(node)
        cache_key = f"{key}_{code}"
        try:
            self.error = None
            if cache_key not in ubkg_cache:
                server = self.config.get(get_server_key(self.config_key))
                server = ensure_trailing_slash_url(server)
                _endpoint = self.config.get(get_endpoint_key(self.config_key, key))
                endpoint = endpoint if endpoint is not None else _endpoint
                url = f"{server}{endpoint}"
                url = url.format(code=code)
                response = requests.get(url)
                if response.ok:
                    ubkg_cache[cache_key] = trim_dict_or_list(response.json())
        except Exception as e:
            self.error = e
            print(e)

        return ubkg_cache[cache_key] if cache_key in ubkg_cache else self.error


def get_from_node(node, key: str = 'code'):
    if type(node) is dict:
        val = node.get(key)
    else:
        val = node
    if type(val) is not str:
        return None
    else:
        return val


def get_server_key(config_key: str) -> str:
    return f"{config_key}_SERVER"


def get_codes_key(config_key: str) -> str:
    return f"{config_key}_CODES"


def get_endpoint_key(config_key: str, key: str) -> str:
    return f"{config_key}_ENDPOINT_{key}"


def verify_config(config: dict, config_key: str = _config_key) -> bool:
    if type(config) is not dict and not isinstance(config, flask.config.Config):
        return False
    else:
        if get_server_key(config_key) not in config or get_codes_key(config_key) not in config:
            return False
        else:
            return True


def initialize_ubkg(config: dict, config_key: str = _config_key):
    try:
        if verify_config(config, config_key):
            ubkg_instance = Ubkg(config, config_key)
            value_str = config.get(get_codes_key(config_key))
            items = json.loads(value_str)
            for node, val in items.items():
                setattr(ubkg_instance, f"{node}", val)
            return ubkg_instance
        else:
            return None
    except Exception as e:
        print(e)
