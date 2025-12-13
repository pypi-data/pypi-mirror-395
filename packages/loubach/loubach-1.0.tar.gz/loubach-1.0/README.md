# Loubach

Offers price fetching, time series analysis, equity pair analysis, and portfolio testing for priceable financial instruments.

## Modules

* **loubach.data:** Base Yahoo Finance API connection module that helps feed **loubach.instrument** modules.
* **loubach.instrument:** Includes functionality for instrument intialization and data fetching
* **loubach.math:** Includes all math related helper modules (i.e.: pd.Series operations, market technicals, trend detection)
* **loubach.portfolio:** Offers Portfolio and Holding object classes
* **loubach.timeseries:** Time series module that helps visualize time series data, bivariate analysis, market technical overlays, portfolio/holding value, etc.

## Example Usage

```bash
from loubach.instrument.equity import Equity
from loubach.technicals import *

# Load equity prices and get RSI as a pd.Series object
AAPL_prices = Equity('AAPL').price(start='2024-12-01', end='2025-12-01')
RSI = rsi(data=AAPL_prices, period=14)
```
