"""
Tools for customizing the logo in a Betaflight OSD font.

Some code were taken and modified from here:
https://github.com/Knifa/MAX7456-Font-Tools
"""
from typing import Generator

from .common import *


def _iter_mcm_tiles(filepath: str) -> Generator[MaxTile, None, None]:
    """Iterate tiles in an MCM font.

    :param filepath: path to an MCM file
    :return: a generator that yields MCM tiles
    """
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


def _mcm_tile_from_image(image: ImageType) -> MaxTile:
    """Create an MCM tile from an image.

    :param image: PIL Image object
    :return: resulting tile as a list of strings
    :raise UnexpectedColorError: image contains a pixel of unexpected color
    """
    width, height = SYMBOL_SIZE
    pixeldata = image.getdata()
    pixels = []
    for i in range(width * height):
        color = pixeldata[i]
        try:
            pixels.append(COLOR_MAP[color])
        except KeyError:
            pos_x, pos_y = i % width, i / width
            raise UnexpectedColorError(tuple(color), pos_x, pos_y)
    lines = ["".join(pixels[i: i + MCM_LINE_LENGTH]) for i in range(0, len(pixels), MCM_LINE_LENGTH)]

    linenum = len(lines)
    if linenum < DATA_CHUNK_SIZE:
        lines += [PAD_CHUNK] * (DATA_CHUNK_SIZE - linenum)

    return lines


def _iter_image_tiles(filepath: str) -> Generator[MaxTile, None, None]:
    """Iterate tiles in an image.

    :param filepath: path to an image file
    :return: a generator that yields MCM tiles
    """
    image = Image.open(filepath).convert('RGB')
    width, height = SYMBOL_SIZE
    horiz_tiles, vert_tiles = LOGO_TILE_SIZE

    expected_width = horiz_tiles * width
    expected_height = vert_tiles * height
    if not (expected_width == image.width and expected_height == image.height):
        raise ImageSizeError((expected_width, expected_height), (image.width, image.height))

    for tile_y in range(vert_tiles):
        for tile_x in range(horiz_tiles):
            left, top = tile_x * width, tile_y * height
            try:
                yield _mcm_tile_from_image(image.crop((left, top, left + width, top + height)))
            except UnexpectedColorError as e:
                e.set_position(e.pos_x + left, e.pos_y + top)
                raise e


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
