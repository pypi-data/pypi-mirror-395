import httpx
import re
import time
from typing import Optional, Dict, Any, List, Union, Tuple

class Blocky:
    def __init__(self, api_key: Optional[str] = None, endpoint: str = 'https://blocky.com.br/api/v1'):
        self.api_key = api_key
        self.endpoint = endpoint.rstrip('/')
        
        headers = {}
        if self.api_key:
            headers['x-api-key'] = self.api_key

        self.client = httpx.AsyncClient(headers=headers, timeout=30.0)
        self.markets: Dict[str, Any] = {}
        self.authenticated = bool(self.api_key) # Presume authenticated if key is provided

    async def close(self):
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def _verify_auth(self) -> bool:
        try:
            # We use a lightweight call to verify; get_wallets usually requires auth
            response = await self.client.get(f"{self.endpoint}/wallets")
            # If 401 or 403, it fails. If 200, we are good.
            return response.status_code == 200
        except:
            return False

    async def _request(self, method: str, path: str, params: Optional[Union[Dict, List[Tuple]]] = None, json: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Internal request handler. 
        Note: params can be a Dict or a List of Tuples to support array parameters (e.g. markets=ETH&markets=BTC).
        """
        url = f"{self.endpoint}/{path}"
        
        try:
            response = await self.client.request(method, url, params=params, json=json)
            response.raise_for_status()
            data = response.json()
            
            # Standardize success check
            if not data.get('success', False):
                raise ValueError(f"API Error: {data.get('error_message', 'Unknown error')}")
            
            return data
        except httpx.HTTPStatusError as e:
            # Attempt to extract API error message if available in response
            try:
                err_data = e.response.json()
                if 'error_message' in err_data:
                    raise ValueError(f"API Error: {err_data['error_message']}")
            except (ValueError, AttributeError):
                pass # JSON decode failed, raise original
            raise e
        except httpx.RequestError as e:
            raise ValueError(f"Network Error: {str(e)}")

    def validate_decimal(self, decimal_str: Optional[str] = None, precision: int = 8, min_value: str = '-99999999.99999999', max_value: str = '99999999.99999999') -> str:
        if not decimal_str:
            raise ValueError("Decimal value is empty.")
        decimal_str = re.sub(r'^\.|\.$', '0.', decimal_str)
        # Regex to validate precision
        regex_pattern = rf'^-?\d{{1,8}}(\.\d{{1,{precision}}})?$'
        if not re.match(regex_pattern, decimal_str):
            raise ValueError(f"Invalid decimal format: {decimal_str}")
        
        decimal_value = float(decimal_str)
        if not (float(min_value) <= decimal_value <= float(max_value)):
            raise ValueError(f"Decimal value must be between {min_value} and {max_value}, provided: {decimal_value}")
        return str(decimal_value)

    async def _get_market_info(self, market: str) -> Optional[Dict[str, Any]]:
        # Refresh markets if cache is empty
        if not self.markets.get('markets'):
             self.markets = await self.get_markets()
             
        for m in self.markets.get('markets', []):
            if m['market'].lower() == market.lower():
                return m
        raise ValueError(f"Market '{market}' not found. Please ensure it exists.")

    # --- PUBLIC ENDPOINTS ---

    async def get_markets(self, get_tickers: bool = False) -> Dict[str, Any]:
        """
        Retrieve all available markets.

        :param get_tickers: If True, includes the 24h ticker data for each market.
        
        Example Response:
        {
            "get_tickers": true,
            "markets": [
                {
                    "base_instrument": "diam",
                    "base_instrument_id": 2,
                    "base_instrument_name": "Diamond",
                    "base_precision": 3,
                    "get_tickers": true,
                    "is_latest_tx_buy": false,
                    "maker_fee": "0.00000000",
                    "market": "xno_xbrl",
                    "market_id": 1,
                    "minimum_base_volume": "0.01000000",
                    "minimum_quote_volume": "0.01000000",
                    "quote_instrument": "xbrl",
                    "quote_instrument_id": 1,
                    "quote_instrument_name": "Iron Ingot",
                    "quote_precision": 3,
                    "taker_fee": "0.00000000",
                    "tick_size": "0.00100000",
                    "ticker": {
                        "base_volume": "0.00000000",
                        "change": "0.00000000",
                        "change_percentage": "0.00000000",
                        "close": "1.00000000",
                        "high": "1.00000000",
                        "low": "1.00000000",
                        "open": "1.00000000",
                        "quote_volume": "0.00000000"
                    }
                }
            ],
            "success": true
        }
        """
        params = {'get_tickers': 'true' if get_tickers else 'false'}
        return await self._request('GET', 'markets', params=params)

    async def get_market(self, market: str, get_tickers: bool = False) -> Dict[str, Any]:
        """
        Retrieve a specific market configuration.

        Example Response:
        {
            "base_instrument": "diam",
            "base_instrument_id": 2,
            "base_instrument_name": "Diamond",
            "base_precision": 3,
            "get_tickers": false,
            "is_latest_tx_buy": false,
            "maker_fee": "0.00000000",
            "market": "xno_xbrl",
            "market_id": 1,
            "minimum_base_volume": "0.01000000",
            "minimum_quote_volume": "0.01000000",
            "quote_instrument": "xbrl",
            "quote_instrument_id": 1,
            "quote_instrument_name": "Iron Ingot",
            "quote_precision": 3,
            "taker_fee": "0.00000000",
            "tick_size": "0.00100000"
        }
        """
        params = {'get_tickers': 'true' if get_tickers else 'false'}
        return await self._request('GET', f'markets/{market}', params=params)

    async def get_ticker(self, market: str) -> Dict[str, Any]:
        """
        Get the 24-hour ticker statistics for a specific market.

        Example Response:
        {
            "base_volume": "0.00000000",
            "change": "0.00000000",
            "change_percentage": "0.00000000",
            "close": "1.00000000",
            "high": "1.00000000",
            "low": "1.00000000",
            "open": "1.00000000",
            "quote_volume": "0.00000000",
            "success": true
        }
        """
        return await self._request('GET', f'markets/{market}/ticker')

    async def get_transactions(self, market: str, count: int = 128) -> Dict[str, Any]:
        """
        Get public transactions (recent trades) for a specific market.
        
        :param count: default 128, max 1024.

        Example Response:
        {
            "count": 3,
            "success": true,
            "transactions": [
                {
                    "created_at": "1761694261515760000",
                    "is_buying_tx": true,
                    "price": "100.00000000",
                    "quantity": "0.01004000"
                },
                {
                    "created_at": "1761694263054188000",
                    "is_buying_tx": true,
                    "price": "100.00000000",
                    "quantity": "0.00136000"
                }
            ]
        }
        """
        params = {'count': count}
        return await self._request('GET', f'markets/{market}/transactions', params=params)

    async def get_orderbook(self, market: str, depth: int = 0, tick_size: Optional[float] = None) -> Dict[str, Any]:
        """
        Fetch the orderbook for a market.
        Note: The backend C++ code uses 'count' as the query parameter for depth.

        Example Response:
        {
            "depth": 0,
            "market": "xno_xbrl",
            "orderbook": {
                "asks": {
                    "base_volume": "0.00000000",
                    "count": 0,
                    "price": [],
                    "quantity": [],
                    "quote_volume": "0.00000000"
                },
                "bids": {
                    "base_volume": "0.00000000",
                    "count": 0,
                    "price": [],
                    "quantity": [],
                    "quote_volume": "0.00000000"
                },
                "spread": "0.00000000",
                "spread_percentage": "0.00000000"
            },
            "success": true,
            "tick_size": "0.00000001"
        }
        """
        params = {'count': depth}
        if tick_size:
            # Backend expects string format for tick_size usually to preserve precision
            params['tick_size'] = f"{tick_size:.8f}".rstrip('0').rstrip('.')
        return await self._request('GET', f'markets/{market}/orderbook', params=params)

    def _parse_timeframe_ns(self, timeframe: Union[int, str]) -> int:
        """Returns timeframe in Nanoseconds."""
        if isinstance(timeframe, int):
            return timeframe # Assuming input is already NS if int
        
        # Mapping based on Svelte ohlcv.store.svelte.ts
        time_map = {
            '1m': 60_000_000_000,
            '3m': 180_000_000_000,
            '5m': 300_000_000_000,
            '30m': 1_800_000_000_000,
            '2H': 7_200_000_000_000,
            '6H': 21_600_000_000_000,
            '8H': 28_800_000_000_000,
            '12H': 43_200_000_000_000,
            '1D': 86_400_000_000_000,
            '3D': 259_200_000_000_000,
            '1W': 604_800_000_000_000,
            '1M': 2_592_000_000_000_000 
        }
        
        if timeframe in time_map:
            return time_map[timeframe]
            
        # Fallback to simple regex parsing if needed (assuming m, h, d)
        match = re.match(r'^(\d+)([mMhwdy])$', timeframe)
        if match:
            num = int(match.group(1))
            unit = match.group(2)
            # 1 second = 1,000,000,000 ns
            ns = 1_000_000_000
            if unit == 'm': return num * 60 * ns
            elif unit == 'h': return num * 3600 * ns
            elif unit == 'd': return num * 86400 * ns
            elif unit == 'w': return num * 604800 * ns
            
        raise ValueError(f"Invalid timeframe: {timeframe}")

    async def get_ohlcv(self, market: str, start: Optional[int] = None, end: Optional[int] = None, timeframe: Union[int, str] = '1m') -> Dict[str, Any]:
        """
        Get OHLCV (Candlestick) data. 
        Timestamps are in NANOSECONDS.

        Example Response:
        {
            "base_volume": ["0.00000000", ...],
            "close": ["1.00000000", ...],
            "end": "1764962830315160000",
            "high": ["1.00000000", ...],
            "low": ["1.00000000", ...],
            "market": "xno_xbrl",
            "open": ["1.00000000", ...],
            "quote_volume": ["0.00000000", ...],
            "start": "1764962770315160000",
            "timeframe": "60000000000",
            "timestamp": ["1764962770315160000", ...]
        }
        """
        timeframe_ns = self._parse_timeframe_ns(timeframe)
        
        if end is None:
            end = time.time_ns()
            
        if start is None:
            # Default to 1440 candles back
            start = end - (timeframe_ns * 1440)
            if start < 0: start = 0
            
        params = {'start': start, 'end': end, 'timeframe': timeframe_ns}
        return await self._request('GET', f'markets/{market}/ohlcv', params=params)

    # --- PRIVATE ENDPOINTS ---

    async def get_wallets(self, sub_wallet_id: int = 0, get_frozen: bool = False, get_all_frozen: bool = False) -> Dict[str, Any]:
        """
        Get user wallets/balances.

        Example Response:
        {
            "wallets": [
                {
                    "balance": "100.00000000",
                    "instrument": "xbrl",
                    "name": "Iron Ingot",
                    "frozen": "0.00000000" // if requested
                },
                {
                    "balance": "50.00000000",
                    "instrument": "diam",
                    "name": "Diamond",
                    "frozen": "0.00000000"
                }
            ],
            "uuid": "o38rgpvraymd"
        }
        """
        if not self.authenticated:
            raise ValueError("Authentication required.")
        params = {
            'sub_wallet_id': sub_wallet_id,
            'get_frozen': 'true' if get_frozen else 'false',
            'get_all_frozen': 'true' if get_all_frozen else 'false'
        }
        return await self._request('GET', 'wallets', params=params)

    async def get_wallet(self, instrument: str, sub_wallet_id: int = 0) -> Dict[str, Any]:
        """
        Get balance for a specific instrument.

        Example Response:
        {
            "balance": "100.00000000",
            "instrument": "xbrl",
            "name": "Iron Ingot",
            "uuid": "o38rgpvraymd"
        }
        """
        if not self.authenticated:
            raise ValueError("Authentication required.")
        params = {'sub_wallet_id': sub_wallet_id}
        return await self._request('GET', f'wallets/{instrument}', params=params)

    async def get_order(self, order_id: int, get_trades: bool = False) -> Dict[str, Any]:
        """
        Get details of a specific order.

        Example Response:
        {
            "created_at": "1760317035761324000",
            "finalized_at": "1760317383410124000",
            "fulfilled": "3.99500000",
            "fulfilled_percentage": "100.00000000",
            "maker_fee": "0.00000000",
            "market": "wool_iron",
            "order_id": 6,
            "price": "0.25000000",
            "quantity": "3.99500000",
            "remaining": "0.00000000",
            "side": "sell",
            "status": "completed",
            "sub_wallet_id": 0,
            "success": true,
            "taker_fee": "0.00000000",
            "type": "limit",
            "uuid": "o38rgpvraymd"
        }
        """
        if not self.authenticated:
            raise ValueError("Authentication required.")
        # C++ uses 'get_trades', not 'get_transactions'
        params = {'get_trades': 'true' if get_trades else 'false'}
        return await self._request('GET', f'orders/{order_id}', params=params)

    async def get_orders(self, limit: int = 10, cursor: Optional[int] = None, start: int = 0, end: Optional[int] = None, sort_order: str = 'desc',
                   get_trades: bool = False, with_trades_only: bool = False, types: Optional[List[str]] = None,
                   markets: Optional[List[str]] = None, sides: Optional[List[str]] = None, statuses: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get list of orders with optional filters.

        Example Response:
        {
            "core_database_ms": "1",
            "core_database_ns": "1284000",
            "cursor": "9223372036854775807",
            "end": 1764962882448681000,
            "get_transactions": false,
            "limit": 10,
            "markets": ["aapl_iron", ...],
            "next_cursor": "-1",
            "orders": [
                {
                    "created_at": "1760317035761324000",
                    "finalized_at": "1760317383410124000",
                    "fulfilled": "3.99500000",
                    "fulfilled_percentage": "100.00000000",
                    "maker_fee": "0.00000000",
                    "market": "wool_iron",
                    "order_id": 6,
                    "price": "0.25000000",
                    "quantity": "3.99500000",
                    "remaining": "0.00000000",
                    "side": "sell",
                    "status": "completed",
                    "sub_wallet_id": 0,
                    "taker_fee": "0.00000000",
                    "type": "limit"
                }
            ],
            "success": true
        }
        """
        
        if not self.authenticated:
            raise ValueError("Authentication required.")
            
        if end is None:
            end = time.time_ns()
            
        if cursor is None:
            # Handle max int64 limits safely
            cursor = (1 << 63) - 1 if sort_order == 'desc' else 0

        # Construct basic params
        params_dict = {
            'limit': limit,
            'cursor': cursor,
            'start': start,
            'end': end,
            'sort_order': sort_order,
            'get_trades': 'true' if get_trades else 'false',
            'with_trades_only': 'true' if with_trades_only else 'false'
        }

        # Convert to list of tuples to handle array parameters correctly (key=val1&key=val2)
        params_list = list(params_dict.items())

        if types:
            for t in types: params_list.append(('types', t))
        if markets:
            for m in markets: params_list.append(('markets', m))
        if sides:
            for s in sides: params_list.append(('sides', s))
        if statuses:
            for st in statuses: params_list.append(('statuses', st))

        return await self._request('GET', 'orders', params=params_list)

    async def create_order(self, type_: str, market: str, side: str, price: Optional[str] = None, quantity: Optional[str] = None,
                     total: Optional[str] = None, sub_wallet_id: int = 0) -> Dict[str, Any]:
        """
        Create a new limit or market order.

        Example Response (Matches get_order structure):
        {
            "order_id": 7,
            "market": "xno_xbrl",
            "price": "100.00000000",
            "quantity": "1.00000000",
            "status": "open",
            "side": "buy",
            "type": "limit",
            "remaining": "1.00000000",
            "fulfilled": "0.00000000",
            "success": true
        }
        """
        if not self.authenticated:
            raise ValueError("Authentication required.")
        
        if side not in ["buy", "sell"]:
            raise ValueError("Side must be either 'buy' or 'sell'.")
        if type_ not in ["market", "limit"]:
            raise ValueError("Type must be either 'market' or 'limit'.")
            
        market_info = await self._get_market_info(market)
        base_precision = market_info['base_precision']
        quote_precision = market_info['quote_precision']
        min_base_vol = float(market_info['minimum_base_volume'])
        min_quote_vol = float(market_info['minimum_quote_volume'])
        
        order_data = {
            'market': market,
            'side': side,
            'type': type_,
            'sub_wallet_id': sub_wallet_id
        }
        
        if type_ == "limit":
            if not price or not quantity:
                raise ValueError("Price and quantity are required for limit orders.")
            
            validated_price = self.validate_decimal(decimal_str=price, precision=quote_precision)
            validated_quantity = self.validate_decimal(decimal_str=quantity, precision=base_precision)
            
            order_data['price'] = validated_price
            order_data['quantity'] = validated_quantity
            
            total_val = float(validated_price) * float(validated_quantity)
            if total_val < min_quote_vol:
                raise ValueError(f"Total {total_val} below minimum quote volume: {min_quote_vol}")
                
        elif type_ == "market":
            if side == "buy":
                if not total:
                    raise ValueError("Total is required for market buy orders.")
                validated_total = self.validate_decimal(decimal_str=total, precision=quote_precision)
                order_data['total'] = validated_total
                if float(validated_total) < min_quote_vol:
                    raise ValueError(f"Total below minimum quote volume: {min_quote_vol}")
            elif side == "sell":
                if not quantity:
                    raise ValueError("Quantity is required for market sell orders.")
                validated_quantity = self.validate_decimal(decimal_str=quantity, precision=base_precision)
                order_data['quantity'] = validated_quantity
                if float(validated_quantity) < min_base_vol:
                    raise ValueError(f"Quantity below minimum base volume: {min_base_vol}")
                    
        return await self._request('POST', 'orders', json=order_data)

    async def cancel_order(self, order_id: int) -> Dict[str, Any]:
        """
        Cancel a specific order.

        Example Response (Returns order state after cancellation):
        {
            "order_id": 167,
            "status": "cancelled",
            "market": "wool_iron",
            "remaining": "4.00000000",
            "success": true
        }
        """
        if not self.authenticated:
            raise ValueError("Authentication required.")
        # handle_cancel_order in C++ does not take any query params (get_transactions was removed)
        return await self._request('DELETE', f'orders/{order_id}')

    async def cancel_orders(self) -> Dict[str, Any]:
        """
        Cancels ALL open orders.
        Note: The C++ backend 'handle_cancel_orders' does not accept filters (markets/sides).
        It cancels everything for the user.
        """
        if not self.authenticated:
            raise ValueError("Authentication required.")
        return await self._request('DELETE', 'orders')

    async def get_trades(self, limit: int = 10, cursor: Optional[int] = None, start: int = 0, end: Optional[int] = None, sort_order: str = 'desc',
                   types: Optional[List[str]] = None, markets: Optional[List[str]] = None, sides: Optional[List[str]] = None, 
                   statuses: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get user trades (executions).

        Example Response:
        {
            "core_database_ms": "0",
            "core_database_ns": "471000",
            "cursor": "9223372036854775807",
            "end": "1764962959124243000",
            "limit": 10,
            "markets": ["aapl_iron", ...],
            "next_cursor": "-1",
            "previous_cursor": "-1",
            "sides": ["buy", "sell"],
            "sort_order": "desc",
            "start": "0",
            "success": true,
            "trades": [
                {
                    "created_at": "1760317383410112963",
                    "fee": "0.00000000",
                    "id": 3,
                    "market": "wool_iron",
                    "price": "0.25000000",
                    "quantity": "3.99500000",
                    "role": "maker",
                    "side": "sell",
                    "total": "0.99875000"
                }
            ],
            "types": ["limit", "market"],
            "uuid": "o38rgpvraymd"
        }
        """
        
        if not self.authenticated:
            raise ValueError("Authentication required.")
            
        if end is None:
            end = time.time_ns()
            
        if cursor is None:
            cursor = (1 << 63) - 1 if sort_order == 'desc' else 0

        params_dict = {
            'limit': limit,
            'cursor': cursor,
            'start': start,
            'end': end,
            'sort_order': sort_order
        }
        
        params_list = list(params_dict.items())

        if types:
            for t in types: params_list.append(('types', t))
        if markets:
            for m in markets: params_list.append(('markets', m))
        if sides:
            for s in sides: params_list.append(('sides', s))
        if statuses:
            for st in statuses: params_list.append(('statuses', st))

        return await self._request('GET', 'trades', params=params_list)

    async def create_transfer(self, instrument: str, quantity: str, memo: Optional[str] = None,
                        source_sub_wallet_id: int = 0, destination_sub_wallet_id: int = 0) -> Dict[str, Any]:
        """
        Transfer funds BETWEEN the same user's wallets (sub-wallets).
        Use this to move funds from sub_wallet 0 to sub_wallet 1 etc.
        Sub-wallet IDs must be integers between 0 and 16384.

        Example Response:
        {
            "id": 101,
            "source_sub_wallet_id": 0,
            "destination_sub_wallet_id": 1,
            "quantity": "100.00000000",
            "instrument": "xbrl",
            "name": "Iron Ingot",
            "memo": "Savings",
            "source_uuid": "...",
            "destination_uuid": "...",
            "success": true
        }
        """
        if not self.authenticated:
            raise ValueError("Authentication required.")

        if source_sub_wallet_id == destination_sub_wallet_id:
            raise ValueError("Source and destination sub-wallets cannot be the same.")

        max_sub_wallet = 16384
        if source_sub_wallet_id > max_sub_wallet or destination_sub_wallet_id > max_sub_wallet:
            raise ValueError(f"Sub-wallet IDs cannot exceed {max_sub_wallet}.")

        data = {
            'instrument': instrument,
            'quantity': quantity,
            'source_sub_wallet_id': source_sub_wallet_id,
            'destination_sub_wallet_id': destination_sub_wallet_id
        }
        if memo:
            data['memo'] = memo
            
        return await self._request('POST', 'transfers', json=data)

    async def get_transfers(self, limit: int = 10, cursor: Optional[int] = None, start: int = 0, end: Optional[int] = None, sort_order: str = 'desc',
                      sub_wallet_ids: Optional[List[int]] = None, instruments: Optional[List[str]] = None, wallets_id_to_ignore: Optional[List[int]] = [65535]) -> Dict[str, Any]:
        """
        Get transfer history.

        Example Response:
        {
            "limit": 10,
            "cursor": "...",
            "transfers": [
                {
                    "id": 123,
                    "source_user_id": 1,
                    "source_user_uuid": "...",
                    "source_sub_wallet_id": 0,
                    "destination_user_id": 1,
                    "destination_user_uuid": "...",
                    "destination_sub_wallet_id": 1,
                    "quantity": "10.00000000",
                    "instrument": "xbrl",
                    "created_at": "1764693660238985728",
                    "memo": "Savings",
                    "role": "sender"
                }
            ],
            "success": true
        }
        """
        if not self.authenticated:
            raise ValueError("Authentication required.")
            
        if end is None:
            end = time.time_ns()
            
        if cursor is None:
            cursor = (1 << 63) - 1 if sort_order == 'desc' else 0

        params_dict = {
            'limit': limit,
            'cursor': cursor,
            'start': start,
            'end': end,
            'sort_order': sort_order
        }
        
        params_list = list(params_dict.items())
        
        if wallets_id_to_ignore:
            for w in wallets_id_to_ignore: params_list.append(('wallets_id_to_ignore', str(w)))
        if sub_wallet_ids:
            for sid in sub_wallet_ids: params_list.append(('sub_wallet_ids', str(sid)))
        if instruments:
            for inst in instruments: params_list.append(('instruments', inst))
            
        return await self._request('GET', 'transfers', params=params_list)

    async def get_deposits(self, limit: int = 15, cursor: Optional[int] = None, start: int = 0, end: Optional[int] = None, sort_order: str = 'desc',
                     instruments: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get user deposit history.

        Example Response:
        {
            "core_database_ms": "4",
            "core_database_ns": "4295000",
            "cursor": "9223372036854775807",
            "deposits": [
                {
                    "address_id": "",
                    "created_at": "1764693660238985728",
                    "instrument": "xbrl",
                    "memo": "",
                    "quantity": "9.00000000",
                    "tx_id": "4766a3f18bf7272f951fb434d7666760_0"
                }
            ],
            "end": "1764962830315160000",
            "instruments": ["aapl", ...],
            "limit": 10,
            "next_cursor": "263",
            "previous_cursor": "-1",
            "sort_order": "desc",
            "start": "0",
            "success": true,
            "uuid": "o38rgpvraymd"
        }
        """
        if not self.authenticated:
            raise ValueError("Authentication required.")
            
        if end is None:
            end = time.time_ns()
            
        if cursor is None:
            cursor = (1 << 63) - 1 if sort_order == 'desc' else 0
            
        params_dict = {
            'limit': limit,
            'cursor': cursor,
            'start': start,
            'end': end,
            'sort_order': sort_order
        }
        
        params_list = list(params_dict.items())
        
        if instruments:
            for inst in instruments: params_list.append(('instruments', inst))
            
        return await self._request('GET', 'deposits', params=params_list)

    async def get_withdrawals(self, limit: int = 15, cursor: Optional[int] = None, start: int = 0, end: Optional[int] = None, sort_order: str = 'desc',
                        instruments: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get user withdrawal history.

        Example Response:
        {
            "core_database_ms": "0",
            "core_database_ns": "808000",
            "cursor": "9223372036854775807",
            "end": "1764962847331078000",
            "instruments": ["aapl", ...],
            "limit": 10,
            "next_cursor": "518",
            "previous_cursor": "-1",
            "sort_order": "desc",
            "start": "0",
            "success": true,
            "uuid": "o38rgpvraymd",
            "withdrawals": [
                {
                    "address_id": "null",
                    "created_at": "1764715067729991680",
                    "instrument": "cobl",
                    "memo": "null",
                    "quantity": "1.00000000",
                    "tx_id": "b393508b5e2748ef0bfa7f8edd98e0a4e24cc0258faf91e0671fce347bc2d036"
                }
            ]
        }
        """
        if not self.authenticated:
            raise ValueError("Authentication required.")
            
        if end is None:
            end = time.time_ns()
            
        if cursor is None:
            cursor = (1 << 63) - 1 if sort_order == 'desc' else 0
            
        params_dict = {
            'limit': limit,
            'cursor': cursor,
            'start': start,
            'end': end,
            'sort_order': sort_order
        }
        
        params_list = list(params_dict.items())
        
        if instruments:
            for inst in instruments: params_list.append(('instruments', inst))
            
        return await self._request('GET', 'withdrawals', params=params_list)

    async def get_deposits_and_withdrawals(self, limit: int = 15, cursor: Optional[int] = None, start: int = 0, end: Optional[int] = None, sort_order: str = 'desc',
                                     instruments: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get unified history of deposits and withdrawals.

        Example Response:
        {
            "core_database_ms": "4",
            "core_database_ns": "4712000",
            "cursor": "9223372036854775807",
            "deposits_and_withdrawals": [
                {
                    "address_id": "null",
                    "created_at": "1764715067729991680",
                    "instrument": "cobl",
                    "memo": "null",
                    "quantity": "1.00000000",
                    "tx_id": "b393508b5e2748ef0bfa7f8edd98e0a4e24cc0258faf91e0671fce347bc2d036",
                    "type": "withdrawal"
                },
                {
                    "address_id": "",
                    "created_at": "1764693660238985728",
                    "instrument": "xbrl",
                    "memo": "",
                    "quantity": "9.00000000",
                    "tx_id": "4766a3f18bf7272f951fb434d7666760_0",
                    "type": "deposit"
                }
            ],
            "end": "1764962863781891000",
            "instruments": ["aapl", ...],
            "limit": 10,
            "next_cursor": "1764645090541014016",
            "previous_cursor": "-1",
            "sort_order": "desc",
            "start": "0",
            "success": true,
            "uuid": "o38rgpvraymd"
        }
        """
        if not self.authenticated:
            raise ValueError("Authentication required.")
            
        if end is None:
            end = time.time_ns()
            
        if cursor is None:
            cursor = (1 << 63) - 1 if sort_order == 'desc' else 0
            
        params_dict = {
            'limit': limit,
            'cursor': cursor,
            'start': start,
            'end': end,
            'sort_order': sort_order
        }
        
        params_list = list(params_dict.items())
        
        if instruments:
            for inst in instruments: params_list.append(('instruments', inst))
            
        return await self._request('GET', 'deposits-and-withdrawals', params=params_list)