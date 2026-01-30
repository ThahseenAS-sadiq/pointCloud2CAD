from matplotlib import projections
import numpy as np

def fit_cylinder(cylinder_cloud):
    """
    Fits a cylinder using PCA-based axis estimation

    Returns:
        axis_dir   : unit vector of cylinder axis
        axis_point : a point on the axis (centroid)
        radius     : cylinder radius
    """
    points = np.asarray(cylinder_cloud.points)

    if points.shape[0] < 50:
        raise ValueError("Not enough points for cylinder fitting")

    # Axis estimation using PCA
    centroid = points.mean(axis=0)
    _, _, vh = np.linalg.svd(points - centroid)
    axis_dir = vh[0]

    # Ensure unit direction
    axis_dir = axis_dir / np.linalg.norm(axis_dir)

    # Compute radius as mean distance from axis
    diffs = points - centroid
    radial_vectors = diffs - np.outer(diffs @ axis_dir, axis_dir)
    radius = np.mean(np.linalg.norm(radial_vectors, axis=1))

    print(f"[CYLINDER FIT] Radius: {radius:.4f}")


    # Project points onto axis to estimate height
    projections = (points - centroid) @ axis_dir
    height = projections.max() - projections.min()

    return axis_dir, centroid, radius, height
