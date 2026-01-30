import numpy as np
import open3d as o3d

def region_growing(
    pcd,
    angle_threshold=30.0,
    min_points=100
):
    """
    Simple normal-based region growing segmentation
    """
    normals = np.asarray(pcd.normals)
    points = np.asarray(pcd.points)

    visited = np.zeros(len(points), dtype=bool)
    regions = []

    cos_thresh = np.cos(np.deg2rad(angle_threshold))

    for i in range(len(points)):
        if visited[i]:
            continue

        seed = i
        stack = [seed]
        region = []

        visited[seed] = True

        while stack:
            idx = stack.pop()
            region.append(idx)

            for j in range(len(points)):
                if visited[j]:
                    continue
                if np.dot(normals[idx], normals[j]) > cos_thresh:
                    visited[j] = True
                    stack.append(j)

        if len(region) >= min_points:
            region_cloud = pcd.select_by_index(region)
            region_cloud.paint_uniform_color(
                np.random.rand(3).tolist()
            )
            regions.append(region_cloud)

    return regions
