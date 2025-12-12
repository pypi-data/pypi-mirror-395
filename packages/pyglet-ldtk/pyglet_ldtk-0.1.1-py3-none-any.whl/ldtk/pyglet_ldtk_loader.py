"""
pyglet_ldtk_loader.py

A module for loading LDtk (Level Designer Toolkit) maps into Pyglet.

Usage:
    loader = Ldtk("path/to/map.ldtk")
    level = loader.levels[0]

    # Add to a batch
    batch = pyglet.graphics.Batch()
    level.addToBatch(batch)

    # Draw
    batch.draw()
"""

import json
import os
import math
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, cast

import pyglet


# ===============================================
#  Enums
# ===============================================
class WorldLayout(str, Enum):
    """Enum for World Layout types."""

    Freeform = "Free"
    GridVania = "GridVania"
    LinearHorizontal = "LinearHorizontal"
    LinearVertical = "LinearVertical"


class LayerType(str, Enum):
    """Enum for Layer types."""

    IntGrid = "IntGrid"
    Entities = "Entities"
    Tiles = "Tiles"
    AutoLayer = "AutoLayer"


class RenderMode(str, Enum):
    """Enum for Entity Render Modes."""

    Rectangle = "Rectangle"
    Ellipse = "Ellipse"
    Tile = "Tile"
    Cross = "Cross"


class TileRenderMode(str, Enum):
    """Enum for Tile Render Modes."""

    Cover = "Cover"
    FitInside = "FitInside"
    Repeat = "Repeat"
    Stretch = "Stretch"
    FullSizeCropped = "FullSizeCropped"
    FullSizeUncropped = "FullSizeUncropped"
    NineSlice = "NineSlice"


class FlipBits(int, Enum):
    """Bitfield enum for Tile flipping."""

    FlipNone = 0
    FlipX = 1
    FlipY = 2
    FlipXY = 3


# ===============================================
#  Helper Classes
# ===============================================
class TilesetRectangle:
    """This object represents a custom sub rectangle in a Tileset image."""

    x: int
    y: int
    w: int
    h: int
    tileset_uid: Optional[int]

    def __init__(
        self, x: int, y: int, w: int, h: int, tileset_uid: Optional[int]
    ) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.tileset_uid = tileset_uid

    @staticmethod
    def from_dict(obj: Any) -> "TilesetRectangle":
        if not isinstance(obj, dict):
            raise TypeError("Expected dict for TilesetRectangle")
        x = obj.get("x", int)
        y = obj.get("y", int)
        w = obj.get("w", int)
        h = obj.get("h", int)
        tileset_uid = obj.get("tilesetUid", int)
        return TilesetRectangle(x, y, w, h, tileset_uid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["x"] = self.x
        result["y"] = self.y
        result["w"] = self.w
        result["h"] = self.h
        result["tilesetUid"] = self.tileset_uid
        return result


class FieldParser:
    """Parses LDtk field instances into usable Python types."""

    @staticmethod
    def parse(layer: Optional["Layer"], field_data: Dict) -> Any:
        val = field_data.get("__value")
        if val is None:
            return None

        type_name = field_data.get("__type", "")

        # 1. Handle Colors (Hex string -> RGB tuple)
        if type_name == "Color":
            # LDtk colors are "#RRGGBB"
            c = val.lstrip("#")
            return tuple(int(c[i : i + 2], 16) for i in (0, 2, 4))

        # 2. Handle Points (Grid Coords -> World Pixel Coords)
        elif type_name == "Point":
            if layer is None:
                return None

            # Val is {'cx': 10, 'cy': 5}
            # Convert to pixel coordinates using the layer's logic
            cx, cy = val["cx"], val["cy"]

            # Use Layer's grid size
            grid = layer.gridSize

            # LDtk (Top-Left) -> Pixel
            ldtk_x = cx * grid + grid / 2
            ldtk_y = cy * grid + grid / 2

            # Convert to Pyglet (Bottom-Left)
            # We need the level height for this.
            # layer.level.sizePx[1]

            final_x = ldtk_x + layer.pxOffset[0]
            final_y = layer.level.sizePx[1] - (ldtk_y + layer.pxOffset[1])

            return (final_x, final_y)

        # 3. Handle Enums (Simple String)
        elif type_name == "Enum":
            return val  # It's already a string, which is fine

        # 4. Handle Arrays (Recursively parse)
        elif type_name.startswith("Array<"):
            # This is a bit complex for a simple parser, but basic lists work fine
            # as raw values usually.
            return val

        return val


# ===============================================
#  Definitions
# ===============================================
class EntityDef:
    """Definition of an Entity from LDtk Project Definitions."""

    def __init__(self, data: Dict):
        """
        Initialize EntityDef.

        Args:
            data (Dict): The 'EntityDefinition' dictionary from LDtk JSON.
        """
        self.uid: int = data["uid"]
        self.identifier: str = data["identifier"]
        self.width: int = data["width"]
        self.height: int = data["height"]
        self.renderMode = RenderMode(data.get("renderMode", "Rectangle"))
        self.tileRenderMode = TileRenderMode(data.get("tileRenderMode", "FitInside"))
        self.tilesetId: Optional[int] = data.get("tilesetId")
        self.tileRect: Optional[Dict] = data.get("tileRect")
        self.nineSliceBorders: List[int] = data.get("nineSliceBorders", [])
        self.pivot: List[float] = [data.get("pivotX", 0.5), data.get("pivotY", 0.5)]


class TilesetDef:
    """Definition of a Tileset, handling image loading and slicing."""

    def __init__(self, file_loc: str, data: Dict):
        """
        Initialize a TilesetDef.

        Args:
            file_loc (str): The absolute path of the LDtk file (for relative path resolution).
            data (Dict): The 'TilesetDefinition' dictionary from LDtk JSON.
        """
        self.data: Dict = data
        self.fileLoc: str = file_loc
        self.identifier: str = self.data["identifier"]
        self.uid: int = self.data["uid"]
        self.tileGridSize: int = self.data["tileGridSize"]
        self.width: int = self.data["__cWid"]
        self.height: int = self.data["__cHei"]

        self.tilesetPath: Optional[str] = None
        self.tileSet: Optional[pyglet.image.AbstractImage] = None

        if self.data.get("relPath"):
            self.tilesetPath = self.data["relPath"]
            abs_path = os.path.abspath(os.path.join(file_loc, "../", self.tilesetPath))
            if os.path.exists(abs_path):
                self.tileSet = pyglet.image.load(abs_path)

    def subsurface(
        self, x: int, y: int, w: int, h: int
    ) -> Optional[pyglet.image.AbstractImage]:
        """
        Get a region of the tileset image.

        Args:
            x (int): X position (Top-Left based).
            y (int): Y position (Top-Left based).
            w (int): Width.
            h (int): Height.

        Returns:
            Optional[pyglet.image.AbstractImage]: The image region, or None if tileset not loaded.
        """
        if not self.tileSet:
            return None
        # Pyglet Y is bottom-up, so we flip Y
        pyglet_y = self.tileSet.height - y - h
        return self.tileSet.get_region(x, pyglet_y, w, h)

    def getTile(self, tile_obj: "Tile") -> Optional[pyglet.image.AbstractImage]:
        """
        Get the texture for a specific Tile instance, applying flips if needed.

        Args:
            tile_obj (Tile): The tile instance.

        Returns:
            Optional[pyglet.image.AbstractImage]: The texture region.
        """
        if not self.tileSet:
            return None
        region = self.subsurface(
            tile_obj.src[0], tile_obj.src[1], self.tileGridSize, self.tileGridSize
        )
        if hasattr(region, "get_transform"):
            return region.get_transform(flip_x=tile_obj.flip_x, flip_y=tile_obj.flip_y)
        return region


# ===============================================
#  Loaders
# ===============================================
class LdtkJSON:
    """Base class for parsing LDtk JSON data."""

    def __init__(self, json_content: Dict[str, Any], file_loc: str = ""):
        """
        Instantiate an LDtk file object with its JSON.

        Args:
            json_content (Dict[str, Any]): The LDtk file's contents
            file_loc (str, optional): The location of the file. Defaults to ''.
        """
        self.ldtkData: Dict = json_content
        self.header: Dict = self.ldtkData.get("__header__", {})
        self.defs: Dict = self.ldtkData.get("defs", {})

        # Parse Definitions
        self.tilesets: Dict[int, TilesetDef] = {}
        for i in self.defs.get("tilesets", []):
            t = TilesetDef(file_loc, i)
            self.tilesets[t.uid] = t

        self.entity_defs: Dict[int, EntityDef] = {}
        for i in self.defs.get("entities", []):
            e = EntityDef(i)
            self.entity_defs[e.uid] = e

        self.levels: List[LdtkLevel] = []

        # Handle Modern "Multi-Worlds" vs Legacy
        if "worlds" in self.ldtkData and self.ldtkData["worlds"]:
            for world in self.ldtkData["worlds"]:
                for lvl in world.get("levels", []):
                    self.levels.append(
                        LdtkLevel(
                            lvl, self.tilesets, self.entity_defs, self.defs, file_loc
                        )
                    )
        else:
            # Fallback to root levels
            for lvl in self.ldtkData.get("levels", []):
                self.levels.append(
                    LdtkLevel(lvl, self.tilesets, self.entity_defs, self.defs, file_loc)
                )


class Ldtk(LdtkJSON):
    """Main entry point for loading an LDtk project from a file."""

    def __init__(self, ldtk_file: str):
        """
        Instantiate an LDtk file object via its file location.

        Args:
            ldtk_file (str): The LDtk file's path.
        """
        with open(ldtk_file, "r", encoding="utf-8") as data:
            dat = json.load(data)
        super().__init__(dat, ldtk_file)


class LdtkLevel:
    """
    Represents a Level within an LDtk project.
    """

    def __init__(
        self,
        data: Dict,
        tilesets: Dict[int, TilesetDef],
        entity_defs: Dict[int, EntityDef],
        defs: Dict,
        file_loc: str,
    ):
        """
        Initialize a Level.

        Args:
            data (Dict): Level JSON data.
            tilesets (Dict): Dictionary of TilesetDefs.
            entity_defs (Dict): Dictionary of EntityDefs.
            defs (Dict): Global Definitions dictionary.
            file_loc (str): Path to the LDtk file.
        """
        self.defs: Dict = defs
        self.data: Dict = data
        self.tilesets: Dict[int, TilesetDef] = tilesets
        self.entity_defs: Dict[int, EntityDef] = entity_defs
        self.fileLoc: str = file_loc

        # External Levels Logic
        if self.data.get("externalRelPath"):
            ext_rel = self.data["externalRelPath"]
            ext_path = os.path.abspath(os.path.join(os.path.dirname(file_loc), ext_rel))
            if os.path.exists(ext_path):
                with open(ext_path, "r", encoding="utf-8") as f:
                    ext_data = json.load(f)
                # Merge relevant fields
                self.data["layerInstances"] = ext_data.get("layerInstances", [])
                self.data["__neighbours"] = ext_data.get("__neighbours", [])

        self.identifier: str = self.data["identifier"]
        self.iid: str = self.data["iid"]
        self.uid: int = self.data["uid"]
        self.worldPos: List[int] = [
            self.data["worldX"],
            self.data["worldY"],
            self.data["worldDepth"],
        ]
        self.bgColour: str = self.data.get("bgColor", "") or self.data.get(
            "__bgColor", ""
        )

        self.bgPic: Optional[pyglet.image.AbstractImage] = None
        if self.data.get("bgRelPath"):
            path = os.path.abspath(
                os.path.join(file_loc, "../", self.data["bgRelPath"])
            )
            if os.path.exists(path):
                self.bgPic = pyglet.image.load(path)

        self.sizePx: List[int] = [self.data["pxWid"], self.data["pxHei"]]

        self.layers: List["Layer"] = []
        self.entities: List["Entity"] = []  # Cache of all entities for lookup

        # Process Layers
        # LDtk order is Top-to-Bottom. Pyglet is Painter's Algo (Back-to-Front).
        raw_layers = self.data.get("layerInstances", [])
        for lay_data in raw_layers:
            layer = Layer(lay_data, self)
            self.layers.append(layer)
            # Cache entities if this layer has them
            if layer.entities:
                self.entities.extend(layer.entities)

        self.layers.reverse()  # Reverse for rendering order

        # For Getters
        self.getCache: List[Dict] = [{}, {}, {}]

    def addToBatch(self, batch: pyglet.graphics.Batch, group_offset: int = 0):
        """
        Add all level layers to a Pyglet Batch.

        Args:
            batch (pyglet.graphics.Batch): The pyglet.graphics.Batch to add sprites to.
            group_offset (int): An integer offset for Groups to ensure layers stack correctly.
        """
        if self.bgColour:
            c = self.bgColour.lstrip("#")
            rgb = (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16))
            from pyglet import shapes

            bg_rect = shapes.Rectangle(
                0,
                0,
                self.sizePx[0],
                self.sizePx[1],
                color=rgb,
                batch=batch,
                group=pyglet.graphics.Group(order=group_offset),
            )
            self._bg_rect_ref = bg_rect

        if self.bgPic:
            scale_x = self.sizePx[0] / self.bgPic.width
            scale_y = self.sizePx[1] / self.bgPic.height
            scale = max(scale_x, scale_y)
            bg_sprite = pyglet.sprite.Sprite(
                self.bgPic,
                x=0,
                y=0,
                batch=batch,
                group=pyglet.graphics.Group(order=group_offset + 1),
            )
            bg_sprite.scale = scale
            self._bg_sprite_ref = bg_sprite

        for i, layer in enumerate(self.layers):
            layer.addToBatch(batch, pyglet.graphics.Group(order=group_offset + 2 + i))

    def GetLayerById(self, layer_id: str) -> "Layer":
        """Find a layer by its identifier."""
        for layer_obj in self.layers:
            if layer_obj.identifier == layer_id:
                return layer_obj
        raise ValueError(f"Layer with identifier {layer_id} not found.")

    def GetAllEntities(
        self, processor: Callable[["Entity"], Any] = lambda e: e
    ) -> List[Any]:
        """Get all entities in the level."""
        o: List[Any] = []
        for e in self.entities:
            resp = processor(e)
            if resp is not None:
                o.append(resp)
        return o

    def GetEntitiesByLayer(
        self,
        layer_id: str,
        processor: Callable[["Entity"], Any] = lambda e: e,
        forceRefreshCache: bool = False,
    ) -> List[Any]:
        """Gets all the entities by their layer identifier."""
        if layer_id not in self.getCache[0] or forceRefreshCache:
            self.getCache[0][layer_id] = []
            for e in self.entities:
                if e.layer.identifier == layer_id:
                    resp = processor(e)
                    if resp is not None:
                        self.getCache[0][layer_id].append(resp)
        return self.getCache[0][layer_id]

    def GetEntitiesByID(
        self,
        identifier: str,
        processor: Callable[["Entity"], Any] = lambda e: e,
        forceRefreshCache: bool = False,
    ) -> List[Any]:
        """Gets all the entities by their identifier."""
        if identifier not in self.getCache[1] or forceRefreshCache:
            self.getCache[1][identifier] = []
            for e in self.entities:
                if e.identifier == identifier:
                    resp = processor(e)
                    if resp is not None:
                        self.getCache[1][identifier].append(resp)
        return self.getCache[1][identifier]

    def GetEntitiesByUID(
        self,
        uid: int,
        processor: Callable[["Entity"], Any] = lambda e: e,
        forceRefreshCache: bool = False,
    ) -> List[Any]:
        """Gets all the entities by their UID."""
        if uid not in self.getCache[2] or forceRefreshCache:
            self.getCache[2][uid] = []
            for e in self.entities:
                if e.defUid == uid:
                    resp = processor(e)
                    if resp is not None:
                        self.getCache[2][uid].append(resp)
        return self.getCache[2][uid]


class Layer:
    """
    Represents a single Layer in an LDtk Level.
    Handles generating Pyglet sprites for Tiles, IntGrid (Rects), and Entities.
    """

    def __init__(self, data: Dict, level: "LdtkLevel"):
        """
        Initialize a Layer.

        Args:
            data (Dict): Layer Instance JSON data.
            level (LdtkLevel): Parent Level.
        """
        self.data: Dict = data
        self.level: "LdtkLevel" = level
        self.type = LayerType(self.data["__type"])

        self.identifier: str = self.data["__identifier"]
        self.gridSize: int = self.data["__gridSize"]
        self.sizeCells: List[int] = [self.data["__cWid"], self.data["__cHei"]]
        self.pxOffset: List[int] = [
            self.data["__pxTotalOffsetX"],
            self.data["__pxTotalOffsetY"],
        ]
        self.opacity: float = self.data["__opacity"]
        self.visible: bool = self.data["visible"]

        self.tileset: Optional[TilesetDef] = None
        if self.data.get("__tilesetDefUid"):
            self.tileset = self.level.tilesets.get(self.data["__tilesetDefUid"])

        # Content Holders
        self.tiles: List[Tile] = []
        self.intgrid: Optional[IntGridCSV] = None
        self.entities: List[Entity] = []

        # Load Content based on Type
        if self.type == LayerType.Entities:
            for inst in self.data.get("entityInstances", []):
                self.entities.append(Entity(self, inst, self.level.tilesets))

        elif self.type == LayerType.IntGrid:
            self.intgrid = IntGridCSV(
                self.data.get("intGridCsv", []),
                self.sizeCells[0],
                self.sizeCells[1],
                self.pxOffset,
                self.gridSize,
            )
            # IntGrid can ALSO have tiles (AutoLayer)
            if self.data.get("autoLayerTiles"):
                self.tiles = [Tile(t, self) for t in self.data["autoLayerTiles"]]

        elif self.type in (LayerType.Tiles, LayerType.AutoLayer):
            src = self.data.get("gridTiles") or self.data.get("autoLayerTiles") or []
            self.tiles = [Tile(t, self) for t in src]

        # Refs for GC
        self.sprites = []
        self.shapes = []

    def addToBatch(
        self,
        batch: pyglet.graphics.Batch,
        group: Optional[pyglet.graphics.Group] = None,
    ):
        """
        Populate the batch with sprites/shapes for this layer.
        Handles the Y-axis inversion from LDtk (Top-Left) to Pyglet (Bottom-Left).
        """
        if not self.visible:
            return

        self.sprites = []
        self.shapes = []

        # 1. Render IntGrid Colors
        if self.type == LayerType.IntGrid and self.intgrid:
            defs = self.level.defs["layers"]
            layerDef = next(
                (i for i in defs if i["uid"] == self.data["layerDefUid"]), {}
            )
            intGridValues = layerDef.get("intGridValues", [])
            vals = [i["value"] for i in intGridValues]

            from pyglet import shapes

            # Optimize: Only draw colored cells
            for y in range(len(self.intgrid.intgrid)):
                row = self.intgrid.intgrid[y]
                for x in range(len(row)):
                    val = row[x]
                    if val != 0 and val in vals:
                        color_hex = intGridValues[vals.index(val)]["color"].lstrip("#")
                        rgb = (
                            int(color_hex[0:2], 16),
                            int(color_hex[2:4], 16),
                            int(color_hex[4:6], 16),
                        )
                        # Invert Y for Pyglet (Bottom-Left origin)
                        # LDtk Y is top-down. Pyglet Y is bottom-up.
                        final_y = (
                            self.level.sizePx[1]
                            - (y * self.gridSize + self.pxOffset[1])
                            - self.gridSize
                        )

                        rect = shapes.Rectangle(
                            x * self.gridSize + self.pxOffset[0],
                            final_y,
                            self.gridSize,
                            self.gridSize,
                            color=rgb,
                            batch=batch,
                            group=group,
                        )
                        rect.opacity = int(255 * self.opacity)
                        self.shapes.append(rect)

        # 2. Render Tiles
        if self.tiles and self.tileset:
            # Find pivot
            defs = self.level.defs["layers"]
            layerDef = next(
                (i for i in defs if i["uid"] == self.data["layerDefUid"]), {}
            )
            layerDef = cast(Dict[str, Any], layerDef)
            pivotX = layerDef.get("tilePivotX", 0)
            pivotY = layerDef.get("tilePivotY", 0)

            for t in self.tiles:
                tex = t.getImg()
                if tex:
                    # Logic to align tile based on pivot (LDtk Top-Left space)
                    size = (tex.width, tex.height)
                    ldtk_y = t.pos[1] - pivotY * size[1] + self.gridSize * pivotY

                    # Convert to Pyglet Bottom-Left space
                    # Pyglet Y = Level Height - (LDtk Top Y + Height)
                    final_x = t.pos[0] - pivotX * size[0] + self.gridSize * pivotX
                    final_y = self.level.sizePx[1] - (ldtk_y + size[1])

                    spr = pyglet.sprite.Sprite(
                        tex, x=final_x, y=final_y, batch=batch, group=group
                    )
                    spr.opacity = int(255 * self.opacity * t.a)
                    self.sprites.append(spr)

        # 3. Render Entities
        if self.entities:
            for ent in self.entities:
                ent_sprites = ent.get_sprites(batch, group)
                for spr in ent_sprites:
                    spr.opacity = int(255 * self.opacity)
                    self.sprites.append(spr)


class Entity:
    """
    Represents an Entity instance in a Level.
    """

    def __init__(self, layer: "Layer", data: Dict, tilesets: Dict[int, TilesetDef]):
        """
        Initialize an Entity.

        Coordinates are automatically converted to Pyglet space (Bottom-Left).

        Args:
            layer (Layer): Parent layer.
            data (Dict): Entity Instance JSON data.
            tilesets (Dict): Map of tileset definitions.
        """
        self.layer = layer
        self.data = data
        self.tilesets = tilesets

        self.identifier = self.data["__identifier"]
        self.defUid = self.data["defUid"]

        # Link to Definition
        self.definition = self.layer.level.entity_defs.get(self.defUid)

        self.width = self.data["width"]
        self.height = self.data["height"]

        self.gridSize = self.layer.gridSize
        self.pivot = self.data.get(
            "__pivot", [0.5, 1.0]
        )  # Default pivot usually bottom-center in LDtk if not set

        # Calculate Position
        px = self.data["px"]
        # LDtk Top-Left coordinate of the entity's bounding box
        ldtk_top = px[1] + self.layer.pxOffset[1] - self.pivot[1] * self.height

        self.x = px[0] + self.layer.pxOffset[0] - self.pivot[0] * self.width
        # Convert to Pyglet Bottom-Left coordinate
        self.y = self.layer.level.sizePx[1] - (ldtk_top + self.height)

        # For rendering
        self.tileData = self.data.get("__tile") or (
            self.definition.tileRect if self.definition else None
        )

        # Parse Fields
        self.props = {}
        for field in self.data.get("fieldInstances", []):
            identifier = field["__identifier"]
            self.props[identifier] = FieldParser.parse(self.layer, field)

    def get_sprites(
        self, batch: pyglet.graphics.Batch, group: Optional[pyglet.graphics.Group]
    ) -> List[pyglet.sprite.Sprite]:
        """
        Returns a list of sprites to represent this entity.
        Handles complex render modes like NineSlice.

        Args:
            batch (pyglet.graphics.Batch): The batch to add sprites to.
            group (pyglet.graphics.Group): The group for ordering.
        """
        sprites = []
        if not self.tileData or not self.definition:
            return sprites

        tilesetId = self.tileData.get("tilesetUid")
        if not tilesetId or tilesetId not in self.tilesets:
            return sprites

        tset = self.tilesets[tilesetId]

        # Base Texture
        tx, ty, tw, th = (
            self.tileData["x"],
            self.tileData["y"],
            self.tileData["w"],
            self.tileData["h"],
        )

        # Render Mode Logic
        mode = self.definition.tileRenderMode

        if mode == TileRenderMode.NineSlice and self.definition.nineSliceBorders:
            # Nine Slice Logic
            T, R, B, L = self.definition.nineSliceBorders  # Top, Right, Bottom, Left

            # If entity is too small, fallback to standard stretch
            if self.width < L + R or self.height < T + B:
                mode = TileRenderMode.Stretch
            else:
                # Slicing
                # 0 1 2
                # 3 4 5
                # 6 7 8

                # Center sizes
                cw = tw - L - R  # Texture Center Width
                ch = th - T - B  # Texture Center Height

                target_cw = self.width - L - R
                target_ch = self.height - T - B

                # Helper to create slice sprite
                def make_slice(sx, sy, sw, sh, dx, dy, dw, dh):
                    if sw <= 0 or sh <= 0 or dw <= 0 or dh <= 0:
                        return
                    img = tset.subsurface(sx, sy, sw, sh)
                    if not img:
                        return

                    # Calculate Y for slice (Inverted from Top-Left relative)
                    # dy is offset from Top.
                    # Pyglet Y = EntityBottom + EntityHeight - dy - dh
                    slice_y = self.y + self.height - dy - dh

                    spr = pyglet.sprite.Sprite(
                        img, x=self.x + dx, y=slice_y, batch=batch, group=group
                    )
                    spr.scale_x = dw / sw
                    spr.scale_y = dh / sh
                    sprites.append(spr)

                # Row 1 (Top)
                make_slice(tx, ty, L, T, 0, 0, L, T)  # TL
                make_slice(tx + L, ty, cw, T, L, 0, target_cw, T)  # T
                make_slice(tx + tw - R, ty, R, T, self.width - R, 0, R, T)  # TR

                # Row 2 (Middle)
                make_slice(tx, ty + T, L, ch, 0, T, L, target_ch)  # L
                make_slice(tx + L, ty + T, cw, ch, L, T, target_cw, target_ch)  # C
                make_slice(
                    tx + tw - R, ty + T, R, ch, self.width - R, T, R, target_ch
                )  # R

                # Row 3 (Bottom)
                make_slice(tx, ty + th - B, L, B, 0, self.height - B, L, B)  # BL
                make_slice(
                    tx + L, ty + th - B, cw, B, L, self.height - B, target_cw, B
                )  # B
                make_slice(
                    tx + tw - R,
                    ty + th - B,
                    R,
                    B,
                    self.width - R,
                    self.height - B,
                    R,
                    B,
                )  # BR

                return sprites

        # Default / Stretch / FitInside
        texture = tset.subsurface(tx, ty, tw, th)
        if not texture:
            return sprites

        spr = pyglet.sprite.Sprite(
            texture, x=self.x, y=self.y, batch=batch, group=group
        )

        if mode == TileRenderMode.FitInside:
            scale = min(self.width / tw, self.height / th)
            spr.scale = scale
            # Center it
            spr.x += (self.width - tw * scale) / 2
            spr.y += (self.height - th * scale) / 2
        else:
            # Stretch or Cover (defaulting to stretch for simplicity)
            spr.scale_x = self.width / tw
            spr.scale_y = self.height / th

        sprites.append(spr)
        return sprites


class IntGridCSV:
    """Helper to parse IntGrid CSV data."""

    def __init__(
        self,
        intgrid: List[int],
        cwid: int,
        chei: int,
        offsets: List[int],
        grid_size: int,
    ):
        """
        Initialize IntGrid parser.

        Args:
            intgrid (List[int]): Flat list of integers from CSV.
            cwid (int): Width in cells.
            chei (int): Height in cells.
            offsets (List[int]): Pixel offsets [x, y].
            grid_size (int): Size of the grid.
        """
        self.intgrid = []
        if cwid > 0:
            count = math.ceil(len(intgrid) / cwid)
            self.intgrid = [intgrid[cwid * i : cwid * (i + 1)] for i in range(count)]


class Tile:
    """Represents a single Tile instance on a layer."""

    def __init__(self, data: Dict, lay: "Layer"):
        """
        Initialize a Tile.

        Args:
            data (Dict): Tile data.
            lay (Layer): Parent layer.
        """
        self.data = data
        self.layer = lay
        self.px = self.data["px"]
        self.src = self.data["src"]
        self.t = self.data["t"]
        self.a = self.data.get("a", 1.0)
        self.pos = (
            self.px[0] + self.layer.pxOffset[0],
            self.px[1] + self.layer.pxOffset[1],
        )

        f = self.data["f"]
        self.flip_value = FlipBits(f)
        self.flip_x = bool(f & FlipBits.FlipX.value)
        self.flip_y = bool(f & FlipBits.FlipY.value)

    def getImg(self):
        """Get the texture for this tile."""
        if self.layer.tileset:
            return self.layer.tileset.getTile(self)
        return None
