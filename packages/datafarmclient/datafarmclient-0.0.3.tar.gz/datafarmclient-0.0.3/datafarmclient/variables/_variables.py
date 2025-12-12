import base64
import logging
import os
from typing import Any, Optional, Union

import requests

from datafarmclient.base import DatafarmClient
from datafarmclient.exceptions import VariableNotFoundError
from datafarmclient.utils import ensure_auth, format_datetime


class Variables:
    """A Variables subclass for the base class."""

    def __init__(self, client: DatafarmClient):
        """
        Args:
            client: The base client allowing the subclass to use
                the shared session and client methods.
        """
        self._client = client

    def __setitem__(self, key, value):
        return self._set_variable(name=key, value=value)

    def __getitem__(self, key):
        return self._get_variable(name=key)

    @ensure_auth
    def get_object_variable(
        self,
        name: str,
        output_dir: Optional[str] = None,
        output_path: Optional[str] = None,
    ) -> Union[str, bytes]:
        """Get an object variable.

        Args:
            name: The name of the variable.
            output_dir: The directory to save the object to.
                The file name will be read from the system.
                Defaults to None.
            output_path: The path to save the object to.
                Defaults to None.

        Returns:
            If neither `output_dir` nor `output_path` are specified,
            the object is returned as bytes.
            Otherwise, the object is saved to the specified path.

        Raises:
            HttpError: Requests threw an exception.
            VariableNotFoundError: If specificed variable doesn't exists.
            ValueError: If variable is not an object.
        """
        body = {"Name": name}
        endpoint = "/Variables/GetValue"
        url = self._client.api_url + endpoint
        response = self._client.session.post(url, json=body)
        response.raise_for_status()
        response_body = response.json()
        if "VariableType" not in response_body:
            raise VariableNotFoundError("Variable does not exist")
        variable_type = response_body["VariableType"]
        if variable_type != "vtObject":
            raise ValueError("Variable is not an object")
        base64_data = response_body["ObjectBase64"]

        if output_dir is None and output_path is None:
            return base64.b64decode(base64_data)
        else:
            output_path = output_path or os.path.join(
                output_dir, response_body["ObjectFileName"]
            )
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(base64_data))
            return output_path

    @ensure_auth
    def set_object_variable(self, name: str, file_path: str) -> requests.Response:
        """Set an object in the session.

        Args:
            name: The name of the object.
            file_path: The file path of the object.

        Returns:
            Response from the API.

        Raises:
            HttpError: Requests threw an exception.
        """
        object_file_name = os.path.basename(file_path)
        object_base64 = base64.b64encode(open(file_path, "rb").read()).decode("utf-8")
        body = {
            "Name": name,
            "ObjectBase64": object_base64,
            "ObjectFileName": object_file_name,
            "VariableType": "vtObject",
        }
        endpoint = "/Variables/SetValue"
        url = self._client.api_url + endpoint
        response = self._client.session.post(url, json=body)
        response.raise_for_status()
        return response

    @ensure_auth
    def create_category(self, name: str) -> str:
        """Create a new variable category.

        Args:
            name: The name of the category.

        Returns:
            Id of the newly created variable category.

        Raises:
            EntityExistsError: The entity already exists in the system.
            HttpError: Requests threw an exception.
        """
        return self._client.entities("enGlobalVariableCategory").create(id_name=name)

    @ensure_auth
    def create_type(self, name: str) -> str:
        """Create a new variable type.

        Args:
            name: The name of the type.

        Returns:
            Id of the newly created variable type.

        Raises:
            EntityExistsError: The entity already exists in the system.
            HttpError: Requests threw an exception.
        """
        return self._client.entities("enGlobalVariableType").create(id_name=name)

    @ensure_auth
    def delete_category(self, name: str) -> requests.Response:
        """Delete a variable category

        Args:
            name: The name of the category.

        Returns:
            Response from the API.

        Raises:
            HttpError: Requests threw an exception
        """
        entity_id = self._client.entities("enGlobalVariableCategory").get(id_name=name)
        return self._client.entities("enGlobalVariableCategory").delete(
            entity_id=entity_id
        )

    @ensure_auth
    def delete_type(self, name: str) -> requests.Response:
        """Delete a variable type

        Args:
            name: The name of the type.

        Returns:
            Response from the API.

        Raises:
            HttpError: Requests threw an exception
        """
        entity_id = self._client.entities("enGlobalVariableType").get(id_name=name)
        return self._client.entities("enGlobalVariableType").delete(entity_id=entity_id)

    @ensure_auth
    def _get_variable(self, name: str) -> Any:
        body = {"Name": name}
        endpoint = "/Variables/GetValue"
        url = self._client.api_url + endpoint
        try:
            response = self._client.session.post(url, json=body)
            response.raise_for_status()
            response_body = response.json()
        except requests.HTTPError as err:
            logging.error(response.json()["error"])
            raise err
        else:
            if "VariableType" not in response_body:
                raise VariableNotFoundError("Variable does not exist")
            variable_type = response_body["VariableType"]
            if variable_type == "vtObject":
                base64_data = response_body["ObjectBase64"]
                return base64.b64decode(base64_data).decode("utf-8")
            return response_body["Value"]

    @ensure_auth
    def _set_variable(
        self,
        name: str,
        value: Optional[Any] = None,
    ):
        """Set a variable in Datafarm.

        Args:
        ----------
        name : str
            The name of the variable.
        value : Any
            The value of the variable.
        """

        if value is None:
            raise ValueError("`value` or `file_path` must be provided")

        variable_type = type(value).__name__

        VARIABLE_TYPE_MAP = {
            "bool": "Boolean",
            "datetime": "DateTime",
            "float": "Double",
            "int": "Integer",
            "str": "String",
        }
        try:
            value_type_name = VARIABLE_TYPE_MAP[variable_type]
        except KeyError:
            raise ValueError(
                f"Invalid variable type {variable_type!r}. "
                f"Must be one of {list(VARIABLE_TYPE_MAP.keys())}."
            )

        if variable_type == "datetime":
            value = format_datetime(value)

        body = {
            f"as{value_type_name}": value,
            "Name": name,
            "VariableType": f"vt{value_type_name}",
        }
        endpoint = "/Variables/SetValue"
        url = self._client.api_url + endpoint
        response = self._client.session.post(url, json=body)
        response.raise_for_status()
        return response
