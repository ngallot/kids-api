from typing import Optional
from dataclasses import dataclass
from configparser import ConfigParser, BasicInterpolation
import os


class EnvInterpolation(BasicInterpolation):
    """Interpolation which expands environment variables in values."""

    def before_get(self, parser, section, option, value, defaults):
        return os.path.expandvars(value)


@dataclass
class KidsApiConfig:
    name: str
    description: str
    debug: bool
    model_url: str

    @staticmethod
    def load():
        env: Optional[str] = os.environ.get('ENV', None)
        if not env:
            raise Exception('Environment variable ENV should be set.')
        config_file = os.path.join(os.getcwd(), 'config', f'{env.lower()}.ini')
        config: ConfigParser = ConfigParser(os.environ, interpolation=EnvInterpolation())
        config.read(config_file)
        config_value = lambda option: config.get(section='APP', option=option)

        return KidsApiConfig(
            name=config_value(option='name'),
            description=config_value(option='description'),
            debug=config.getboolean(section='APP', option='debug'),
            model_url=config_value('model_url')
        )
