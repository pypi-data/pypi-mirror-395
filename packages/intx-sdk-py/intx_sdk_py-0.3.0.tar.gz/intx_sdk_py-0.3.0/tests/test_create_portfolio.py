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
from intx_sdk.services.portfolios import CreatePortfolioRequest
from intx_sdk.credentials import Credentials
from tests.test_constants import BASE_URL


class TestCreatePortfolio(unittest.TestCase):

    @patch('intx_sdk.client.Client.request')
    def test_create_portfolio_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "portfolio_id": "dummy_portfolio_id",
            "portfolio_uuid": "dummy_uuid",
            "name": "Test Portfolio 5111",
            "user_uuid": "user_uuid",
            "maker_fee_rate": "0.0",
            "taker_fee_rate": "0.0002",
            "trading_lock": False,
            "withdrawal_lock": False,
            "borrow_disabled": False,
            "is_lsp": False,
            "is_default": False,
            "cross_collateral_enabled": False,
            "auto_margin_enabled": False,
            "pre_launch_trading_enabled": False,
            "position_offsets_enabled": False
        }
        mock_request.return_value = mock_response

        credentials = Credentials(
            access_key="test_key",
            passphrase="test_passphrase",
            signing_key="test_signing_key"
        )
        client = IntxServicesClient(credentials, base_url=BASE_URL)

        request = CreatePortfolioRequest(name="My Test Portfolio")
        response = client.portfolios.create_portfolio(request)

        self.assertEqual(response.portfolio.portfolio_id, "dummy_portfolio_id")
        self.assertEqual(response.portfolio.name, "Test Portfolio 5111")

    @patch('intx_sdk.client.Client.request')
    def test_create_portfolio_failure(self, mock_request):
        mock_request.side_effect = Exception("API error")

        credentials = Credentials(
            access_key="test_key",
            passphrase="test_passphrase",
            signing_key="test_signing_key"
        )
        client = IntxServicesClient(credentials, base_url="https://api-n5e1.coinbase.com/api/v1")

        request = CreatePortfolioRequest(name="My Test Portfolio")
        with self.assertRaises(Exception) as context:
            client.portfolios.create_portfolio(request)

        self.assertTrue('API error' in str(context.exception))


if __name__ == "__main__":
    unittest.main()
