import pytest
from ldtk.pyglet_ldtk_loader import FieldParser


def test_parse_color():
    field = {"__type": "Color", "__value": "#ff0000"}
    assert FieldParser.parse(None, field) == (255, 0, 0)


def test_parse_point(mocker):
    # Mock Layer structure
    layer = mocker.MagicMock()
    layer.gridSize = 16
    layer.pxOffset = [0, 0]
    layer.level.sizePx = [256, 256]

    # LDtk Point: cx=10, cy=5
    # Grid=16.
    # LDtk Pixel Coords (Top-Left):
    # x = 10*16 + 8 = 168
    # y = 5*16 + 8 = 88

    # Pyglet Pixel Coords (Bottom-Left):
    # Y = Height - Y_ldtk = 256 - 88 = 168

    field = {"__type": "Point", "__value": {"cx": 10, "cy": 5}}

    result = FieldParser.parse(layer, field)
    assert result == (168, 168)


def test_parse_point_with_offsets(mocker):
    layer = mocker.MagicMock()
    layer.gridSize = 16
    layer.pxOffset = [10, 20]  # Offset X=10, Y=20
    layer.level.sizePx = [256, 256]

    # LDtk Pixel Coords (Top-Left relative to level):
    # Grid center: 168, 88

    # Formula:
    # final_x = ldtk_x + layer.pxOffset[0] = 168 + 10 = 178
    # final_y = layer.level.sizePx[1] - (ldtk_y + layer.pxOffset[1])
    #         = 256 - (88 + 20) = 256 - 108 = 148

    field = {"__type": "Point", "__value": {"cx": 10, "cy": 5}}

    result = FieldParser.parse(layer, field)
    assert result == (178, 148)
