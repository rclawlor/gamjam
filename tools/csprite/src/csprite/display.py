# Standard library imports
import typing as t


TABLE_WIDTH = 30


class DisplayTable():
    def __init__(self, header: str):
        self._header = header
        self._data = {}
        self._palettes = {}
        self.w = TABLE_WIDTH

    def add_row(self, key: str, value: t.Any) -> None:
        """Add row to table"""
        self._data[key] = value

    def add_palette(self, key: str, colours: list) -> None:
        """Add palette to table"""
        palette = ""
        for r, g, b in colours:
            palette += f"\033[38;2;{r};{g};{b}m■\033[0m"
        self._palettes[key] = palette

    def _generate_header(self) -> None:
        """Print header with border"""
        print(
            "╒" + self.w * "═" + "╕\n"
            "│" + "{:^{width}}".format(self._header, width=self.w) + "│\n"
            "╞" + self.w * "═" + "╡"
        )

    def _generate_rows(self) -> None:
        """Print table rows"""
        for k, v in self._data.items():
            print(
                "│"
                + "{:>{width}}: ".format(k, width=self.w // 2)
                + "{:<{width}}".format(v, width=self.w // 2 - 2)
                + "│"
            )

    def _generate_palettes(self) -> None:
        """Print table palettes"""
        for k, v in self._palettes.items():
            print(
                "│"
                + "{:>{width}}: ".format(k, width=self.w // 2)
                + "{:<{width}}     ".format(v, width=self.w // 2)
                + "│"
            )

    def _generate_footer(self) -> None:
        """Print table footer"""
        print("└" + self.w * "─" + "┘")

    def draw(self) -> None:
        """Draw table to stdout"""
        self._generate_header()
        self._generate_rows()
        self._generate_palettes()
        self._generate_footer()
