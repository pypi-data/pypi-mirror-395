# shapeedit

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/pgroenbaek/shapeedit?style=flat&label=Latest%20Version)](https://github.com/pgroenbaek/shapeedit/releases)
[![Python 3.7+](https://img.shields.io/badge/Python-3.7%2B-blue?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License GNU GPL v3](https://img.shields.io/badge/License-%20%20GNU%20GPL%20v3%20-lightgrey?style=flat&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NDAgNTEyIj4KICA8IS0tIEZvbnQgQXdlc29tZSBGcmVlIDYuNy4yIGJ5IEBmb250YXdlc29tZSAtIGh0dHBzOi8vZm9udGF3ZXNvbWUuY29tIExpY2Vuc2UgLSBodHRwczovL2ZvbnRhd2Vzb21lLmNvbS9saWNlbnNlL2ZyZWUgQ29weXJpZ2h0IDIwMjUgRm9udGljb25zLCBJbmMuIC0tPgogIDxwYXRoIGZpbGw9IndoaXRlIiBkPSJNMzg0IDMybDEyOCAwYzE3LjcgMCAzMiAxNC4zIDMyIDMycy0xNC4zIDMyLTMyIDMyTDM5OC40IDk2Yy01LjIgMjUuOC0yMi45IDQ3LjEtNDYuNCA1Ny4zTDM1MiA0NDhsMTYwIDBjMTcuNyAwIDMyIDE0LjMgMzIgMzJzLTE0LjMgMzItMzIgMzJsLTE5MiAwLTE5MiAwYy0xNy43IDAtMzItMTQuMy0zMi0zMnMxNC4zLTMyIDMyLTMybDE2MCAwIDAtMjk0LjdjLTIzLjUtMTAuMy00MS4yLTMxLjYtNDYuNC01Ny4zTDEyOCA5NmMtMTcuNyAwLTMyLTE0LjMtMzItMzJzMTQuMy0zMiAzMi0zMmwxMjggMGMxNC42LTE5LjQgMzcuOC0zMiA2NC0zMnM0OS40IDEyLjYgNjQgMzJ6bTU1LjYgMjg4bDE0NC45IDBMNTEyIDE5NS44IDQzOS42IDMyMHpNNTEyIDQxNmMtNjIuOSAwLTExNS4yLTM0LTEyNi03OC45Yy0yLjYtMTEgMS0yMi4zIDYuNy0zMi4xbDk1LjItMTYzLjJjNS04LjYgMTQuMi0xMy44IDI0LjEtMTMuOHMxOS4xIDUuMyAyNC4xIDEzLjhsOTUuMiAxNjMuMmM1LjcgOS44IDkuMyAyMS4xIDYuNyAzMi4xQzYyNy4yIDM4MiA1NzQuOSA0MTYgNTEyIDQxNnpNMTI2LjggMTk1LjhMNTQuNCAzMjBsMTQ0LjkgMEwxMjYuOCAxOTUuOHpNLjkgMzM3LjFjLTIuNi0xMSAxLTIyLjMgNi43LTMyLjFsOTUuMi0xNjMuMmM1LTguNiAxNC4yLTEzLjggMjQuMS0xMy44czE5LjEgNS4zIDI0LjEgMTMuOGw5NS4yIDE2My4yYzUuNyA5LjggOS4zIDIxLjEgNi43IDMyLjFDMjQyIDM4MiAxODkuNyA0MTYgMTI2LjggNDE2UzExLjcgMzgyIC45IDMzNy4xeiIvPgo8L3N2Zz4=&logoColor=%23ffffff)](https://github.com/pgroenbaek/shapeedit/blob/master/LICENSE)

This Python module provides a wrapper around the shape data structure from [shapeio](https://github.com/pgroenbaek/shapeio), offering operations for modifying existing MSTS and ORTS shape files.

Depending on how the module is used, you may end up with unusual-looking shapes; however, the implemented operations ensure that shapes remain error-free and usable in MSTS and Open Rails.

At this stage, only a limited set of operations is implemented. If you need additional functionality or have any other suggestions, you are welcome to request them by creating an issue.

List of companion modules:
- [shapeio](https://github.com/pgroenbaek/shapeio) - offers functions to convert shapes between structured text format and Python objects.
- [trackshape-utils](https://github.com/pgroenbaek/trackshape-utils) - offers additional utilities for working with track shapes.
- [pyffeditc](https://github.com/pgroenbaek/pyffeditc) - handles compression and decompression of shape files through the `ffeditc_unicode.exe` utility found in MSTS installations.
- [pytkutils](https://github.com/pgroenbaek/pytkutils) - handles compression and decompression of shape files through the `TK.MSTS.Tokens.dll` library by Okrasa Ghia.

## Installation

### Install from PyPI

```sh
pip install --upgrade shapeedit
```

### Install from wheel

If you have downloaded a `.whl` file from the [Releases](https://github.com/pgroenbaek/shapeedit/releases) page, install it with:

```sh
pip install path/to/shapeedit-<version>‑py3‑none‑any.whl
```

Replace `<version>` with the actual version number in the filename.

### Install from source

```sh
git clone https://github.com/pgroenbaek/shapeedit.git
pip install --upgrade ./shapeedit
```

## Capabilities

The exact capabilities of this Python module might not be immediately obvious, so here's an overview with some examples and screenshots.

You can perform pretty cool edits on existing shapes using this set of tools.

### Modification of existing geometry

Existing geometry within shapes can be modified. Vertex positions, texture coordinates, and normal vectors are all adjustable.

The original shapes and textures below are by Norbert Rieger. In the [first example](https://github.com/pgroenbaek/dbtracks-extras/blob/master/scripts/DBxfb/convert_db1s_to_db1fb.py), the LZB cable is moved below the trackbed, and texture images are swapped to convert DB1s track sections into DB1fb.

In the [second example](https://github.com/pgroenbaek/dbtracks-extras/blob/master/scripts/V4hs1t_RKL/convert_db1z1t_to_v4hs1trkl.py), trackbed vertices are repositioned to mimic the concrete slabs of the V4hs_RKL track sections. Here, texture images are also swapped.

![DB1s vs. DB1fb](https://github.com/pgroenbaek/shapeedit/blob/master/images/DB1s_DB1fb.png)

![DB1s vs. V4hs1t_RKL](https://github.com/pgroenbaek/shapeedit/blob/master/images/V4hs1t_RKL.png)

### Addition of new geometry

Brand-new geometry, i.e., new vertices and triangles, can also be inserted into existing shapes.

In [this example](https://github.com/pgroenbaek/nremb-atracks/blob/master/scripts/NR_Emb_AT/change_nrembrails_to_atracksrails.py), the original NR_Emb shapes are by Norbert Rieger. The square railheads that match the old XTracks track system are extended with new geometry and folded up to match Eric's newer ATracks shapes.

This particular example is somewhat more advanced compared to the others, as the script quite literally weaves new geometry into both curved and straight track sections from stratch.

![NR_Emb vs. NR_Emb_AT](https://github.com/pgroenbaek/shapeedit/blob/master/images/NR_Emb_AT.png)

The edited NR_Emb shapes with ATracks rails are available for download at [trainsim.com](https://www.trainsim.com/forums/filelib/search-fileid?fid=90029).

### Removal of geometry

Triangles connecting existing vertices can also be removed, effetively making geometry no longer visible even though the vertices technically remain.

In [this example](https://github.com/pgroenbaek/nohab-my/blob/master/scripts/remove_mirrors.py), the side mirrors of the Nohab MY locomotive model by Pál Tamás are removed.

![Nohab MY mirror removal](https://github.com/pgroenbaek/shapeedit/blob/master/images/NohabMyMirrors.png)

### Transferring geometry

Geometry can also be transferred from one shape to another.

In [this example](https://github.com/pgroenbaek/dblslip7_5d-ohw/blob/master/scripts/DblSlip7_5d/make_ohw_dblslip7_5d.py), the overhead wires are copied from one of Norbert Rieger's DblSlip7_5d shapes onto the animated DblSlip7_5d switches by Laci1959.

![DB2_DblSlip7_5d vs. DB2f_DblSlip7_5d](https://github.com/pgroenbaek/shapeedit/blob/master/images/DblSlip7_5d.png)

The edited DblSlip7\_5d shapes are available for download at [the-train.de](https://the-train.de/downloads/entry/11283-dbtracks-doppelte-kreuzungsweiche-dkw-7-5/).

### Addition of new textures, primitives or sub-objects

At present, operations that add new textures, primitives, or sub-objects are not implemented in this module. The goal is to eventually support those capabilites.

You can attempt such modifications manually through [shapeio](https://github.com/pgroenbaek/shapeio), as the entire shape data structure can be accessed and modified using that module.

Just keep in mind that you are not going to have the abstraction layer provided in this module. The one that makes things easy and keeps the shape error-free.

## Usage

Before using this Python module, it is important to understand the basic structure of how geometry is stored within a shape.

The overall structure consists of six elements. These are all accessible through the API of the module:
- **LOD Control:** The top-level element, which contains one or more distance levels. Usually, there is only one of these per shape.
- **Distance Level:** Defines a distance level in meters. All sub-objects contained within it are visible when the shape is viewed within that range in the simulator. Typically, shapes have one or more of these, with the father distance levels containing less detailed geometry than those closer to the shape.
- **Sub Object:** Defines a sub-part of the overall shape at a given distance level. Typically, there are one or more of these within each distance level. Each sub-object contains a list of vertices and primitives.
- **Vertex:** Defines a point within the shape geometry. Each vertex also references a texture coordinate (UV) and a normal vector used for lighting calculations.
- **Primitive:** A collection of triangles. Typically, one or more are defined, and each primitive is associated with a primstate and a matrix. Primstates define which lighting configurations and which texture gets applied to the primitive's faces. Matrices define how the internal coordinate system within the shape is transformed into world-space coordinates when the shape is rendered.
- **Triangle:** A set of three vertices that forms a triangle within the shape geometry. Each triangle also references a normal vector that determine its facing direction.

The basic structure of these elements is as follows:
```
LOD Controls
└── Distance Levels
    └── Sub Objects
        ├── Vertices
        └── Primitives
            └── Triangles
```

In the module's API, vertices that are associated with a specific primitive or triangle can be accessed through those elements for convenience.

You will need to inspect the shape manually in a text editor to determine the exact distance level values, sub-object indexes, and primstate names/indexes to use.

### Modification of existing geometry

```python
import shapeio
from shapeedit import ShapeEditor

my_shape = shapeio.load("./path/to/example.s")

shape_editor = ShapeEditor(my_shape)

sub_object = shape_editor.lod_control(0).distance_level(200).sub_object(0)

# Set point/uv_point/normal data of all vertices within the subobject to zero.
for vertex in sub_object.vertices():
    vertex.point.x = 0.0
    vertex.point.y = 0.0
    vertex.point.z = 0.0
    vertex.uv_point.u = 0.0
    vertex.uv_point.v = 0.0
    vertex.normal.x = 0.0
    vertex.normal.y = 0.0
    vertex.normal.z = 0.0

shapeio.dump(my_shape, "./path/to/output.s")
```

### Addition of new vertices and triangles

```python
import shapeio
from shapeio.shape import Point, UVPoint, Vector
from shapeedit import ShapeEditor

my_shape = shapeio.load("./path/to/example.s")

shape_editor = ShapeEditor(my_shape)

# Add three new vertices to primitives associated with prim_state_idx 22.
# Connect the three vertices added to each primitive with a triangle.
for lod_control in shape_editor.lod_controls():
    for distance_level in lod_control.distance_levels():
        for sub_object in distance_level.sub_objects():
            for primitive in sub_object.primitives(prim_state_index=22):
                new_point1 = Point(0.0, 0.0, 0.0)
                new_point2 = Point(1.0, 0.0, 0.0)
                new_point3 = Point(2.0, 0.0, 1.0)
                new_uv_point = UVPoint(0.0, 0.0)
                new_normal = Vector(0.0, 0.0, 0.0)

                new_vertex1 = primitive.add_vertex(new_point1, new_uv_point, new_normal)
                new_vertex2 = primitive.add_vertex(new_point2, new_uv_point, new_normal)
                new_vertex3 = primitive.add_vertex(new_point3, new_uv_point, new_normal)

                primitive.insert_triangle(new_vertex1, new_vertex2, new_vertex3)

shapeio.dump(my_shape, "./path/to/output.s")
```

### Removal of triangles

```python
import shapeio
from shapeedit import ShapeEditor

my_shape = shapeio.load("./path/to/example.s")

shape_editor = ShapeEditor(my_shape)

# Remove all triangles from primitives associated with any prim_state named "Rails".
for lod_control in shape_editor.lod_controls():
    for distance_level in lod_control.distance_levels():
        for sub_object in distance_level.sub_objects():
            for primitive in sub_object.primitives(prim_state_name="Rails"):
                for vertex in primitive.vertices():
                    primitive.remove_triangles_connected_to(vertex)

shapeio.dump(my_shape, "./path/to/output.s")
```

## Running Tests

You can run tests manually or use `tox` to test across multiple Python versions.

### Run Tests Manually
First, install the required dependencies:

```sh
pip install pytest
```

Then, run tests with:

```sh
pytest
```


### Run Tests with `tox`

First, install the required dependencies:

```sh
pip install tox
```

Then, run tests with:

```sh
tox
```

This will execute tests for all Python versions specified in `tox.ini`.


## Roadmap

Possible future features to be added:
- Ability to add new textures and primitives
- Ability to remove vertices from primitives
- Ability to edit things like light configurations, animations, etc.
- And possibly more..

Please make an issue if you have any good ideas, or if you need something that has not yet been implemented.

Pull requests are also welcome.

## Contributing

Contributions of all kinds are welcome. These could be suggestions, issues, bug fixes, documentation improvements, or new features.

For more details see the [contribution guidelines](https://github.com/pgroenbaek/shapeedit/blob/master/CONTRIBUTING.md).

## License

This Python module was created by Peter Grønbæk Andersen and is licensed under [GNU GPL v3](https://github.com/pgroenbaek/shapeedit/blob/master/LICENSE).
