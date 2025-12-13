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
from intx_sdk.services.portfolios import ListPortfoliosRequest
from intx_sdk.credentials import Credentials
from tests.test_constants import BASE_URL


class TestListPortfolios(unittest.TestCase):

    @patch('intx_sdk.client.Client.request')
    def test_list_portfolios_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "portfolio_id": "dummy_id_1",
                "portfolio_uuid": "dummy_uuid_1",
                "name": "dummy_portfolio_1",
                "user_uuid": "dummy_user_uuid_1",
                "maker_fee_rate": "0",
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
            },
            {
                "portfolio_id": "dummy_id_2",
                "portfolio_uuid": "dummy_uuid_2",
                "name": "dummy_portfolio_2",
                "user_uuid": "dummy_user_uuid_2",
                "maker_fee_rate": "0",
                "taker_fee_rate": "0.0002",
                "trading_lock": False,
                "withdrawal_lock": False,
                "borrow_disabled": False,
                "is_lsp": False,
                "is_default": True,
                "cross_collateral_enabled": False,
                "auto_margin_enabled": False,
                "pre_launch_trading_enabled": False,
                "position_offsets_enabled": False
            }
        ]
        mock_request.return_value = mock_response

        credentials = Credentials(
            access_key="test_key",
            passphrase="test_passphrase",
            signing_key="test_signing_key"
        )
        client = IntxServicesClient(credentials, base_url=BASE_URL)

        request = ListPortfoliosRequest()
        response = client.portfolios.list_portfolios(request)

        self.assertEqual(len(response.portfolios), 2)
        self.assertTrue(all(isinstance(portfolio.portfolio_id, str) for portfolio in response.portfolios))
        self.assertTrue(all(isinstance(portfolio.is_default, bool) for portfolio in response.portfolios))

    @patch('intx_sdk.client.Client.request')
    def test_list_portfolios_failure(self, mock_request):
        mock_request.side_effect = Exception("API error")

        credentials = Credentials(
            access_key="test_key",
            passphrase="test_passphrase",
            signing_key="test_signing_key"
        )
        client = IntxServicesClient(credentials, base_url="https://api-n5e1.coinbase.com/api/v1")

        request = ListPortfoliosRequest()
        with self.assertRaises(Exception) as context:
            client.portfolios.list_portfolios(request)

        self.assertTrue('API error' in str(context.exception))


if __name__ == "__main__":
    unittest.main()
