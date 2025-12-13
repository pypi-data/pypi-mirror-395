from typing import Dict, Optional, List

import pandas as pd

from pychanlun.stroke import Stroke, Item


class Segment(Stroke):

    def __init__(self, symbol: str, source: Dict[str, pd.DataFrame]):
        self.segments: Dict[str, Optional[pd.DataFrame]] = {}
        super().__init__(symbol, source)

    def _process_interval(self, interval: str) -> None:
        super()._process_interval(interval)

        stroke_df = self.strokes[interval]
        if stroke_df is None or stroke_df.empty:
            self.segments[interval] = None
            return

        strokes = list(stroke_df.itertuples())

        segment_df = self._form_segments(strokes)
        self.segments[interval] = segment_df

    def _form_segments(self, strokes: List) -> Optional[pd.DataFrame]:
        rows, temps = [], []
        for index, stroke in enumerate(strokes):
            temps.append(Item(index, stroke))

            is_last_stroke = index == len(strokes) - 1
            temps = self._process_strokes(rows, temps, is_last_stroke)
            if is_last_stroke:
                rows.append(stroke)

        return self.to_dataframe(rows, ['high', 'low'])

    def _process_strokes(self, rows: List, temps: List[Item], is_last_stroke: bool) -> List[Item]:
        count = len(temps)
        if count == 3:
            return self._handle_three_strokes(temps, is_last_stroke)
        elif count == 4:
            return self._handle_four_strokes(rows, temps, is_last_stroke)
        elif count == 5:
            return self._handle_five_strokes(temps, is_last_stroke)
        elif count >= 6 and count % 2 == 0:
            return self._handle_even_strokes(rows, temps, is_last_stroke)
        elif count >= 7 and count % 2 != 0:
            return self._handle_odd_strokes(rows, temps, is_last_stroke)
        return temps

    def _handle_three_strokes(self, temps: List[Item], is_last_stroke: bool) -> List[Item]:
        curr_stroke, next_stroke = temps[0], temps[2]
        if is_last_stroke or self._is_valid_segment(curr_stroke, next_stroke):
            return [next_stroke]
        return temps

    def _handle_four_strokes(self, rows: List, temps: List[Item], is_last_stroke: bool) -> List[Item]:
        curr_stroke, next_stroke, last_stroke = temps[0], temps[1], temps[3]
        if is_last_stroke or self._is_segment_extend(curr_stroke, next_stroke, last_stroke):
            rows.append(curr_stroke.item)
            return [last_stroke]
        return temps

    def _handle_five_strokes(self, temps: List[Item], is_last_stroke: bool) -> List[Item]:
        curr_stroke, next_stroke = temps[0], temps[4]
        if is_last_stroke or self._is_valid_segment(curr_stroke, next_stroke):
            return [next_stroke]
        return temps

    def _handle_even_strokes(self, rows: List, temps: List[Item], is_last_stroke: bool) -> List[Item]:
        curr_stroke, next_stroke, last_stroke = temps[0], temps[-3], temps[-1]
        if is_last_stroke or self._is_segment_extend(curr_stroke, next_stroke, last_stroke):
            rows.append(curr_stroke.item)
            return [last_stroke]
        return temps

    def _handle_odd_strokes(self, rows: List, temps: List[Item], is_last_stroke: bool) -> List[Item]:
        curr_stroke, next_stroke, last_stroke = temps[0], temps[-3], temps[-1]
        if is_last_stroke or self._can_split_from_middle(curr_stroke, next_stroke, last_stroke):
            rows.append(curr_stroke.item)
            mid_stroke = self._find_middle_stroke(temps, curr_stroke)
            rows.append(mid_stroke.item)
            return [last_stroke]
        return temps

    def _is_valid_segment(self, curr_stroke: Item, next_stroke: Item) -> bool:
        if self.is_top(curr_stroke.item):
            return next_stroke.item.high >= curr_stroke.item.high
        elif self.is_bottom(curr_stroke.item):
            return next_stroke.item.low <= curr_stroke.item.low
        return False

    def _is_segment_extend(self, curr_stroke: Item, next_stroke: Item, last_stroke: Item) -> bool:
        if self.is_top(curr_stroke.item):
            return last_stroke.item.low <= next_stroke.item.low
        elif self.is_bottom(curr_stroke.item):
            return last_stroke.item.high >= next_stroke.item.high
        return False

    def _can_split_from_middle(self, curr_stroke: Item, next_stroke: Item, last_stroke: Item) -> bool:
        if self.is_top(curr_stroke.item):
            return last_stroke.item.high >= next_stroke.item.high
        elif self.is_bottom(curr_stroke.item):
            return last_stroke.item.low <= next_stroke.item.low
        return False

    def _find_middle_stroke(self, temps: List[Item], curr_stroke: Item) -> Item:
        if self.is_top(curr_stroke.item):
            return self._find_lowest_middle(temps)
        else:
            return self._find_highest_middle(temps)

    @staticmethod
    def _find_lowest_middle(temps: List[Item]) -> Item:
        lowest = None
        for index in range(3, len(temps) - 3):
            stroke = temps[index]
            if lowest is None or stroke.item.low < lowest.item.low:
                lowest = stroke
        return lowest

    @staticmethod
    def _find_highest_middle(temps: List[Item]) -> Item:
        highest = None
        for index in range(3, len(temps) - 3):
            stroke = temps[index]
            if highest is None or stroke.item.high > highest.item.high:
                highest = stroke
        return highest
