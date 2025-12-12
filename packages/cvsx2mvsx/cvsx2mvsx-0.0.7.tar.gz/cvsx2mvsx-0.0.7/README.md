# cvsx2mvsx

**cvsx2mvsx** is a Python library and CLI tool designed to convert **CVSX** archives into **MVSX** or **MVS Stories** formats.

## Installation


```bash
pip install cvsx2mvsx
```

## CLI Usage

Convert a CVSX file to an MVSX archive:

```bash
cvsx2mvsx --input data/example.cvsx --output output.mvsx
```

Convert a CVSX file to the Stories format:

```bash
cvsx2mvsx --input data/example.cvsx --output output.stories --format stories
```

### Lattice to Mesh Conversion

If your input CVSX contains Lattice segmentations (voxel masks) and you wish to convert them to meshes rather than volumes:

```bash
cvsx2mvsx --input data/example.cvsx --output output.mvsx --lattice-to-mesh
```

### Arguments

| Argument | Description | Default |
| :--- | :--- | :--- |
| `--input` | Path to the input `.cvsx` file. | Required |
| `--output` | Path to the output file (`.mvsx` or `.stories`). | Required |
| `--format` | Output format type (`mvsx` or `stories`). | `mvsx` |
| `--lattice-to-mesh` | Enable Marching Cubes conversion for lattice data. | `False` |

## Python API Usage

You can use the library programmatically to integrate the conversion pipeline into your own Python scripts.

### MVSX Pipeline

```python
from cvsx2mvsx.etl.pipelines.mvsx import MVSXPipeline

pipeline = MVSXPipeline(
    cvsx_path="path/to/input.cvsx",
    output_path="path/to/output.mvsx",
    lattice_to_mesh=True  # Optional: Convert voxel masks to meshes
)

pipeline.run()
```

### Stories Pipeline

```python
from cvsx2mvsx.etl.pipelines.stories import StoriesPipeline

pipeline = StoriesPipeline(
    cvsx_path="path/to/input.cvsx",
    output_path="path/to/output.stories"
)

pipeline.run()
```

## Architecture

The library follows a strict **ETL (Extract, Transform, Load) Pipeline** pattern:

1.  **Extract**:
      * Unzips the `.cvsx` archive.
      * Parses `index.json`, metadata, and binary CIF files using `ciftools`.
      * Loads Geometric primitives from JSON.
2.  **Transform**:
      * Converts CVSX internal models to an intermediate internal representation.
      * Performs heavy lifting like `LatticeTransformer` (Marching Cubes)
      * Generates MolViewSpec state descriptions (`index.mvsj`).
3.  **Load**:
      * Encodes binary data (BCIF) for volumes and meshes.
      * Packages the state and assets into the final `.mvsx` Zip archive or `.stories` binary blob.

