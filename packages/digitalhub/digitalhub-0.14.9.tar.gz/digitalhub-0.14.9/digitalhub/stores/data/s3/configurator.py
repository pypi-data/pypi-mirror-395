# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from botocore.config import Config

from digitalhub.stores.configurator.configurator import configurator
from digitalhub.stores.configurator.enums import ConfigurationVars, CredentialsVars


class S3StoreConfigurator:
    """
    Configurator class for S3 store configuration and credentials management.
    """

    def __init__(self):
        self._validate()

    ##############################
    # Configuration methods
    ##############################

    def get_client_config(self) -> dict:
        """
        Gets S3 credentials (access key, secret key, session token, and other config).

        Parameters
        ----------
        creds : dict
            The credentials dictionary.

        Returns
        -------
        dict
            A dictionary containing the S3 credentials.
        """
        creds = configurator.get_config_creds()
        return {
            "endpoint_url": creds[ConfigurationVars.S3_ENDPOINT_URL.value],
            "aws_access_key_id": creds[CredentialsVars.S3_ACCESS_KEY_ID.value],
            "aws_secret_access_key": creds[CredentialsVars.S3_SECRET_ACCESS_KEY.value],
            "aws_session_token": creds[CredentialsVars.S3_SESSION_TOKEN.value],
            "config": Config(
                region_name=creds[ConfigurationVars.S3_REGION.value],
                signature_version=creds[ConfigurationVars.S3_SIGNATURE_VERSION.value],
            ),
        }

    def _validate(self) -> None:
        """
        Validate if all required keys are present in the configuration.
        """
        required_keys = [
            ConfigurationVars.S3_ENDPOINT_URL.value,
            CredentialsVars.S3_ACCESS_KEY_ID.value,
            CredentialsVars.S3_SECRET_ACCESS_KEY.value,
        ]
        current_keys = configurator.get_config_creds()
        missing_keys = []
        for key in required_keys:
            if key not in current_keys or current_keys[key] is None:
                missing_keys.append(key)
        if missing_keys:
            raise ValueError(f"Missing required variables for S3 store: {', '.join(missing_keys)}")

    def eval_retry(self) -> bool:
        """
        Evaluate the status of retry lifecycle.

        Returns
        -------
        bool
            True if a retry action was performed, otherwise False.
        """
        return configurator.eval_retry()
