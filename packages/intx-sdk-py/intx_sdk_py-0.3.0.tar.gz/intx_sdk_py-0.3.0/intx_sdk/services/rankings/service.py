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
from intx_sdk.utils import append_query_param
from .get_rankings import GetRankingsRequest, GetRankingsResponse


class RankingsService:
    def __init__(self, client: Client):
        self.client = client

    def get_rankings(self, request: GetRankingsRequest) -> GetRankingsResponse:
        path = "/rankings/statistics"
        query_params = ""
        if request.instrument_type:
            query_params = append_query_param(query_params, 'instrument_type', request.instrument_type)
        if request.period:
            query_params = append_query_param(query_params, 'period', request.period)
        if request.instruments:
            query_params = append_query_param(query_params, 'instruments', request.instruments)
        response = self.client.request("GET", path, query=query_params, allowed_status_codes=request.allowed_status_codes)
        return GetRankingsResponse(rankings=response.json())
