import numpy as np

def fit_plane(plane_cloud):
    """
    Fits a plane using least squares on a segmented plane cloud
    Returns: (a, b, c, d) for ax + by + cz + d = 0
    """
    points = np.asarray(plane_cloud.points)

    # Plane fitting using SVD
    centroid = points.mean(axis=0)
    uu, ss, vv = np.linalg.svd(points - centroid)
    normal = vv[2, :]

    a, b, c = normal
    d = -normal.dot(centroid)

    print("[PLANE FIT] Plane equation:", a, b, c, d)
    return a, b, c, d
