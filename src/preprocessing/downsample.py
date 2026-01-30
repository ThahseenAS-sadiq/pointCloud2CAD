import open3d as o3d

def downsample_pointcloud(pcd, voxel_size=0.01):
    
    """
    Downsamples the point cloud using voxel grid filtering
    and estimates normals
    """
    if pcd.is_empty():
        raise ValueError("Point cloud is empty")

    pcd = pcd.voxel_down_sample(voxel_size=voxel_size)

    pcd.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(
            radius=voxel_size * 2,
            max_nn=30
        )
    )

    print(f"[DOWNSAMPLE] Points after downsampling: {len(pcd.points)}")
    return pcd
