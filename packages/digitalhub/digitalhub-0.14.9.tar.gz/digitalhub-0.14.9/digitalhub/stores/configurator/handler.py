# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
from typing import Any

from digitalhub.stores.configurator.enums import ConfigurationVars, CredentialsVars, SetCreds
from digitalhub.stores.configurator.ini_module import (
    load_file,
    load_key,
    load_profile,
    set_current_profile,
    write_file,
)
from digitalhub.utils.generic_utils import list_enum


class ConfigurationHandler:
    """
    Handler for loading and writing configuration variables.
    """

    def __init__(self):
        self._current_profile = self._read_current_profile()
        self._configuration: dict[str, Any] = self.load_configuration()
        self._credentials: dict[str, Any] = self.load_credentials()

    @staticmethod
    def _read_env(variables: list) -> dict:
        """
        Read configuration variables from the .dhcore file.

        Parameters
        ----------
        variables : list
            List of environment variable names to read.

        Returns
        -------
        dict
            Dictionary of environment variables.
        """
        return {var: os.getenv(var) for var in variables}

    @staticmethod
    def _read_file(variables: list, profile: str) -> dict:
        """
        Read configuration variables from the .dhcore file.

        Parameters
        ----------
        variables : list
            List of environment variable names to read.
        profile : str
            Profile name to read from.

        Returns
        -------
        dict
            Dictionary of configuration variables.
        """
        file = load_file()
        return {var: load_key(file, profile, var) for var in variables}

    ##############################
    # Configuration methods
    ##############################

    def load_configuration(self) -> dict[str, Any]:
        """
        Load configuration with env > file precedence.

        Returns
        -------
        dict
            Merged configuration dictionary.
        """
        profile = self.get_current_profile()
        variables = list_enum(ConfigurationVars)
        env_config = self._read_env(variables)
        file_config = self._read_file(variables, profile)
        return {**file_config, **{k: v for k, v in env_config.items() if v is not None}}

    def reload_configuration(self) -> None:
        """
        Reload configuration from environment and file.
        """
        self._configuration = self.load_configuration()

    def get_configuration(self) -> dict[str, Any]:
        """
        Get the merged configuration dictionary.

        Returns
        -------
        dict[str, Any]
            The configuration dictionary.
        """
        return self._configuration

    ##############################
    # Credentials methods
    ##############################

    def load_credentials(self) -> dict[str, Any]:
        """
        Load credentials with file > env precedence.

        Parameters
        ----------
        profile : str
            Profile name to load credentials from.

        Returns
        -------
        dict
            Merged credentials dictionary.
        """
        variables = list_enum(CredentialsVars)
        env_config = self._read_env(variables)
        file_config = self._read_file(variables, self.get_current_profile())
        return {**env_config, **{k: v for k, v in file_config.items() if v is not None}}

    def reload_credentials(self) -> None:
        """
        Reload credentials from environment and file.
        """
        self._credentials = self.load_credentials()

    def reload_credentials_from_env(self) -> None:
        """
        Reload credentials from environment where env > file precedence.
        Its a partial reload only from env variables used as fallback.
        """
        variables = list_enum(CredentialsVars)
        env_config = self._read_env(variables)
        file_config = self._read_file(variables, self.get_current_profile())
        self._credentials = {**file_config, **{k: v for k, v in env_config.items() if v is not None}}

    def get_credentials(self) -> dict[str, Any]:
        """
        Get the merged credentials dictionary.

        Returns
        -------
        dict[str, Any]
            The credentials dictionary.
        """
        return self._credentials

    ##############################
    # Profile Methods
    ##############################

    @staticmethod
    def _read_current_profile() -> str:
        """
        Read the current credentials profile name.

        Returns
        -------
        str
            Name of the credentials profile.
        """
        profile = os.getenv(SetCreds.DH_PROFILE.value)
        if profile is not None:
            return profile
        file = load_file()
        profile = load_profile(file)
        if profile is not None:
            return profile
        return SetCreds.DEFAULT.value

    def set_current_profile(self, profile: str) -> None:
        """
        Set the current credentials profile name.

        Parameters
        ----------
        profile : str
            Name of the credentials profile to set.
        """
        self._current_profile = profile
        set_current_profile(profile)
        self.reload_configuration()
        self.reload_credentials()

    def get_current_profile(self) -> str:
        """
        Get the current credentials profile name.

        Returns
        -------
        str
            Name of the current credentials profile.
        """
        return self._current_profile

    def write_file(self, variables: dict) -> None:
        """
        Write variables to the .dhcore file for the current profile.

        Parameters
        ----------
        infos : dict
            Information to write.
        profile : str
            Profile name to write to.
        """
        write_file(variables, self._current_profile)
