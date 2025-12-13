from typing import Dict, Optional, List, Tuple

import numpy as np
import pandas as pd


class Stock:
    MA_PERIODS = (5, 10, 20, 30, 60, 120, 250)
    MACD_FAST, MACD_SLOW, MACD_SIGNAL = 12, 26, 9
    BB_PERIOD, BB_K = 20, 2

    def __init__(self, symbol: str, sources: Dict[str, pd.DataFrame]):
        self.symbol = symbol
        self.sources = sources
        self._process_all_intervals()

    def _process_all_intervals(self) -> None:
        for interval in self.sources.keys():
            self._process_interval(interval)

    def _process_interval(self, interval: str) -> None:
        source_df = self.sources[interval]
        if source_df is None or source_df.empty:
            return

        source_df = self._normalize_sources(source_df)
        source_df = self._add_source_moving_averages(source_df)
        source_df = self._add_source_macd(source_df)
        source_df = self._add_source_bollinger_bands(source_df)
        self.sources[interval] = source_df

    @staticmethod
    def _normalize_sources(df: pd.DataFrame) -> pd.DataFrame:
        df.columns = df.columns.str.lower()

        required = ['open', 'high', 'low', 'close', 'volume']
        missing = [col for col in required if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        if not isinstance(df.index, pd.DatetimeIndex):
            raise ValueError(f"DataFrame index must be DatetimeIndex, got {type(df.index).__name__}")

        df.index.name = 'datetime'
        return df

    def _add_source_moving_averages(self, df: pd.DataFrame) -> pd.DataFrame:
        for window in self.MA_PERIODS:
            df[f'ma{window}'] = df['close'].rolling(window=window).mean()
        return df

    def _add_source_macd(self, df: pd.DataFrame) -> pd.DataFrame:
        ema_fast = df['close'].ewm(span=self.MACD_FAST, adjust=False).mean()
        ema_slow = df['close'].ewm(span=self.MACD_SLOW, adjust=False).mean()
        df['macd'] = ema_fast - ema_slow
        df['macd_dea'] = df['macd'].ewm(span=self.MACD_SIGNAL, adjust=False).mean()
        df['macd_dif'] = df['macd'] - df['macd_dea']
        return df

    def _add_source_bollinger_bands(self, df: pd.DataFrame) -> pd.DataFrame:
        df['bb'] = df['close'].rolling(window=self.BB_PERIOD).mean()
        rolling_std = df['close'].rolling(window=self.BB_PERIOD).std()
        df['bb_upper'] = df['bb'] + (self.BB_K * rolling_std)
        df['bb_lower'] = df['bb'] - (self.BB_K * rolling_std)
        return df

    @staticmethod
    def is_top(item: Tuple) -> bool:
        return np.isnan(item.low) and not np.isnan(item.high)

    @staticmethod
    def is_bottom(item: Tuple) -> bool:
        return np.isnan(item.high) and not np.isnan(item.low)

    @staticmethod
    def to_dataframe(rows: List, columns: Optional[list] = None) -> Optional[pd.DataFrame]:
        if not rows:
            return None

        df = pd.DataFrame(rows).set_index('Index')
        df.index.name = 'datetime'
        return df if columns is None else df[columns]
