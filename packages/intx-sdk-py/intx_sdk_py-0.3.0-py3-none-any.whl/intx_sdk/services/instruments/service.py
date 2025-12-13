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
from .get_aggregated_candles import GetAggregatedCandlesRequest, GetAggregatedCandlesResponse
from .get_daily_trading_volumes import GetDailyTradingVolumesRequest, GetDailyTradingVolumesResponse
from .get_historical_funding_rates import GetHistoricalFundingRatesRequest, GetHistoricalFundingRatesResponse
from .get_instrument_details import GetInstrumentDetailsRequest, GetInstrumentDetailsResponse
from .get_quote_per_instrument import GetQuotePerInstrumentRequest, GetQuotePerInstrumentResponse
from .list_instruments import ListInstrumentsRequest, ListInstrumentsResponse


class InstrumentsService:
    def __init__(self, client: Client):
        self.client = client

    def get_aggregated_candles(self, request: GetAggregatedCandlesRequest) -> GetAggregatedCandlesResponse:
        path = f"/instruments/{request.instrument}/candles"
        query_params = append_query_param("", 'granularity', request.granularity)
        query_params = append_query_param(query_params, 'start', request.start)
        query_params = append_query_param(query_params, 'end', request.end)
        response = self.client.request("GET", path, query=query_params, allowed_status_codes=request.allowed_status_codes)
        return GetAggregatedCandlesResponse(**response.json())

    def get_daily_trading_volumes(self, request: GetDailyTradingVolumesRequest) -> GetDailyTradingVolumesResponse:
        path = "/instruments/volumes/daily"
        query_params = append_pagination_params("", request.pagination)
        query_params = append_query_param(query_params, 'instruments', request.instruments)
        query_params = append_query_param(query_params, 'time_from', request.time_from)
        query_params = append_query_param(query_params, 'show_other', request.show_other)
        response = self.client.request("GET", path, query=query_params, allowed_status_codes=request.allowed_status_codes)
        return GetDailyTradingVolumesResponse(**response.json())

    def get_historical_funding_rates(self, request: GetHistoricalFundingRatesRequest) -> GetHistoricalFundingRatesResponse:
        path = f"/instruments/{request.instrument}/funding"
        query_params = append_pagination_params("", request.pagination)
        response = self.client.request("GET", path, query=query_params, allowed_status_codes=request.allowed_status_codes)
        return GetHistoricalFundingRatesResponse(**response.json())

    def get_instrument_details(self, request: GetInstrumentDetailsRequest) -> GetInstrumentDetailsResponse:
        path = f"/instruments/{request.instrument}"
        response = self.client.request("GET", path, allowed_status_codes=request.allowed_status_codes)
        return GetInstrumentDetailsResponse(**response.json())

    def get_quote_per_instrument(self, request: GetQuotePerInstrumentRequest) -> GetQuotePerInstrumentResponse:
        path = f"/instruments/{request.instrument}/quote"
        response = self.client.request("GET", path, allowed_status_codes=request.allowed_status_codes)
        return GetQuotePerInstrumentResponse(**response.json())

    def list_instruments(self, request: ListInstrumentsRequest) -> ListInstrumentsResponse:
        path = "/instruments"
        response = self.client.request("GET", path, allowed_status_codes=request.allowed_status_codes)
        return ListInstrumentsResponse(instruments=response.json())
