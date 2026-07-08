from .utils import load_dataset as _load_dataset
from .fxmacrodata import load_fxmacrodata_calendar


# Load FOREX datasets
FOREX_EURUSD_1H_ASK = _load_dataset('FOREX_EURUSD_1H_ASK', 'Time')

# Load Stocks datasets
STOCKS_GOOGL = _load_dataset('STOCKS_GOOGL', 'Date')

__all__ = [
    'FOREX_EURUSD_1H_ASK',
    'STOCKS_GOOGL',
    'load_fxmacrodata_calendar',
]
