#!/usr/bin/env python3
"""
opinion_api_client - Clean prediction market API client

Clean and simple, no ugly naming
"""

__version__ = "0.1.0"

# Core API
from opinion_api.api.prediction_market_api import PredictionMarketApi as _PredictionMarketApi
from opinion_api.api.user_api import UserApi as _UserApi

class MarketAPI(_PredictionMarketApi):
    """Market API"""
    pass

class UserAPI(_UserApi):
    """User API"""
    pass

# Convenience functions
from opinion_api import Configuration, ApiClient

def create_client(host, api_key=None, **kwargs):
    """Create market client"""
    config = Configuration(host=host, **kwargs)
    if api_key:
        config.api_key['apikey'] = api_key
    api_client = ApiClient(config)
    return MarketAPI(api_client)

def create_user_client(host, api_key=None, **kwargs):
    """Create user client"""
    config = Configuration(host=host, **kwargs)
    if api_key:
        config.api_key['apikey'] = api_key
    api_client = ApiClient(config)
    return UserAPI(api_client)

# Data model aliases
from opinion_api.models.openapi_balance_resp_open_api import OpenapiBalanceRespOpenAPI as Balance
from opinion_api.models.openapi_market_data_open_api import OpenapiMarketDataOpenAPI as Market
from opinion_api.models.openapi_order_data_open_api import OpenapiOrderDataOpenAPI as Order
from opinion_api.models.openapi_position_data_open_api import OpenapiPositionDataOpenAPI as Position
from opinion_api.models.v2_add_order_req import V2AddOrderReq as OrderRequest
from opinion_api.models.v2_add_order_resp import V2AddOrderResp as OrderResponse

# Backward compatibility
PredictionMarketApi = MarketAPI
MarketApi = MarketAPI

__all__ = [
    "MarketAPI",
    "UserAPI",
    "create_client",
    "create_user_client",
    "Balance",
    "Market",
    "Order",
    "Position",
    "OrderRequest",
    "OrderResponse",
    "PredictionMarketApi",
    "MarketApi",
]