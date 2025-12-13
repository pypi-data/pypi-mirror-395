# Copyright 2024-present Coinbase Global, Inc.
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

import unittest
from unittest.mock import patch, MagicMock
from intx_sdk import IntxServicesClient
from intx_sdk.services.portfolios import GetBalanceForPortfolioAssetRequest
from intx_sdk.credentials import Credentials
from tests.test_constants import BASE_URL


class TestGetBalanceForPortfolioAsset(unittest.TestCase):

    @patch('intx_sdk.client.Client.request')
    def test_get_balance_for_portfolio_asset_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "asset_id": "BTC-ID",
            "asset_name": "BTC",
            "asset_uuid": "btc-uuid",
            "quantity": 1.5,
            "hold": 0.0,
            "hold_available_for_collateral": 0.0,
            "transfer_hold": 0.0,
            "collateral_value": 0.0,
            "max_withdraw_amount": 1.5,
            "loan": 0.0,
            "loan_collateral_requirement": 0.0,
            "pledged_collateral_quantity": 0.0,
            "loan_initial_margin_contribution": 0.0,
            "collateral_backed_overdraft_loan": 0.0,
            "user_requested_loan": 0.0,
            "unreconciled_amount": 0.0,
            "max_undelegate_amount": 0.0
        }
        mock_request.return_value = mock_response

        credentials = Credentials(
            access_key="test_key",
            passphrase="test_passphrase",
            signing_key="test_signing_key"
        )
        client = IntxServicesClient(credentials, base_url=BASE_URL)

        request = GetBalanceForPortfolioAssetRequest(portfolio="dummy_portfolio_id", asset="BTC")
        response = client.portfolios.get_balance_for_portfolio_asset(request)

        self.assertEqual(response.balance.asset_name, "BTC")
        self.assertEqual(response.balance.quantity, 1.5)

    @patch('intx_sdk.client.Client.request')
    def test_get_balance_for_portfolio_asset_failure(self, mock_request):
        mock_request.side_effect = Exception("API error")

        credentials = Credentials(
            access_key="test_key",
            passphrase="test_passphrase",
            signing_key="test_signing_key"
        )
        client = IntxServicesClient(credentials, base_url="https://api-n5e1.coinbase.com/api/v1")

        request = GetBalanceForPortfolioAssetRequest(portfolio="dummy_portfolio_id", asset="BTC")
        with self.assertRaises(Exception) as context:
            client.portfolios.get_balance_for_portfolio_asset(request)

        self.assertTrue('API error' in str(context.exception))


if __name__ == "__main__":
    unittest.main()