"""
Synchronous Blocky API client using requests.
"""

import re
import time
from typing import Any, Dict, List, Optional, Tuple, Union

import requests

from blocky.exceptions import (
    BlockyAPIError,
    BlockyAuthenticationError,
    BlockyMarketNotFoundError,
    BlockyNetworkError,
    BlockyValidationError,
)
from blocky.utils import (
    DEFAULT_ENDPOINT,
    DEFAULT_TIMEOUT,
    MAX_INT64,
    MAX_SUB_WALLET_ID,
    parse_timeframe_ns,
    validate_decimal,
)


class Blocky:
    """
    Synchronous client for the Blocky Crypto Exchange API.
    
    This client uses the `requests` library for HTTP communication.
    For async operations, use `AsyncBlocky` instead.
    
    Example:
        >>> from blocky import Blocky
        >>> 
        >>> # Public API (no authentication)
        >>> client = Blocky()
        >>> markets = client.get_markets()
        >>> 
        >>> # Private API (requires authentication)
        >>> client = Blocky(api_key="your-api-key")
        >>> wallets = client.get_wallets()
    
    Args:
        api_key: Optional API key for authenticated endpoints.
        endpoint: Base URL for the API (default: https://blocky.com.br/api/v1).
        timeout: Request timeout in seconds (default: 30).
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: str = DEFAULT_ENDPOINT,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        self.api_key = api_key
        self.endpoint = endpoint.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self._markets_cache: Dict[str, Any] = {}
        
        # Set headers
        if self.api_key:
            self.session.headers.update({'x-api-key': self.api_key})
        
        self.authenticated = bool(self.api_key)

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Union[Dict, List[Tuple]]] = None,
        json: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Internal request handler.
        
        Args:
            method: HTTP method (GET, POST, DELETE).
            path: API endpoint path.
            params: Query parameters (dict or list of tuples for array params).
            json: JSON body for POST requests.
            
        Returns:
            API response as dictionary.
            
        Raises:
            BlockyAPIError: On API errors.
            BlockyNetworkError: On network failures.
        """
        url = f"{self.endpoint}/{path}"
        
        try:
            if method == 'GET':
                response = self.session.get(url, params=params, timeout=self.timeout)
            elif method == 'POST':
                response = self.session.post(url, params=params, json=json, timeout=self.timeout)
            elif method == 'DELETE':
                response = self.session.delete(url, params=params, timeout=self.timeout)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            data = response.json()
            
            # Check for API-level errors
            if not data.get('success', False):
                raise BlockyAPIError(
                    data.get('error_message', 'Unknown error'),
                    status_code=response.status_code,
                )
            
            return data
            
        except requests.exceptions.HTTPError as e:
            # Try to extract error message from response
            try:
                if e.response is not None:
                    err_data = e.response.json()
                    if 'error_message' in err_data:
                        if e.response.status_code in (401, 403):
                            raise BlockyAuthenticationError(
                                err_data['error_message'],
                                status_code=e.response.status_code,
                            )
                        raise BlockyAPIError(
                            err_data['error_message'],
                            status_code=e.response.status_code,
                        )
            except (ValueError, AttributeError):
                pass
            raise BlockyAPIError(str(e), status_code=getattr(e.response, 'status_code', None))
            
        except requests.exceptions.RequestException as e:
            raise BlockyNetworkError(f"Network error: {str(e)}")

    def _require_auth(self) -> None:
        """Raise if authentication is not configured."""
        if not self.authenticated:
            raise BlockyAuthenticationError("Authentication required. Provide an API key.")

    def _get_market_info(self, market: str) -> Dict[str, Any]:
        """Get cached market configuration."""
        if not self._markets_cache.get('markets'):
            self._markets_cache = self.get_markets()
        
        for m in self._markets_cache.get('markets', []):
            if m['market'].lower() == market.lower():
                return m
        
        raise BlockyMarketNotFoundError(market)

    # =========================================================================
    # PUBLIC ENDPOINTS
    # =========================================================================

    def get_markets(self, get_tickers: bool = False) -> Dict[str, Any]:
        """
        Retrieve all available markets.
        
        Args:
            get_tickers: If True, includes 24h ticker data for each market.
            
        Returns:
            Dictionary containing list of markets with their configurations.
            
        Example:
            >>> client.get_markets(get_tickers=True)
            {
                'success': True,
                'markets': [
                    {
                        'market': 'diam_iron',
                        'base_instrument': 'diam',
                        'quote_instrument': 'iron',
                        'ticker': {...}  # if get_tickers=True
                    },
                    ...
                ]
            }
        """
        params = {'get_tickers': 'true' if get_tickers else 'false'}
        return self._request('GET', 'markets', params=params)

    def get_market(self, market: str, get_tickers: bool = False) -> Dict[str, Any]:
        """
        Retrieve a specific market configuration.
        
        Args:
            market: Market symbol (e.g., 'diam_iron').
            get_tickers: If True, includes 24h ticker data.
            
        Returns:
            Market configuration dictionary.
        """
        params = {'get_tickers': 'true' if get_tickers else 'false'}
        return self._request('GET', f'markets/{market}', params=params)

    def get_ticker(self, market: str) -> Dict[str, Any]:
        """
        Get 24-hour ticker statistics for a market.
        
        Args:
            market: Market symbol (e.g., 'diam_iron').
            
        Returns:
            Ticker data with open, high, low, close, volume, and change.
        """
        return self._request('GET', f'markets/{market}/ticker')

    def get_transactions(self, market: str, count: int = 128) -> Dict[str, Any]:
        """
        Get recent public trades for a market.
        
        Args:
            market: Market symbol.
            count: Number of transactions to retrieve (default: 128, max: 1024).
            
        Returns:
            Dictionary with list of recent transactions.
        """
        params = {'count': count}
        return self._request('GET', f'markets/{market}/transactions', params=params)

    def get_orderbook(
        self,
        market: str,
        depth: int = 0,
        tick_size: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Fetch the orderbook for a market.
        
        Args:
            market: Market symbol.
            depth: Number of price levels (0 = all).
            tick_size: Optional price aggregation level.
            
        Returns:
            Orderbook with bids and asks arrays.
        """
        params: Dict[str, Any] = {'depth': depth}
        if tick_size:
            params['tick_size'] = f"{tick_size:.8f}".rstrip('0').rstrip('.')
        return self._request('GET', f'markets/{market}/orderbook', params=params)

    def get_ohlcv(
        self,
        market: str,
        start: Optional[int] = None,
        end: Optional[int] = None,
        timeframe: Union[int, str] = '1m',
    ) -> Dict[str, Any]:
        """
        Get OHLCV (candlestick) data.
        
        Args:
            market: Market symbol.
            start: Start timestamp in nanoseconds (default: 1440 candles ago).
            end: End timestamp in nanoseconds (default: now).
            timeframe: Candle interval (e.g., '1m', '1H', '1D', or nanoseconds).
            
        Returns:
            OHLCV data with timestamp, open, high, low, close, and volume arrays.
        """
        timeframe_ns = parse_timeframe_ns(timeframe)
        
        if end is None:
            end = time.time_ns()
        if start is None:
            start = max(0, end - (timeframe_ns * 1440))
        
        params = {'start': start, 'end': end, 'timeframe': timeframe_ns}
        return self._request('GET', f'markets/{market}/ohlcv', params=params)

    # =========================================================================
    # PRIVATE ENDPOINTS - WALLETS
    # =========================================================================

    def get_wallets(
        self,
        sub_wallet_id: int = 0,
        get_frozen: bool = False,
        get_all_frozen: bool = False,
    ) -> Dict[str, Any]:
        """
        Get all wallet balances.
        
        Args:
            sub_wallet_id: Sub-wallet to query (default: 0).
            get_frozen: Include frozen balance for the queried sub-wallet.
            get_all_frozen: Include frozen balances across all sub-wallets.
            
        Returns:
            Dictionary with wallet balances.
            
        Raises:
            BlockyAuthenticationError: If not authenticated.
        """
        self._require_auth()
        params = {
            'sub_wallet_id': sub_wallet_id,
            'get_frozen': 'true' if get_frozen else 'false',
            'get_all_frozen': 'true' if get_all_frozen else 'false',
        }
        return self._request('GET', 'wallets', params=params)

    def get_wallet(self, instrument: str, sub_wallet_id: int = 0) -> Dict[str, Any]:
        """
        Get balance for a specific instrument.
        
        Args:
            instrument: Instrument symbol (e.g., 'iron').
            sub_wallet_id: Sub-wallet to query.
            
        Returns:
            Wallet balance for the instrument.
            
        Raises:
            BlockyAuthenticationError: If not authenticated.
        """
        self._require_auth()
        params = {'sub_wallet_id': sub_wallet_id}
        return self._request('GET', f'wallets/{instrument}', params=params)

    # =========================================================================
    # PRIVATE ENDPOINTS - ORDERS
    # =========================================================================

    def get_order(self, order_id: int, get_trades: bool = False) -> Dict[str, Any]:
        """
        Get details of a specific order.
        
        Args:
            order_id: The order ID.
            get_trades: Include associated trades.
            
        Returns:
            Order details.
            
        Raises:
            BlockyAuthenticationError: If not authenticated.
        """
        self._require_auth()
        params = {'get_trades': 'true' if get_trades else 'false'}
        return self._request('GET', f'orders/{order_id}', params=params)

    def get_orders(
        self,
        limit: int = 10,
        cursor: Optional[int] = None,
        start: int = 0,
        end: Optional[int] = None,
        sort_order: str = 'desc',
        get_trades: bool = False,
        with_trades_only: bool = False,
        types: Optional[List[str]] = None,
        markets: Optional[List[str]] = None,
        sides: Optional[List[str]] = None,
        statuses: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Get list of orders with optional filters.
        
        Args:
            limit: Maximum number of orders to return.
            cursor: Pagination cursor.
            start: Start timestamp in nanoseconds.
            end: End timestamp in nanoseconds.
            sort_order: 'asc' or 'desc'.
            get_trades: Include trades for each order.
            with_trades_only: Only return orders that have trades.
            types: Filter by order types ('limit', 'market').
            markets: Filter by market symbols.
            sides: Filter by sides ('buy', 'sell').
            statuses: Filter by statuses ('open', 'completed', 'cancelled').
            
        Returns:
            Dictionary with orders list and pagination info.
            
        Raises:
            BlockyAuthenticationError: If not authenticated.
        """
        self._require_auth()
        
        if end is None:
            end = time.time_ns()
        if cursor is None:
            cursor = MAX_INT64 if sort_order == 'desc' else 0

        params_list: List[Tuple[str, Any]] = [
            ('limit', limit),
            ('cursor', cursor),
            ('start', start),
            ('end', end),
            ('sort_order', sort_order),
            ('get_trades', 'true' if get_trades else 'false'),
            ('with_trades_only', 'true' if with_trades_only else 'false'),
        ]

        if types:
            for t in types:
                params_list.append(('types', t))
        if markets:
            for m in markets:
                params_list.append(('markets', m))
        if sides:
            for s in sides:
                params_list.append(('sides', s))
        if statuses:
            for st in statuses:
                params_list.append(('statuses', st))

        return self._request('GET', 'orders', params=params_list)

    def create_order(
        self,
        type_: str,
        market: str,
        side: str,
        price: Optional[str] = None,
        quantity: Optional[str] = None,
        total: Optional[str] = None,
        sub_wallet_id: int = 0,
    ) -> Dict[str, Any]:
        """
        Create a new limit or market order.
        
        Args:
            type_: Order type ('limit' or 'market').
            market: Market symbol (e.g., 'diam_iron').
            side: Order side ('buy' or 'sell').
            price: Price for limit orders.
            quantity: Quantity for limit orders and market sell orders.
            total: Total spend for market buy orders.
            sub_wallet_id: Sub-wallet to use for the order.
            
        Returns:
            Created order details.
            
        Raises:
            BlockyAuthenticationError: If not authenticated.
            BlockyValidationError: If order parameters are invalid.
            
        Example:
            >>> # Limit buy order
            >>> client.create_order('limit', 'diam_iron', 'buy', price='100', quantity='1')
            >>> 
            >>> # Market buy order (specify total to spend)
            >>> client.create_order('market', 'diam_iron', 'buy', total='10')
            >>> 
            >>> # Market sell order (specify quantity to sell)
            >>> client.create_order('market', 'diam_iron', 'sell', quantity='5')
        """
        self._require_auth()
        
        if side not in ('buy', 'sell'):
            raise BlockyValidationError("Side must be 'buy' or 'sell'.")
        if type_ not in ('market', 'limit'):
            raise BlockyValidationError("Type must be 'market' or 'limit'.")
        
        market_info = self._get_market_info(market)
        base_precision = market_info['base_precision']
        quote_precision = market_info['quote_precision']
        min_base_vol = float(market_info['minimum_base_volume'])
        min_quote_vol = float(market_info['minimum_quote_volume'])
        
        order_data: Dict[str, Any] = {
            'market': market,
            'side': side,
            'type': type_,
            'sub_wallet_id': sub_wallet_id,
        }
        
        if type_ == 'limit':
            if not price or not quantity:
                raise BlockyValidationError("Price and quantity are required for limit orders.")
            
            validated_price = validate_decimal(price, precision=quote_precision)
            validated_quantity = validate_decimal(quantity, precision=base_precision)
            
            order_data['price'] = validated_price
            order_data['quantity'] = validated_quantity
            
            total_val = float(validated_price) * float(validated_quantity)
            if total_val < min_quote_vol:
                raise BlockyValidationError(
                    f"Order total ({total_val}) below minimum quote volume ({min_quote_vol})."
                )
                
        elif type_ == 'market':
            if side == 'buy':
                if not total:
                    raise BlockyValidationError("Total is required for market buy orders.")
                validated_total = validate_decimal(total, precision=quote_precision)
                order_data['total'] = validated_total
                if float(validated_total) < min_quote_vol:
                    raise BlockyValidationError(
                        f"Total ({validated_total}) below minimum quote volume ({min_quote_vol})."
                    )
            else:  # sell
                if not quantity:
                    raise BlockyValidationError("Quantity is required for market sell orders.")
                validated_quantity = validate_decimal(quantity, precision=base_precision)
                order_data['quantity'] = validated_quantity
                if float(validated_quantity) < min_base_vol:
                    raise BlockyValidationError(
                        f"Quantity ({validated_quantity}) below minimum base volume ({min_base_vol})."
                    )
        
        return self._request('POST', 'orders', json=order_data)

    def cancel_order(self, order_id: int, get_trades: bool = False) -> Dict[str, Any]:
        """
        Cancel a specific order.
        
        Args:
            order_id: The order ID to cancel.
            get_trades: If True, include the trades array for the cancelled order.
            
        Returns:
            Cancelled order details, optionally with trades.
            
        Raises:
            BlockyAuthenticationError: If not authenticated.
        """
        self._require_auth()
        params: Dict[str, Any] = {}
        if get_trades:
            params['get_trades'] = 'true'
        return self._request('DELETE', f'orders/{order_id}', params=params if params else None)

    def cancel_orders(
        self,
        markets: Optional[List[str]] = None,
        sides: Optional[List[str]] = None,
        get_trades: bool = False,
    ) -> Dict[str, Any]:
        """
        Cancel open orders with optional filters.
        
        Args:
            markets: List of market symbols to cancel orders for (default: all markets).
            sides: List of sides to cancel ('buy', 'sell') (default: both).
            get_trades: If True, include trades array for each cancelled order.
            
        Returns:
            Result with 'orders' array containing cancelled orders.
            
        Raises:
            BlockyAuthenticationError: If not authenticated.
            
        Example:
            >>> # Cancel all orders for a specific market
            >>> client.cancel_orders(markets=['diam_iron'])
            >>> 
            >>> # Cancel only sell orders across all markets
            >>> client.cancel_orders(sides=['sell'])
            >>> 
            >>> # Cancel all orders (no filters)
            >>> client.cancel_orders()
        """
        self._require_auth()
        
        params_list: List[Tuple[str, Any]] = []
        
        if get_trades:
            params_list.append(('get_trades', 'true'))
        if markets:
            for m in markets:
                params_list.append(('markets', m))
        if sides:
            for s in sides:
                params_list.append(('sides', s))
        
        return self._request('DELETE', 'orders', params=params_list if params_list else None)

    # =========================================================================
    # PRIVATE ENDPOINTS - TRADES
    # =========================================================================

    def get_trades(
        self,
        limit: int = 10,
        cursor: Optional[int] = None,
        start: int = 0,
        end: Optional[int] = None,
        sort_order: str = 'desc',
        types: Optional[List[str]] = None,
        markets: Optional[List[str]] = None,
        sides: Optional[List[str]] = None,
        statuses: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Get user trade history (executions).
        
        Args:
            limit: Maximum number of trades to return.
            cursor: Pagination cursor.
            start: Start timestamp in nanoseconds.
            end: End timestamp in nanoseconds.
            sort_order: 'asc' or 'desc'.
            types: Filter by order types.
            markets: Filter by market symbols.
            sides: Filter by sides.
            statuses: Filter by statuses.
            
        Returns:
            Dictionary with trades list and pagination info.
            
        Raises:
            BlockyAuthenticationError: If not authenticated.
        """
        self._require_auth()
        
        if end is None:
            end = time.time_ns()
        if cursor is None:
            cursor = MAX_INT64 if sort_order == 'desc' else 0

        params_list: List[Tuple[str, Any]] = [
            ('limit', limit),
            ('cursor', cursor),
            ('start', start),
            ('end', end),
            ('sort_order', sort_order),
        ]

        if types:
            for t in types:
                params_list.append(('types', t))
        if markets:
            for m in markets:
                params_list.append(('markets', m))
        if sides:
            for s in sides:
                params_list.append(('sides', s))
        if statuses:
            for st in statuses:
                params_list.append(('statuses', st))

        return self._request('GET', 'trades', params=params_list)

    # =========================================================================
    # PRIVATE ENDPOINTS - TRANSFERS
    # =========================================================================

    def create_transfer(
        self,
        instrument: str,
        quantity: str,
        memo: Optional[str] = None,
        source_sub_wallet_id: int = 0,
        destination_sub_wallet_id: int = 0,
    ) -> Dict[str, Any]:
        """
        Transfer funds between your own sub-wallets.
        
        Args:
            instrument: Instrument to transfer (e.g., 'iron').
            quantity: Amount to transfer.
            memo: Optional memo/note.
            source_sub_wallet_id: Source sub-wallet ID (0-16384).
            destination_sub_wallet_id: Destination sub-wallet ID (0-16384).
            
        Returns:
            Transfer result details.
            
        Raises:
            BlockyAuthenticationError: If not authenticated.
            BlockyValidationError: If transfer parameters are invalid.
        """
        self._require_auth()
        
        if source_sub_wallet_id == destination_sub_wallet_id:
            raise BlockyValidationError("Source and destination sub-wallets cannot be the same.")
        
        if source_sub_wallet_id > MAX_SUB_WALLET_ID or destination_sub_wallet_id > MAX_SUB_WALLET_ID:
            raise BlockyValidationError(f"Sub-wallet IDs cannot exceed {MAX_SUB_WALLET_ID}.")
        
        data: Dict[str, Any] = {
            'instrument': instrument,
            'quantity': quantity,
            'source_sub_wallet_id': source_sub_wallet_id,
            'destination_sub_wallet_id': destination_sub_wallet_id,
        }
        if memo:
            data['memo'] = memo
        
        return self._request('POST', 'transfers', json=data)

    def get_transfers(
        self,
        limit: int = 10,
        cursor: Optional[int] = None,
        start: int = 0,
        end: Optional[int] = None,
        sort_order: str = 'desc',
        sub_wallet_ids: Optional[List[int]] = None,
        instruments: Optional[List[str]] = None,
        wallets_id_to_ignore: Optional[List[int]] = None,
    ) -> Dict[str, Any]:
        """
        Get transfer history.
        
        Args:
            limit: Maximum number of transfers to return.
            cursor: Pagination cursor.
            start: Start timestamp in nanoseconds.
            end: End timestamp in nanoseconds.
            sort_order: 'asc' or 'desc'.
            sub_wallet_ids: Filter by sub-wallet IDs.
            instruments: Filter by instruments.
            wallets_id_to_ignore: Sub-wallet IDs to exclude.
            
        Returns:
            Dictionary with transfers list and pagination info.
            
        Raises:
            BlockyAuthenticationError: If not authenticated.
        """
        self._require_auth()
        
        if end is None:
            end = time.time_ns()
        if cursor is None:
            cursor = MAX_INT64 if sort_order == 'desc' else 0
        if wallets_id_to_ignore is None:
            wallets_id_to_ignore = [65535]

        params_list: List[Tuple[str, Any]] = [
            ('limit', limit),
            ('cursor', cursor),
            ('start', start),
            ('end', end),
            ('sort_order', sort_order),
        ]

        for w in wallets_id_to_ignore:
            params_list.append(('wallets_id_to_ignore', str(w)))
        if sub_wallet_ids:
            for sid in sub_wallet_ids:
                params_list.append(('sub_wallet_ids', str(sid)))
        if instruments:
            for inst in instruments:
                params_list.append(('instruments', inst))

        return self._request('GET', 'transfers', params=params_list)

    # =========================================================================
    # PRIVATE ENDPOINTS - DEPOSITS & WITHDRAWALS
    # =========================================================================

    def get_deposits(
        self,
        limit: int = 15,
        cursor: Optional[int] = None,
        start: int = 0,
        end: Optional[int] = None,
        sort_order: str = 'desc',
        instruments: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Get deposit history.
        
        Args:
            limit: Maximum number of deposits to return.
            cursor: Pagination cursor.
            start: Start timestamp in nanoseconds.
            end: End timestamp in nanoseconds.
            sort_order: 'asc' or 'desc'.
            instruments: Filter by instruments.
            
        Returns:
            Dictionary with deposits list and pagination info.
            
        Raises:
            BlockyAuthenticationError: If not authenticated.
        """
        self._require_auth()
        
        if end is None:
            end = time.time_ns()
        if cursor is None:
            cursor = MAX_INT64 if sort_order == 'desc' else 0

        params_list: List[Tuple[str, Any]] = [
            ('limit', limit),
            ('cursor', cursor),
            ('start', start),
            ('end', end),
            ('sort_order', sort_order),
        ]

        if instruments:
            for inst in instruments:
                params_list.append(('instruments', inst))

        return self._request('GET', 'deposits', params=params_list)

    def get_withdrawals(
        self,
        limit: int = 15,
        cursor: Optional[int] = None,
        start: int = 0,
        end: Optional[int] = None,
        sort_order: str = 'desc',
        instruments: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Get withdrawal history.
        
        Args:
            limit: Maximum number of withdrawals to return.
            cursor: Pagination cursor.
            start: Start timestamp in nanoseconds.
            end: End timestamp in nanoseconds.
            sort_order: 'asc' or 'desc'.
            instruments: Filter by instruments.
            
        Returns:
            Dictionary with withdrawals list and pagination info.
            
        Raises:
            BlockyAuthenticationError: If not authenticated.
        """
        self._require_auth()
        
        if end is None:
            end = time.time_ns()
        if cursor is None:
            cursor = MAX_INT64 if sort_order == 'desc' else 0

        params_list: List[Tuple[str, Any]] = [
            ('limit', limit),
            ('cursor', cursor),
            ('start', start),
            ('end', end),
            ('sort_order', sort_order),
        ]

        if instruments:
            for inst in instruments:
                params_list.append(('instruments', inst))

        return self._request('GET', 'withdrawals', params=params_list)

    def get_deposits_and_withdrawals(
        self,
        limit: int = 15,
        cursor: Optional[int] = None,
        start: int = 0,
        end: Optional[int] = None,
        sort_order: str = 'desc',
        instruments: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Get unified history of deposits and withdrawals.
        
        Args:
            limit: Maximum number of records to return.
            cursor: Pagination cursor.
            start: Start timestamp in nanoseconds.
            end: End timestamp in nanoseconds.
            sort_order: 'asc' or 'desc'.
            instruments: Filter by instruments.
            
        Returns:
            Dictionary with combined deposits and withdrawals list.
            
        Raises:
            BlockyAuthenticationError: If not authenticated.
        """
        self._require_auth()
        
        if end is None:
            end = time.time_ns()
        if cursor is None:
            cursor = MAX_INT64 if sort_order == 'desc' else 0

        params_list: List[Tuple[str, Any]] = [
            ('limit', limit),
            ('cursor', cursor),
            ('start', start),
            ('end', end),
            ('sort_order', sort_order),
        ]

        if instruments:
            for inst in instruments:
                params_list.append(('instruments', inst))

        return self._request('GET', 'deposits-and-withdrawals', params=params_list)
