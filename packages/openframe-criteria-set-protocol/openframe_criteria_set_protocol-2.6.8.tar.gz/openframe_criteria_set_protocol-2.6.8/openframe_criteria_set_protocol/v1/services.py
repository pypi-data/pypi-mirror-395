from abc import ABC, abstractmethod
from typing import Optional, Generic
from typing import TypeVar

from .errors import CriteriaSetIdNotFoundError, CriteriaSetVersionNotFoundError
from .types import CriteriaTree, Metadata, TaskItemValueMap, StreamMatrixResponse, DataMap

ParametersType = TypeVar("ParametersType", bound=dict)


# A class representing a specific version of a specific criteria set
class ICriteriaSetService(ABC, Generic[ParametersType]):
    # ID of the criteria set
    id: str

    # Specific version of the criteria set this class represents, SemVer-formatted
    version: str

    # Validate the given parameters
    @abstractmethod
    def validate_parameters(self, parameters: ParametersType):
        pass

    # Get the metadata for this criteria set version
    @abstractmethod
    def get_metadata(self) -> Metadata:
        pass

    # Get the metadata for this criteria set version
    @abstractmethod
    def get_data_map(
            self,
            parameters: Optional[ParametersType] = None,
            values: Optional[TaskItemValueMap] = None
    ) -> DataMap:
        pass

    # Get the criteria tree for the given parameters
    @abstractmethod
    def get_criteria_tree(
            self,
            parameters: Optional[ParametersType] = None,
            values: Optional[TaskItemValueMap] = None
    ) -> CriteriaTree:
        pass

    # Stream the matrix for the given parameters
    @abstractmethod
    def stream_matrix(
            self,
            parameters: Optional[ParametersType] = None,
            values: Optional[TaskItemValueMap] = None,
            additional: Optional[any] = None
    ) -> StreamMatrixResponse:
        pass


class ManagerService:
    criteria_set_services: dict[str, list[ICriteriaSetService]]

    def __init__(self, criteria_set_services: Optional[dict[str, list[ICriteriaSetService]]] = None):
        self.criteria_set_services = criteria_set_services if criteria_set_services is not None else dict()

    # Get the criteria sets and versions available to this service
    def get_criteria_sets_and_versions(self) -> dict[str, list[Metadata]]:
        criteria_sets_and_versions = dict()
        for criteria_set_id, services in self.criteria_set_services.items():
            criteria_sets_and_versions[criteria_set_id] = [service.get_metadata() for service in services]
        return criteria_sets_and_versions

    # Get the criteria set with the given ID. If no version is requested, return the latest version
    def get_service_for_criteria_set(self, criteria_set_id: str, version: Optional[str] = None) -> ICriteriaSetService:
        if criteria_set_id not in self.criteria_set_services:
            raise CriteriaSetIdNotFoundError()

        services_for_criteria_set_id = self.criteria_set_services[criteria_set_id]
        if version is None:
            if len(services_for_criteria_set_id):
                return services_for_criteria_set_id[-1]
            raise CriteriaSetIdNotFoundError()

        for service in services_for_criteria_set_id:
            if service.version == version:
                return service
        raise CriteriaSetVersionNotFoundError()
