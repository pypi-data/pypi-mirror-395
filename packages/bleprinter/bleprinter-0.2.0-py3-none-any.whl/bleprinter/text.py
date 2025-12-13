import cv2

from bleprinter.const import FONT_FAMILY, FONT_SIZE_MULTIPLIER


class Text:
    size: int
    bold: bool
    underline: bool
    centered: bool
    content: str

    def __init__(
        self,
        content: str,
        size: int = 1,
        bold: bool = False,
        underline: bool = False,
        centered: bool = False,
    ):
        self.content = content
        self.size = size
        self.bold = bold
        self.underline = underline
        self.centered = centered

    def dimensions(self) -> tuple[int, int]:
        (width, height), baseline = cv2.getTextSize(
            self.content,
            FONT_FAMILY,
            FONT_SIZE_MULTIPLIER * self.size,
            self.thickness(),
        )
        return width, height + baseline

    def thickness(self) -> int:
        if self.bold:
            if self.size > 3:
                return 3
            else:
                return 2
        return 1
