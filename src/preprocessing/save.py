import open3d as o3d

def save_pointcloud(pcd, output_path):
    """
    Saves point cloud to disk
    """
    if pcd.is_empty():
        raise ValueError("Point cloud is empty")

    o3d.io.write_point_cloud(output_path, pcd)
    print(f"[SAVE] Point cloud saved to {output_path}")
