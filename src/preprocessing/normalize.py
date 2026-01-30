import numpy as np
import open3d as o3d

def normalize_pointcloud(pcd):
    
    """
    Centers the point cloud at origin and scales to unit size
    """
    if pcd.is_empty():
        raise ValueError("Point cloud is empty")

    points = np.asarray(pcd.points)

    centroid = points.mean(axis=0)
    points -= centroid

    max_distance = np.max(np.linalg.norm(points, axis=1))
    points /= max_distance

    pcd.points = o3d.utility.Vector3dVector(points)

    print("[NORMALIZE] Point cloud normalized")
    return pcd
