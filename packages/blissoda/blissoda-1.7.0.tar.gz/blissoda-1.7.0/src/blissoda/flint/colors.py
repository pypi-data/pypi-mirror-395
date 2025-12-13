from typing import Optional


class ColorCycler:
    """Cycles through a predefined hex color palette."""

    def __init__(
        self,
        palette_name: Optional[str] = None,
        max_colors: Optional[int] = None,
    ):
        if palette_name is None:
            palette_name = "tableau_10"
        if palette_name not in _COLOR_PALETTES:
            raise ValueError(f"Unknown palette: {palette_name}")

        colors = _COLOR_PALETTES[palette_name]
        self._colors = colors
        self._next_index = 0
        self._max_colors = max_colors or len(colors)

    @property
    def max_colors(self) -> int:
        return self._max_colors

    @max_colors.setter
    def max_colors(self, max_colors: int) -> None:
        self._max_colors = max(max_colors, 0)
        self.reset()

    def next(self) -> str:
        """Return the next color in the cycle (hex string)."""
        color = self._colors[self._next_index]
        n = min(len(self._colors), self.max_colors)
        self._next_index = (self._next_index + 1) % n
        return color

    def reset(self):
        """Reset the cycle to the beginning."""
        self._next_index = 0


_COLOR_PALETTES = {
    "primary": [
        "#386CB0",  # Blue
        "#CC79A7",  # Pink
        "#66A61E",  # Green
        "#E7298A",  # Magenta
        "#7570B3",  # Purple
        "#E6AB02",  # Mustard
        "#A6761D",  # Brown
        "#66CCEE",  # Light Blue
        "#D55E00",  # Orange
        "#009E73",  # Teal
        "#F0E442",  # Yellow
        "#323232",  # Neutral Gray
    ],
    "dark_mode": [
        "#5B9BD5",  # Sky Blue
        "#ED7D31",  # Orange
        "#A5A5A5",  # Gray
        "#FFC000",  # Gold
        "#70AD47",  # Green
        "#255E91",  # Deep Blue
        "#C0504D",  # Red
        "#8064A2",  # Violet
        "#3B9B95",  # Teal
        "#F27CAE",  # Pink
        "#4472C4",  # Indigo
        "#FFD966",  # Warm Yellow
    ],
    "soft": [
        "#B3CDE3",  # Powder Blue
        "#FBB4AE",  # Soft Coral
        "#CCEBC5",  # Mint Green
        "#DECAE4",  # Lavender
        "#FED9A6",  # Peach
        "#FFFFCC",  # Light Yellow
        "#E5D8BD",  # Sand
        "#FDDAEC",  # Rose
        "#C8E6C9",  # Sage
        "#CCCCFF",  # Periwinkle
        "#FFE6CC",  # Cream
        "#CCFFE5",  # Mint
    ],
    "tol_bright": [
        "#4477AA",  # Blue
        "#66CCEE",  # Cyan
        "#228833",  # Green
        "#CCBB44",  # Yellow
        "#EE6677",  # Red
        "#AA3377",  # Purple
        "#BBBBBB",  # Gray
    ],
    "okabe_ito": [
        "#E69F00",  # Orange
        "#56B4E9",  # Sky Blue
        "#009E73",  # Bluish Green
        "#F0E442",  # Yellow
        "#0072B2",  # Blue
        "#D55E00",  # Vermillion
        "#CC79A7",  # Reddish Purple
    ],
    "tableau_10": [
        "#1F77B4",  # Blue
        "#FF7F0E",  # Orange
        "#2CA02C",  # Green
        "#D62728",  # Red
        "#9467BD",  # Purple
        "#8C564B",  # Brown
        "#E377C2",  # Pink
        "#7F7F7F",  # Gray
        "#BCBD22",  # Olive
        "#17BECF",  # Cyan
    ],
}
