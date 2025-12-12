# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.context.builder import context_builder
from digitalhub.entities._commons.enums import EntityTypes
from digitalhub.factory.entity import entity_factory
from digitalhub.stores.client.builder import get_client
from digitalhub.stores.client.enums import ApiCategories, BackendOperations
from digitalhub.utils.exceptions import ContextError, EntityNotExistsError

if typing.TYPE_CHECKING:
    from digitalhub.context.context import Context
    from digitalhub.entities.project._base.entity import Project


def build_context(project: Project, overwrite: bool = False) -> Context:
    """
    Build a new context for a project.

    Creates or updates a context instance for the given project
    in the global context registry.

    Parameters
    ----------
    project : Project
        The project object used to build the context.
    overwrite : bool
        If True, overwrites existing context if it exists. Default is False.

    Returns
    -------
    Context
        The newly created or existing context instance.
    """
    return context_builder.build(project, overwrite)


def get_context(project: str) -> Context:
    """
    Get the context for a given project name.

    Parameters
    ----------
    project : str
        Project name.

    Returns
    -------
    Context
        The context for the given project name.
    """
    try:
        return context_builder.get(project)
    except ContextError:
        try:
            return get_context_from_remote(project)
        except EntityNotExistsError as e:
            raise ContextError(f"Context '{project}' not found remotely nor locally.") from e


def get_context_from_remote(project: str) -> Context:
    """
    Fetch project context from remote backend and create local context.


    Parameters
    ----------
    project : str
        The name of the project to fetch from remote.

    Returns
    -------
    Context
        The context instance created from the remote project data.
    """
    try:
        client = get_client()
        api = client.build_api(
            ApiCategories.BASE.value,
            BackendOperations.READ.value,
            entity_type=EntityTypes.PROJECT.value,
            entity_name=project,
        )
        obj = client.read_object(api)
        entity_factory.build_entity_from_dict(obj)
        return context_builder.get(project)
    except EntityNotExistsError:
        raise ContextError(f"Project '{project}' not found.")


def delete_context(project: str) -> None:
    """
    Delete the context for a given project name.

    Parameters
    ----------
    project : str
        Project name.
    """
    context_builder.remove(project)
