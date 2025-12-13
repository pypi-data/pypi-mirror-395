from dataclasses import dataclass
from typing import Dict, Optional, Any, List, Tuple

import pandas as pd
from pychanlun.segment import Segment


@dataclass
class Range:
    start: Any
    end: Any
    high: float
    low: float


class Pivot(Segment):

    def __init__(self, symbol: str, source: Dict[str, pd.DataFrame]):
        self.stroke_pivots: Dict[str, Optional[pd.DataFrame]] = {}
        self.segment_pivots: Dict[str, Optional[pd.DataFrame]] = {}
        super().__init__(symbol, source)

    def _process_interval(self, interval: str) -> None:
        super()._process_interval(interval)

        source_df = self.sources[interval]
        stroke_df = self.strokes[interval]
        if source_df is not None and stroke_df is not None:
            stroke_pivot_df = self._identify_pivots(stroke_df, source_df)
            self.stroke_pivots[interval] = stroke_pivot_df
        else:
            self.stroke_pivots[interval] = None

        segment_df = self.segments[interval]
        if source_df is not None and segment_df is not None:
            segment_pivot_df = self._identify_pivots(segment_df, source_df)
            self.segment_pivots[interval] = segment_pivot_df
        else:
            self.segment_pivots[interval] = None

    def _identify_pivots(self, segment_df: pd.DataFrame, source_df: pd.DataFrame) -> Optional[pd.DataFrame]:
        segment_df = pd.DataFrame(segment_df)
        segment_df['price'] = segment_df['macd'] = segment_df['level'] = segment_df['status'] = 0

        segments = list(segment_df.itertuples())

        rows = self._process_pivots(segments)
        self._merge_overlapping_pivots(rows)

        self._set_pivot_metrics(rows, source_df)
        return self.to_dataframe(rows, ['high', 'low', 'price', 'macd', 'level', 'status'])

    def _process_pivots(self, segments: List) -> List:
        rows = []

        index = 0
        while index < len(segments) - 4:
            entry_segment = segments[index]
            range_1 = self._get_range(segments, index + 1)
            range_3 = self._get_range(segments, index + 3)
            pivot = self._calculate_pivot_zone(range_1, range_3)

            if not self._is_valid_pivot(pivot) and not self._can_initiate_pivot(pivot, entry_segment):
                index += 1
                continue

            length = self._extend_pivots(pivot, segments, index)
            exit_segment = segments[index + length + 4]
            exit_segment = self._update_pivot_zone(pivot, range_1, exit_segment)

            rows.append(range_1.start)
            rows.append(exit_segment)
            index += length + 4

        return rows

    def _get_range(self, segments: List, index: int) -> Range:
        start, end = segments[index], segments[index + 1]
        high = start.high if self.is_top(start) else end.high
        low = start.low if self.is_bottom(start) else end.low
        return Range(start, end, high, low)

    @staticmethod
    def _calculate_pivot_zone(range_1: Range, range_3: Range) -> Range:
        high = min(range_1.high, range_3.high)
        low = max(range_1.low, range_3.low)
        return Range(range_1.start, range_3.end, high, low)

    @staticmethod
    def _is_valid_pivot(pivot: Range) -> bool:
        return pivot.high > pivot.low

    def _can_initiate_pivot(self, pivot: Range, segment: Tuple) -> bool:
        if self.is_top(segment):
            return segment.high > pivot.low
        else:
            return segment.low < pivot.high

    def _extend_pivots(self, pivot: Range, segments: List, index: int) -> int:
        length = 0
        while index + length < len(segments) - 7:
            next_range = self._get_range(segments, index + length + 5)
            if self._is_outside_pivot(pivot, next_range):
                break
            length += 1
        return length

    @staticmethod
    def _is_outside_pivot(pivot: Range, next_range: Range) -> bool:
        return next_range.high < pivot.low or next_range.low > pivot.high

    def _update_pivot_zone(self, pivot: Range, range_1: Range, exit_segment) -> Any:
        if self.is_top(range_1.start):
            range_1.start = range_1.start._replace(high=pivot.high)
            exit_segment = exit_segment._replace(low=pivot.low)
        else:
            range_1.start = range_1.start._replace(low=pivot.low)
            exit_segment = exit_segment._replace(high=pivot.high)
        return exit_segment

    def _merge_overlapping_pivots(self, rows: List) -> None:
        index = 0
        while index < len(rows) - 3:
            pivot_1 = self._get_range(rows, index)
            pivot_2 = self._get_range(rows, index + 2)

            if not self._is_pivot_overlap(pivot_1, pivot_2):
                index += 2
                continue

            if self.is_top(pivot_1.start):
                high = min(pivot_1.high, pivot_2.high)
                pivot_1.start = pivot_1.start._replace(high=high)
                low = max(pivot_1.low, pivot_2.low)
                pivot_2.end = pivot_2.end._replace(low=low)
            else:
                low = max(pivot_1.low, pivot_2.low)
                pivot_1.start = pivot_1.start._replace(low=low)
                high = min(pivot_1.high, pivot_2.high)
                pivot_2.end = pivot_2.end._replace(high=high)

            rows[index] = pivot_1.start
            rows[index + 3] = pivot_2.end
            rows.remove(pivot_1.end)
            rows.remove(pivot_2.start)

    @staticmethod
    def _is_pivot_overlap(range_1: Range, range_3: Range) -> bool:
        return range_3.high > range_1.low and range_3.low < range_1.high

    def _set_pivot_metrics(self, rows: List, source_df: pd.DataFrame) -> None:
        level = 0
        for i in range(0, len(rows) - 3, 2):
            pivot_1 = self._get_range(rows, i)
            pivot_2 = self._get_range(rows, i + 2)

            level = self._set_pivot_trend(pivot_1, pivot_2, level)
            self._set_pivot_macd(pivot_1, pivot_2, source_df)
            self._detect_pivot_divergence(pivot_1, pivot_2)

            rows[i] = pivot_1.start
            rows[i + 1] = pivot_1.end
            rows[i + 2] = pivot_2.start
            rows[i + 3] = pivot_2.end

        if len(rows) > 0:
            last = self._get_range(rows, -2)
            self._set_pivot_macd(last, None, source_df)
            rows[-1] = last.end

    @staticmethod
    def _set_pivot_trend(pivot_1: Range, pivot_2: Range, level: int) -> int:
        if level == 0:
            pivot_1.start = pivot_1.start._replace(level=0)
            pivot_1.end = pivot_1.end._replace(level=1)

        if pivot_2.high > pivot_1.high:
            pivot_1.end = pivot_1.end._replace(price=pivot_1.low)
            if level < 0:
                level = 0
            level += 1
            pivot_2.start = pivot_2.start._replace(level=level, price=pivot_2.high)
            pivot_2.end = pivot_2.end._replace(level=level + 1)
        else:
            pivot_1.end = pivot_1.end._replace(price=pivot_1.high)
            if level > 0:
                level = 0
            level -= 1
            pivot_2.start = pivot_2.start._replace(level=level, price=pivot_2.low)
            pivot_2.end = pivot_2.end._replace(level=level - 1)
        return level

    @staticmethod
    def _set_pivot_macd(pivot_1: Optional[Range], pivot_2: Optional[Range], source_df: pd.DataFrame) -> None:
        mask = pd.Series([True] * len(source_df), index=source_df.index)
        if pivot_1 is not None:
            mask &= source_df.index >= pivot_1.end.Index
        if pivot_2 is not None:
            mask &= source_df.index <= pivot_2.start.Index

        if pivot_2 is not None:
            if pivot_2.start.level > 0:
                mask &= source_df.macd > source_df.macd_dea
            elif pivot_2.start.level < 0:
                mask &= source_df.macd < source_df.macd_dea

        macd_sum = source_df[mask].macd_dif.sum()
        if pivot_1 is not None:
            pivot_1.end = pivot_1.end._replace(macd=macd_sum)
        if pivot_2 is not None:
            pivot_2.start = pivot_2.start._replace(macd=macd_sum)

    @staticmethod
    def _detect_pivot_divergence(pivot_1: Range, pivot_2: Range) -> None:
        status = 0
        if 0 < pivot_1.start.level < pivot_2.start.level:
            status = 1 if pivot_1.start.macd > pivot_1.end.macd else 0
        elif 0 > pivot_1.start.level > pivot_2.start.level:
            status = 1 if pivot_1.start.macd < pivot_1.end.macd else 0

        pivot_1.start = pivot_1.start._replace(status=status)
        pivot_1.end = pivot_1.end._replace(status=status)
