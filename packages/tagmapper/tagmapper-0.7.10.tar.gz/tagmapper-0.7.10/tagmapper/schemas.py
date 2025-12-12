from typing import List
import yaml
from tagmapper.connector_api import get_api_client
from tagmapper.generic_model import ModelTemplate


class Schema:
    """A class containing metadata for a schema. And methods to get the complete yaml."""

    def __init__(self, file_name, owner, name, description, version):
        self.file_name = file_name
        self.owner = owner
        self.name = name
        self.description = description
        self.version = version

    def __repr__(self):
        return f"Schemas(filename='{self.file_name}', owner='{self.owner}', name='{self.name}', description='{self.description}', version={self.version})"

    def to_dict(self) -> dict:
        """Convert the object to a dictionary."""
        return {
            "file_name": self.file_name,
            "owner": self.owner,
            "name": self.name,
            "description": self.description,
            "version": self.version,
        }

    def get_yaml(self):
        """
        Get the YAML file for the schema
        """

        if len(self.file_name) == 0:
            # Assume self-service schema
            try:
                url = f"/get-schema?Model_Owner={self.owner}&Model_Name={self.name}"
                data = get_api_client().get_json(url)
                if isinstance(data, dict) and "data" in data.keys():
                    data = data["data"]
                    if isinstance(data, list):
                        data = data[0]

                    file_name = data["filename"]
                    url = f"/download-schema?filename={file_name}"
            except:
                raise ValueError("Schema not found for the given owner and name.")
        else:
            url = f"/download-spd-schema?filename={self.file_name}"
        return yaml.safe_load(get_api_client().get_file(url, "", stream=True))

    def get_ModelTemplate(self):
        """
        Get the ModelTemplate for the schema
        """
        return ModelTemplate(self.get_yaml())

    @staticmethod
    def from_dict(data) -> "Schema":
        """Create an instance from a dictionary."""

        if "filename" not in data.keys():
            data["filename"] = ""
        if "description" not in data.keys():
            data["description"] = ""
        if "version" not in data.keys():
            data["version"] = 0
        if "owner" not in data.keys():
            data["owner"] = data["model_owner"]

        if "name" not in data.keys():
            data["name"] = data["model_name"]

        return Schema(
            file_name=data["filename"],
            owner=data["owner"],
            name=data["name"],
            description=data["description"],
            version=data["version"],
        )

    @staticmethod
    def get_self_service_schemas() -> List["Schema"]:
        """
        Get existing self-service schemas from the API.
        """

        url = "/get-schema-details"
        response = get_api_client().get_json(url)

        if isinstance(response, dict):
            if "data" in response.keys():
                return [Schema.from_dict(item) for item in response["data"]]
            elif "schemas" in response.keys():
                return [Schema.from_dict(item) for item in response["schemas"]]
        raise ValueError("Response is not a valid JSON object")

    @staticmethod
    def download_schema(file_name: str, model_owner: str, model_name: str):
        """Download the yaml file for a self-service schema from the given URL and save it to current working directory."""
        url = f"/download-schema?Model_Owner={model_owner}&Model_Name={model_name}"
        get_api_client().get_file(url, file_name, stream=True)

    @staticmethod
    def get_SPD_schemas() -> List["Schema"]:
        """
        Get existing SPD-schemas from the API.
        """

        url = "/get-spd-schema"
        response = get_api_client().get_json(url)

        if isinstance(response, dict):
            if "data" in response.keys():
                return [Schema.from_dict(item) for item in response["data"]]
        raise ValueError("Response is not a valid JSON object")

    @staticmethod
    def download_SPD_schema(file_name: str):
        """Download the yaml file for a SPD-schema from the given URL and save it to current working directory."""
        url = f"/download-spd-schema?filename={file_name}"
        get_api_client().get_file(url, file_name, stream=True)
