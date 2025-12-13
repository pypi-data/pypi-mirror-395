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
#  limitations under the License.

import unittest
from unittest.mock import patch, MagicMock
from intx_sdk import IntxServicesClient
from intx_sdk.services.portfolios import GetPortfolioDetailsRequest
from intx_sdk.credentials import Credentials
from tests.test_constants import BASE_URL


class TestGetPortfolioDetails(unittest.TestCase):

    @patch('intx_sdk.client.Client.request')
    def test_get_portfolio_details_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "summary": {
                "collateral": "1000.00",
                "unrealized_pnl": "0.0",
                "unrealized_pnl_percent": "0.0",
                "position_notional": "0.0",
                "open_position_notional": "0.0",
                "pending_fees": "0.0",
                "borrow": "0.0",
                "accrued_interest": "0.0",
                "rolling_debt": "0.0",
                "balance": "1000.00",
                "buying_power": "1000.00",
                "portfolio_initial_margin": 0.0,
                "portfolio_current_margin": 0.0,
                "portfolio_maintenance_margin": 0.0,
                "portfolio_close_out_margin": 0.0,
                "in_liquidation": False,
                "unrealized_pnl_notional": 0.0,
                "portfolio_initial_margin_notional": 0.0,
                "portfolio_maintenance_margin_notional": 0.0,
                "portfolio_close_out_margin_notional": 0.0,
                "margin_override": 0.0,
                "lock_up_initial_margin": 0.0,
                "loan_collateral_requirement": "0.0",
                "position_offset_notional": 0.0
            },
            "balances": [],
            "positions": []
        }
        mock_request.return_value = mock_response

        credentials = Credentials(
            access_key="test_key",
            passphrase="test_passphrase",
            signing_key="test_signing_key"
        )
        client = IntxServicesClient(credentials, base_url=BASE_URL)

        request = GetPortfolioDetailsRequest(portfolio="dummy_portfolio_id")
        response = client.portfolios.get_portfolio_details(request)

        self.assertEqual(response.portfolio_detail.summary.balance, "1000.00")
        self.assertEqual(response.portfolio_detail.summary.collateral, "1000.00")
        self.assertIsInstance(response.portfolio_detail.balances, list)
        self.assertIsInstance(response.portfolio_detail.positions, list)

    @patch('intx_sdk.client.Client.request')
    def test_get_portfolio_details_failure(self, mock_request):
        mock_request.side_effect = Exception("API error")

        credentials = Credentials(
            access_key="test_key",
            passphrase="test_passphrase",
            signing_key="test_signing_key"
        )
        client = IntxServicesClient(credentials, base_url="https://api-n5e1.coinbase.com/api/v1")

        request = GetPortfolioDetailsRequest(portfolio="dummy_portfolio_id")
        with self.assertRaises(Exception) as context:
            client.portfolios.get_portfolio_details(request)

        self.assertTrue('API error' in str(context.exception))


if __name__ == "__main__":
    unittest.main()
