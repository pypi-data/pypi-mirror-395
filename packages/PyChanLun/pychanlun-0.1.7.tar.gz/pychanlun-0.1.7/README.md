# PyChanLun

Applying the **Chan Theory (Chan Lun)** to analyze stock trading information.

### **What is PyChanLun?**

PyChanLun is a **Python library** designed to perform technical analysis on stock market data using the principles of **Chan Theory**.

It implements a hierarchical structure of core Chan Theory concepts, starting from raw price data and building up through:

1.  **Sticks** (`Stick`)
2.  **Fractals** (`Fractal`)
3.  **Strokes** (`Stroke`)
4.  **Segments** (`Segment`)
5.  **Pivots** (`Pivot`)
6.  **Signals** (`Signal`)

The library processes time-series data to identify key structural components and generate trading-related data like **pivots**, **trend levels**, and **trading signals**, combining price action with indicators like **MACD**.

### **Where is the data coming from?**

PyChanLun uses the **yfinance** library to download historical stock data.

  * The data acquisition logic is encapsulated in the **`Source`** class.
  * It fetches **OHLCV** (Open, High, Low, Close, Volume) data for a given stock symbol across various time intervals (`1m`, `5m`, `30m`, `1d`, `1wk`, `1mo`).
  * The `Source` class also calculates common technical indicators like **Moving Averages (MA)**, **MACD (Moving Average Convergence Divergence)**, and **Bollinger Bands (BB)** on the raw data.
  * Special handling is included for filtering trading hours for **Chinese stock markets** (symbols ending in `.SZ` or `.SS`) for intraday intervals.

### **What data does PyChanLun create?**

PyChanLun generates several layers of processed data based on the original OHLCV information, with the main entry point being the **`Chan`** class, which acts as a data retriever.

| Data Type                    | Class/Method                                                              | Description                                                                                                                                             |
|:-----------------------------|:--------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Sources**                  | `Chan.get_sources()`                                                      | Raw OHLCV data with MA, MACD, BB calculated.                                                                                                            |
| **Sticks**                   | `Chan.get_sticks()`                                                       | Chan Theory (Chan Lun) stick data (`Stick` class). <br> Columns: `datetime`, `high`, `low`.                                                             |
| **Fractals**                 | `Chan.get_fractals()`                                                     | Top fractal and bottom fractal data (`Fractal` class). <br> Columns: `datetime`, `high`, `low`.                                               |
| **Strokes**                  | `Chan.get_strokes()`                                                      | Constructed stroke data (`Stroke` class). <br> Column: `datetime`, `stroke`.                                                                            |
| **Segments**                 | `Chan.get_segments()`                                                     | Constructed segment data (`Segment` class), a higher level of structural grouping. <br> Column: `datetime`, `segment`.                                  |
| **Pivots (Stroke/Segment)**  | `Chan.get_stroke_pivots()` <br> `Chan.get_segment_pivots()`               | Identified pivot (`Pivot` class) data based on the stroke or segment data. <br> Columns: `datetime`, `end`, `high`, `low` , `level`, and `status`.      |
| **Trends (Stroke/Segment)**  | `Chan.get_stroke_pivot_trends()` <br> `Chan.get_segment_pivot_trends()`   | Pivot trend data (`Trend` class) summarizing the price movement between alternating pivots. <br> Columns: `datetime`, `end`, `open`, `close`.           |
| **Signals (Stroke/Segment)** | `Chan.get_stroke_pivot_signals()` <br> `Chan.get_segment_pivot_signals()` | Trading signal data (`Signal` class) generated based on the pivots and MACD divergence. <br> Columns: `datetime`, `stroke` (or `segment`) and `signal`. |

### **How to use PyChanLun?**

The primary way to interact with PyChanLun is through the **`Chan`** class, providing a unified interface to access all generated data for a specific stock symbol.

#### 1\. **Initialization**

Instantiate the `Chan` object with the stock symbol and source data you want to analyze. It will trigger structural analysis across all time intervals of the source data (`1m`, `5m`, `30m`, `1d`, `1wk`, `1mo`).

```python
from pychanlun.chan import Chan

# Initialize the Chan object for Apple (AAPL)
chan = Chan('AAPL', source)
```

#### 2\. **Accessing Data**

Use the various `get_*` methods, specifying the desired **time interval** as a string argument (e.g., `1m`, `1d`). The methods return a Pandas DataFrame containing the analyzed data.

```python
# Get the Stick data for the 1-minute interval
sticks_df = chan.get_sticks('1m')
print("Sticks Data (1m):\n", sticks_df.head())

# Get the Stroke Pivot data for the 30-minute interval
stroke_pivots_df = chan.get_stroke_pivots('30m')
print("\nStroke Pivots (30m):\n", stroke_pivots_df.head())

# Get Segment-level trading signals for the 1-day interval
segment_signals_df = chan.get_segment_pivot_signals('1d')
print("\nSegment Signals (1d):\n", segment_signals_df.head())
```