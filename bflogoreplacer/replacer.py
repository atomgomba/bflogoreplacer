"""
Tools for customizing the logo in a Betaflight OSD font.

Some code were taken and modified from here:
https://github.com/Knifa/MAX7456-Font-Tools
"""
from typing import Generator

from .common import *


def _iter_mcm_tiles(filepath: str) -> Generator[MaxTile, None, None]:
    with open(filepath) as fp:
        lines = [line.rstrip() for line in fp.readlines()]

    expected_line_count = SYMBOL_COUNT * DATA_CHUNK_SIZE + 1
    line_count = len(lines)
    if line_count < expected_line_count:
        # wrong input data length
        raise DataLengthError(expected_line_count, line_count)

    if not lines[HEADER_INDEX] == HEADER_SIGNATURE:
        # missing header
        raise MissingHeaderError()

    data = lines[DATA_INDEX:]
    for i in range(SYMBOL_COUNT):
        yield data[i * DATA_CHUNK_SIZE:i * DATA_CHUNK_SIZE + DATA_CHUNK_SIZE]


def _iter_image_tiles(filepath: str) -> Generator[MaxTile, None, None]:
    image = Image.open(filepath).convert('RGB')
    width, height = SYMBOL_SIZE
    horiz_tiles = int(image.width / width)
    vert_tiles = int(image.height / height)

    expected_width = horiz_tiles * width
    expected_height = vert_tiles * height
    if not (expected_width == image.width and expected_height == image.height):
        raise ImageSizeError((expected_width, expected_height), (image.width, image.height))

    for y in range(vert_tiles):
        for x in range(horiz_tiles):
            left, top = x * width, y * height
            yield _mcm_tile_from_image(image.crop((left, top, left + width, top + height)))


def _mcm_tile_from_image(image: ImageType) -> MaxTile:
    width, height = SYMBOL_SIZE
    pixeldata = image.getdata()
    pixels = [COLOR_MAP.get(pixeldata[i], DEFAULT_COLOR) for i in range(width * height)]
    lines = ["".join(pixels[i: i + MCM_LINE_LENGTH]) for i in range(0, len(pixels), MCM_LINE_LENGTH)]

    linenum = len(lines)
    if linenum < DATA_CHUNK_SIZE:
        lines += [PAD_CHUNK] * (DATA_CHUNK_SIZE - linenum)

    return lines


def replace_logo(mcm_path: str, image_path: str) -> str:
    """Replace the Betaflight logo in an MCM font file with another image.

    :param mcm_path: path to the font file
    :param image_path: path to the image
    :return: resulting font as a string
    """
    result = [HEADER_SIGNATURE]
    for i, orig_tile in enumerate(_iter_mcm_tiles(mcm_path)):
        if i == BETAFLIGTH_LOGO_START_INDEX:
            break
        result.append("\n".join(orig_tile))
    for new_tile in _iter_image_tiles(image_path):
        result.append("\n".join(new_tile))
    return "\n".join(result)
