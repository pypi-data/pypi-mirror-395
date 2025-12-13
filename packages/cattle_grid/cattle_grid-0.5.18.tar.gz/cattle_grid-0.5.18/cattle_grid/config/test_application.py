from dynaconf import Dynaconf


from .application import ApplicationConfig
from .validators import all_validators


def test_application_config_empty():
    settings = Dynaconf(validators=all_validators)

    result = ApplicationConfig.from_settings(settings)

    assert result.testing is False
