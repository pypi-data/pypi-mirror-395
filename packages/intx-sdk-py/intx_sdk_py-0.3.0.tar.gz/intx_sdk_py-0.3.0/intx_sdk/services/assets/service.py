# Copyright 2025-present Coinbase Global, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from intx_sdk.client import Client
from intx_sdk.services.model import Asset, SupportedNetwork
from .list_assets import ListAssetsRequest, ListAssetsResponse
from .get_asset_details import GetAssetDetailsRequest, GetAssetDetailsResponse
from .get_supported_networks import GetSupportedNetworksRequest, GetSupportedNetworksResponse


class AssetsService:
    def __init__(self, client: Client):
        self.client = client

    def list_assets(self, request: ListAssetsRequest) -> ListAssetsResponse:
        path = "/assets"
        response = self.client.request("GET", path, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return ListAssetsResponse(assets=[Asset(**a) for a in data])

    def get_asset_details(self, request: GetAssetDetailsRequest) -> GetAssetDetailsResponse:
        path = f"/assets/{request.asset}"
        response = self.client.request("GET", path, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return GetAssetDetailsResponse(asset=Asset(**data))

    def get_supported_networks(self, request: GetSupportedNetworksRequest) -> GetSupportedNetworksResponse:
        path = f"/assets/{request.asset}/networks"
        response = self.client.request("GET", path, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return GetSupportedNetworksResponse(networks=[SupportedNetwork(**n) for n in data])
