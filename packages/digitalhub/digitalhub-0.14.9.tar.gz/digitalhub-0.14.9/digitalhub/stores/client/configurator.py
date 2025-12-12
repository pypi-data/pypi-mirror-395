# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing
from warnings import warn

from requests import request

from digitalhub.stores.client.enums import AuthType
from digitalhub.stores.configurator.configurator import configurator
from digitalhub.stores.configurator.enums import ConfigurationVars, CredentialsVars
from digitalhub.utils.exceptions import ClientError
from digitalhub.utils.generic_utils import list_enum
from digitalhub.utils.uri_utils import has_remote_scheme

if typing.TYPE_CHECKING:
    from requests import Response


DEFAULT_TIMEOUT = 60


class ClientConfigurator:
    """
    DHCore client configurator for credential management and authentication.

    Handles loading credentials from environment variables and configuration files,
    evaluates authentication types, and manages token refresh operations. Supports
    multiple authentication methods: EXCHANGE (personal access token), OAUTH2
    (access + refresh tokens), ACCESS_TOKEN (access token only), and BASIC
    (username + password).

    The configurator automatically determines the best authentication method and
    handles token exchange for personal access tokens by switching to file-based
    credential storage.
    """

    keys = [*list_enum(ConfigurationVars), *list_enum(CredentialsVars)]

    def __init__(self) -> None:
        """
        Initialize DHCore configurator and evaluate authentication type.
        """
        self._validate()
        self._auth_type: str | None = None
        self.set_auth_type()

    ##############################
    # Credentials methods
    ##############################

    @staticmethod
    def _sanitize_endpoint(endpoint: str | None = None) -> str | None:
        """
        Validate and normalize endpoint URL.

        Ensures proper HTTP/HTTPS scheme, trims whitespace, and removes trailing slashes.

        Parameters
        ----------
        endpoint : str
            Endpoint URL to sanitize.

        Returns
        -------
        str or None
            Sanitized URL or None if input was None.

        Raises
        ------
        ClientError
            If endpoint lacks http:// or https:// scheme.
        """
        if endpoint is None:
            return
        if not has_remote_scheme(endpoint):
            raise ClientError("Invalid endpoint scheme. Must start with http:// or https://.")

        endpoint = endpoint.strip()
        return endpoint.removesuffix("/")

    def get_endpoint(self) -> str:
        """
        Get the configured DHCore backend endpoint.

        Returns the sanitized and validated endpoint URL from current credential source.

        Returns
        -------
        str
            DHCore backend endpoint URL.

        Raises
        ------
        KeyError
            If endpoint not configured in current credential source.
        """
        config = configurator.get_configuration()
        endpoint = config[ConfigurationVars.DHCORE_ENDPOINT.value]
        return self._sanitize_endpoint(endpoint)

    ##############################
    # Auth methods
    ##############################

    def set_auth_type(self) -> None:
        """
        Determine authentication type from available credentials.

        Evaluates credentials in priority order: EXCHANGE (personal access token),
        OAUTH2 (access + refresh tokens), ACCESS_TOKEN (access only), BASIC
        (username + password). For EXCHANGE type, automatically exchanges the
        personal access token and switches to file-based credentials storage.
        """
        creds = configurator.get_credentials()
        self._auth_type = self._eval_auth_type(creds)
        # If we have an exchange token, we need to get a new access token.
        # Therefore, we change the origin to file, where the refresh token is written.
        # We also try to fetch the PAT from both env and file
        if self._auth_type == AuthType.EXCHANGE.value:
            self.refresh_credentials()

    def refreshable_auth_types(self) -> bool:
        """
        Check if current authentication supports token refresh.

        Returns True for OAUTH2 (refresh token) and EXCHANGE (personal access token),
        False for BASIC and ACCESS_TOKEN.

        Returns
        -------
        bool
            Whether authentication type supports refresh.
        """
        return self._auth_type in [AuthType.OAUTH2.value, AuthType.EXCHANGE.value]

    def get_auth_parameters(self, kwargs: dict) -> dict:
        """
        Add authentication headers/parameters to HTTP request kwargs.

        Adds Authorization Bearer header for token-based auth or auth tuple
        for basic authentication.

        Parameters
        ----------
        kwargs : dict
            HTTP request arguments to modify.

        Returns
        -------
        dict
            Modified kwargs with authentication parameters.
        """
        creds = configurator.get_credentials()
        if self._auth_type in (
            AuthType.EXCHANGE.value,
            AuthType.OAUTH2.value,
            AuthType.ACCESS_TOKEN.value,
        ):
            access_token = creds[CredentialsVars.DHCORE_ACCESS_TOKEN.value]
            if "headers" not in kwargs:
                kwargs["headers"] = {}
            kwargs["headers"]["Authorization"] = f"Bearer {access_token}"
        elif self._auth_type == AuthType.BASIC.value:
            user = creds[CredentialsVars.DHCORE_USER.value]
            password = creds[CredentialsVars.DHCORE_PASSWORD.value]
            kwargs["auth"] = (user, password)
        return kwargs

    def _evaluate_auth_flow(self, url: str, creds: dict) -> Response:
        """
        Evaluate the auth flow to execute.

        Parameters
        ----------
        url : str
            Token endpoint URL.
        creds : dict
            Available credential values.
        """
        if (client_id := creds.get(ConfigurationVars.DHCORE_CLIENT_ID.value)) is None:
            raise ClientError("Client id not set.")

        # Handling of token refresh
        if self._auth_type == AuthType.OAUTH2.value:
            return self._call_refresh_endpoint(
                url,
                client_id=client_id,
                refresh_token=creds.get(CredentialsVars.DHCORE_REFRESH_TOKEN.value),
                grant_type="refresh_token",
                scope="credentials",
            )

        ## Handling of token exchange
        return self._call_refresh_endpoint(
            url,
            client_id=client_id,
            subject_token=creds.get(CredentialsVars.DHCORE_PERSONAL_ACCESS_TOKEN.value),
            subject_token_type="urn:ietf:params:oauth:token-type:pat",
            grant_type="urn:ietf:params:oauth:grant-type:token-exchange",
            scope="credentials",
        )

    def refresh_credentials(self) -> None:
        """
        Refresh authentication tokens using OAuth2 flows.
        """
        if not self.refreshable_auth_types():
            raise ClientError(f"Auth type {self._auth_type} does not support refresh.")

        # Get credentials and configuration
        creds = configurator.get_config_creds()

        # Get token refresh from creds
        if (url := creds.get(ConfigurationVars.OAUTH2_TOKEN_ENDPOINT.value)) is None:
            url = self._get_refresh_endpoint()
        url = self._sanitize_endpoint(url)

        # Execute the appropriate auth flow
        response = self._evaluate_auth_flow(url, creds)

        # Raise an error if the response indicates failure
        response.raise_for_status()

        # Export new credentials to file
        self._export_new_creds(response.json())

        configurator.reload_credentials()

    def evaluate_refresh(self) -> bool:
        """
        Check if token refresh should be attempted.

        Returns
        -------
        bool
            True if token refresh is applicable, otherwise False.
        """
        try:
            self.refresh_credentials()
            return True
        except Exception:
            if not configurator.eval_retry():
                warn(
                    "Failed to refresh credentials after retry"
                    " (checked credentials from file and env)."
                    " Please check your credentials"
                    " and make sure they are up to date."
                    " (refresh tokens, password, etc.)."
                )
                return False
            return self.evaluate_refresh()

    def _get_refresh_endpoint(self) -> str:
        """
        Discover OAuth2 token endpoint from issuer well-known configuration.

        Queries /.well-known/openid-configuration to extract token_endpoint for
        credential refresh operations.

        Parameters
        ----------
        creds : dict
            Available credential values.

        Returns
        -------
        str
            Token endpoint URL for credential refresh.
        """
        config = configurator.get_configuration()

        # Get issuer endpoint
        if (endpoint_issuer := config.get(ConfigurationVars.DHCORE_ISSUER.value)) is None:
            raise ClientError("Issuer endpoint not set.")

        # Standard issuer endpoint path
        url = endpoint_issuer + "/.well-known/openid-configuration"
        url = self._sanitize_endpoint(url)

        # Call issuer to get refresh endpoint
        r = request("GET", url, timeout=60)
        r.raise_for_status()
        return r.json().get("token_endpoint")

    def _call_refresh_endpoint(
        self,
        url: str,
        **kwargs,
    ) -> Response:
        """
        Make OAuth2 token refresh request.

        Sends POST request with form-encoded payload using required OAuth2
        content type and 60-second timeout.

        Parameters
        ----------
        url : str
            Token endpoint URL.
        **kwargs : dict
            Token request parameters (grant_type, client_id, etc.).

        Returns
        -------
        Response
            Raw HTTP response for caller handling.
        """
        # Send request to get new access token
        payload = {**kwargs}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        return request(
            "POST",
            url,
            data=payload,
            headers=headers,
            timeout=DEFAULT_TIMEOUT,
        )

    def _eval_auth_type(self, creds: dict) -> str | None:
        """
        Determine authentication type from available credentials.

        Evaluates in priority order: EXCHANGE (personal access token), OAUTH2
        (access + refresh tokens), ACCESS_TOKEN (access only), BASIC (username + password).

        Parameters
        ----------
        creds : dict
            Available credential values.

        Returns
        -------
        str or None
            Authentication type from AuthType enum, or None if no valid credentials.
        """
        if creds[CredentialsVars.DHCORE_PERSONAL_ACCESS_TOKEN.value] is not None:
            return AuthType.EXCHANGE.value
        if (
            creds[CredentialsVars.DHCORE_ACCESS_TOKEN.value] is not None
            and creds[CredentialsVars.DHCORE_REFRESH_TOKEN.value] is not None
        ):
            return AuthType.OAUTH2.value
        if creds[CredentialsVars.DHCORE_ACCESS_TOKEN.value] is not None:
            return AuthType.ACCESS_TOKEN.value
        if (
            creds[CredentialsVars.DHCORE_USER.value] is not None
            and creds[CredentialsVars.DHCORE_PASSWORD.value] is not None
        ):
            return AuthType.BASIC.value
        return None

    def _export_new_creds(self, response: dict) -> None:
        """
        Save refreshed credentials and switch to file-based storage.

        Persists new tokens (access_token, refresh_token, etc.) to configuration
        file and switches credential origin to file storage.

        Parameters
        ----------
        response : dict
            OAuth2 token response with new credentials.
        """
        keys_to_prefix = [
            CredentialsVars.DHCORE_REFRESH_TOKEN.value,
            CredentialsVars.DHCORE_ACCESS_TOKEN.value,
            ConfigurationVars.DHCORE_CLIENT_ID.value,
            ConfigurationVars.DHCORE_ISSUER.value,
            ConfigurationVars.OAUTH2_TOKEN_ENDPOINT.value,
        ]
        for key in keys_to_prefix:
            if key == ConfigurationVars.OAUTH2_TOKEN_ENDPOINT.value:
                prefix = "oauth2_"
            else:
                prefix = "dhcore_"
            key = key.lower()
            if key.removeprefix(prefix) in response:
                response[key] = response.pop(key.removeprefix(prefix))
        configurator.write_file(response)

    def _validate(self) -> None:
        """
        Validate if all required keys are present in the configuration.
        """
        required_keys = [ConfigurationVars.DHCORE_ENDPOINT.value]
        current_keys = configurator.get_config_creds()
        for key in required_keys:
            if current_keys.get(key) is None:
                raise ClientError(f"Required configuration key '{key}' is missing.")

    ###############################
    # Utility methods
    ###############################

    def get_credentials_and_config(self) -> dict:
        """
        Get current authentication credentials and configuration.

        Returns
        -------
        dict
            Current authentication credentials and configuration.
        """
        return configurator.get_config_creds()
