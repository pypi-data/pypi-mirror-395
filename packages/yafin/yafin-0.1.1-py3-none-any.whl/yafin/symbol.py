import logging
from types import TracebackType
from typing import Any, Literal, Self, overload

from .client import (
    AsyncClient,
    Client,
    _SingletonAsyncClientManager,
    _SingletonClientManager,
)
from .const import _RESULT_KEY_MAP, QUOTE_SUMMARY_MODULES
from .utils import _alog_func, _log_func, get_types_with_frequency

logger = logging.getLogger(__name__)


class SymbolBase:
    """Base for synchronous and asynchronous Symbol classes for a specific ticker.

    Attributes:
        ticker: Ticker symbol.
    """

    _TICKER_KEY_MAP = {
        'get_chart': 'ticker',
        'get_quote': 'tickers',
        'get_quote_type': 'tickers',
        'get_quote_summary': 'ticker',
        'get_timeseries': 'ticker',
        'get_options': 'ticker',
        'get_search': 'tickers',
        'get_recommendations': 'tickers',
        'get_insights': 'tickers',
        'get_ratings': 'ticker',
    }

    def __init__(self, ticker: str) -> None:
        """Create new Symbol instance.

        Args:
            ticker: Ticker symbol.
        """
        self.ticker = ticker


class Symbol(SymbolBase):
    """Symbol class for a specific ticker.

    Warning: HTTP resources closing
        Uses http resources, so do not forget to close them after use to avoid resource
            leakage or use context manager.

    Attributes:
        ticker: Ticker symbol.
        _client:
            Client instance, that is used for all http requests.
                (Is lazily initialized.)

    Methods:
        get_chart: Get chart data for the ticker.
        get_quote: Get quote for the ticker.
        get_quote_type: Get quote type for the ticker.
        get_quote_summary_all_modules: Get quote summary for all modules for the ticker.
        get_asset_profile: Get asset profile for the ticker.
        get_summary_profile: Get summary profile for the ticker.
        get_summary_detail: Get summary detail for the ticker.
        get_price: Get price data for the ticker.
        get_default_key_statistics: Get default key statistics for the ticker.
        get_financial_data: Get financial data for the ticker.
        get_calendar_events: Get calendar events for the ticker.
        get_sec_filings: Get sec filings for the ticker.
        get_upgrade_downgrade_history: Get upgrade downgrade history for the ticker.
        get_institution_ownership: Get institution ownership for the ticker.
        get_fund_ownership: Get fund ownership for the ticker.
        get_major_direct_holders: Get major direct holders for the ticker.
        get_major_holders_breakdown: Get major holders breakdown for the ticker.
        get_insider_transactions: Get insider transactions for the ticker.
        get_insider_holders: Get insider holders for the ticker.
        get_net_share_purchase_activity: Get net share purchase activity for the ticker.
        get_earnings: Get earnings for the ticker.
        get_earnings_history: Get earnings history for the ticker.
        get_earnings_trend: Get earnings trend for the ticker.
        get_industry_trend: Get industry trend for the ticker.
        get_index_trend: Get index trend for the ticker.
        get_sector_trend: Get sector trend for the ticker.
        get_recommendation_trend: Get recommendation trend for the ticker.
        get_page_views: Get page views for the ticker.
        get_income_statement: Get income statement for the ticker.
        get_balance_sheet: Get balance sheet for the ticker.
        get_cash_flow: Get cash flow statement for the ticker.
        get_options: Get options data for the ticker.
        get_search: Get search results for the ticker.
        get_recommendations: Get analyst recommendations for the ticker.
        get_insights: Get insights for the ticker.
        get_ratings: Get ratings for the ticker.
    """

    def __init__(self, ticker: str) -> None:
        """Create new Symbol instance.

        Args:
            ticker: Ticker symbol.
        """
        super().__init__(ticker)
        self._client: Client | None = None

    def _get_client(self) -> None:
        if self._client is None:
            self._client = _SingletonClientManager._get_client()

    def close(self) -> None:
        """Release the client if open for current symbol.

        Note:
            Only if no other symbols are using the client singleton, is the client
                closed.
        """
        if self._client is not None:
            _SingletonClientManager._release_client()
            self._client = None

    def __enter__(self) -> Self:
        """When entering context manager, get the client."""
        self._get_client()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> None:
        """When closing context manager, release the client."""
        self.close()

    @overload
    def _call_client_method(
        self,
        method_name: Literal['get_search', 'get_ratings'],
        kwargs: dict[str, Any] | None = None,
    ) -> dict[str, Any]: ...

    @overload
    def _call_client_method(
        self, method_name: str, kwargs: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]: ...

    def _call_client_method(
        self, method_name: str, kwargs: dict[str, Any] | None = None
    ) -> list[dict[str, Any]] | dict[str, Any]:
        # not using use *args, **kwargs, to be compatible with
        # Symbols._call_client_method

        kwargs = kwargs or {}
        ticker_key = self._TICKER_KEY_MAP[method_name]

        if ticker_key:
            kwargs[ticker_key] = self.ticker

        result_key = _RESULT_KEY_MAP.get(method_name)

        self._get_client()
        method = getattr(self._client, method_name)
        response_json = method(**kwargs)

        # search does not have result key
        return response_json[result_key]['result'] if result_key else response_json

    @_log_func
    def get_chart(
        self,
        interval: str,
        period_range: str | None = None,
        period1: int | float | None = None,
        period2: int | float | None = None,
        include_pre_post: bool | None = None,
        include_div: bool = True,
        include_split: bool = True,
        include_earn: bool = True,
        include_capital_gain: bool = True,
    ) -> dict[str, Any]:
        """Get chart data for the ticker.

        Args:
            interval: Data interval.
            period_range: Range of the period.
            period1: Start timestamp in seconds. (optional, default: None)
            period2: End timestamp in seconds. (optional, default: None)
            include_pre_post: Whether to include pre and post market.
            include_div: Whether to include dividends.
            include_split: Whether to include stock splits.
            include_earn: Whether to include earnings.
            include_capital_gain: Whether to include capital gains.

        Returns: Chart response result json.

        Note:
            Even though the the endpoint param is called range, period_range was chosen
            to avoid collision with python built-in method name.
        """
        kwargs: dict[str, Any] = {'interval': interval}

        if period_range is not None:
            kwargs['period_range'] = period_range

        if period1 is not None:
            kwargs['period1'] = period1

        if period2 is not None:
            kwargs['period2'] = period2

        if include_pre_post is not None:
            kwargs['include_pre_post'] = include_pre_post

        events_list = []

        if include_div:
            events_list.append('div')

        if include_split:
            events_list.append('split')

        if include_earn:
            events_list.append('earn')

        if include_capital_gain:
            events_list.append('capitalGain')

        if events_list:
            kwargs['events'] = ','.join(events_list)

        chart_result_list = self._call_client_method('get_chart', kwargs)
        return chart_result_list[0]

    @_log_func
    def get_quote(self, include_pre_post: bool | None = None) -> dict[str, Any]:
        """Get quote for the ticker.

        Args:
            include_pre_post: Whether to include pre and post market.

        Returns: Quote response result json.
        """
        kwargs = (
            {'include_pre_post': include_pre_post}
            if include_pre_post is not None
            else {}
        )
        quote_result_list = self._call_client_method('get_quote', kwargs)
        return quote_result_list[0]

    @_log_func
    def get_quote_type(self) -> dict[str, Any]:
        """Get quote type for the ticker.

        Returns: Quote type response result json.
        """
        quote_type_result_list = self._call_client_method('get_quote_type')
        return quote_type_result_list[0]

    @_log_func
    def get_quote_summary_all_modules(self) -> dict[str, Any]:
        """Get quote summary for all modules for the ticker.

        Returns: Quote summary with all modules response result json.
        """
        kwargs: dict[str, Any] = {'modules': QUOTE_SUMMARY_MODULES}
        quote_summary_result_list = self._call_client_method(
            'get_quote_summary', kwargs
        )
        return quote_summary_result_list[0]

    @_log_func
    def _get_quote_summary_single_module(self, module: str) -> dict[str, Any]:
        kwargs: dict[str, Any] = {'modules': module}
        quote_summary_result_list = self._call_client_method(
            'get_quote_summary', kwargs
        )
        return quote_summary_result_list[0][module]

    @_log_func
    def get_asset_profile(self) -> dict[str, Any]:
        """Get asset profile for the ticker.

        Returns: Quote summary with asset profile module response result json.
        """
        return self._get_quote_summary_single_module('assetProfile')

    @_log_func
    def get_summary_profile(self) -> dict[str, Any]:
        """Get summary profile for the ticker.

        Returns: Quote summary with summary profile module response result json.
        """
        return self._get_quote_summary_single_module('summaryProfile')

    @_log_func
    def get_summary_detail(self) -> dict[str, Any]:
        """Get summary detail for the ticker.

        Returns: Quote summary with summary detail module response result json.
        """
        return self._get_quote_summary_single_module('summaryDetail')

    @_log_func
    def get_price(self) -> dict[str, Any]:
        """Get price data for the ticker.

        Returns: Quote summary with price data module response result json.
        """
        return self._get_quote_summary_single_module('price')

    @_log_func
    def get_default_key_statistics(self) -> dict[str, Any]:
        """Get default key statistics for the ticker.

        Returns: Quote summary with default key statistics module response result json.
        """
        return self._get_quote_summary_single_module('defaultKeyStatistics')

    @_log_func
    def get_financial_data(self) -> dict[str, Any]:
        """Get financial data for the ticker.

        Returns: Quote summary with financial data module response result json.
        """
        return self._get_quote_summary_single_module('financialData')

    @_log_func
    def get_calendar_events(self) -> dict[str, Any]:
        """Get calendar events for the ticker.

        Returns: Quote summary with calendar events module response result json.
        """
        return self._get_quote_summary_single_module('calendarEvents')

    @_log_func
    def get_sec_filings(self) -> dict[str, Any]:
        """Get sec filings for the ticker.

        Returns: Quote summary with sec filings module response result json.
        """
        return self._get_quote_summary_single_module('secFilings')

    @_log_func
    def get_upgrade_downgrade_history(self) -> list[dict[str, Any]]:
        """Get upgrade downgrade history for the ticker.

        Returns:
            Quote summary with upgrade downgrade history module response results
                json.
        """
        result = self._get_quote_summary_single_module('upgradeDowngradeHistory')
        return result['history']

    @_log_func
    def get_institution_ownership(self) -> list[dict[str, Any]]:
        """Get institution ownership for the ticker.

        Returns: Quote summary with institution ownership module response results json.
        """
        result = self._get_quote_summary_single_module('institutionOwnership')
        return result['ownershipList']

    @_log_func
    def get_fund_ownership(self) -> list[dict[str, Any]]:
        """Get fund ownership for the ticker.

        Returns: Quote summary with fund ownership module response results json.
        """
        result = self._get_quote_summary_single_module('fundOwnership')
        return result['ownershipList']

    @_log_func
    def get_major_direct_holders(self) -> dict[str, Any]:
        """Get major direct holders for the ticker.

        Returns: Quote summary with direct holders module response result json.
        """
        return self._get_quote_summary_single_module('majorDirectHolders')

    @_log_func
    def get_major_holders_breakdown(self) -> dict[str, Any]:
        """Get major holders breakdown for the ticker.

        Returns: Quote summary with holders breakdown module response result json.
        """
        return self._get_quote_summary_single_module('majorHoldersBreakdown')

    @_log_func
    def get_insider_transactions(self) -> list[dict[str, Any]]:
        """Get insider transactions for the ticker.

        Returns: Quote summary with insider transactions module response results json.
        """
        result = self._get_quote_summary_single_module('insiderTransactions')
        return result['transactions']

    @_log_func
    def get_insider_holders(self) -> list[dict[str, Any]]:
        """Get insider holders for the ticker.

        Returns: Quote summary with insider holders module response results json.
        """
        result = self._get_quote_summary_single_module('insiderHolders')
        return result['holders']

    @_log_func
    def get_net_share_purchase_activity(self) -> dict[str, Any]:
        """Get net share purchase activity for the ticker.

        Returns:
            Quote summary with net share purchase activity module response result
                json.
        """
        return self._get_quote_summary_single_module('netSharePurchaseActivity')

    @_log_func
    def get_earnings(self) -> dict[str, Any]:
        """Get earnings for the ticker.

        Returns: Quote summary with earnings module response result json.
        """
        return self._get_quote_summary_single_module('earnings')

    @_log_func
    def get_earnings_history(self) -> list[dict[str, Any]]:
        """Get earnings history for the ticker.

        Returns: Quote summary with earnings history module response results json.
        """
        result = self._get_quote_summary_single_module('earningsHistory')
        return result['history']

    @_log_func
    def get_earnings_trend(self) -> list[dict[str, Any]]:
        """Get earnings trend for the ticker.

        Returns: Quote summary with earnings trend module response results json.
        """
        result = self._get_quote_summary_single_module('earningsTrend')
        return result['trend']

    @_log_func
    def get_industry_trend(self) -> dict[str, Any]:
        """Get industry trend for the ticker.

        Returns: Quote summary with industry trend module response result json.
        """
        return self._get_quote_summary_single_module('industryTrend')

    @_log_func
    def get_index_trend(self) -> dict[str, Any]:
        """Get index trend for the ticker.

        Returns: Quote summary with index trend module response result json.
        """
        return self._get_quote_summary_single_module('indexTrend')

    @_log_func
    def get_sector_trend(self) -> dict[str, Any]:
        """Get sector trend for the ticker.

        Returns: Quote summary with sector trend module response result json.
        """
        return self._get_quote_summary_single_module('sectorTrend')

    @_log_func
    def get_recommendation_trend(self) -> list[dict[str, Any]]:
        """Get recommendation trend for the ticker.

        Returns: Quote summary with recommendation trend module response results json.
        """
        result = self._get_quote_summary_single_module('recommendationTrend')
        return result['trend']

    @_log_func
    def get_page_views(self) -> dict[str, Any]:
        """Get page views for the ticker.

        Returns: Quote summary with page views module response result json.
        """
        return self._get_quote_summary_single_module('pageViews')

    @_log_func
    def _get_financials(
        self,
        frequency: str,
        typ: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[dict[str, Any]]:
        kwargs: dict[str, Any] = {
            'types': get_types_with_frequency(typ, frequency),
            'period1': period1,
            'period2': period2,
        }
        return self._call_client_method('get_timeseries', kwargs)

    @_log_func
    def get_income_statement(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[dict[str, Any]]:
        """Get income statement for the ticker.

        Args:
            frequency: annual, quarterly or trailing.
            period1:
                Start timestamp in seconds. (optional, default: 1st Jan 2020 timestamp)
            period2: End timestamp in seconds. (optional, default: now timestamp)

        Returns: Income statement response results json.
        """
        return self._get_financials(frequency, 'income_statement', period1, period2)

    @_log_func
    def get_balance_sheet(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[dict[str, Any]]:
        """Get balance sheet for the ticker.

        Args:
            frequency: annual, quarterly or trailing.
            period1:
                Start timestamp in seconds. (optional, default: 1st Jan 2020 timestamp)
            period2: End timestamp in seconds. (optional, default: now timestamp)

        Returns: Balance sheet response results json.
        """
        return self._get_financials(frequency, 'balance_sheet', period1, period2)

    @_log_func
    def get_cash_flow(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[dict[str, Any]]:
        """Get cash flow statement for the ticker.

        Args:
            frequency: annual, quarterly or trailing.
            period1:
                Start timestamp in seconds. (optional, default: 1st Jan 2020 timestamp)
            period2: End timestamp in seconds. (optional, default: now timestamp)

        Returns: Cash flow response results json.
        """
        return self._get_financials(frequency, 'cash_flow', period1, period2)

    @_log_func
    def get_options(self) -> dict[str, Any]:
        """Get options data for the ticker.

        Returns: Options response result json.
        """
        options_result_list = self._call_client_method('get_options')
        return options_result_list[0]

    @_log_func
    def get_search(self) -> dict[str, Any]:
        """Get search results for the ticker.

        Returns: Search result json.
        """
        return self._call_client_method('get_search')

    @_log_func
    def get_recommendations(self) -> dict[str, Any]:
        """Get analyst recommendations for the ticker.

        Returns: Recommendations response result json.
        """
        recommendations_result_list = self._call_client_method('get_recommendations')
        return recommendations_result_list[0]

    @_log_func
    def get_insights(self) -> dict[str, Any]:
        """Get insights for the ticker.

        Returns: Insights response result json.
        """
        insights_result_list = self._call_client_method('get_insights')
        return insights_result_list[0]

    @_log_func
    def get_ratings(self) -> dict[str, Any]:
        """Get ratings for the ticker.

        Returns: Ratings result json.
        """
        return self._call_client_method('get_ratings')


class AsyncSymbol(SymbolBase):
    """Asynchronous Symbol class for a specific ticker.

    Warning: HTTP resources closing
        Uses http resources, so do not forget to close them after use to avoid resource
            leakage or use context manager.

    Attributes:
        ticker: Ticker symbol.
        _client:
            Client instance, that is used for all http requests.
                (Is lazily initialized.)

    Methods:
        get_chart: Get chart data for the ticker.
        get_quote: Get quote for the ticker.
        get_quote_type: Get quote type for the ticker.
        get_quote_summary_all_modules: Get quote summary for all modules for the ticker.
        get_asset_profile: Get asset profile for the ticker.
        get_summary_profile: Get summary profile for the ticker.
        get_summary_detail: Get summary detail for the ticker.
        get_price: Get price data for the ticker.
        get_default_key_statistics: Get default key statistics for the ticker.
        get_financial_data: Get financial data for the ticker.
        get_calendar_events: Get calendar events for the ticker.
        get_sec_filings: Get sec filings for the ticker.
        get_upgrade_downgrade_history: Get upgrade downgrade history for the ticker.
        get_institution_ownership: Get institution ownership for the ticker.
        get_fund_ownership: Get fund ownership for the ticker.
        get_major_direct_holders: Get major direct holders for the ticker.
        get_major_holders_breakdown: Get major holders breakdown for the ticker.
        get_insider_transactions: Get insider transactions for the ticker.
        get_insider_holders: Get insider holders for the ticker.
        get_net_share_purchase_activity: Get net share purchase activity for the ticker.
        get_earnings: Get earnings for the ticker.
        get_earnings_history: Get earnings history for the ticker.
        get_earnings_trend: Get earnings trend for the ticker.
        get_industry_trend: Get industry trend for the ticker.
        get_index_trend: Get index trend for the ticker.
        get_sector_trend: Get sector trend for the ticker.
        get_recommendation_trend: Get recommendation trend for the ticker.
        get_page_views: Get page views for the ticker.
        get_income_statement: Get income statement for the ticker.
        get_balance_sheet: Get balance sheet for the ticker.
        get_cash_flow: Get cash flow statement for the ticker.
        get_options: Get options data for the ticker.
        get_search: Get search results for the ticker.
        get_recommendations: Get analyst recommendations for the ticker.
        get_insights: Get insights for the ticker.
        get_ratings: Get ratings for the ticker.
    """

    def __init__(self, ticker: str) -> None:
        """Create new AsyncSymbol instance.

        Args:
            ticker: Ticker symbol.
        """
        super().__init__(ticker)
        self._client: AsyncClient | None = None

    def _get_client(self) -> None:
        if self._client is None:
            self._client = _SingletonAsyncClientManager._get_client()

    async def close(self) -> None:
        """Release the client if open for current symbol.

        Note:
            Only if no other symbols are using the client singleton, is the client
                closed.
        """
        if self._client is not None:
            await _SingletonAsyncClientManager._release_client()
            self._client = None

    async def __aenter__(self) -> Self:
        """When entering context manager, get the client."""
        self._get_client()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> None:
        """When closing context manager, release the client."""
        await self.close()

    @overload
    async def _call_client_method(
        self,
        method_name: Literal['get_search', 'get_ratings'],
        kwargs: dict[str, Any] | None = None,
    ) -> dict[str, Any]: ...

    @overload
    async def _call_client_method(
        self, method_name: str, kwargs: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]: ...

    async def _call_client_method(
        self, method_name: str, kwargs: dict[str, Any] | None = None
    ) -> list[dict[str, Any]] | dict[str, Any]:
        # not using use *args, **kwargs, to be compatible with
        # AsyncSymbols._call_client_method

        kwargs = kwargs or {}
        ticker_key = self._TICKER_KEY_MAP[method_name]

        if ticker_key:
            kwargs[ticker_key] = self.ticker

        result_key = _RESULT_KEY_MAP.get(method_name)

        self._get_client()
        method = getattr(self._client, method_name)
        response_json = await method(**kwargs)

        # search does not have result key
        return response_json[result_key]['result'] if result_key else response_json

    @_alog_func
    async def get_chart(
        self,
        interval: str,
        period_range: str | None = None,
        period1: int | float | None = None,
        period2: int | float | None = None,
        include_pre_post: bool | None = None,
        include_div: bool = True,
        include_split: bool = True,
        include_earn: bool = True,
        include_capital_gain: bool = True,
    ) -> dict[str, Any]:
        """Get chart data for the ticker.

        Args:
            interval: Data interval.
            period_range: Range of the period.
            period1: Start timestamp in seconds. (optional, default: None)
            period2: End timestamp in seconds. (optional, default: None)
            include_pre_post: Whether to include pre and post market.
            include_div: Whether to include dividends.
            include_split: Whether to include stock splits.
            include_earn: Whether to include earnings.
            include_capital_gain: Whether to include capital gains.

        Returns: Chart response result json.

        Note:
            Even though the the endpoint param is called range, period_range was chosen
            to avoid collision with python built-in method name.
        """
        kwargs: dict[str, Any] = {'interval': interval}

        if period_range is not None:
            kwargs['period_range'] = period_range

        if period1 is not None:
            kwargs['period1'] = period1

        if period2 is not None:
            kwargs['period2'] = period2

        if include_pre_post is not None:
            kwargs['include_pre_post'] = include_pre_post

        events_list = []

        if include_div:
            events_list.append('div')

        if include_split:
            events_list.append('split')

        if include_earn:
            events_list.append('earn')

        if include_capital_gain:
            events_list.append('capitalGain')

        if events_list:
            kwargs['events'] = ','.join(events_list)

        chart_result_list = await self._call_client_method('get_chart', kwargs)
        return chart_result_list[0]

    @_alog_func
    async def get_quote(self, include_pre_post: bool | None = None) -> dict[str, Any]:
        """Get quote for the ticker.

        Args:
            include_pre_post: Whether to include pre and post market.

        Returns: Quote response result json.
        """
        kwargs = (
            {'include_pre_post': include_pre_post}
            if include_pre_post is not None
            else {}
        )
        quote_result_list = await self._call_client_method('get_quote', kwargs)
        return quote_result_list[0]

    @_alog_func
    async def get_quote_type(self) -> dict[str, Any]:
        """Get quote type for the ticker.

        Returns: Quote type response result json.
        """
        quote_type_result_list = await self._call_client_method('get_quote_type')
        return quote_type_result_list[0]

    @_alog_func
    async def get_quote_summary_all_modules(self) -> dict[str, Any]:
        """Get quote summary for all modules for the ticker.

        Returns: Quote summary with all modules response result json.
        """
        kwargs: dict[str, Any] = {
            'modules': QUOTE_SUMMARY_MODULES,
        }
        quote_summary_result_list = await self._call_client_method(
            'get_quote_summary', kwargs
        )
        return quote_summary_result_list[0]

    @_alog_func
    async def _get_quote_summary_single_module(self, module: str) -> dict[str, Any]:
        kwargs: dict[str, Any] = {'modules': module}
        quote_summary_result_list = await self._call_client_method(
            'get_quote_summary', kwargs
        )
        return quote_summary_result_list[0][module]

    @_alog_func
    async def get_asset_profile(self) -> dict[str, Any]:
        """Get asset profile for the ticker.

        Returns: Quote summary with asset profile module response result json.
        """
        return await self._get_quote_summary_single_module('assetProfile')

    @_alog_func
    async def get_summary_profile(self) -> dict[str, Any]:
        """Get summary profile for the ticker.

        Returns: Quote summary with summary profile module response result json.
        """
        return await self._get_quote_summary_single_module('summaryProfile')

    @_alog_func
    async def get_summary_detail(self) -> dict[str, Any]:
        """Get summary detail for the ticker.

        Returns: Quote summary with summary detail module response result json.
        """
        return await self._get_quote_summary_single_module('summaryDetail')

    @_alog_func
    async def get_price(self) -> dict[str, Any]:
        """Get price data for the ticker.

        Returns: Quote summary with price data module response result json.
        """
        return await self._get_quote_summary_single_module('price')

    @_alog_func
    async def get_default_key_statistics(self) -> dict[str, Any]:
        """Get default key statistics for the ticker.

        Returns: Quote summary with default key statistics module response result json.
        """
        return await self._get_quote_summary_single_module('defaultKeyStatistics')

    @_alog_func
    async def get_financial_data(self) -> dict[str, Any]:
        """Get financial data for the ticker.

        Returns: Quote summary with financial data module response result json.
        """
        return await self._get_quote_summary_single_module('financialData')

    @_alog_func
    async def get_calendar_events(self) -> dict[str, Any]:
        """Get calendar events for the ticker.

        Returns: Quote summary with calendar events module response result json.
        """
        return await self._get_quote_summary_single_module('calendarEvents')

    @_alog_func
    async def get_sec_filings(self) -> dict[str, Any]:
        """Get sec filings for the ticker.

        Returns: Quote summary with sec filings module response result json.
        """
        return await self._get_quote_summary_single_module('secFilings')

    @_alog_func
    async def get_upgrade_downgrade_history(self) -> list[dict[str, Any]]:
        """Get upgrade downgrade history for the ticker.

        Returns:
            Quote summary with upgrade downgrade history module response results
                json.
        """
        result = await self._get_quote_summary_single_module('upgradeDowngradeHistory')
        return result['history']

    @_alog_func
    async def get_institution_ownership(self) -> list[dict[str, Any]]:
        """Get institution ownership for the ticker.

        Returns: Quote summary with institution ownership module response results json.
        """
        result = await self._get_quote_summary_single_module('institutionOwnership')
        return result['ownershipList']

    @_alog_func
    async def get_fund_ownership(self) -> list[dict[str, Any]]:
        """Get fund ownership for the ticker.

        Returns: Quote summary with fund ownership module response results json.
        """
        result = await self._get_quote_summary_single_module('fundOwnership')
        return result['ownershipList']

    @_alog_func
    async def get_major_direct_holders(self) -> dict[str, Any]:
        """Get major direct holders for the ticker.

        Returns: Quote summary with direct holders module response result json.
        """
        return await self._get_quote_summary_single_module('majorDirectHolders')

    @_alog_func
    async def get_major_holders_breakdown(self) -> dict[str, Any]:
        """Get major holders breakdown for the ticker.

        Returns: Quote summary with holders breakdown module response result json.
        """
        return await self._get_quote_summary_single_module('majorHoldersBreakdown')

    @_alog_func
    async def get_insider_transactions(self) -> list[dict[str, Any]]:
        """Get insider transactions for the ticker.

        Returns: Quote summary with insider transactions module response results json.
        """
        result = await self._get_quote_summary_single_module('insiderTransactions')
        return result['transactions']

    @_alog_func
    async def get_insider_holders(self) -> list[dict[str, Any]]:
        """Get insider holders for the ticker.

        Returns: Quote summary with insider holders module response results json.
        """
        result = await self._get_quote_summary_single_module('insiderHolders')
        return result['holders']

    @_alog_func
    async def get_net_share_purchase_activity(self) -> dict[str, Any]:
        """Get net share purchase activity for the ticker.

        Returns:
            Quote summary with net share purchase activity module response result
                json.
        """
        return await self._get_quote_summary_single_module('netSharePurchaseActivity')

    @_alog_func
    async def get_earnings(self) -> dict[str, Any]:
        """Get earnings for the ticker.

        Returns: Quote summary with earnings module response result json.
        """
        return await self._get_quote_summary_single_module('earnings')

    @_alog_func
    async def get_earnings_history(self) -> list[dict[str, Any]]:
        """Get earnings history for the ticker.

        Returns: Quote summary with earnings history module response results json.
        """
        result = await self._get_quote_summary_single_module('earningsHistory')
        return result['history']

    @_alog_func
    async def get_earnings_trend(self) -> list[dict[str, Any]]:
        """Get earnings trend for the ticker.

        Returns: Quote summary with earnings trend module response results json.
        """
        result = await self._get_quote_summary_single_module('earningsTrend')
        return result['trend']

    @_alog_func
    async def get_industry_trend(self) -> dict[str, Any]:
        """Get industry trend for the ticker.

        Returns: Quote summary with industry trend module response result json.
        """
        return await self._get_quote_summary_single_module('industryTrend')

    @_alog_func
    async def get_index_trend(self) -> dict[str, Any]:
        """Get index trend for the ticker.

        Returns: Quote summary with index trend module response result json.
        """
        return await self._get_quote_summary_single_module('indexTrend')

    @_alog_func
    async def get_sector_trend(self) -> dict[str, Any]:
        """Get sector trend for the ticker.

        Returns: Quote summary with sector trend module response result json.
        """
        return await self._get_quote_summary_single_module('sectorTrend')

    @_alog_func
    async def get_recommendation_trend(self) -> list[dict[str, Any]]:
        """Get recommendation trend for the ticker.

        Returns: Quote summary with recommendation trend module response results json.
        """
        result = await self._get_quote_summary_single_module('recommendationTrend')
        return result['trend']

    @_alog_func
    async def get_page_views(self) -> dict[str, Any]:
        """Get page views for the ticker.

        Returns: Quote summary with page views module response result json.
        """
        return await self._get_quote_summary_single_module('pageViews')

    @_alog_func
    async def _get_financials(
        self,
        frequency: str,
        typ: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[dict[str, Any]]:
        kwargs: dict[str, Any] = {
            'types': get_types_with_frequency(typ, frequency),
            'period1': period1,
            'period2': period2,
        }
        return await self._call_client_method('get_timeseries', kwargs)

    @_alog_func
    async def get_income_statement(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[dict[str, Any]]:
        """Get income statement for the ticker.

        Args:
            frequency: annual, quarterly or trailing.
            period1:
                Start timestamp in seconds. (optional, default: 1st Jan 2020 timestamp)
            period2: End timestamp in seconds. (optional, default: now timestamp)

        Returns: Income statement response results json.
        """
        return await self._get_financials(
            frequency, 'income_statement', period1, period2
        )

    @_alog_func
    async def get_balance_sheet(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[dict[str, Any]]:
        """Get balance sheet for the ticker.

        Args:
            frequency: annual, quarterly or trailing.
            period1:
                Start timestamp in seconds. (optional, default: 1st Jan 2020 timestamp)
            period2: End timestamp in seconds. (optional, default: now timestamp)

        Returns: Balance sheet response results json.
        """
        return await self._get_financials(frequency, 'balance_sheet', period1, period2)

    @_alog_func
    async def get_cash_flow(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[dict[str, Any]]:
        """Get cash flow statement for the ticker.

        Args:
            frequency: annual, quarterly or trailing.
            period1:
                Start timestamp in seconds. (optional, default: 1st Jan 2020 timestamp)
            period2: End timestamp in seconds. (optional, default: now timestamp)

        Returns: Cash flow response results json.
        """
        return await self._get_financials(frequency, 'cash_flow', period1, period2)

    @_alog_func
    async def get_options(self) -> dict[str, Any]:
        """Get options data for the ticker.

        Returns: Options response result json.
        """
        options_result_list = await self._call_client_method('get_options')
        return options_result_list[0]

    @_alog_func
    async def get_search(self) -> dict[str, Any]:
        """Get search results for the ticker.

        Returns: Search result json.
        """
        return await self._call_client_method('get_search')

    @_alog_func
    async def get_recommendations(self) -> dict[str, Any]:
        """Get analyst recommendations for the ticker.

        Returns: Recommendations response result json.
        """
        recommendations_result_list = await self._call_client_method(
            'get_recommendations'
        )
        return recommendations_result_list[0]

    @_alog_func
    async def get_insights(self) -> dict[str, Any]:
        """Get insights for the ticker.

        Returns: Insights response result json.
        """
        insights_result_list = await self._call_client_method('get_insights')
        return insights_result_list[0]

    @_alog_func
    async def get_ratings(self) -> dict[str, Any]:
        """Get ratings for the ticker.

        Returns: Ratings result json.
        """
        return await self._call_client_method('get_ratings')
