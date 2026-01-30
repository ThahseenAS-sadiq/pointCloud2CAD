import open3d as o3d
import numpy as np


def pointcloud_to_mesh(
    input_ply,
    output_obj,
    output_mesh_ply,
    method="poisson"
):
    # -----------------------------
    # Load point cloud
    # -----------------------------
    pcd = o3d.io.read_point_cloud(input_ply)
    if pcd.is_empty():
        raise ValueError("Input point cloud is empty")

    # -----------------------------
    # STRONG normal estimation
    # -----------------------------
    pcd.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(
            radius=0.03,
            max_nn=50
        )
    )

    # 🔑 CRITICAL: orient normals
    pcd.orient_normals_consistent_tangent_plane(k=50)

    # -----------------------------
    # Surface Reconstruction
    # -----------------------------
    if method == "poisson":
        mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
            pcd,
            depth=11
        )

        densities = np.asarray(densities)
        mesh = mesh.select_by_index(
            densities > np.percentile(densities, 10)
        )

    elif method == "ball_pivoting":
        distances = pcd.compute_nearest_neighbor_distance()
        avg_dist = np.mean(distances)

        radii = [avg_dist * 1.5, avg_dist * 2.5, avg_dist * 3.5]
        mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
            pcd,
            o3d.utility.DoubleVector(radii)
        )

    else:
        raise ValueError("Unknown reconstruction method")

    # -----------------------------
    # Cleanup mesh
    # -----------------------------
    mesh.remove_degenerate_triangles()
    mesh.remove_duplicated_triangles()
    mesh.remove_duplicated_vertices()
    mesh.remove_non_manifold_edges()
    mesh.compute_vertex_normals()

    # -----------------------------
    # Save outputs
    # -----------------------------
    o3d.io.write_triangle_mesh(output_obj, mesh)
    o3d.io.write_triangle_mesh(output_mesh_ply, mesh)

    print("[MESH] OBJ saved to:", output_obj)
    print("[MESH] Mesh PLY saved to:", output_mesh_ply)

    return mesh
