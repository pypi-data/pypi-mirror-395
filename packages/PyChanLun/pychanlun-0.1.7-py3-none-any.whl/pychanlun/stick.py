from typing import Dict, Optional, List, Tuple

import pandas as pd
from pychanlun.stock import Stock


class Stick(Stock):

    def __init__(self, symbol: str, source: Dict[str, pd.DataFrame]):
        self.sticks: Dict[str, Optional[pd.DataFrame]] = {}
        super().__init__(symbol, source)

    def _process_interval(self, interval: str) -> None:
        super()._process_interval(interval)

        source_df = self.sources[interval]
        if source_df is None or source_df.empty:
            self.sticks[interval] = None
            return

        sources = list(source_df.itertuples())

        index = self._find_initial_direction(sources)
        if index is None:
            self.sticks[interval] = None
            return

        stick_df = self._merge_to_sticks(sources, index)
        self.sticks[interval] = stick_df

    def _find_initial_direction(self, sources: List) -> Optional[int]:
        for index in range(len(sources) - 1):
            prev_source, curr_source = sources[index], sources[index + 1]
            if self._is_going_up(prev_source, curr_source) or self._is_going_down(prev_source, curr_source):
                return index
        return None

    @staticmethod
    def _is_going_up(curr_source: Tuple, next_source: Tuple) -> bool:
        return curr_source.high < next_source.high and curr_source.low < next_source.low

    @staticmethod
    def _is_going_down(curr_source: Tuple, next_source: Tuple) -> bool:
        return curr_source.high > next_source.high and curr_source.low > next_source.low

    def _merge_to_sticks(self, sources: List, index: int) -> Optional[pd.DataFrame]:
        rows = [sources[index]]

        prev_source, curr_source = sources[index], sources[index + 1]
        for index in range(index + 2, len(sources)):
            next_source = sources[index]
            is_going_up = self._is_going_up(prev_source, curr_source)

            if self._can_merge_inside(curr_source, next_source):
                curr_source = self._merge_inside(curr_source, next_source, is_going_up)
            elif self._can_merge_outside(curr_source, next_source):
                curr_source = self._merge_outside(curr_source, next_source, is_going_up)
            else:
                rows.append(curr_source)
                prev_source, curr_source = curr_source, next_source

        rows.append(curr_source)
        return self.to_dataframe(rows, ['high', 'low'])

    @staticmethod
    def _can_merge_inside(curr_source: Tuple, next_source: Tuple) -> bool:
        return curr_source.high >= next_source.high and curr_source.low <= next_source.low

    @staticmethod
    def _can_merge_outside(curr_source: Tuple, next_source: Tuple) -> bool:
        return curr_source.high <= next_source.high and curr_source.low >= next_source.low

    @staticmethod
    def _merge_inside(curr_source: Tuple, next_source: Tuple, is_going_up: bool) -> Tuple:
        if is_going_up:
            return curr_source._replace(low=next_source.low)
        else:
            return curr_source._replace(high=next_source.high)

    @staticmethod
    def _merge_outside(curr_source: Tuple, next_source: Tuple, is_going_up: bool) -> Tuple:
        if is_going_up:
            return next_source._replace(low=curr_source.low)
        else:
            return next_source._replace(high=curr_source.high)
