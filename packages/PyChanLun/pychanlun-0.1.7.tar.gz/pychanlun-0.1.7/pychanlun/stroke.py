from dataclasses import dataclass
from typing import Dict, Optional, Any, List

import pandas as pd

from pychanlun.fractal import Fractal


@dataclass
class Item:
    index: int
    item: Any


class Stroke(Fractal):
    MIN_LENGTH = 4

    def __init__(self, symbol: str, source: Dict[str, pd.DataFrame]):
        self.strokes: Dict[str, Optional[pd.DataFrame]] = {}
        super().__init__(symbol, source)

    def _process_interval(self, interval: str) -> None:
        super()._process_interval(interval)

        fractal_df = self.fractals[interval]
        if fractal_df is None or fractal_df.empty:
            self.strokes[interval] = None
            return

        fractals = list(fractal_df.itertuples())

        stroke_df = self._form_strokes(fractals)
        self.strokes[interval] = stroke_df

    def _form_strokes(self, fractals: List) -> Optional[pd.DataFrame]:
        rows, temps = [], []

        for index, fractal in enumerate(fractals):
            if not self.is_top(fractal) and not self.is_bottom(fractal):
                continue

            temps.append(Item(index, fractal))

            is_last_fractal = index == len(fractals) - 1
            temps = self._process_fractals(rows, temps, is_last_fractal)
            if is_last_fractal:
                rows.append(fractal)

        return self.to_dataframe(rows, ['high', 'low'])

    def _process_fractals(self, rows: List, temps: List[Item], is_last_fractal: bool) -> List[Item]:
        count = len(temps)
        if count == 2:
            return self._handle_two_fractals(rows, temps, is_last_fractal)
        elif count == 3:
            return self._handle_three_fractals(temps, is_last_fractal)
        elif count == 4:
            return self._handle_four_fractals(rows, temps, is_last_fractal)
        elif count == 5:
            return self._handle_five_fractals(temps, is_last_fractal)
        elif count == 6:
            return self._handle_six_fractals(rows, temps)
        return temps

    def _handle_two_fractals(self, rows: List, temps: List[Item], is_last_fractal: bool) -> List[Item]:
        curr_fractal, next_fractal = temps[0], temps[1]
        if is_last_fractal or self._is_valid_stroke(curr_fractal, next_fractal):
            rows.append(curr_fractal.item)
            return [next_fractal]
        return temps

    def _handle_three_fractals(self, temps: List[Item], is_last_fractal: bool) -> List[Item]:
        curr_fractal, next_fractal = temps[0], temps[2]
        if is_last_fractal or self._can_extend_stroke(curr_fractal, next_fractal):
            return [next_fractal]
        return temps

    def _handle_four_fractals(self, rows: List, temps: List[Item], is_last_fractal: bool) -> List[Item]:
        curr_fractal, next_fractal = temps[0], temps[3]
        if is_last_fractal or self._is_valid_stroke(curr_fractal, next_fractal):
            rows.append(curr_fractal.item)
            return [next_fractal]
        return temps

    def _handle_five_fractals(self, temps: List[Item], is_last_fractal: bool) -> List[Item]:
        curr_fractal, next_fractal = temps[0], temps[4]
        if is_last_fractal or self._can_extend_stroke(curr_fractal, next_fractal):
            return [next_fractal]
        return temps

    @staticmethod
    def _handle_six_fractals(rows: List, temps: List[Item]) -> List[Item]:
        curr_fractal, next_fractal = temps[0], temps[5]
        rows.append(curr_fractal.item)
        return [next_fractal]

    def _is_valid_stroke(self, curr_fractal: Item, next_fractal: Item) -> bool:
        return next_fractal.index - curr_fractal.index >= self.MIN_LENGTH

    def _can_extend_stroke(self, curr_fractal: Item, next_fractal: Item) -> bool:
        if self.is_top(curr_fractal.item):
            return next_fractal.item.high >= curr_fractal.item.high
        elif self.is_bottom(curr_fractal.item):
            return next_fractal.item.low <= curr_fractal.item.low
        return False
