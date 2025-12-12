# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.stores.configurator.configurator import configurator


def set_current_profile(profile: str) -> None:
    """
    Set the current credentials profile.

    Parameters
    ----------
    profile : str
        Name of the credentials profile to set.
    """
    configurator.set_current_profile(profile)


def get_current_profile() -> str:
    """
    Get the name of the current credentials profile.

    Returns
    -------
    str
        Name of the current credentials profile.
    """
    return configurator.get_current_profile()
