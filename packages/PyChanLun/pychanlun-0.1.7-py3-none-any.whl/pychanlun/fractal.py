from typing import Dict, Optional, List, Tuple

import numpy as np
import pandas as pd
from pychanlun.stick import Stick


class Fractal(Stick):

    def __init__(self, symbol: str, source: Dict[str, pd.DataFrame]):
        self.fractals: Dict[str, Optional[pd.DataFrame]] = {}
        super().__init__(symbol, source)

    def _process_interval(self, interval: str) -> None:
        super()._process_interval(interval)

        stick_df = self.sticks[interval]
        if stick_df is None or stick_df.empty:
            self.fractals[interval] = None
            return

        sticks = list(stick_df.itertuples())

        fractal_df = self._scan_for_fractals(sticks)
        self.fractals[interval] = fractal_df

    def _scan_for_fractals(self, sticks: List) -> Optional[pd.DataFrame]:
        rows = []

        for index in range(1, len(sticks)):
            prev_stick, curr_stick = sticks[index - 1], sticks[index]
            next_stick = sticks[index + 1] if index < len(sticks) - 1 else None
            rows.append(self._classify_fractal(prev_stick, curr_stick, next_stick))

        return self.to_dataframe(rows, ['high', 'low'])

    def _classify_fractal(self, prev_stick: Tuple, curr_stick: Tuple, next_stick: Tuple) -> Tuple:
        if self._is_top_fractal(prev_stick, curr_stick, next_stick):
            return curr_stick._replace(low=np.nan)
        elif self._is_bottom_fractal(prev_stick, curr_stick, next_stick):
            return curr_stick._replace(high=np.nan)
        else:
            return curr_stick._replace(high=np.nan, low=np.nan)

    @staticmethod
    def _is_top_fractal(prev_stick: Tuple, curr_stick: Tuple, next_stick: Tuple) -> bool:
        prev_is_low = prev_stick is None or curr_stick.high > prev_stick.high
        next_is_low = next_stick is None or curr_stick.high > next_stick.high
        return prev_is_low and next_is_low

    @staticmethod
    def _is_bottom_fractal(prev_stick: Tuple, curr_stick: Tuple, next_stick: Tuple) -> bool:
        prev_is_high = prev_stick is None or curr_stick.low < prev_stick.low
        next_is_high = next_stick is None or curr_stick.low < next_stick.low
        return prev_is_high and next_is_high
