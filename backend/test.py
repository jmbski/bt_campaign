import toml
from warskald import EnvironmentProps

ENV_PROPS = EnvironmentProps()
APP_NAME = 'pybuild'
APP_PROPS = ENV_PROPS.get(APP_NAME)
max_attempts = APP_PROPS.max_install_attempts
print(max_attempts, type(max_attempts))