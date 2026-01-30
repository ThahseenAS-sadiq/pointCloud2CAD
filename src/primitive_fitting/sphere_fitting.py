import numpy as np

def fit_sphere(sphere_cloud):
    """
    Fits a sphere using least squares
    Returns: center (x, y, z), radius
    """
    points = np.asarray(sphere_cloud.points)

    A = np.hstack([2 * points, np.ones((points.shape[0], 1))])
    b = np.sum(points ** 2, axis=1)

    C, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

    center = C[:3]
    radius = np.sqrt(C[3] + np.sum(center ** 2))

    print("[SPHERE FIT] Center:", center, "Radius:", radius)
    
    return center, radius
