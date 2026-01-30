import open3d as o3d
import numpy as np

def cluster_pointcloud(pcd, eps=0.02, min_points=100):
    """
    Clusters point cloud using DBSCAN
    """
    labels = np.array(
        pcd.cluster_dbscan(
            eps=eps,
            min_points=min_points,
            print_progress=True
        )
    )

    max_label = labels.max()
    clusters = []

    for i in range(max_label + 1):
        indices = np.where(labels == i)[0]
        cluster = pcd.select_by_index(indices)
        cluster.paint_uniform_color(np.random.rand(3).tolist())
        clusters.append(cluster)

    return clusters
