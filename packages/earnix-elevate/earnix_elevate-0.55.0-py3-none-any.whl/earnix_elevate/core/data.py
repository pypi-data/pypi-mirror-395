from ..clients.data import (
    ApiClient,
    Configuration,
    DatasetServiceApi,
    DataTableServiceApi,
    ExportJobServiceApi,
)
from .common import BaseElevateClient, BaseElevateService


class DataClient(BaseElevateClient, ApiClient):
    _route = "/api/data"
    _conf_class = Configuration


class DataTableService(BaseElevateService, DataTableServiceApi):
    _client_class = DataClient


class DatasetService(BaseElevateService, DatasetServiceApi):
    _client_class = DataClient


class ExportJobService(BaseElevateService, ExportJobServiceApi):
    _client_class = DataClient
