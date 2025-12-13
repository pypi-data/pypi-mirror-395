from ..clients.imx import (
    ApiClient,
    Configuration,
    ConnectionServiceApi,
    DataSourceServiceApi,
    DataTargetServiceApi,
    ExportServiceApi,
)
from .common import BaseElevateClient, BaseElevateService


class ImxClient(BaseElevateClient, ApiClient):
    _route = "/api/imx"
    _conf_class = Configuration


class ConnectionService(BaseElevateService, ConnectionServiceApi):
    _client_class = ImxClient


class DataSourceService(BaseElevateService, DataSourceServiceApi):
    _client_class = ImxClient


class DataTargetService(BaseElevateService, DataTargetServiceApi):
    _client_class = ImxClient


class ExportService(BaseElevateService, ExportServiceApi):
    _client_class = ImxClient
