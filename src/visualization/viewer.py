import open3d as o3d
import numpy as np

# -------------------------------
# Point Cloud Visualization
# -------------------------------

def show_pointcloud(pcd, title="Point Cloud"):
    """
    Visualize a single point cloud
    """
    print(f"[VIEWER] Displaying: {title}")
    o3d.visualization.draw_geometries([pcd], window_name=title)


def show_multiple_pointclouds(pcd_list, title="Segmented Point Clouds"):
    """
    Visualize multiple point clouds together
    """
    print(f"[VIEWER] Displaying multiple clouds: {title}")
    o3d.visualization.draw_geometries(pcd_list, window_name=title)


# -------------------------------
# Segmentation Visualization
# -------------------------------

def show_planes(planes):
    """
    Visualize RANSAC-detected planes
    planes = list of dicts {id, model, cloud}
    """
    clouds = [p["cloud"] for p in planes]
    o3d.visualization.draw_geometries(
        clouds,
        window_name="RANSAC Planes"
    )


# -------------------------------
# Primitive Visualization (Conceptual)
# -------------------------------

def colorize_cloud(pcd, color=[1, 0, 0]):
    """
    Apply uniform color to point cloud
    """
    pcd.paint_uniform_color(color)
    return pcd


# -------------------------------
# CAD Visualization (Optional)
# -------------------------------

def show_cad_shape(shape):
    """
    Visualize CAD B-Rep shape (requires pythonOCC GUI)
    """
    try:
        from OCC.Display.SimpleGui import init_display
        display, start_display, _, _ = init_display()
        display.DisplayShape(shape, update=True)
        start_display()
    except ImportError:
        print("[VIEWER] pythonOCC display not available")
