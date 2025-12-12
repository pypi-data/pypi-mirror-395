import random

from shapely.geometry import GeometryCollection, LineString, Point, shape
from shapely.ops import split, unary_union

from .disk import load_raw_json


async def load_geometry_collection(geojson_path):
    d = await load_raw_json(geojson_path)
    return unary_union([shape(_) for _ in d['features']])


def make_random_points(source_geometry, target_count):
    points = []
    minimum_x, minimum_y, maximum_x, maximum_y = source_geometry.bounds
    while len(points) < target_count:
        # Generate random points inside bounds
        random_points = [Point(
            random.uniform(minimum_x, maximum_x),  # noqa: S311
            random.uniform(minimum_y, maximum_y),  # noqa: S311
        ) for _ in range(target_count)]
        # Retain points inside region
        collection = unary_union(random_points + points)
        intersection = collection.intersection(source_geometry)
        if intersection.geom_type == 'Point':
            points = [intersection]
        else:
            points = list(intersection.geoms)
    # Trim if there are too many
    return points[:target_count]


def slice_geometry(source_geometry, target_x_count=1, target_y_count=1):
    minimum_x, minimum_y, maximum_x, maximum_y = source_geometry.bounds
    dx = (maximum_x - minimum_x) / target_x_count
    dy = (maximum_y - minimum_y) / target_y_count
    x_lines = [LineString([
        (minimum_x + i * dx, minimum_y),
        (minimum_x + i * dx, maximum_y),
    ]) for i in range(1, target_x_count)]
    y_lines = [LineString([
        (minimum_x, minimum_y + i * dy),
        (maximum_x, minimum_y + i * dy),
    ]) for i in range(1, target_y_count)]
    geometry_collection = source_geometry
    for line in x_lines + y_lines:
        geometry_collection = split(geometry_collection, line)
    if geometry_collection.geom_type != 'GeometryCollection':
        geometry_collection = GeometryCollection(geometry_collection)
    return geometry_collection
