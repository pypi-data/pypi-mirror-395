from typing import Tuple, Optional, Dict, List, Any

from .layout_element import LayoutElement


class ContentSizeFitter:

    def __init__(self, fit_mode: str = "preferred"):
        self.fit_mode = fit_mode  

    def fit_size(self, element: LayoutElement, available_width: int, available_height: int) -> Tuple[int, int]:
        min_w, min_h = element.get_min_size()
        pref_w, pref_h = element.get_preferred_size()
        flex_w, flex_h = element.get_flexible_size()

        if self.fit_mode == "preferred":
            return (pref_w, pref_h)
        elif self.fit_mode == "min":
            return (min_w, min_h)
        elif self.fit_mode == "flexible":
            
            final_w = min_w + flex_w if flex_w > 0 else pref_w
            final_h = min_h + flex_h if flex_h > 0 else pref_h
            return (min(final_w, available_width), min(final_h, available_height))
        else:
            return (pref_w, pref_h)