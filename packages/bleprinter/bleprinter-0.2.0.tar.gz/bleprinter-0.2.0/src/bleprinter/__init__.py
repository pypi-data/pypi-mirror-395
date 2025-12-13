import cv2
import numpy as np
import textwrap

from bleprinter.ble import run_ble
from bleprinter.cmds import PRINT_WIDTH, cmds_print_img
from bleprinter.const import FONT_SIZE_MULTIPLIER, FONT_FAMILY
from bleprinter.text import Text


class Printer:
    content: list[Text] = []

    def __receipt_height(self):
        minimum = sum([ht for _, ht in [frag.dimensions() for frag in self.content]])
        minimum += 10 * len(self.content)
        return (minimum + 7) & ~7  # Round up to multiple of 8

    def __image_from_text(self):
        img = np.zeros((self.__receipt_height(), PRINT_WIDTH), np.uint8)
        running_height = 0

        for fragment in self.content:
            width, height = fragment.dimensions()
            x = 10 if not fragment.centered else int((PRINT_WIDTH - width) / 2)
            _ = cv2.putText(
                img,
                fragment.content,
                (x, running_height + height),
                FONT_FAMILY,
                FONT_SIZE_MULTIPLIER * fragment.size,
                (255, 255, 255),
                fragment.thickness(),
                cv2.LINE_AA,
            )
            if fragment.underline:
                _ = cv2.line(
                    img,
                    (x, running_height + height),
                    (x + width, running_height + height),
                    (255, 255, 255),
                    2,
                )

            running_height += height + 10

        return img

    def __write_lines(
        self,
        lines: list[str],
        size: int = 1,
        bold: bool = False,
        underline: bool = False,
        centered: bool = False,
    ):
        self.content.extend(
            [Text(line, size, bold, underline, centered) for line in lines]
        )

    def textln(
        self,
        text: str,
        size: int = 1,
        bold: bool = False,
        underline: bool = False,
        centered: bool = False,
    ):
        self.__write_lines(text.splitlines(), size, bold, underline, centered)

    def textln_wrapped(
        self,
        text: str,
        width: int = 72,
        size: int = 1,
        bold: bool = False,
        underline: bool = False,
        centered: bool = False,
    ):
        out: list[str] = []
        lines = text.splitlines()
        wrapper = textwrap.TextWrapper(width)
        for line in lines:
            out += wrapper.wrap(line)

        self.__write_lines(out, size, bold, underline, centered)

    async def cut(self):
        data = cmds_print_img(self.__image_from_text())
        await run_ble(data)
