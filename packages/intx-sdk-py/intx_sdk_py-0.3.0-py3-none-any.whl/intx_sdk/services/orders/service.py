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

from dataclasses import asdict
from intx_sdk.client import Client
from intx_sdk.utils import append_pagination_params, append_query_param
from .cancel_order import CancelOrderRequest, CancelOrderResponse
from .cancel_orders import CancelOrdersRequest, CancelOrdersResponse
from .create_order import CreateOrderRequest, CreateOrderResponse
from .get_order_details import GetOrderDetailsRequest, GetOrderDetailsResponse
from .list_open_orders import ListOpenOrdersRequest, ListOpenOrdersResponse
from .modify_open_order import ModifyOpenOrderRequest, ModifyOpenOrderResponse


class OrdersService:
    def __init__(self, client: Client):
        self.client = client

    def cancel_order(self, request: CancelOrderRequest) -> CancelOrderResponse:
        path = f"/orders/{request.id}"
        query = f"portfolio={request.portfolio}"
        response = self.client.request("DELETE", path, query=query, allowed_status_codes=request.allowed_status_codes)
        return CancelOrderResponse(**response.json())

    def cancel_orders(self, request: CancelOrdersRequest) -> CancelOrdersResponse:
        path = "/orders"
        query_params = append_query_param("", 'portfolio', request.portfolio)
        query_params = append_query_param(query_params, 'instrument', request.instrument)
        query_params = append_query_param(query_params, 'side', request.side)
        query_params = append_query_param(query_params, 'instrument_type', request.instrument_type)
        response = self.client.request("DELETE", path, query=query_params, allowed_status_codes=request.allowed_status_codes)
        return CancelOrdersResponse(orders=response.json())

    def create_order(self, request: CreateOrderRequest) -> CreateOrderResponse:
        path = "/orders"
        body = {k: v for k, v in asdict(request).items() if v is not None and k != 'allowed_status_codes'}
        response = self.client.request("POST", path, body=body, allowed_status_codes=request.allowed_status_codes)
        return CreateOrderResponse(**response.json())

    def get_order_details(self, request: GetOrderDetailsRequest) -> GetOrderDetailsResponse:
        path = f"/orders/{request.order_id}"
        query_params = append_query_param("", 'portfolio', request.portfolio)
        response = self.client.request("GET", path, query=query_params, allowed_status_codes=request.allowed_status_codes)
        return GetOrderDetailsResponse(**response.json())

    def list_open_orders(self, request: ListOpenOrdersRequest) -> ListOpenOrdersResponse:
        path = "/orders"
        query_params = append_pagination_params("", request.pagination)
        query_params = append_query_param(query_params, 'portfolio', request.portfolio)
        query_params = append_query_param(query_params, 'instrument', request.instrument)
        query_params = append_query_param(query_params, 'instrument_type', request.instrument_type)
        query_params = append_query_param(query_params, 'client_order_id', request.client_order_id)
        query_params = append_query_param(query_params, 'event_type', request.event_type)
        query_params = append_query_param(query_params, 'order_type', request.order_type)
        query_params = append_query_param(query_params, 'side', request.side)
        query_params = append_query_param(query_params, 'ref_datetime', request.ref_datetime)
        response = self.client.request("GET", path, query=query_params, allowed_status_codes=request.allowed_status_codes)
        return ListOpenOrdersResponse(orders=response.json())

    def modify_open_order(self, request: ModifyOpenOrderRequest) -> ModifyOpenOrderResponse:
        path = f"/orders/{request.id}"
        body = {k: v for k, v in asdict(request).items() if v is not None and k not in ['allowed_status_codes', 'id']}
        response = self.client.request("PUT", path, body=body, allowed_status_codes=request.allowed_status_codes)
        return ModifyOpenOrderResponse(**response.json())
