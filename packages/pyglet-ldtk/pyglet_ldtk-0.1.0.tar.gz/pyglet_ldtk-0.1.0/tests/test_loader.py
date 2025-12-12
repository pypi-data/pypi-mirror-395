import json
import pytest

from ldtk.pyglet_ldtk_loader import Ldtk, LdtkLevel, LayerType, TileRenderMode

# --- Fixtures ---


@pytest.fixture
def mock_pyglet(mocker):
    """Mocks pyglet.image.load and other display-dependent functions."""
    mock_pg = mocker.patch("ldtk.pyglet_ldtk_loader.pyglet")
    # Mock image.load to return a dummy object with width/height
    mock_img = mocker.MagicMock()
    mock_img.width = 100
    mock_img.height = 100
    mock_img.get_region.return_value = mocker.MagicMock()  # Mock subsurface
    mock_pg.image.load.return_value = mock_img
    yield mock_pg


@pytest.fixture
def sample_ldtk_json():
    """Returns a minimal valid LDtk JSON structure for testing."""
    return {
        "__header__": {},
        "defs": {
            "tilesets": [
                {
                    "uid": 101,
                    "identifier": "Grass",
                    "relPath": "tiles.png",
                    "tileGridSize": 16,
                    "__cWid": 10,
                    "__cHei": 10,
                    "pxWid": 160,
                    "pxHei": 160,
                }
            ],
            "entities": [
                {
                    "uid": 201,
                    "identifier": "Player",
                    "width": 16,
                    "height": 16,
                    "renderMode": "Rectangle",
                    "tileRenderMode": "FitInside",
                    "tilesetId": 101,
                    "tileRect": {"tilesetUid": 101, "x": 0, "y": 0, "w": 16, "h": 16},
                }
            ],
            "layers": [
                {
                    "uid": 301,
                    "identifier": "Entities",
                    "type": "Entities",
                    "tilePivotX": 0.5,
                    "tilePivotY": 1.0,
                }
            ],
        },
        "levels": [
            {
                "identifier": "Level_0",
                "iid": "lvl_id_1",
                "uid": 1,
                "worldX": 0,
                "worldY": 0,
                "worldDepth": 0,
                "pxWid": 320,
                "pxHei": 240,
                "__bgColor": "#000000",
                "layerInstances": [
                    {
                        "__identifier": "Entities",
                        "__type": "Entities",
                        "__gridSize": 16,
                        "__cWid": 20,
                        "__cHei": 15,
                        "__pxTotalOffsetX": 0,
                        "__pxTotalOffsetY": 0,
                        "__opacity": 1.0,
                        "visible": True,
                        "layerDefUid": 301,
                        "entityInstances": [
                            {
                                "__identifier": "Player",
                                "iid": "ent_1",
                                "defUid": 201,
                                "width": 16,
                                "height": 16,
                                "px": [100, 200],  # x=100, y=200 (Top-Left)
                                "__pivot": [0.5, 1.0],  # Bottom-Center Pivot
                            }
                        ],
                    }
                ],
            }
        ],
    }


# --- Tests ---


def test_ldtk_initialization(mock_pyglet, sample_ldtk_json, mocker):
    """Test if the Ldtk class parses the JSON correctly."""

    # Mock opening the file
    mocker.patch(
        "builtins.open", mocker.mock_open(read_data=json.dumps(sample_ldtk_json))
    )
    loader = Ldtk("dummy_map.ldtk")

    assert len(loader.tilesets) == 1
    assert len(loader.entity_defs) == 1
    assert len(loader.levels) == 1
    assert isinstance(loader.levels[0], LdtkLevel)
    assert loader.levels[0].identifier == "Level_0"


def test_coordinate_conversion(mock_pyglet, sample_ldtk_json, mocker):
    """
    Critical Test: Ensure LDtk Top-Left coordinates are converted to Pyglet Bottom-Left.

    LDtk Y (Top-Down): 200
    Level Height: 240
    Entity Height: 16
    Pivot Y: 1.0

    Formula used in loader:
    ldtk_top = px[1] + offset - pivot * height
             = 200 + 0 - 1.0 * 16 = 184
    pyglet_y = level_height - (ldtk_top + height)
             = 240 - (184 + 16) = 40
    """
    mocker.patch(
        "builtins.open", mocker.mock_open(read_data=json.dumps(sample_ldtk_json))
    )
    loader = Ldtk("dummy_map.ldtk")

    level = loader.levels[0]
    layer = level.layers[0]  # Entities layer
    entity = layer.entities[0]  # Player

    # Verify X (Unchanged mostly)
    # x = 100 - 0.5 * 16 = 92
    assert entity.x == 92

    # Verify Y (Inverted)
    # Expected result based on logic above: 40
    assert entity.y == 40


def test_layer_ordering(mock_pyglet, sample_ldtk_json, mocker):
    """Ensure layers are stored in reverse order for Painter's Algorithm rendering."""

    data = sample_ldtk_json
    # Add a second layer to the JSON
    data["levels"][0]["layerInstances"].append(
        {
            "__identifier": "Tiles",
            "__type": "Tiles",
            "__gridSize": 16,
            "__cWid": 20,
            "__cHei": 15,
            "__pxTotalOffsetX": 0,
            "__pxTotalOffsetY": 0,
            "__opacity": 1.0,
            "visible": True,
            "layerDefUid": 301,  # Reusing for simplicity
            "gridTiles": [],
        }
    )

    mocker.patch("builtins.open", mocker.mock_open(read_data=json.dumps(data)))
    loader = Ldtk("dummy_map.ldtk")

    level = loader.levels[0]

    # In JSON: [Entities, Tiles] (Top to Bottom)
    # In Loader: Should be [Tiles, Entities] (Back to Front / Bottom to Top)
    assert len(level.layers) == 2
    assert level.layers[0].identifier == "Tiles"
    assert level.layers[0].type == LayerType.Tiles
    assert level.layers[1].identifier == "Entities"
    assert level.layers[1].type == LayerType.Entities


def test_level_methods(mock_pyglet, sample_ldtk_json, mocker):
    """Test LdtkLevel methods like GetLayerById and GetEntities*."""

    mocker.patch(
        "builtins.open", mocker.mock_open(read_data=json.dumps(sample_ldtk_json))
    )
    loader = Ldtk("dummy_map.ldtk")

    level = loader.levels[0]

    # Test GetLayerById
    layer = level.GetLayerById("Entities")
    assert layer.identifier == "Entities"
    assert layer.type == LayerType.Entities

    with pytest.raises(ValueError):
        level.GetLayerById("NonExistent")

    # Test GetAllEntities
    # We have 1 entity in the sample
    all_ents = level.GetAllEntities()
    assert len(all_ents) == 1
    assert all_ents[0].identifier == "Player"

    # Test GetEntitiesByLayer
    layer_ents = level.GetEntitiesByLayer("Entities")
    assert len(layer_ents) == 1
    assert layer_ents[0] == all_ents[0]

    empty_layer_ents = level.GetEntitiesByLayer(
        "NonExistentLayer"
    )  # Should return empty list if cache empty?
    # Wait, GetEntitiesByLayer implementation:
    # if layer_id not in self.getCache[0]...
    #   for e in self.entities: if e.layer.identifier == layer_id...
    # So if layer doesn't exist, it just returns empty list.
    assert len(empty_layer_ents) == 0

    # Test GetEntitiesByID
    player_ents = level.GetEntitiesByID("Player")
    assert len(player_ents) == 1
    assert player_ents[0].identifier == "Player"

    # Test GetEntitiesByUID
    # Player defUid is 201
    uid_ents = level.GetEntitiesByUID(201)
    assert len(uid_ents) == 1
    assert uid_ents[0].defUid == 201


def test_entity_sprite_generation(mock_pyglet, sample_ldtk_json, mocker):
    """Test that get_sprites creates pyglet sprites with correct texture."""

    mocker.patch(
        "builtins.open", mocker.mock_open(read_data=json.dumps(sample_ldtk_json))
    )
    mocker.patch("os.path.exists", return_value=True)
    loader = Ldtk("dummy_map.ldtk")

    entity = loader.levels[0].layers[0].entities[0]

    # Create a dummy batch and group
    mock_batch = mocker.MagicMock()
    mock_group = mocker.MagicMock()

    sprites = entity.get_sprites(mock_batch, mock_group)

    assert len(sprites) == 1
    # Check that Sprite was created with correct initial X
    # Note: Since Sprite is mocked, we check the call arguments
    # We access the LAST call because other sprites might have been created (though here only 1 expected)
    args, kwargs = mock_pyglet.sprite.Sprite.call_args
    assert kwargs["x"] == entity.x

    # Check that it attempted to slice the texture from the tileset
    # The TilesetDef.subsurface method calls pyglet image get_region
    # We can check if get_region was called on the mock image
    mock_pyglet.image.load.return_value.get_region.assert_called()


def test_enums(mock_pyglet, sample_ldtk_json, mocker):
    """Test that strings are correctly converted to Enums."""
    mocker.patch(
        "builtins.open", mocker.mock_open(read_data=json.dumps(sample_ldtk_json))
    )
    loader = Ldtk("dummy_map.ldtk")

    entity_def = loader.entity_defs[201]

    assert entity_def.renderMode == "Rectangle"  # Should match Enum string value
    assert entity_def.tileRenderMode == TileRenderMode.FitInside
