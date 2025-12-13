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
from intx_sdk.services.portfolios import TransferFundsRequest
from intx_sdk.credentials import Credentials
from tests.test_constants import BASE_URL


class TestTransferFunds(unittest.TestCase):

    @patch('intx_sdk.client.Client.request')
    def test_transfer_funds_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True
        }
        mock_request.return_value = mock_response

        credentials = Credentials(
            access_key="test_key",
            passphrase="test_passphrase",
            signing_key="test_signing_key"
        )
        client = IntxServicesClient(credentials, base_url=BASE_URL)

        request = TransferFundsRequest(
            from_portfolio="portfolio_1",
            to_portfolio="portfolio_2",
            asset="BTC",
            amount="0.5"
        )
        response = client.portfolios.transfer_funds(request)

        self.assertTrue(response.transfer_result.success)

    @patch('intx_sdk.client.Client.request')
    def test_transfer_funds_failure(self, mock_request):
        mock_request.side_effect = Exception("API error")

        credentials = Credentials(
            access_key="test_key",
            passphrase="test_passphrase",
            signing_key="test_signing_key"
        )
        client = IntxServicesClient(credentials, base_url="https://api-n5e1.coinbase.com/api/v1")

        request = TransferFundsRequest(
            from_portfolio="portfolio_1",
            to_portfolio="portfolio_2",
            asset="BTC",
            amount="0.5"
        )
        with self.assertRaises(Exception) as context:
            client.portfolios.transfer_funds(request)

        self.assertTrue('API error' in str(context.exception))


if __name__ == "__main__":
    unittest.main()
