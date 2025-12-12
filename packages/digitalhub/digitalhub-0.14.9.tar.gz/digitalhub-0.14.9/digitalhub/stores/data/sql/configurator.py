# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.stores.configurator.configurator import configurator
from digitalhub.stores.configurator.enums import ConfigurationVars, CredentialsVars


class SqlStoreConfigurator:
    """
    Configurator class for SQL store configuration and credentials management.
    """

    def __init__(self):
        self._validate()

    def get_sql_conn_string(self) -> str:
        """
        Generate PostgreSQL connection string from stored credentials.

        Returns
        -------
        str
            A PostgreSQL connection string in the format:
            'postgresql://username:password@host:port/database'
        """
        creds = self.get_sql_credentials()
        user = creds[CredentialsVars.DB_USERNAME.value]
        password = creds[CredentialsVars.DB_PASSWORD.value]
        host = creds[ConfigurationVars.DB_HOST.value]
        port = creds[ConfigurationVars.DB_PORT.value]
        database = creds[ConfigurationVars.DB_DATABASE.value]
        return f"postgresql://{user}:{password}@{host}:{port}/{database}"

    def get_sql_credentials(self) -> dict:
        """
        Get all configured database credentials as a dictionary.

        Retrieves all available database credentials from the configured
        source and returns them as a dictionary with all credential keys
        from self.keys mapped to their values.

        Returns
        -------
        dict
            Dictionary containing all credential key-value pairs from self.keys.
            Keys correspond to database connection parameters such as
            username, password, host, port, database, and platform.
        """
        keys = [
            CredentialsVars.DB_USERNAME.value,
            CredentialsVars.DB_PASSWORD.value,
            ConfigurationVars.DB_HOST.value,
            ConfigurationVars.DB_PORT.value,
            ConfigurationVars.DB_DATABASE.value,
        ]
        creds = configurator.get_config_creds()
        return {key: creds.get(key) for key in keys}

    def eval_retry(self) -> bool:
        """
        Evaluate the status of retry lifecycle.

        Returns
        -------
        bool
            True if a retry should be attempted, False otherwise.
        """
        return configurator.eval_retry()

    def _validate(self) -> None:
        """
        Validate if all required keys are present in the configuration.
        """
        required_keys = [
            ConfigurationVars.DB_HOST.value,
            ConfigurationVars.DB_PORT.value,
            ConfigurationVars.DB_DATABASE.value,
            CredentialsVars.DB_USERNAME.value,
            CredentialsVars.DB_PASSWORD.value,
        ]
        current_keys = configurator.get_config_creds()
        missing_keys = []
        for key in required_keys:
            if key not in current_keys or current_keys[key] is None:
                missing_keys.append(key)
        if missing_keys:
            raise ValueError(f"Missing required variables for SQL store: {', '.join(missing_keys)}")
