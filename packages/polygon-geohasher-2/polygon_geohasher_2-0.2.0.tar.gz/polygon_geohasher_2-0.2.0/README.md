# polygon-geohasher-2

> [!NOTE]
> This is a minimally maintained fork of the original
> [Bonsanto/polygon-geohasher](https://github.com/Bonsanto/polygon-geohasher) repo, which does not appear to be
> actively maintained.
>
> The original project is published to PyPi under the package name `polygon-geohasher`; *this* project is published
> under the package name `polygon-geohasher-2`. My goal is to provide a stable package that works with all actively
> maintained Python versions (those with a status of `bugfix` or `security`
> [here](https://devguide.python.org/versions/)). I will likely *not* implement any feature enhancements, but
> contributions are welcome!


Polygon Geohasher is an open source Python package for converting Shapely's
polygons into a set of geohashes. It obtains the set of geohashes
inside a polygon or geohashes that touch (intersect) the polygon. This library uses
    [python-geohash](https://pypi.python.org/pypi/Geohash/) and
[shapely](http://toblerity.org/shapely/).


## Requirements
Polygon Geohasher requires:

- Python >= 3.10, < 3.15.
- GEOS >= 3.3 (due to shapely).

### Supported Python & Shapely Versions

| Python Version | Shapely 1          | Shapely 2          |
|----------------|--------------------|--------------------|
| 3.10           | :heavy_check_mark: | :heavy_check_mark: |
| 3.11           | :heavy_check_mark: | :heavy_check_mark: |
| 3.12           | :x:                | :heavy_check_mark: |
| 3.13           | :x:                | :heavy_check_mark: |
| 3.14           | :x:                | :heavy_check_mark: |

## Installing
Linux users can get Polygon Geohasher from the Python Package Index with
pip (8+):

`$ pip install polygon-geohasher-2`

## Usage
Here are some simple examples:

```python
from polygon_geohasher import polygon_to_geohashes, geohashes_to_polygon
from shapely import geometry

polygon = geometry.Polygon([(-99.1795917, 19.432134), (-99.1656847, 19.429034),
                            (-99.1776492, 19.414236), (-99.1795917, 19.432134)])
inner_geohashes_polygon = geohashes_to_polygon(polygon_to_geohashes(polygon, 7))
outer_geohashes_polygon = geohashes_to_polygon(polygon_to_geohashes(polygon, 7, False))
```


`geohash_to_polygon(geohash)`:

This function receives a geohash and returns a Shapely's Polygon.

`geohashes_to_polygon(geohashes)`:

This function receives a set of geohashes and returns a Shapely's Polygon or MultiPolygon.


`polygon_to_geohashes(polygon, precision[, inner=True])`:

This function receives a Shapely's Polygon and the precision of geohashes 
to be used to create a polygon and returns a set of geohashes
(strings) that covers said polygon. It also receives an optional
parameter `inner` that defines the way in which those polygons will be created.
If an `inner` parameter is given, then only contained geohashes will be used; otherwise, 
intersected geohashes will be used.

See geohashed polygons resulting from both options (with and without `inner`) in the 
following example:

![Example](./docs/images/geohashed-polygon-1.jpg)

## Development

To install the development environment:

```console
$ pip install -r requirements-dev.txt
```

To run the tests:

```console
$ pytest
```

To run the linter:

```console
flake8 .
```

### Type Checking

This project uses `mypy` to check type annotations. Please run the following command prior
to submitting a PR:

```console
$ mypy .
```
