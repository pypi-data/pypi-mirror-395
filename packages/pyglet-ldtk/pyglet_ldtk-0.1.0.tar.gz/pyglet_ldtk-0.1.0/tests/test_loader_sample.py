import os
import pytest

from ldtk.pyglet_ldtk_loader import Ldtk, LayerType, Entity

# Samples directory relative to this test file
SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "samples")

samples = [
    "AutoLayers_1_basic.ldtk",
    "AutoLayers_2_stamps.ldtk",
    "AutoLayers_3_Mosaic.ldtk",
    "AutoLayers_4_Assistant.ldtk",
    "AutoLayers_5_Advanced.ldtk",
    "AutoLayers_6_OptionalRules.ldtk",
    "AutoLayers_7_Biomes.ldtk",
    "Entities.ldtk",
    "SeparateLevelFiles.ldtk",
    "Test_file_for_API_showing_all_features.ldtk",
    "Typical_2D_platformer_example.ldtk",
    "Typical_TopDown_example.ldtk",
    "WorldMap_Free_layout.ldtk",
    "WorldMap_GridVania_layout.ldtk",
]


@pytest.fixture
def mock_pyglet(mocker):
    """Mocks pyglet to avoid display connection."""
    mock_pg = mocker.patch("ldtk.pyglet_ldtk_loader.pyglet")
    mock_img = mocker.MagicMock()
    mock_img.width = 100
    mock_img.height = 100
    # Mock get_region to return another mock that can be used as texture
    mock_region = mocker.MagicMock()
    mock_region.width = 10
    mock_region.height = 10
    mock_img.get_region.return_value = mock_region

    mock_pg.image.load.return_value = mock_img
    yield mock_pg


def test_load_sample(mock_pyglet):
    """Test loading all sample files."""
    for path in samples:
        full_path = os.path.join(SAMPLES_DIR, path)
        if os.path.exists(full_path):
            try:
                Ldtk(full_path)
            except Exception as e:
                pytest.fail(f"Failed to load {path}: {e}")
        else:
            pytest.warns(UserWarning, match=f"Sample file not found: {full_path}")


def get_field_value(entity: Entity, field_identifier: str):
    """Helper to extract a field value from an entity instance."""
    for field in entity.data.get("fieldInstances", []):
        if field["__identifier"] == field_identifier:
            return field["__value"]
    return None


def test_many_features(mock_pyglet):
    """Port of test_many_features using pyglet_ldtk_loader."""
    path = os.path.join(SAMPLES_DIR, "Test_file_for_API_showing_all_features.ldtk")
    if not os.path.exists(path):
        pytest.skip(f"Sample file {path} not found")

    example = Ldtk(path)

    assert isinstance(example.levels, list)
    assert len(example.levels) == 4

    fst_level = example.levels[0]
    assert fst_level.identifier == "Everything"
    assert isinstance(fst_level.defs, dict)

    # Iterate over layers in the first level
    # Note: loader.layers is reversed (Back-to-Front) compared to LDtk JSON (Front-to-Back)
    # We iterate and check by identifier

    found_layers = set()

    for layer in fst_level.layers:
        found_layers.add(layer.identifier)
        assert isinstance(
            layer.data, dict
        )  # defs are in data or separate? loader has layer.tileset (TilesetDef)

        if layer.identifier == "Entities":
            assert layer.type == LayerType.Entities
            assert not layer.tiles  # auto_layer_tiles is None
            assert not layer.intgrid  # int_grid_csv is empty/None

            for instance in layer.entities:
                assert isinstance(instance, Entity)
                assert (
                    instance.definition is not None
                )  # Like isinstance(instance.defs, arcadeLDtk.Defs)

                target_value = get_field_value(instance, "target")
                if target_value:
                    assert isinstance(target_value, dict)
                    # Resolution of entity reference is not directly supported by loader methods
                    # But we can verify the structure exists
                    assert "entityIid" in target_value
                    assert "levelIid" in target_value

        elif layer.identifier == "IntGrid_8px_grid":
            assert layer.type == LayerType.IntGrid

        elif layer.identifier == "PureAutoLayer":
            assert layer.type == LayerType.AutoLayer

        elif layer.identifier == "IntGrid_without_rules":
            assert layer.type == LayerType.IntGrid
            assert not layer.tiles  # has_tiles() is False

        elif layer.identifier == "IntGrid_with_rules":
            assert layer.type == LayerType.IntGrid
            assert layer.tiles  # has_tiles() is True

        elif layer.identifier == "Tiles":
            assert layer.type == LayerType.Tiles
            assert layer.tiles  # has_tiles()

    # Ensure we visited expected layers
    expected_layers = {
        "Entities",
        "IntGrid_8px_grid",
        "PureAutoLayer",
        "IntGrid_without_rules",
        "IntGrid_with_rules",
        "Tiles",
    }
    # Use set.issubset because there might be other layers
    assert expected_layers.issubset(found_layers)
