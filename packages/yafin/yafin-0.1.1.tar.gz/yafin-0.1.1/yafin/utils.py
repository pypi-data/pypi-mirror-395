import logging
from collections.abc import Callable
from functools import wraps
from typing import Any, NoReturn, Type
from urllib.parse import urlencode

from .const import (
    _ALL_TYPES_SET,
    _TYPES,
    CALENDAR_EVENT_MODULES_SET,
    EVENTS_SET,
    FREQUENCIES,
    INTERVALS,
    PERIOD_RANGES,
    QUOTE_SUMMARY_MODULES_SET,
)
from .exceptions import TrailingBalanceSheetError

logger = logging.getLogger(__name__)


def _encode_url(url: str, params: dict[str, Any] | None = None) -> str:
    """Print URL with parameters.

    Args:
        url: base url, where query param will be added.
        params: http request query parameters.

    Returns: url with params
    """
    if params is None:
        return url

    params_copy = params.copy()

    if 'crumb' in params:
        params_copy['crumb'] = 'REDACTED'

    return f'{url}?{urlencode(params_copy)}'


def _error(msg: str, err_cls: Type[Exception] = Exception) -> NoReturn:
    """Log error message and raise exception.

    Args:
        msg: error message (hint), that will be logged and raised.
        err_cls: class of the raised error, default Exception.
    """
    logger.error(msg)
    raise err_cls(msg)


def _check_interval(interval: str) -> None:
    if interval not in INTERVALS:
        _error(
            msg=f'Invalid {interval=}. Valid values: {INTERVALS}',
            err_cls=ValueError,
        )


def _check_period_range(period_range: str) -> None:
    if period_range not in PERIOD_RANGES:
        _error(
            msg=f'Invalid {period_range=}. Valid values: {PERIOD_RANGES}',
            err_cls=ValueError,
        )


def _check_events(events: set[str]) -> None:
    if not events <= EVENTS_SET:
        _error(
            msg=(f'Invalid events: {events - EVENTS_SET}. Valid values: {EVENTS_SET}'),
            err_cls=ValueError,
        )


def _check_quote_summary_modules(quote_summary_modules: set[str]) -> None:
    if not quote_summary_modules <= QUOTE_SUMMARY_MODULES_SET:
        _error(
            msg=(
                f'Invalid modules: {quote_summary_modules - QUOTE_SUMMARY_MODULES_SET}. '  # noqa: E501
                f'Valid values: {QUOTE_SUMMARY_MODULES_SET}'
            ),
            err_cls=ValueError,
        )


def _check_calendar_event_modules(calendar_event_modules: set[str]) -> None:
    if not calendar_event_modules <= CALENDAR_EVENT_MODULES_SET:
        _error(
            msg=(
                f'Invalid modules: {calendar_event_modules - CALENDAR_EVENT_MODULES_SET}. '  # noqa: E501
                f'Valid values: {CALENDAR_EVENT_MODULES_SET}'
            ),
            err_cls=ValueError,
        )


def _check_types(types: set[str]) -> None:
    if not types <= _ALL_TYPES_SET:
        _error(
            msg=(
                f'Invalid types: {types - _ALL_TYPES_SET}. '
                f'Valid values: {_ALL_TYPES_SET}'
            ),
            err_cls=ValueError,
        )


def _check_typ(typ: str) -> None:
    if typ not in _TYPES.keys():
        _error(msg=f'Invalid {typ=}. Valid values: {_TYPES.keys()}', err_cls=ValueError)


def _check_frequency(typ: str, frequency: str | None) -> None:
    if typ != 'other' and frequency not in FREQUENCIES:
        _error(
            msg=f'Invalid {frequency=}. Valid values: {FREQUENCIES}', err_cls=ValueError
        )

    elif typ == 'other' and frequency is not None:
        _error(
            msg=f'Frequency {frequency=} not allowed for type other.',
            err_cls=ValueError,
        )

    if typ == 'balance_sheet' and frequency == 'trailing':
        _error(
            msg=f'{frequency=} not allowed for balance sheet.',
            err_cls=TrailingBalanceSheetError,
        )


def get_types_with_frequency(typ: str, frequency: str | None = None) -> str:
    """Enrich types with frequency.

    Args:
        frequency:
            frequency used for timeseries endpoint, e.g.: annual, quarterly or trailing.
        typ:
            type of types, e.g.: income_statement, balance_sheet or cash_flow,
            which is used for fetching all types for given financial.
            e.g. for income_statement: NetIncome,EBIT,EBITDA,GrossProfit, ...

    Returns:
        types enriched with frequency e.g. for income_statement:
            trailingNetIncome,trailingEBIT,trailingEBITDA,trailingGrossProfit, ...

    Raises:
        ValueError: If frequency or typ are not in list of valid values.
        TrailingBalanceSheetError:
            If attempting to request balance sheet with trailing
                frequency.
    """
    _check_typ(typ)
    _check_frequency(typ, frequency)

    types = _TYPES[typ]
    types_with_frequency = [f'{frequency}{t}' if frequency else t for t in types]
    return ','.join(types_with_frequency)


def _get_func_name(func: Callable[..., Any], args: tuple[Any, ...]) -> str:
    """Helper function for function name logging.

    Args:
        func: python function
        args: arguments to the function

    Returns: function name
    """
    # check if first argument is class instance (self)
    if args and hasattr(args[0], func.__name__):
        return f'{args[0].__class__.__name__}.{func.__name__}'

    return func.__name__


def _alog_func(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator for logging functions."""

    @wraps(func)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        func_name = _get_func_name(func, args)

        logger.debug(f'{func_name} was called.')
        result = await func(*args, **kwargs)
        logger.debug(f'{func_name} finished.')

        return result

    return async_wrapper


def _log_func(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator for logging functions."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        func_name = _get_func_name(func, args)

        logger.debug(f'{func_name} was called.')
        result = func(*args, **kwargs)
        logger.debug(f'{func_name} finished.')

        return result

    return wrapper
