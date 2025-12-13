# BLEPrinter

BLEPrinter is a library for working with "cat printers," a sort of cheap
receipt printer which communicates using an undocumented protocol over
Bluetooth Low Energy. Unlike similar programs, BLEPrinter is:

1. Text-oriented, and
2. Meant to be used in other projects.

It achieves the former by taking in formatted text, rendering those
inputs an as image, before sending the result over the wire.

Due to the obfuscated nature of the printers, my own limited access to
the hardware, and a principled allocation of resources, this code has
not been verified to work with all similar devices in every situation.
BLEPrinter strives to be robust and sensical, well typed and formatted,
not necessarily to handle every edge case.

Where improvements are to be made—I would be thrilled to hear from you
and accept your contributions. In particular, weaving in support for
images and other content types (such as barcodes or QR codes) would be
first on the hypothetical project roadmap.

## Documentation and Usage

```python
import asyncio
from bleprinter import Printer

def main():
  p = Printer()
  p.textln("Hello World!", size=4, bold=True, centered=True)
  p.textln("from figbert", size=2, centered=True)

  p.textln("Neat Heading", underline=True)
  p.textln("Fin.")

  asyncio.run(p.cut())
```


## Dependencies
- [bleak](https://github.com/hbldh/bleak)
- [opencv-python](https://github.com/opencv/opencv-python)

## References
- [catprinter](https://github.com/rbaron/catprinter)
- [python-escpos](https://github.com/python-escpos/python-escpos)
