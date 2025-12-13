from enum import IntEnum
from typing import Dict, Optional, List

import pandas as pd
from pychanlun.pivot import Pivot, Range


class SignalType(IntEnum):
    FIRST_BUY = 1
    SECOND_BUY = 2
    THIRD_BUY = 3
    FIRST_SELL = -1
    SECOND_SELL = -2
    THIRD_SELL = -3


class Signal(Pivot):

    def __init__(self, symbol: str, source: Dict[str, pd.DataFrame]):
        self.stroke_signals: Dict[str, Optional[pd.DataFrame]] = {}
        self.segment_signals: Dict[str, Optional[pd.DataFrame]] = {}
        super().__init__(symbol, source)

    def _process_interval(self, interval: str) -> None:
        super()._process_interval(interval)

        stroke_df = self.strokes[interval]
        stroke_pivot_df = self.stroke_pivots[interval]
        if stroke_df is not None and stroke_pivot_df is not None:
            self.stroke_signals[interval] = self._generate_signals(stroke_df, stroke_pivot_df)
        else:
            self.stroke_signals[interval] = None

        segment_df = self.segments[interval]
        segment_pivot_df = self.segment_pivots[interval]
        if segment_df is not None and segment_pivot_df is not None:
            self.segment_signals[interval] = self._generate_signals(segment_df, segment_pivot_df)
        else:
            self.segment_signals[interval] = None

    def _generate_signals(self, segment_df: pd.DataFrame, pivot_df: pd.DataFrame) -> Optional[pd.DataFrame]:
        segment_df = pd.DataFrame(segment_df)
        segment_df['signal'] = 0

        pivots = list(pivot_df.itertuples())

        rows = []

        for index in range(0, len(pivots) - 3, 2):
            curr_pivot = self._get_range(pivots, index)
            next_pivot = self._get_range(pivots, index + 2)
            segments = list(segment_df.loc[curr_pivot.end.Index: next_pivot.end.Index].itertuples())

            if curr_pivot.start.status > 0:
                if curr_pivot.end.level > curr_pivot.start.level:
                    self._check_first_second_sell(rows, segments)
                elif curr_pivot.end.level < curr_pivot.start.level:
                    self._check_first_second_buy(rows, segments)

            if curr_pivot.start.status == 0:
                self._check_third_sell(rows, segments, curr_pivot)
                self._check_third_buy(rows, segments, curr_pivot)

        return self.to_dataframe(rows, ['high', 'low', 'signal'])

    def _check_first_second_sell(self, rows: List, segments: List) -> None:
        if len(segments) < 4:
            return

        for i in range(len(segments) - 3):
            next_segment_1 = segments[i + 1]
            next_segment_3 = segments[i + 3]

            if self.is_top(next_segment_1) and next_segment_3.high < next_segment_1.high:
                rows.append(next_segment_1._replace(signal=SignalType.FIRST_SELL))
                rows.append(next_segment_3._replace(signal=SignalType.SECOND_SELL))
                return

    def _check_first_second_buy(self, rows: List, segments: List) -> None:
        if len(segments) < 4:
            return

        for i in range(len(segments) - 3):
            next_segment_1 = segments[i + 1]
            next_segment_3 = segments[i + 3]

            if self.is_bottom(next_segment_1) and next_segment_3.low > next_segment_1.low:
                rows.append(next_segment_1._replace(signal=SignalType.FIRST_BUY))
                rows.append(next_segment_3._replace(signal=SignalType.SECOND_BUY))
                return

    def _check_third_sell(self, rows: List, segments: List, curr_pivot: Range) -> None:
        if len(segments) < 3:
            return

        next_segment_1 = segments[1]
        next_segment_2 = segments[2]

        if self.is_top(next_segment_1):
            if next_segment_1.high < curr_pivot.low:
                rows.append(next_segment_1._replace(signal=SignalType.THIRD_SELL))
        if self.is_top(next_segment_2):
            if next_segment_2.high < curr_pivot.low:
                rows.append(next_segment_2._replace(signal=SignalType.THIRD_SELL))

    def _check_third_buy(self, rows: List, segments: List, curr_pivot: Range) -> None:
        if len(segments) < 3:
            return

        next_segment_1 = segments[1]
        next_segment_2 = segments[2]

        if self.is_bottom(next_segment_1):
            if next_segment_1.low > curr_pivot.high:
                rows.append(next_segment_1._replace(signal=SignalType.THIRD_BUY))
        if self.is_bottom(next_segment_2):
            if next_segment_2.low > curr_pivot.high:
                rows.append(next_segment_2._replace(signal=SignalType.THIRD_BUY))
