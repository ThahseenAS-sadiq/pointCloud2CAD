import open3d as o3d

mesh = o3d.io.read_triangle_mesh("data/outputs/final_mesh.ply")
mesh.compute_vertex_normals()

# (Optional but recommended)
mesh.remove_degenerate_triangles()
mesh.remove_duplicated_triangles()
mesh.remove_duplicated_vertices()
mesh.remove_non_manifold_edges()

o3d.io.write_triangle_mesh(
    "data/outputs/final_mesh.stl",
    mesh
)

print("[OK] STL mesh saved")


# =====================================================
# PREPROCESSING
# =====================================================
from src.preprocessing.denoise import remove_noise
from src.preprocessing.downsample import downsample_pointcloud
from src.preprocessing.normalize import normalize_pointcloud
from src.preprocessing.save import save_pointcloud

print("=== PREPROCESSING ===")
pcd = o3d.io.read_point_cloud("data/raw_pointcloud/input.ply")

pcd = remove_noise(pcd)
pcd = downsample_pointcloud(pcd, voxel_size=0.01)
pcd = normalize_pointcloud(pcd)

save_pointcloud(pcd, "data/outputs/preprocessed.ply")

# =====================================================
# SEGMENTATION – PLANES (RANSAC)
# =====================================================
from src.segmentation.ransac_segmentation import segment_planes

print("\n=== PLANE SEGMENTATION ===")
planes, remaining_cloud = segment_planes(
    pcd,
    distance_threshold=0.01,
    min_points=300
)

print(f"Detected {len(planes)} planar segments")

import os

os.makedirs("data/segmented", exist_ok=True)

# Save each detected plane
for plane in planes:
    o3d.io.write_point_cloud(
        f"data/segmented/plane_{plane['id']}.ply",
        plane["cloud"]
    )

# Save remaining points
o3d.io.write_point_cloud(
    "data/segmented/remaining.ply",
    remaining_cloud
)

# =====================================================
# PRIMITIVE FITTING – PLANES
# =====================================================
from src.primitive_fitting.plane_fitting import fit_plane

print("\n=== PLANE FITTING ===")
plane_parameters = []

for plane in planes:
    params = fit_plane(plane["cloud"])
    plane_parameters.append(params)

print(f"Fitted {len(plane_parameters)} planes")

# =====================================================
# CYLINDER + HOLE DETECTION
# =====================================================
from src.segmentation.cylinder_segmentation import segment_cylinder_candidates
from src.primitive_fitting.cylinder_fitting import fit_cylinder

print("\n=== CYLINDER + HOLE DETECTION ===")

cylinder_clouds = segment_cylinder_candidates(
    remaining_cloud,
    normal_angle_thresh=15,
    min_points=300
)

cylinder_parameters = []
for cyl in cylinder_clouds:
    axis_dir, axis_pt, radius = fit_cylinder(cyl)
    cylinder_parameters.append((axis_dir, axis_pt, radius))

print(f"Detected {len(cylinder_parameters)} cylindrical holes")

# =====================================================
# VISUALIZATION
# =====================================================
from src.visualization.viewer import show_multiple_pointclouds

print("\n=== VISUALIZATION ===")

plane_clouds = [p["cloud"] for p in planes]

all_clouds = plane_clouds + cylinder_clouds
if not remaining_cloud.is_empty():
    all_clouds.append(remaining_cloud)

show_multiple_pointclouds(all_clouds, "Planes + Cylinders + Remaining")

# Optional Open3D viewer
o3d.visualization.draw_geometries(
    all_clouds,
    window_name="Full Segmentation Result"
)

# =====================================================
# CAD SOLID + HOLE CREATION
# =====================================================
from src.topology.cad_builder import create_base_solid, cut_cylindrical_hole
from src.cad_export.step_export import export_step

print("\n=== CAD SOLID + HOLE CREATION ===")

# Create base solid
cad_solid = create_base_solid(
    length=2.0,
    width=2.0,
    height=1.0
)

# Cut holes
for axis_dir, axis_pt, radius in cylinder_parameters:
    cad_solid = cut_cylindrical_hole(
        cad_solid,
        axis_pt,
        axis_dir,
        radius,
        depth=2.0
    )

# Export STEP
export_step(cad_solid, "data/outputs/final_model.step")


# =====================================================
# POINT CLOUD → MESH (OBJ + PLY)
# =====================================================
from src.mesh_reconstruction.pointcloud_to_mesh import pointcloud_to_mesh

import os

print("\n=== POINT CLOUD → MESH RECONSTRUCTION ===")

os.makedirs("data/outputs", exist_ok=True)

mesh = pointcloud_to_mesh(
    input_ply="data/raw_pointcloud/input.ply",
    output_obj="data/outputs/final_mesh.obj",
    output_mesh_ply="data/outputs/final_mesh.ply",
    method="ball_pivoting"  # BEST for ring / circular shapes
)

# =============================
# SANITY CHECK (IMPORTANT)
# =============================
print("\n=== MESH SANITY CHECK ===")
print("Vertices:", len(mesh.vertices))
print("Triangles:", len(mesh.triangles))
print("Is watertight:", mesh.is_watertight())
print("Bounding box:", mesh.get_axis_aligned_bounding_box())

# =============================
# SAFE MESH VISUALIZATION
# =============================

# Move mesh to center
mesh.translate(-mesh.get_center())

vis = o3d.visualization.Visualizer()
vis.create_window(
    window_name="Reconstructed Mesh",
    width=1280,
    height=800
)

vis.add_geometry(mesh)

# Add bounding box (helps camera)
bbox = mesh.get_axis_aligned_bounding_box()
bbox.color = (1, 0, 0)
vis.add_geometry(bbox)

# Reset camera correctly
vis.reset_view_point(True)

# Render options
opt = vis.get_render_option()
opt.mesh_show_back_face = True
opt.light_on = True

vis.run()
vis.destroy_window()
