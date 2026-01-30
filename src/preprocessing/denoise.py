import open3d as o3d

def remove_noise(pcd, nb_neighbors=20, std_ratio=2.0):
    
    """
    Removes noisy points using Statistical Outlier Removal
    """
    if pcd.is_empty():
        raise ValueError("Point cloud is empty")

    pcd, _ = pcd.remove_statistical_outlier(
        nb_neighbors=nb_neighbors,
        std_ratio=std_ratio
    )

    print(f"[DENOISE] Points after denoising: {len(pcd.points)}")
    return pcd
