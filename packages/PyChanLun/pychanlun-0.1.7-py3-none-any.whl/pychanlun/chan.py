from typing import Optional

import pandas as pd

from pychanlun.signal import Signal


class Chan(Signal):

    def get_sources(self, interval: str) -> Optional[pd.DataFrame]:
        return self.sources[interval]

    def get_sticks(self, interval: str) -> Optional[pd.DataFrame]:
        source_df = self.sources[interval]
        stick_df = self.sticks[interval]
        if source_df is None or stick_df is None:
            return None

        return source_df[[]].join(stick_df, how='left')

    def get_fractals(self, interval: str) -> Optional[pd.DataFrame]:
        fractal_df = self.fractals[interval]
        if fractal_df is None:
            return None

        has_fractal = fractal_df['high'].notna() | fractal_df['low'].notna()
        return fractal_df[has_fractal]

    def get_strokes(self, interval: str) -> Optional[pd.DataFrame]:
        stroke_df = self.strokes[interval]
        if stroke_df is None:
            return None

        stroke_df = pd.DataFrame(stroke_df)
        stroke_df['stroke'] = stroke_df['high'].fillna(stroke_df['low'])
        return stroke_df[['stroke']]

    def get_stroke_pivots(self, interval: str) -> Optional[pd.DataFrame]:
        pivot_df = self.stroke_pivots[interval]
        if pivot_df is None:
            return None

        return self._format_pivots(pivot_df)

    def get_stroke_pivot_trends(self, interval: str) -> Optional[pd.DataFrame]:
        pivot_df = self.stroke_pivots[interval]
        if pivot_df is None:
            return None

        return self._format_trends(pivot_df[1:-1])

    def get_stroke_pivot_signals(self, interval: str) -> Optional[pd.DataFrame]:
        signal_df = self.stroke_signals[interval]
        if signal_df is None:
            return None

        return self._format_signals(signal_df, 'stroke')

    def get_segments(self, interval: str) -> Optional[pd.DataFrame]:
        segment_df = self.segments[interval]
        if segment_df is None:
            return None

        segment_df = pd.DataFrame(segment_df)
        segment_df['segment'] = segment_df['high'].fillna(segment_df['low'])
        return segment_df[['segment']]

    def get_segment_pivots(self, interval: str) -> Optional[pd.DataFrame]:
        pivot_df = self.segment_pivots[interval]
        if pivot_df is None:
            return None

        return self._format_pivots(pivot_df)

    def get_segment_pivot_trends(self, interval: str) -> Optional[pd.DataFrame]:
        pivot_df = self.segment_pivots[interval]
        if pivot_df is None:
            return None

        return self._format_trends(pivot_df[1:-1])

    def get_segment_pivot_signals(self, interval: str) -> Optional[pd.DataFrame]:
        signal_df = self.segment_signals[interval]
        if signal_df is None:
            return None

        return self._format_signals(signal_df, 'segment')

    @staticmethod
    def _format_pivots(df: pd.DataFrame) -> pd.DataFrame:
        df = pd.DataFrame({
            'datetime': df.index.values[::2],
            'end': df.index.values[1::2],
            'entry_high': df['high'].values[::2],
            'exit_high': df['high'].values[1::2],
            'entry_low': df['low'].values[::2],
            'exit_low': df['low'].values[1::2],
            'level': df['level'].values[::2],
            'status': df['status'].values[::2]
        })
        df['high'] = df['entry_high'].fillna(df['exit_high'])
        df['low'] = df['entry_low'].fillna(df['exit_low'])
        df.set_index('datetime', inplace=True)
        return df[['end', 'high', 'low', 'level', 'status']]

    @staticmethod
    def _format_trends(df: pd.DataFrame) -> pd.DataFrame:
        df = pd.DataFrame({
            'datetime': df.index.values[::2],
            'end': df.index.values[1::2],
            'open': df['price'].values[::2],
            'close': df['price'].values[1::2]
        })
        df.set_index('datetime', inplace=True)
        return df[['end', 'open', 'close']]

    @staticmethod
    def _format_signals(df: pd.DataFrame, name: str) -> pd.DataFrame:
        df = pd.DataFrame(df)
        df[name] = df['high'].fillna(df['low'])
        return df[[name, 'signal']]
