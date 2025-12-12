import os
import pytest
import importlib
from . import TARGET_MODULE_NAME

# Test target module import
environment_var_helper = importlib.import_module(f"{TARGET_MODULE_NAME}.wrapper.environment_var_helper")
EnvironmentVarHelper = environment_var_helper.EnvironmentVarHelper
MissingArgumentError = environment_var_helper.MissingArgumentError


class TestGetToken:
    def test_returns_original_token_if_not_None(self):
        arg_token = "a token"
        token = EnvironmentVarHelper.get_token(arg_token)
        assert token == arg_token

    def test_returns_environment_variable_if_original_token_is_None(self):
        # Arrange
        arg_token = None
        env_var_token = "token stored as env variable"
        os.environ['OSDUTOKEN'] = env_var_token

        # Act
        token = EnvironmentVarHelper.get_token(arg_token)

        # Assert
        assert token == env_var_token

        # Teardown
        os.environ.pop('OSDUTOKEN')

    def test_raises_MissingArgumentError_when_original_token_is_None_and_environment_var_not_set(self):
        arg_token = None
        with pytest.raises(MissingArgumentError):
            EnvironmentVarHelper.get_token(arg_token)


class TestGetConfigPath:
    def test_returns_original_config_path_if_not_None(self):
        arg_config_path = "path/to/config/file.json"
        config_path = EnvironmentVarHelper.get_config_path(arg_config_path)
        assert config_path == arg_config_path

    def test_returns_environment_variable_if_original_config_path_is_None(self):
        # Arrange
        arg_config_path = None
        env_var_config_path = "config/path/as/environment/variable.json"
        os.environ['CONFIGPATH'] = env_var_config_path

        # Act
        config_path = EnvironmentVarHelper.get_config_path(arg_config_path)

        # Assert
        assert config_path == env_var_config_path

        # Teardown
        os.environ.pop('CONFIGPATH')

    def test_raises_MissingArgumentError_when_original_config_path_is_None_and_environment_var_not_set(self):
        arg_config_path = None
        with pytest.raises(MissingArgumentError):
            EnvironmentVarHelper.get_config_path(arg_config_path)
