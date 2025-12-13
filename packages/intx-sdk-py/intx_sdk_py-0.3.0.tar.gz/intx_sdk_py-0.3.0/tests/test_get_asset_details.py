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
from intx_sdk.services.assets import GetAssetDetailsRequest
from intx_sdk.credentials import Credentials
from tests.test_constants import BASE_URL


class TestGetAssetDetails(unittest.TestCase):

    @patch('intx_sdk.client.Client.request')
    def test_get_asset_details_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "asset_id": "BTC-ID",
            "asset_name": "BTC",
            "asset_uuid": "btc-uuid",
            "status": "ACTIVE",
            "collateral_weight": "0.9",
            "supported_networks_enabled": False,
            "min_borrow_qty": "0.001",
            "max_borrow_qty": "10.0",
            "loan_collateral_requirement_multiplier": "1.0",
            "ecosystem_collateral_limit_breached": False,
            "loan_initial_margin": "0.1",
            "max_loan_leverage": "10.0"
        }
        mock_request.return_value = mock_response

        credentials = Credentials(
            access_key="test_key",
            passphrase="test_passphrase",
            signing_key="test_signing_key"
        )
        client = IntxServicesClient(credentials, base_url=BASE_URL)

        request = GetAssetDetailsRequest(asset="BTC")
        response = client.assets.get_asset_details(request)

        self.assertEqual(response.asset.asset_name, "BTC")
        self.assertEqual(response.asset.status, "ACTIVE")
        self.assertEqual(response.asset.collateral_weight, "0.9")

    @patch('intx_sdk.client.Client.request')
    def test_get_asset_details_failure(self, mock_request):
        mock_request.side_effect = Exception("API error")

        credentials = Credentials(
            access_key="test_key",
            passphrase="test_passphrase",
            signing_key="test_signing_key"
        )
        client = IntxServicesClient(credentials, base_url="https://api-n5e1.coinbase.com/api/v1")

        request = GetAssetDetailsRequest(asset="BTC-PERP")
        with self.assertRaises(Exception) as context:
            client.assets.get_asset_details(request)

        self.assertTrue('API error' in str(context.exception))


if __name__ == "__main__":
    unittest.main()