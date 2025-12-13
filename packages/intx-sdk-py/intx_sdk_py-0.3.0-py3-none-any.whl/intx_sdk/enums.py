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

from enum import Enum


class AssetStatus(Enum):
    """An asset level status that would affect all markets with the asset"""
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"


class RecipientType(Enum):
    """Filter by recipient type"""
    CRYPTO_ADDRESS = "CRYPTO_ADDRESS"
    COUNTERPARTY_ID = "COUNTERPARTY_ID"


class FeeTierType(Enum):
    """The type of fee tier"""
    REGULAR = "REGULAR"
    LIQUIDITY_PROGRAM = "LIQUIDITY_PROGRAM"


class InstrumentType(Enum):
    """The type of instrument"""
    SPOT = "SPOT"
    PERP = "PERP"


class Granularity(Enum):
    """The aggregation period of the candles data"""
    ONE_DAY = "ONE_DAY"
    SIX_HOUR = "SIX_HOUR"
    TWO_HOUR = "TWO_HOUR"
    ONE_HOUR = "ONE_HOUR"
    THIRTY_MINUTE = "THIRTY_MINUTE"
    FIFTEEN_MINUTE = "FIFTEEN_MINUTE"
    FIVE_MINUTE = "FIVE_MINUTE"
    ONE_MINUTE = "ONE_MINUTE"


class InstrumentMode(Enum):
    """The mode of instrument"""
    STANDARD = "STANDARD"
    PRE_LAUNCH = "PRE_LAUNCH"
    PRE_LAUNCH_CONVERTING = "PRE_LAUNCH_CONVERTING"


class TradingState(Enum):
    """An market level status affecting all trading within the market"""
    TRADING = "TRADING"
    PAUSED = "PAUSED"
    HALT = "HALT"
    DELISTED = "DELISTED"
    EXTERNAL = "EXTERNAL"
    AUCTION_MODE = "AUCTION_MODE"
    CANCEL_ONLY = "CANCEL_ONLY"
    POST_ONLY = "POST_ONLY"
    LIMIT_ONLY = "LIMIT_ONLY"
    TRADING_DISABLED = "TRADING_DISABLED"
    CANCEL_ONLY_ENFORCED_BY_COINBASE_INTERNATIONAL_EXCHANGE = "CANCEL_ONLY_ENFORCED_BY_COINBASE_INTERNATIONAL_EXCHANGE"
    COINBASE_EXCHANGE_UNREACHABLE = "COINBASE_EXCHANGE_UNREACHABLE"


class OrderSide(Enum):
    """The side of the transaction"""
    BUY = "BUY"
    SELL = "SELL"


class OrderType(Enum):
    """The type of the order"""
    LIMIT = "LIMIT"
    MARKET = "MARKET"
    STOP_LIMIT = "STOP_LIMIT"
    STOP = "STOP"
    TAKE_PROFIT_STOP_LOSS = "TAKE_PROFIT_STOP_LOSS"


class TimeInForce(Enum):
    """Time in force for the order"""
    GTC = "GTC"
    IOC = "IOC"
    GTT = "GTT"
    FOK = "FOK"


class StpMode(Enum):
    """Specifies the behavior for self match handling"""
    NONE = "NONE"
    AGGRESSING = "AGGRESSING"
    RESTING = "RESTING"
    BOTH = "BOTH"
    DECREMENT_AND_CANCEL = "DECREMENT_AND_CANCEL"


class EventType(Enum):
    """The most recent type of event that happened to the order"""
    NEW = "NEW"
    TRADE = "TRADE"
    CANCELED = "CANCELED"
    REPLACED = "REPLACED"
    PENDING_CANCEL = "PENDING_CANCEL"
    REJECTED = "REJECTED"
    PENDING_NEW = "PENDING_NEW"
    EXPIRED = "EXPIRED"
    PENDING_REPLACE = "PENDING_REPLACE"
    STOP_TRIGGERED = "STOP_TRIGGERED"


class OrderStatus(Enum):
    """The status of the order"""
    WORKING = "WORKING"
    DONE = "DONE"


class AlgoStrategy(Enum):
    """Specifies the algorithmic trading strategy for the order"""
    TWAP = "TWAP"


class LoanAction(Enum):
    """The loan update action to take"""
    ACQUIRE = "ACQUIRE"
    REPAY = "REPAY"


class MarginCallStatus(Enum):
    """The status of the margin call"""
    NOT_LIQUIDATING = "NOT_LIQUIDATING"
    MARGIN_CALL_PENDING = "MARGIN_CALL_PENDING"
    LIQUIDATING = "LIQUIDATING"


class RankingsInstrumentType(Enum):
    """Identifies the instruments by type for rankings"""
    SPOT = "SPOT"
    PERPETUAL_FUTURE = "PERPETUAL_FUTURE"


class RankingsPeriod(Enum):
    """Identifies the lookback window for the rankings query"""
    YESTERDAY = "YESTERDAY"
    LAST_7_DAYS = "LAST_7_DAYS"
    THIS_MONTH = "THIS_MONTH"
    LAST_30_DAYS = "LAST_30_DAYS"
    LAST_MONTH = "LAST_MONTH"


class TransferType(Enum):
    """The type of transfer"""
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"
    STIPEND = "STIPEND"
    INTERNAL = "INTERNAL"
    FUNDING = "FUNDING"
    ALL = "ALL"
    LOAN_ACQUIRE = "LOAN_ACQUIRE"
    LOAN_REPAY = "LOAN_REPAY"
    LOAN_INTEREST_CHARGE = "LOAN_INTEREST_CHARGE"
    REAL_TIME_SETTLEMENT = "REAL_TIME_SETTLEMENT"
    ALL_LOANS = "ALL_LOANS"
    LIQUIDATION_EQUITY_CLAWBACK = "LIQUIDATION_EQUITY_CLAWBACK"
    POSITION_TRANSFER = "POSITION_TRANSFER"


class TransferStatus(Enum):
    """The current status of the transfer"""
    PROCESSED = "PROCESSED"
    NEW = "NEW"
    FAILED = "FAILED"
    STARTED = "STARTED"
