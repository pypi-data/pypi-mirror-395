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
import os
from typing import Optional, Any, Callable, Type
from intx_sdk.client import Client
from intx_sdk.credentials import Credentials
from intx_sdk.constants import PRODUCTION_BASE_URL, SANDBOX_BASE_URL


class LazyProperty:
    def __init__(self, factory: Callable[['IntxServicesClient'], Any]):
        self.factory = factory
        self.attr_name = None

    def __set_name__(self, owner: Type, name: str):
        self.attr_name = f'_lazy_{name}'

    def __get__(self, instance: 'IntxServicesClient', owner: Type = None):
        if instance is None:
            return self

        # Check if already cached
        if hasattr(instance, self.attr_name):
            return getattr(instance, self.attr_name)

        # Create and cache the service
        service = self.factory(instance)
        setattr(instance, self.attr_name, service)
        return service


def lazy_service(service_factory):
    def factory(client_instance: 'IntxServicesClient'):
        # Handle both lambda functions and direct class references
        if callable(service_factory) and getattr(service_factory, '__name__', None) == '<lambda>':
            # It's a lambda function that returns the class
            service_class = service_factory()
        else:
            # It's a direct class reference
            service_class = service_factory
        return service_class(client_instance._client)

    return LazyProperty(factory)


class IntxServicesClient:
    def __init__(self, credentials: Credentials, base_url: Optional[str] = None):
        self._client = Client(credentials, base_url=base_url)

    @classmethod
    def from_env(cls, variable_name: str = 'INTX_CREDENTIALS',
                 base_url: Optional[str] = None) -> 'IntxServicesClient':
        credentials = Credentials.from_env(variable_name)

        # Priority order for base_url:
        # 1. Explicit base_url parameter
        # 2. INTX_BASE_URL environment variable
        # 3. Default to PRODUCTION_BASE_URL
        if base_url is None:
            base_url = os.getenv('INTX_BASE_URL', PRODUCTION_BASE_URL)

        return cls(credentials, base_url)

    @property
    def client(self) -> Client:
        return self._client

    # Import services dynamically to avoid circular imports
    portfolios = lazy_service(lambda: __import__('intx_sdk.services.portfolios', fromlist=['PortfoliosService']).PortfoliosService)
    rankings = lazy_service(lambda: __import__('intx_sdk.services.rankings', fromlist=['RankingsService']).RankingsService)
    positionoffsets = lazy_service(lambda: __import__('intx_sdk.services.positionoffsets', fromlist=['PositionOffsetsService']).PositionOffsetsService)
    transfers = lazy_service(lambda: __import__('intx_sdk.services.transfers', fromlist=['TransfersService']).TransfersService)
    orders = lazy_service(lambda: __import__('intx_sdk.services.orders', fromlist=['OrdersService']).OrdersService)
    index = lazy_service(lambda: __import__('intx_sdk.services.index', fromlist=['IndexService']).IndexService)
    instruments = lazy_service(lambda: __import__('intx_sdk.services.instruments', fromlist=['InstrumentsService']).InstrumentsService)
    assets = lazy_service(lambda: __import__('intx_sdk.services.assets', fromlist=['AssetsService']).AssetsService)
    feerates = lazy_service(lambda: __import__('intx_sdk.services.feerates', fromlist=['FeeRatesService']).FeeRatesService)
    addressbook = lazy_service(lambda: __import__('intx_sdk.services.addressbook', fromlist=['AddressBookService']).AddressBookService)
