# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.context.api import get_context
from digitalhub.entities._commons.utils import get_project_from_key, is_valid_key, parse_entity_key
from digitalhub.utils.exceptions import EntityError

if typing.TYPE_CHECKING:
    from digitalhub.context.context import Context


def parse_identifier(
    identifier: str,
    project: str | None = None,
    entity_type: str | None = None,
    entity_kind: str | None = None,
    entity_id: str | None = None,
) -> tuple[str, str, str | None, str | None, str | None]:
    """
    Parse and validate entity identifier into its components.

    Processes an entity identifier that can be either a full entity key
    (store://) or a simple entity name. When using a simple name,
    additional parameters must be provided for proper identification.

    Parameters
    ----------
    identifier : str
        The entity identifier to parse. Can be either a full entity key
        (store://project/entity_type/kind/name:id) or a simple entity name.
    project : str
        The project name. Required when identifier is not a full key.
    entity_type : str
        The entity type. Required when identifier is not a full key.
    entity_kind : str
        The entity kind specification.
    entity_id : str
        The entity version identifier.

    Returns
    -------
    tuple[str, str, str | None, str | None, str | None]
        A tuple containing (project_name, entity_type, entity_kind,
        entity_name, entity_id) parsed from the identifier.

    Raises
    ------
    ValueError
        If identifier is not a full key and project or entity_type is None.
    """
    if not is_valid_key(identifier):
        if project is None or entity_type is None:
            raise ValueError("Project and entity type must be specified.")
        return project, entity_type, entity_kind, identifier, entity_id
    return parse_entity_key(identifier)


def get_context_from_identifier(
    identifier: str,
    project: str | None = None,
) -> Context:
    """
    Retrieve context instance from entity identifier or project name.

    Extracts project information from the identifier and returns the
    corresponding context. If the identifier is not a full key, the
    project parameter must be provided explicitly.

    Parameters
    ----------
    identifier : str
        The entity identifier to extract context from. Can be either
        a full entity key (store://...) or a simple entity name.
    project : str
        The project name. Required when identifier is not a full key.

    Returns
    -------
    Context
        The context instance associated with the identified project.

    Raises
    ------
    EntityError
        If identifier is not a full key and project parameter is None.
    """
    if not is_valid_key(identifier):
        if project is None:
            raise EntityError("Specify project if you do not specify entity key.")
    else:
        project = get_project_from_key(identifier)

    return get_context(project)
