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
from intx_sdk.utils import append_query_param, append_pagination_params
from .get_index_candles import GetIndexCandlesRequest, GetIndexCandlesResponse
from .get_index_composition import GetIndexCompositionRequest, GetIndexCompositionResponse
from .get_index_composition_history import GetIndexCompositionHistoryRequest, GetIndexCompositionHistoryResponse
from .get_index_price import GetIndexPriceRequest, GetIndexPriceResponse


class IndexService:
    def __init__(self, client: Client):
        self.client = client

    def get_index_candles(self, request: GetIndexCandlesRequest) -> GetIndexCandlesResponse:
        path = f"/index/{request.index}/candles"
        query_params = append_query_param("", 'granularity', request.granularity)
        query_params = append_query_param(query_params, 'start', request.start)
        if request.end:
            query_params = append_query_param(query_params, 'end', request.end)
        response = self.client.request("GET", path, query=query_params, allowed_status_codes=request.allowed_status_codes)
        return GetIndexCandlesResponse(aggregations=response.json())

    def get_index_composition(self, request: GetIndexCompositionRequest) -> GetIndexCompositionResponse:
        path = f"/index/{request.index}/composition"
        response = self.client.request("GET", path, allowed_status_codes=request.allowed_status_codes)
        return GetIndexCompositionResponse(composition=response.json())

    def get_index_composition_history(self, request: GetIndexCompositionHistoryRequest) -> GetIndexCompositionHistoryResponse:
        path = f"/index/{request.index}/composition-history"
        query_params = append_query_param("", 'time_from', request.time_from)
        query_params = append_pagination_params(query_params, request.pagination)
        response = self.client.request("GET", path, query=query_params, allowed_status_codes=request.allowed_status_codes)
        return GetIndexCompositionHistoryResponse(compositions=response.json())

    def get_index_price(self, request: GetIndexPriceRequest) -> GetIndexPriceResponse:
        path = f"/index/{request.index}/price"
        response = self.client.request("GET", path, allowed_status_codes=request.allowed_status_codes)
        return GetIndexPriceResponse(price=response.json())
