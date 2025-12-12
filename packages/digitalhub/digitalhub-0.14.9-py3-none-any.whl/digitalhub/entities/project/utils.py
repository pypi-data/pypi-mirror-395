# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing
from pathlib import Path

from digitalhub.utils.generic_utils import import_function

if typing.TYPE_CHECKING:
    from digitalhub.entities.project._base.entity import Project

CHECK_FILENAME = ".CHECK"
SETUP_MODULE = "setup_project.py"
SETUP_FUNCTION = "setup"


def setup_project(project: Project, setup_kwargs: dict | None = None) -> Project:
    """
    Search for setup_project.py file and launch setup hanlder as project hook.

    Parameters
    ----------
    project : Project
        The project to scafold.
    setup_kwargs : dict
        Arguments to pass to setup handler.

    Returns
    -------
    Project
        Set up project.
    """
    setup_kwargs = setup_kwargs if setup_kwargs is not None else {}
    check_pth = Path(project.spec.source, CHECK_FILENAME)
    setup_pth = Path(project.spec.source, SETUP_MODULE)
    if setup_pth.exists() and not check_pth.exists():
        setup_fnc = import_function(setup_pth, SETUP_FUNCTION)
        project = setup_fnc(project, **setup_kwargs)
        check_pth.touch()
    return project
