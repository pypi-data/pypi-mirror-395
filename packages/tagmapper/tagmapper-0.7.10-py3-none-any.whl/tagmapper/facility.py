from typing import List

from tagmapper.connector_api import get_api_client


class Facility:
    _facilities = []

    def __init__(self, data) -> None:
        self.gov_fcty_name = data.get("gov_fcty_name", "")
        self.ioc_plant = data.get("ioc_plant", "")
        pass

    def __str__(self) -> str:
        return f"Facility: {self.gov_fcty_name} / {self.ioc_plant}"

    @classmethod
    def get_facility_by_name(cls, name: str) -> "Facility":
        """
        Get facility by name
        """

        name = name.casefold()

        facilities = cls.get_all_facilities()
        for f in facilities:
            if f.gov_fcty_name.casefold() == name or f.ioc_plant.casefold() == name:
                return f
        raise ValueError(f"Facility with name {name} not found")

    @classmethod
    def get_all_facilities(cls) -> List["Facility"]:
        """
        Get all facilities
        """

        if len(cls._facilities) == 0:
            data = get_api_client().get_json(
                "/facility-master", {"limit": 100, "offset": 0}
            )
            if isinstance(data, dict) and "data" in data.keys():
                facilities = []
                for f in data["data"]:
                    facilities.append(Facility(f))
            cls._facilities = facilities

        return cls._facilities
