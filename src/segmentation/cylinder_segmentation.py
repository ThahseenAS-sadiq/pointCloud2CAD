import numpy as np
import open3d as o3d

def segment_cylinder_candidates(
    pcd,
    normal_angle_thresh=25,
    min_points=80
):
    """
    Extracts cylinder-like regions using
    spatial + normal consistency
    """

    normals = np.asarray(pcd.normals)
    points = np.asarray(pcd.points)

    visited = np.zeros(len(points), dtype=bool)
    clusters = []

    cos_thresh = np.cos(np.deg2rad(normal_angle_thresh))

    # 🔑 spatial search
    kdtree = o3d.geometry.KDTreeFlann(pcd)

    for i in range(len(points)):
        if visited[i]:
            continue

        stack = [i]
        cluster = []
        visited[i] = True

        while stack:
            idx = stack.pop()
            cluster.append(idx)

            # 🔑 only nearby points
            _, idxs, _ = kdtree.search_radius_vector_3d(
                points[idx],
                0.02   # tune if needed
            )

            for j in idxs:
                if visited[j]:
                    continue

                if abs(np.dot(normals[idx], normals[j])) > cos_thresh:
                    visited[j] = True
                    stack.append(j)

        if len(cluster) >= min_points:
            cyl_cloud = pcd.select_by_index(cluster)
            cyl_cloud.paint_uniform_color([0, 0, 1])
            clusters.append(cyl_cloud)

    print(f"[CYLINDER SEG] Found {len(clusters)} cylinder candidates")
    return clusters
