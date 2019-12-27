import hypothesis.strategies
import pytest
import six

from granula.exception import EnvironmentVariableError
from granula.operator import EnvironmentVariable
from tests.strategies import CONFIG, TEXT, WORD, INTEGER, FLOAT
from tests.utils import replace_environment, remove_from_environment


@hypothesis.given(CONFIG, WORD, TEXT)
def test_environment_variable_text(config, name, value):
    value = value.replace(u'\0', u'\\0')
    if six.PY2:
        # python2 environ does not allow unicode values
        value = value.encode('utf8')

    with replace_environment(variables={name: value}):
        assert EnvironmentVariable(name).apply(config) == value


@hypothesis.given(CONFIG, WORD, INTEGER)
def test_environment_variable_int(config, name, value):
    env_value = six.text_type(value)
    if six.PY2:
        # python2 environ does not allow unicode values
        env_value = env_value.encode('utf8')

    with replace_environment(variables={name: env_value}):
        assert EnvironmentVariable(name).apply(config) == value


@hypothesis.given(CONFIG, WORD, FLOAT)
def test_environment_variable_float(config, name, value):
    env_value = six.text_type(value)
    if six.PY2:
        # python2 environ does not allow unicode values
        env_value = env_value.encode('utf8')

    with replace_environment(variables={name: env_value}):
        assert EnvironmentVariable(name).apply(config) == value


@hypothesis.given(CONFIG, WORD, hypothesis.strategies.from_regex(r'^[Tt]rue$'))
def test_environment_variable_bool_true(config, name, value):
    env_value = value
    if six.PY2:
        # python2 environ does not allow unicode values
        env_value = env_value.encode('utf8')

    with replace_environment(variables={name: env_value}):
        assert EnvironmentVariable(name).apply(config) is True


@hypothesis.given(CONFIG, WORD, hypothesis.strategies.from_regex(r'^[Ff]alse$'))
def test_environment_variable_bool_false(config, name, value):
    env_value = value
    if six.PY2:
        # python2 environ does not allow unicode values
        env_value = env_value.encode('utf8')

    with replace_environment(variables={name: env_value}):
        assert EnvironmentVariable(name).apply(config) is False


@hypothesis.given(CONFIG, WORD, hypothesis.strategies.from_regex(r'^([Nn]one|[Nn]ull)$'))
def test_environment_variable_null(config, name, value):
    env_value = value
    if six.PY2:
        # python2 environ does not allow unicode values
        env_value = env_value.encode('utf8')

    with replace_environment(variables={name: env_value}):
        assert EnvironmentVariable(name).apply(config) is None


@hypothesis.given(CONFIG, WORD)
def test_environment_variable_not_set(config, name):
    with remove_from_environment(name):
        with pytest.raises(EnvironmentVariableError) as context:
            EnvironmentVariable(name).apply(config)

        message = u'Environment variable "{}" is not set'.format(name)
        assert six.text_type(context.value) == message
