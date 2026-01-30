import open3d as o3d
import numpy as np

def segment_planes(
    pcd,
    distance_threshold=0.01,
    ransac_n=3,
    num_iterations=1000,
    min_points=500
):
    """
    Iteratively extracts planar segments using RANSAC
    """
    planes = []
    rest = pcd

    plane_id = 0
    while len(rest.points) > min_points:
        plane_model, inliers = rest.segment_plane(
            distance_threshold=distance_threshold,
            ransac_n=ransac_n,
            num_iterations=num_iterations
        )

        if len(inliers) < min_points:
            break

        plane_cloud = rest.select_by_index(inliers)
        plane_cloud.paint_uniform_color(
            np.random.rand(3).tolist()
        )

        planes.append({
            "id": plane_id,
            "model": plane_model,
            "cloud": plane_cloud
        })

        rest = rest.select_by_index(inliers, invert=True)
        plane_id += 1

    return planes, rest
