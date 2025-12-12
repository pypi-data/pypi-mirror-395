import json
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import requests

from datafarmclient.base import DatafarmClient
from datafarmclient.exceptions import (
    EntityExistsError,
    EntityNotFoundError,
)
from datafarmclient.schemas import EntityType
from datafarmclient.utils import (
    ensure_auth,
    json_to_pandas,
)


class Entities:
    """A Entitites subclass for the base class."""

    def __init__(self, class_id: EntityType, client: DatafarmClient):
        """Entities need to be instantiated with an entitytype.

        Args:
            class_id: Entitytype specifying which entity to work with
            client: The base client allowing the subclass to use
                the shared session and client methods.
        """
        self._client = client
        self.class_id = class_id

    @ensure_auth
    def create(self, id_name: str, fields: Optional[Dict[str, str]] = None) -> str:
        """Create an entity.

        Args:
            id_name: The ID name of the new entity.
            fields: The fields of the new entity.

        Returns:
            Id of the newly created entity

        Raises:
            EntityExistsError: The entity already exists in the system
            HttpError: Requests threw an exception
        """
        field_names, field_values = self._get_field_names_and_values(fields)

        body = {
            "ClassID": self.class_id,
            "IDName": id_name,
            "FieldNames": field_names,
            "FieldValues": field_values,
        }
        url = self._client.api_url + "/Entities/Create"
        response = self._client.session.post(url, json=body)
        try:
            response.raise_for_status()
        except requests.HTTPError as err:
            if err.response.status_code == 409:
                raise EntityExistsError(
                    f"Entity with ID {id_name!r} already exists in class {self.class_id!r}."
                )
            else:
                raise
        return response.json()["EntityID"]

    @ensure_auth
    def exists(self, id_name: str, fields: Optional[Dict[str, str]] = None) -> bool:
        """Check if an entity exists or not

        Args:
            id_name: The ID name of the entity.
            fields: The fields of the entity.

        Returns:
            A boolean result based on whether or not an entity
            with that ID name already exists

        Raises:
            HttpError: Requests threw an exception
        """
        field_names, field_values = self._get_field_names_and_values(fields)
        body = {
            "ClassID": self.class_id,
            "IDName": id_name,
            "FieldNames": field_names,
            "FieldValues": field_values,
        }
        url = self._client.api_url + "/Entities/Exists"
        response = self._client.session.post(url, json=body)
        response.raise_for_status()
        if "EntityID" not in response.json():
            return False
        return True

    @ensure_auth
    def get(
        self,
        id_name: str,
    ) -> str:
        """Get the ID of an entity.

        Args:
            id_name: The ID name of the entity.

        Returns:
            The id of the entity

        Raises:
            HttpError: Requests threw an exception
        """

        body = {
            "ClassID": self.class_id,
            "IDName": id_name,
        }
        url = self._client.api_url + "/Entities/Exists"
        response = self._client.session.post(url, json=body)
        response.raise_for_status()
        if "EntityID" not in response.json():
            raise EntityNotFoundError("Entity does not exist")
        return response.json()["EntityID"]

    @ensure_auth
    def update(
        self,
        entity_id: str,
        fields: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        """Update an entity.

        Args:
            entity_id: The ID of the entity.
            fields: The fields to update of the entity.

        Returns:
            Response from the API.

        Raises:
            HttpError: Requests threw an exception
        """
        field_names, field_values = self._get_field_names_and_values(fields)

        body = {
            "ClassID": self.class_id,
            "EntityID": entity_id,
            "FieldNames": field_names,
            "FieldValues": field_values,
        }
        url = self._client.api_url + "/Entities/Update"
        response = self._client.session.post(url, json=body)
        try:
            response.raise_for_status()
        except requests.HTTPError as err:
            if err.response.status_code == 404:
                raise EntityNotFoundError(
                    f"Entity with ID {entity_id!r} not found in class {self.class_id!r}."
                )
            else:
                raise
        return response.json()

    @ensure_auth
    def delete(self, entity_id: str) -> requests.Response:
        """Delete an entity.

        Args:
            entity_id: The ID of the entity to delete.

        Returns:
            Response from the API.

        Raises:
            HttpError: Requests threw an exception
        """

        body = {"ClassID": self.class_id, "EntityID": entity_id}
        url = self._client.api_url + "/Entities/Delete"
        response = self._client.session.post(url, json=body)
        response.raise_for_status()
        return response

    @ensure_auth
    def metadata(self) -> pd.DataFrame:
        """Get the metadata of an EntityType.

        Returns:
            Pandas DataFrame containing the results

        Raises:
            HttpError: Requests threw an exception
        """

        body = {"ClassID": self.class_id}
        url = f"{self._client.api_url}/Entities/MetaData"
        response = self._client.session.post(url, json=body)
        response.raise_for_status()

        return json_to_pandas(json.dumps(response.json()))

    @ensure_auth
    def list(self, fields: Optional[List[str]] = None) -> pd.DataFrame:
        """List all entities of the chosen type.

        Returns:
            Pandas DataFrame containing the results

        Raises:
            HttpError: Requests threw an exception
        """
        url = self._client.api_url + "/Entities/List"
        body = {
            "ClassID": self.class_id,
            "Fields": [] if not fields else fields,
        }
        response = self._client.session.post(url, json=body)
        response.raise_for_status()
        data = response.json()

        return json_to_pandas(json.dumps(data))

    # TODO Metadata attribute / cached property
    def _get_field_names_and_values(
        self, fields: Optional[Dict[str, Any]] = None
    ) -> Tuple[List[str], List[Any]]:
        """Converts a dictionary to two lists, one with keys and one with values."""
        if fields is None:
            return [], []
        return list(fields.keys()), list(fields.values())
