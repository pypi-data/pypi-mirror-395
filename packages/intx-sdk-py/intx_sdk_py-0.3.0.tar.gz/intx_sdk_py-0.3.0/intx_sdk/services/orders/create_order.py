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

from dataclasses import dataclass
from typing import Optional, List
from intx_sdk.services.model import Order
from intx_sdk.enums import OrderSide, OrderType, TimeInForce, StpMode, AlgoStrategy


@dataclass
class CreateOrderRequest:
    client_order_id: str
    side: OrderSide
    size: str
    tif: TimeInForce
    instrument: str
    type: OrderType
    price: Optional[str] = None
    stop_price: Optional[str] = None
    stop_limit_price: Optional[str] = None
    expire_time: Optional[str] = None
    portfolio: Optional[str] = None
    user: Optional[str] = None
    stp_mode: Optional[StpMode] = None
    post_only: Optional[str] = None
    close_only: Optional[str] = None
    algo_strategy: Optional[AlgoStrategy] = None
    allowed_status_codes: Optional[List[int]] = None


@dataclass
class CreateOrderResponse(Order):
    pass
