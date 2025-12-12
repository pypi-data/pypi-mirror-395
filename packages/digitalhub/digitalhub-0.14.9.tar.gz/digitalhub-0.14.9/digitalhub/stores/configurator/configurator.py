# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.stores.configurator.handler import ConfigurationHandler


class Configurator:
    """
    Configurator class for configuration and credentials management.
    """

    def __init__(self):
        self._handler = ConfigurationHandler()
        self._reload_from_env = False

    ##############################
    # Configuration
    ##############################

    def get_configuration(self) -> dict:
        """
        Retrieve the current configuration.

        Returns
        -------
        dict
            Dictionary of configuration variables.
        """
        return self._handler.get_configuration()

    ##############################
    # Credentials
    ##############################

    def get_credentials(self) -> dict:
        """
        Retrieve the current credentials.

        Returns
        -------
        dict
            Dictionary of credentials.
        """
        return self._handler.get_credentials()

    def eval_retry(self) -> bool:
        """
        Evaluate credentials reload based on retry logic.

        Returns
        -------
        bool
            True if a retry action was performed, otherwise False.
        """
        current_creds = self.get_credentials()
        reread_creds = self._handler.load_credentials()

        # Compare cached and file credentials.
        # If different, reload in cache.
        if current_creds != reread_creds:
            self.reload_credentials()
            return True

        # Check if we need to reload from env only
        if not self._reload_from_env:
            self._handler.reload_credentials_from_env()
            self._reload_from_env = True
            return True

        return False

    def reload_credentials(self) -> None:
        """
        Reload credentials from environment and file.
        """
        self._handler.reload_credentials()

    ###############################
    # Profile methods
    ###############################

    def set_current_profile(self, profile: str) -> None:
        """
        Set the current profile.

        Parameters
        ----------
        profile : str
            Name of the profile to set.
        """
        self._handler.set_current_profile(profile)

    ################################
    # Other methods
    ################################

    def write_file(self, variables: dict) -> None:
        """
        Write the current configuration and credentials to file.

        Parameters
        ----------
        variables : dict
            Dictionary of variables to write.
        """
        self._handler.write_file(variables)

    def get_config_creds(self) -> dict:
        """
        Get merged configuration and credentials.

        Returns
        -------
        dict
            Merged configuration and credentials dictionary.
        """
        return {**self.get_configuration(), **self.get_credentials()}


configurator = Configurator()
