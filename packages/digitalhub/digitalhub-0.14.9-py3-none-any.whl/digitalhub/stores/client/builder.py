# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.stores.client.client import Client


class ClientBuilder:
    """
    Client builder class. Creates and returns client instance.
    """

    def __init__(self) -> None:
        self._client: Client = None

    def build(self) -> Client:
        """
        Method to create a client instance.

        Returns
        -------
        Client
            Returns the client instance.
        """
        if self._client is None:
            self._client = Client()
        return self._client


client_builder = ClientBuilder()


def get_client() -> Client:
    """
    Wrapper around ClientBuilder.build.

    Returns
    -------
    Client
        The client instance.
    """
    return client_builder.build()
