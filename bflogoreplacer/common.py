from typing import Tuple

from PIL import Image


class McmError(BaseException):
    pass


class MissingHeaderError(McmError):
    def __str__(self):
        return "Corrupt file: missing header"


class DataLengthError(McmError):
    def __init__(self, expected_line_count: int, line_count: int):
        super().__init__()
        self.expected_line_count = expected_line_count  # type: int
        self.line_count = line_count  # type: int

    def __str__(self):
        return "Corrupt file: not enough lines: {:d} (expected {:d})" \
               .format(self.line_count, self.expected_line_count)


class ImageSizeError(McmError):
    def __init__(self, expected_size: Tuple[int, int], image_size: Tuple[int, int]):
        super().__init__()
        self.expected_size = expected_size  # type: Tuple[int, int]
        self.image_size = image_size  # type: Tuple[int, int]

    def __str__(self):
        return "Invalid image size: {0[0]:d}×{0[1]:d} (expected {1[0]:d}×{1[1]:d})" \
               .format(self.image_size, self.expected_size)


HEADER_INDEX = 0
HEADER_SIGNATURE = 'MAX7456'
DATA_INDEX = HEADER_INDEX + 1
DATA_CHUNK_SIZE = 64
SYMBOL_COUNT = 256
SYMBOL_SIZE = (12, 18)
MCM_LINE_LENGTH = 4
COLOR_MAP = {
    0: '00',
    1: '10',
    (0, 0, 0): '00',
    (255, 255, 255): '10',
    (0, 0, 0, 255): '00',
    (255, 255, 255, 255): '10',
}
DEFAULT_COLOR = '01'
PAD_CHUNK = DEFAULT_COLOR * MCM_LINE_LENGTH
BETAFLIGTH_LOGO_START_INDEX = 160

ImageType = Image.Image
MaxTile = list
