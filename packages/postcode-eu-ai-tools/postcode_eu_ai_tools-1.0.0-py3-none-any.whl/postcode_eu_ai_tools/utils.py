import os
import tomllib
from getpass import getpass
from platformdirs import user_config_dir


def get_config_file() -> str:
    config_dir = user_config_dir('postcode-eu-ai-tools', appauthor='Postcode.eu')
    return os.path.join(config_dir, 'config.toml')

def get_api_credentials() -> tuple[str, str]:
    api_key = os.getenv('POSTCODE_EU_API_KEY') or None
    api_secret = os.getenv('POSTCODE_EU_API_SECRET') or None
    if api_key and api_secret:
        return api_key, api_secret

    config_file = get_config_file()
    if os.path.exists(config_file):
        try:
            with open(config_file, 'rb') as f:
                config = tomllib.load(f)
            api_key = config.get('api_key')
            api_secret = config.get('api_secret')
        except (tomllib.TOMLDecodeError) as e:
            print(f'Invalid config.toml: {e}')

        if api_key and api_secret:
            return api_key, api_secret

    raise ValueError('No credentials found.')


def save_api_credentials() -> None:
    api_key = getpass('Postcode.eu API key: ')
    api_secret = getpass('Postcode.eu API secret: ')

    config_file = get_config_file()
    os.makedirs(os.path.dirname(config_file), exist_ok=True)

    with open(config_file, 'w') as f:
        _ = f.write(f'api_key = "{api_key}"\n')
        _ = f.write(f'api_secret = "{api_secret}"\n')

    print(f'Credentials stored in {config_file}')
