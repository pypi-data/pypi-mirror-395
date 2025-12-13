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
from intx_sdk.services.model import (
    CounterpartyIdResult,
    CryptoAddressResult,
    Transfer,
    TransferPaginationResult,
    TransfersResult,
    CounterpartyValidation,
    WithdrawToCounterpartyResult,
    WithdrawToCryptoResult,
    PortfolioInfo,
)
from .create_counterparty_id import CreateCounterpartyIdRequest, CreateCounterpartyIdResponse
from .create_crypto_address import CreateCryptoAddressRequest, CreateCryptoAddressResponse
from .get_transfer import GetTransferRequest, GetTransferResponse
from .list_transfers import ListTransfersRequest, ListTransfersResponse
from .validate_counterparty_id import ValidateCounterpartyIdRequest, ValidateCounterpartyIdResponse
from .withdraw_to_counterparty_id import WithdrawToCounterpartyIdRequest, WithdrawToCounterpartyIdResponse
from .withdraw_to_crypto_address import WithdrawToCryptoAddressRequest, WithdrawToCryptoAddressResponse


class TransfersService:
    def __init__(self, client: Client):
        self.client = client

    def create_counterparty_id(self, request: CreateCounterpartyIdRequest) -> CreateCounterpartyIdResponse:
        path = "/transfers/create-counterparty-id"
        body = {k: v for k, v in asdict(request).items() if v is not None and k != 'allowed_status_codes'}
        response = self.client.request("POST", path, body=body, allowed_status_codes=request.allowed_status_codes)
        return CreateCounterpartyIdResponse(counterparty_id_result=response.json())

    def create_crypto_address(self, request: CreateCryptoAddressRequest) -> CreateCryptoAddressResponse:
        path = "/transfers/address"
        body = {k: v for k, v in asdict(request).items() if v is not None and k != 'allowed_status_codes'}
        response = self.client.request("POST", path, body=body, allowed_status_codes=request.allowed_status_codes)
        return CreateCryptoAddressResponse(crypto_address_result=response.json())

    def get_transfer(self, request: GetTransferRequest) -> GetTransferResponse:
        path = f"/transfers/{request.transfer_uuid}"
        response = self.client.request("GET", path, allowed_status_codes=request.allowed_status_codes)
        return GetTransferResponse(transfer=response.json())

    def list_transfers(self, request: ListTransfersRequest) -> ListTransfersResponse:
        path = "/transfers"
        query_params = append_pagination_params("", request.pagination)
        query_params = append_query_param(query_params, 'portfolios', request.portfolios)
        query_params = append_query_param(query_params, 'time_from', request.time_from)
        query_params = append_query_param(query_params, 'time_to', request.time_to)
        query_params = append_query_param(query_params, 'status', request.status)
        query_params = append_query_param(query_params, 'type', request.type)
        response = self.client.request("GET", path, query=query_params, allowed_status_codes=request.allowed_status_codes)
        return ListTransfersResponse(transfers_result=response.json())

    def validate_counterparty_id(self, request: ValidateCounterpartyIdRequest) -> ValidateCounterpartyIdResponse:
        path = "/transfers/validate-counterparty-id"
        body = {k: v for k, v in asdict(request).items() if v is not None and k != 'allowed_status_codes'}
        response = self.client.request("POST", path, body=body, allowed_status_codes=request.allowed_status_codes)
        return ValidateCounterpartyIdResponse(counterparty_validation=response.json())

    def withdraw_to_counterparty_id(self, request: WithdrawToCounterpartyIdRequest) -> WithdrawToCounterpartyIdResponse:
        path = "/transfers/withdraw/counterparty"
        body = {k: v for k, v in asdict(request).items() if v is not None and k != 'allowed_status_codes'}
        response = self.client.request("POST", path, body=body, allowed_status_codes=request.allowed_status_codes)
        return WithdrawToCounterpartyIdResponse(withdraw_result=response.json())

    def withdraw_to_crypto_address(self, request: WithdrawToCryptoAddressRequest) -> WithdrawToCryptoAddressResponse:
        path = "/transfers/withdraw"
        body = {k: v for k, v in asdict(request).items() if v is not None and k != 'allowed_status_codes'}
        response = self.client.request("POST", path, body=body, allowed_status_codes=request.allowed_status_codes)
        return WithdrawToCryptoAddressResponse(withdraw_result=response.json())
