import numpy as np
from rtree import index
import itertools
from shapely.geometry import shape, mapping
from shapely.ops import unary_union
from scipy.spatial import Voronoi
import config

def voronoi_finite_polygons_2d(points, radius=None):
    """Reconstruct infinite Voronoi regions in a
    2D diagram to finite regions.
    Source:
    [https://stackoverflow.com/a/20678647/1595060](https://stackoverflow.com/a/20678647/1595060)
    """
    vor = Voronoi(np.array(points))
    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input")
    new_regions = []
    new_vertices = vor.vertices.tolist()
    center = vor.points.mean(axis=0)
    if radius is None:
        radius = vor.points.ptp().max()
    # Construct a map containing all ridges for a
    # given point
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points,
                                  vor.ridge_vertices):
        all_ridges.setdefault(
            p1, []).append((p2, v1, v2))
        all_ridges.setdefault(
            p2, []).append((p1, v1, v2))

    all_keys = list(all_ridges.keys())

    # Reconstruct infinite regions
    for p1, region in enumerate(vor.point_region):
        vertices = vor.regions[region]
        if all(v >= 0 for v in vertices):
            # finite region
            new_regions.append(vertices)
            continue
        if p1 not in all_keys:
            print("Hmm couldn't reconstruct that voronoi region for some region")
            continue
        # reconstruct a non-finite region
        ridges = all_ridges[p1]
        new_region = [v for v in vertices if v >= 0]
        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                # finite ridge: already in the region
                continue
            # Compute the missing endpoint of an
            # infinite ridge
            t = vor.points[p2] - \
                vor.points[p1]  # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # normal
            midpoint = vor.points[[p1, p2]]. \
                mean(axis=0)
            direction = np.sign(
                np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[v2] + \
                direction * radius
            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())
        # Sort region counterclockwise.
        vs = np.asarray([new_vertices[v]
                         for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(
            vs[:, 1] - c[1], vs[:, 0] - c[0])
        new_region = np.array(new_region)[
            np.argsort(angles)]
        new_regions.append(new_region.tolist())
    return new_regions, np.asarray(new_vertices)
       

def get_code_for_voronoi_region(region, centroids, centroid_index, code): 
    region_shape = shape(region["geometry"])
    candidate_points = list(centroid_index.intersection(region_shape.bounds))

    for idx in candidate_points:
        centroid_shape = shape(centroids[idx]["geometry"])
        if region_shape.intersects(centroid_shape):
            region["properties"][code] = centroids[idx]["properties"][code]
            return


def create_centroids(feature, code, centroids, output_centroid_shp):
    contours = []
    if feature['geometry']['type'] == 'MultiPolygon':
        for polygon in shape(feature['geometry']):
            contours.append(polygon)
    else:
        contours.append(feature['geometry'])
    
    for contour in contours:
        geom = shape(contour)
        try_cent = geom.centroid
        cent = list(try_cent.coords)
        centroid_feature = {
            "type": "Feature",
            "properties": {
                code: feature['properties'][code]
            },
            "geometry": {
                "type": "Point",
                "coordinates": [cent[0][0], cent[0][1]]
            }
        }
        centroids.append(centroid_feature)
        output_centroid_shp.write(centroid_feature)

def create_index_for_centroids(centroids):
    idx = index.Index()
    i = 0
    for centroid in centroids:
        centroid_shape = shape(centroid["geometry"])
        idx.insert(i, centroid_shape.bounds)
        i += 1
    return idx

def clip_orig_by_voronoi(orig_features, out_regions, output_shp_buffered, code, adminCode):
    for f in orig_features:
        country_info = config.get_country_config_by_country_code(f['properties']['CNTRY_ISO3'])
        if "requiresBuffer" in country_info[adminCode] and country_info[adminCode]["requiresBuffer"] is False:
            output_shp_buffered.write(f)
            continue

        inters = []
        clipped_geom = shape(f['geometry'])
        for region in out_regions:
            if f["properties"][code] == region["properties"][code]:
                inters.append(clipped_geom.intersection(shape(region['geometry'])))

        if len(inters) > 0:
            out = mapping(unary_union(inters))
        else:
            out = mapping(clipped_geom)
        if (out['type'] != 'Polygon') or (out['type'] != 'MultiPolygon'):
            output_shp_buffered.write({'geometry': out, 'properties': f["properties"]})
