# regionx

A high-performance Python library for astronomical region operations, powered by Rust. `regionx` provides fast spherical geometry calculations for identifying sources within regions on the celestial sphere.

## Features

- **Fast spherical geometry operations** - Rust-powered performance for large astronomical catalogs
- **Simple Python interface** - Easy-to-use classes for common astronomical regions
- **Batch operations** - Efficiently check multiple points at once
- **Three region types**:
  - `Polygon` - Arbitrary spherical polygons defined by vertices
  - `Aperture` - Circular regions on the sky
  - `Anulus` - Annular (ring-shaped) regions

## Installation

```bash
pip install regionx
```

Or build from source:

```bash
git clone https://github.com/yourusername/regionx.git
cd regionx
pip install maturin
maturin develop --release
```

## Usage

### Polygon

Create spherical polygons and check if sky coordinates fall within them.

```python
from regionx import Polygon

# Define a polygon with RA/Dec vertices (in degrees)
ra_vertices = [10.0, 15.0, 15.0, 10.0]
dec_vertices = [20.0, 20.0, 25.0, 25.0]

polygon = Polygon(ra_vertices, dec_vertices)

# Check a single point
is_inside = polygon.is_inside(ra_point=12.5, dec_point=22.5)
print(f"Point is inside: {is_inside}")

# Check multiple points at once (much faster for large catalogs)
ra_points = [12.0, 16.0, 11.0, 14.0]
dec_points = [22.0, 22.0, 24.0, 21.0]
results = polygon.check_points(ra_points, dec_points)
print(f"Results: {results}")  # [True, False, True, True]
```

### Aperture

Create circular apertures for source identification.

```python
from regionx import Aperture

# Create a circular aperture centered at RA=180°, Dec=45° with 2° radius
aperture = Aperture(ra_center=180.0, dec_center=45.0, radius_deg=2.0)

# Check single point
is_inside = aperture.is_inside(ra_point=181.0, dec_point=45.5)

# Check multiple points
ra_catalog = [180.5, 179.5, 185.0, 180.0]
dec_catalog = [45.2, 44.8, 45.0, 46.5]
mask = aperture.check_points(ra_catalog, dec_catalog)
```

### Anulus

Create annular (ring-shaped) regions for background estimation or source selection.

```python
from regionx import Anulus

# Create an annulus with inner radius 1° and outer radius 3°
anulus = Anulus(
    ra_center=150.0, 
    dec_center=-30.0, 
    inner_radius=1.0, 
    outer_radius=3.0
)

# Check single point
is_inside = anulus.is_inside(ra_point=151.5, dec_point=-30.5)

# Check multiple points
ra_points = [150.5, 150.1, 152.5, 154.0]
dec_points = [-30.2, -30.0, -29.5, -30.0]
mask = anulus.check_points(ra_points, dec_points)
```

## Working with Astronomical Catalogs

Here's a complete example using numpy arrays and astronomical data:

```python
import numpy as np
from regionx import Aperture

# Load your catalog (example with random data)
catalog_ra = np.random.uniform(0, 360, 100000)
catalog_dec = np.random.uniform(-90, 90, 100000)

# Define a search region
search_region = Aperture(ra_center=180.0, dec_center=0.0, radius_deg=5.0)

# Find all sources in the region
inside_mask = search_region.check_points(
    catalog_ra.tolist(), 
    catalog_dec.tolist()
)

# Filter your catalog
sources_in_region = np.array(inside_mask)
filtered_ra = catalog_ra[sources_in_region]
filtered_dec = catalog_dec[sources_in_region]

print(f"Found {np.sum(sources_in_region)} sources in the region")
```

## API Reference

### Polygon

**Constructor:**
- `Polygon(ra_vertices: List[float], dec_vertices: List[float])`
  - `ra_vertices`: Right ascension coordinates of polygon vertices (degrees)
  - `dec_vertices`: Declination coordinates of polygon vertices (degrees)

**Methods:**
- `is_inside(ra_point: float, dec_point: float) -> bool`
- `check_points(ra_points: List[float], dec_points: List[float]) -> List[bool]`

### Aperture

**Constructor:**
- `Aperture(ra_center: float, dec_center: float, radius_deg: float)`
  - `ra_center`: Right ascension of aperture center (degrees)
  - `dec_center`: Declination of aperture center (degrees)
  - `radius_deg`: Aperture radius (degrees)

**Methods:**
- `is_inside(ra_point: float, dec_point: float) -> bool`
- `check_points(ra_points: List[float], dec_points: List[float]) -> List[bool]`

### Anulus

**Constructor:**
- `Anulus(ra_center: float, dec_center: float, inner_radius: float, outer_radius: float)`
  - `ra_center`: Right ascension of center (degrees)
  - `dec_center`: Declination of center (degrees)
  - `inner_radius`: Inner radius (degrees)
  - `outer_radius`: Outer radius (degrees)

**Methods:**
- `is_inside(ra_point: float, dec_point: float) -> bool`
- `check_points(ra_points: List[float], dec_points: List[float]) -> List[bool]`

## Coordinate System

All coordinates are in degrees:
- **RA (Right Ascension)**: 0° to 360°
- **Dec (Declination)**: -90° to +90°

The library correctly handles spherical geometry, including regions that cross the RA=0°/360° boundary and poles.

## Performance Tips

1. **Use batch operations**: `check_points()` is much faster than calling `is_inside()` repeatedly
2. **Convert numpy arrays to lists**: `ra_array.tolist()` before passing to `check_points()`
3. **Reuse region objects**: Create the region once and reuse it for multiple queries

## License

MIT
## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

Built on top of the `astroxide` Rust library for spherical geometry calculations.