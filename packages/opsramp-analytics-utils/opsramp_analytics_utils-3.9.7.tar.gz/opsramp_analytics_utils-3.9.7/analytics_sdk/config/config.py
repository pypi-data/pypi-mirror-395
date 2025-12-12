import os
import yaml
import logging
import time

CONFIG_CONTENT = None
SECTION_CONFIG_CONENT = None

VAL_NOT_FOUND = 'Not Found'
EXPORT_TO_OS = os.getenv('EXPORT_TO_OS', True)

logger = logging.getLogger(__name__)

def init_config():
    start_ts = int(time.time())
    global CONFIG_CONTENT
    if CONFIG_CONTENT is None:
        logger.info('initiated config....')
        CONFIGMAP_FILE_PATH = os.getenv('CONFIGMAP_FILE_PATH', None)
        if CONFIGMAP_FILE_PATH is None:
            logging.error(f'Unable to config props.. Aborting...')
            return
        CONFIG_CONTENT = {}
        try:
            with open(CONFIGMAP_FILE_PATH, 'r') as file:
                CONFIG_CONTENT = yaml.safe_load(file)
        except Exception as e:
            logging.error(f'Unable to config props.. Aborting... Exception :: {e}')
            raise Exception(f'Reading Config map failed ::: {e}')
        end_ts = int(time.time())
        logger.info(f'config loaded....{end_ts-start_ts}s')


def load_config_map():
    init_config()
    return CONFIG_CONTENT


def load_all_props():
    global SECTION_CONFIG_CONENT
    if SECTION_CONFIG_CONENT is None:
        all_props = {}
        config_content = load_config_map()
        if config_content is not None:
            for sec in config_content:
                section_props = load_props_by_section(sec)
                if section_props is not None:
                    all_props.update(section_props)
        SECTION_CONFIG_CONENT = all_props.copy()
    else:
        all_props = SECTION_CONFIG_CONENT.copy()
    return all_props


def load_props_by_section(section):
    props = {}
    config_content = load_config_map()
    if config_content is not None:
        if section is not None:
            if section in config_content:
                for prop in config_content[section]:
                    props[prop] = config_content[section][prop]
    return props


def load_value(prop_key, section=None, default_value=None):
    value = default_value

    if _is_key_found_in_env(prop_key):
        return _modify_value(_load_env_value(prop_key))

    config_content = load_config_map()
    if config_content is not None:
        props = None
        if section is None or len(section) <= 0:
            props = load_all_props()
        else:
            props = load_props_by_section(section)
        
        value = _load_value_by_key(props, prop_key, default_value)

    value = _modify_value(value)
    if EXPORT_TO_OS:
        os.environ[_prepare_env_key(prop_key)] = str(value)

    return value


def _modify_value(value):
    if value:
        try:
            value = int(value)
        except:
            if value == "True":
                return True
            elif value == "False":
                return False
            elif 'none' == value.lower():
                return None
            else:
                return value
    return value


def _load_value_by_key(props, key, default_value=None):
    value = default_value
    if key is not None and len(key) >= 0:
        env_value = _load_env_value(key)
        if VAL_NOT_FOUND != env_value:
            value = env_value
        else:
            key = key.replace("_", ".").lower()
            if props is not None and len(props) >= 0:
                if key in props:
                    value = props[key]
    return value


def _prepare_env_key(key):
    if key:
        key = key.replace('.', '_').upper()
    return key


def _load_env_value(key):
    value = VAL_NOT_FOUND
    if key is not None and len(key) >= 0:
        env_key = _prepare_env_key(key)
        env_value = os.getenv(env_key, VAL_NOT_FOUND)
        return env_value
    return value


def _is_key_found_in_env(key):
    value = _load_env_value(key)
    if value == VAL_NOT_FOUND:
        return False
    return True