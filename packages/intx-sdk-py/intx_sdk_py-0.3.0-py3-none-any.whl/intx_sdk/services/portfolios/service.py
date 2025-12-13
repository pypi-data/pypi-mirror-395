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
from intx_sdk.utils import append_query_param, append_pagination_params
from intx_sdk.services.model import (
    Portfolio,
    AssetLoan,
    AssetBalance,
    LoanAvailability,
    PortfolioLoan,
    OpenPositionLimit,
    PortfolioSummary,
    PortfolioDetail,
    PortfolioPosition,
    TotalOpenPositionLimit,
    PortfolioFeeRate,
    PortfolioFillPaginationResult,
    PortfolioFillsResult,
    TransferResult,
    MarginOverrideResult,
    LoanPreview,
)
from .list_portfolios import ListPortfoliosRequest, ListPortfoliosResponse
from .acquire_or_repay_loan import AcquireOrRepayLoanRequest, AcquireOrRepayLoanResponse
from .create_portfolio import CreatePortfolioRequest, CreatePortfolioResponse
from .enable_disable_auto_margin import EnableDisableAutoMarginRequest, EnableDisableAutoMarginResponse
from .enable_disable_cross_collateral import EnableDisableCrossCollateralRequest, EnableDisableCrossCollateralResponse
from .get_balance_for_portfolio_asset import GetBalanceForPortfolioAssetRequest, GetBalanceForPortfolioAssetResponse
from .get_fund_transfer_limit import GetFundTransferLimitRequest, GetFundTransferLimitResponse
from .get_portfolio import GetPortfolioRequest, GetPortfolioResponse
from .get_portfolio_details import GetPortfolioDetailsRequest, GetPortfolioDetailsResponse
from .get_portfolio_summary import GetPortfolioSummaryRequest, GetPortfolioSummaryResponse
from .get_position_for_portfolio_instrument import GetPositionForPortfolioInstrumentRequest, GetPositionForPortfolioInstrumentResponse
from .list_portfolio_balances import ListPortfolioBalancesRequest, ListPortfolioBalancesResponse
from .list_portfolio_fills import ListPortfolioFillsRequest, ListPortfolioFillsResponse
from .list_portfolio_fee_rates import ListPortfolioFeeRatesRequest, ListPortfolioFeeRatesResponse
from .transfer_position import TransferPositionRequest, TransferPositionResponse
from .transfer_funds import TransferFundsRequest, TransferFundsResponse
from .set_margin_override import SetMarginOverrideRequest, SetMarginOverrideResponse
from .preview_loan_update import PreviewLoanUpdateRequest, PreviewLoanUpdateResponse
from .patch_portfolio import PatchPortfolioRequest, PatchPortfolioResponse
from .list_portfolio_positions import ListPortfolioPositionsRequest, ListPortfolioPositionsResponse
from .get_asset_loan_availability import GetAssetLoanAvailabilityRequest, GetAssetLoanAvailabilityResponse
from .get_loan_info_for_portfolio_asset import GetLoanInfoForPortfolioAssetRequest, GetLoanInfoForPortfolioAssetResponse
from .update_portfolio import UpdatePortfolioRequest, UpdatePortfolioResponse
from .list_open_position_limits_for_all_instruments import ListOpenPositionLimitsForAllInstrumentsRequest, ListOpenPositionLimitsForAllInstrumentsResponse
from .list_fills_by_portfolios import ListFillsByPortfoliosRequest, ListFillsByPortfoliosResponse
from .list_active_loans_for_portfolio import ListActiveLoansForPortfolioRequest, ListActiveLoansForPortfolioResponse
from .get_open_position_limits_for_portfolio_instrument import GetOpenPositionLimitsForPortfolioInstrumentRequest, GetOpenPositionLimitsForPortfolioInstrumentResponse
from .get_the_total_open_position_limit_for_portfolio import GetTheTotalOpenPositionLimitForPortfolioRequest, GetTheTotalOpenPositionLimitForPortfolioResponse


class PortfoliosService:
    def __init__(self, client: Client):
        self.client = client

    def list_portfolios(self, request: ListPortfoliosRequest) -> ListPortfoliosResponse:
        path = "/portfolios"
        response = self.client.request("GET", path, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return ListPortfoliosResponse(portfolios=[Portfolio(**p) for p in data])

    def create_portfolio(self, request: CreatePortfolioRequest) -> CreatePortfolioResponse:
        path = "/portfolios"
        body = {"name": request.name}
        response = self.client.request("POST", path, body=body, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return CreatePortfolioResponse(portfolio=Portfolio(**data))

    def acquire_or_repay_loan(self, request: AcquireOrRepayLoanRequest) -> AcquireOrRepayLoanResponse:
        path = f"/portfolios/{request.portfolio}/loans/{request.asset}"
        body = {k: v for k, v in asdict(request).items() if v is not None and k != 'allowed_status_codes'}
        response = self.client.request("POST", path, body=body, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return AcquireOrRepayLoanResponse(loan=AssetLoan(**data))

    def enable_disable_auto_margin(self, request: EnableDisableAutoMarginRequest) -> EnableDisableAutoMarginResponse:
        path = f"/portfolios/{request.portfolio}/auto-margin-enabled"
        body = {"enabled": request.enabled}
        response = self.client.request("POST", path, body=body, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return EnableDisableAutoMarginResponse(portfolio=Portfolio(**data))

    def enable_disable_cross_collateral(self, request: EnableDisableCrossCollateralRequest) -> EnableDisableCrossCollateralResponse:
        path = f"/portfolios/{request.portfolio}/cross-collateral-enabled"
        body = {"enabled": request.enabled}
        response = self.client.request("POST", path, body=body, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return EnableDisableCrossCollateralResponse(portfolio=Portfolio(**data))

    def get_balance_for_portfolio_asset(self, request: GetBalanceForPortfolioAssetRequest) -> GetBalanceForPortfolioAssetResponse:
        path = f"/portfolios/{request.portfolio}/balances/{request.asset}"
        response = self.client.request("GET", path, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return GetBalanceForPortfolioAssetResponse(balance=AssetBalance(**data))

    def get_fund_transfer_limit(self, request: GetFundTransferLimitRequest) -> GetFundTransferLimitResponse:
        path = f"/portfolios/transfer/{request.portfolio}/{request.asset}/transfer-limit"
        response = self.client.request("GET", path, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return GetFundTransferLimitResponse(max_portfolio_transfer_amount=data)

    def get_portfolio(self, request: GetPortfolioRequest) -> GetPortfolioResponse:
        path = f"/portfolios/{request.portfolio}"
        response = self.client.request("GET", path, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return GetPortfolioResponse(portfolio=Portfolio(**data))

    def get_portfolio_details(self, request: GetPortfolioDetailsRequest) -> GetPortfolioDetailsResponse:
        path = f"/portfolios/{request.portfolio}/detail"
        response = self.client.request("GET", path, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return GetPortfolioDetailsResponse(portfolio_detail=PortfolioDetail(**data))

    def get_portfolio_summary(self, request: GetPortfolioSummaryRequest) -> GetPortfolioSummaryResponse:
        path = f"/portfolios/{request.portfolio}/summary"
        response = self.client.request("GET", path, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return GetPortfolioSummaryResponse(portfolio_summary=PortfolioSummary(**data))

    def get_position_for_portfolio_instrument(self, request: GetPositionForPortfolioInstrumentRequest) -> GetPositionForPortfolioInstrumentResponse:
        path = f"/portfolios/{request.portfolio}/positions/{request.instrument}"
        response = self.client.request("GET", path, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return GetPositionForPortfolioInstrumentResponse(position=PortfolioPosition(**data))

    def list_portfolio_balances(self, request: ListPortfolioBalancesRequest) -> ListPortfolioBalancesResponse:
        path = f"/portfolios/{request.portfolio}/balances"
        response = self.client.request("GET", path, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return ListPortfolioBalancesResponse(balances=[AssetBalance(**b) for b in data])

    def list_portfolio_fills(self, request: ListPortfolioFillsRequest) -> ListPortfolioFillsResponse:
        path = f"/portfolios/{request.portfolio}/fills"
        query_params = append_pagination_params("", request.pagination)
        query_params = append_query_param(query_params, 'portfolio', request.portfolio)
        query_params = append_query_param(query_params, 'order_id', request.order_id)
        query_params = append_query_param(query_params, 'client_order_id', request.client_order_id)
        query_params = append_query_param(query_params, 'ref_datetime', request.ref_datetime)
        query_params = append_query_param(query_params, 'time_from', request.time_from)
        response = self.client.request("GET", path, query=query_params, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return ListPortfolioFillsResponse(fills_result=PortfolioFillsResult(**data))

    def list_portfolio_fee_rates(self, request: ListPortfolioFeeRatesRequest) -> ListPortfolioFeeRatesResponse:
        path = "/portfolios/fee-rates"
        response = self.client.request("GET", path, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return ListPortfolioFeeRatesResponse(fee_rates=[PortfolioFeeRate(**f) for f in data])

    def transfer_position(self, request: TransferPositionRequest) -> TransferPositionResponse:
        path = "/portfolios/transfer-position"
        body = {
            "from": request.from_portfolio,
            "to": request.to_portfolio,
            "instrument": request.instrument,
            "quantity": request.quantity,
            "side": request.side
        }
        response = self.client.request("POST", path, body=body, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return TransferPositionResponse(transfer_result=TransferResult(**data))

    def transfer_funds(self, request: TransferFundsRequest) -> TransferFundsResponse:
        path = "/portfolios/transfer"
        body = {
            "from": request.from_portfolio,
            "to": request.to_portfolio,
            "asset": request.asset,
            "amount": request.amount
        }
        response = self.client.request("POST", path, body=body, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return TransferFundsResponse(transfer_result=TransferResult(**data))

    def set_margin_override(self, request: SetMarginOverrideRequest) -> SetMarginOverrideResponse:
        path = "/portfolios/margin"
        body = {k: v for k, v in asdict(request).items() if v is not None and k != 'allowed_status_codes'}
        response = self.client.request("POST", path, body=body, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return SetMarginOverrideResponse(margin_override_result=MarginOverrideResult(**data))

    def preview_loan_update(self, request: PreviewLoanUpdateRequest) -> PreviewLoanUpdateResponse:
        path = f"/portfolios/{request.portfolio}/loans/{request.asset}/preview"
        body = {k: v for k, v in asdict(request).items() if v is not None and k not in ['portfolio', 'asset', 'allowed_status_codes']}
        response = self.client.request("POST", path, body=body, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return PreviewLoanUpdateResponse(loan_preview=LoanPreview(**data))

    def patch_portfolio(self, request: PatchPortfolioRequest) -> PatchPortfolioResponse:
        path = f"/portfolios/{request.portfolio}"
        body = {k: v for k, v in asdict(request).items() if v is not None and k not in ['portfolio', 'portfolio_name', 'allowed_status_codes']}
        response = self.client.request("PATCH", path, body=body, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return PatchPortfolioResponse(portfolio=Portfolio(**data))

    def list_portfolio_positions(self, request: ListPortfolioPositionsRequest) -> ListPortfolioPositionsResponse:
        path = f"/portfolios/{request.portfolio}/positions"
        response = self.client.request("GET", path, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return ListPortfolioPositionsResponse(positions=[PortfolioPosition(**p) for p in data])

    def get_asset_loan_availability(self, request: GetAssetLoanAvailabilityRequest) -> GetAssetLoanAvailabilityResponse:
        path = f"/portfolios/{request.portfolio}/loans/{request.asset}/availability"
        response = self.client.request("GET", path, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return GetAssetLoanAvailabilityResponse(loan_availability=LoanAvailability(**data))

    def get_loan_info_for_portfolio_asset(self, request: GetLoanInfoForPortfolioAssetRequest) -> GetLoanInfoForPortfolioAssetResponse:
        path = f"/portfolios/{request.portfolio}/loans/{request.asset}"
        response = self.client.request("GET", path, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return GetLoanInfoForPortfolioAssetResponse(portfolio_loan=PortfolioLoan(**data))

    def update_portfolio(self, request: UpdatePortfolioRequest) -> UpdatePortfolioResponse:
        path = f"/portfolios/{request.portfolio}"
        body = {"name": request.name}
        response = self.client.request("PUT", path, body=body, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return UpdatePortfolioResponse(portfolio=Portfolio(**data))

    def list_open_position_limits_for_all_instruments(self, request: ListOpenPositionLimitsForAllInstrumentsRequest) -> ListOpenPositionLimitsForAllInstrumentsResponse:
        path = f"/portfolios/{request.portfolio}/position-limits/positions"
        response = self.client.request("GET", path, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return ListOpenPositionLimitsForAllInstrumentsResponse(position_limits=[OpenPositionLimit(**pl) for pl in data])

    def list_fills_by_portfolios(self, request: ListFillsByPortfoliosRequest) -> ListFillsByPortfoliosResponse:
        path = "/portfolios/fills"
        query_params = append_pagination_params("", request.pagination)
        query_params = append_query_param(query_params, 'portfolios', request.portfolios)
        query_params = append_query_param(query_params, 'order_id', request.order_id)
        query_params = append_query_param(query_params, 'client_order_id', request.client_order_id)
        query_params = append_query_param(query_params, 'ref_datetime', request.ref_datetime)
        query_params = append_query_param(query_params, 'time_from', request.time_from)
        response = self.client.request("GET", path, query=query_params, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return ListFillsByPortfoliosResponse(fills_result=PortfolioFillsResult(**data))

    def list_active_loans_for_portfolio(self, request: ListActiveLoansForPortfolioRequest) -> ListActiveLoansForPortfolioResponse:
        path = f"/portfolios/{request.portfolio}/loans"
        response = self.client.request("GET", path, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return ListActiveLoansForPortfolioResponse(loans=[PortfolioLoan(**l) for l in data])

    def get_open_position_limits_for_portfolio_instrument(self, request: GetOpenPositionLimitsForPortfolioInstrumentRequest) -> GetOpenPositionLimitsForPortfolioInstrumentResponse:
        path = f"/portfolios/{request.portfolio}/position-limits/positions/{request.instrument}"
        response = self.client.request("GET", path, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return GetOpenPositionLimitsForPortfolioInstrumentResponse(open_position_limit=OpenPositionLimit(**data))

    def get_the_total_open_position_limit_for_portfolio(self, request: GetTheTotalOpenPositionLimitForPortfolioRequest) -> GetTheTotalOpenPositionLimitForPortfolioResponse:
        path = f"/portfolios/{request.portfolio}/position-limits"
        response = self.client.request("GET", path, allowed_status_codes=request.allowed_status_codes)
        data = response.json()
        return GetTheTotalOpenPositionLimitForPortfolioResponse(total_open_position_limit=TotalOpenPositionLimit(**data))
