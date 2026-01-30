import numpy as np
from OCC.Core.BRepPrimAPI import (
    BRepPrimAPI_MakeBox,
    BRepPrimAPI_MakeCylinder
)
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Core.gp import gp_Ax2, gp_Pnt, gp_Dir


# =====================================================
# BASE SOLID
# =====================================================
def create_base_solid(length=2.0, width=2.0, height=1.0):
    """
    Creates a base CAD solid (box)
    """
    box = BRepPrimAPI_MakeBox(length, width, height).Shape()
    print("[CAD] Base solid created")
    return box


# =====================================================
# CUT CYLINDRICAL HOLE
# =====================================================
def cut_cylindrical_hole(base_shape, axis_point, axis_dir, radius, depth=2.0):
    """
    Cuts a cylindrical hole from a CAD solid
    """
    axis_dir = axis_dir / np.linalg.norm(axis_dir)

    axis = gp_Ax2(
        gp_Pnt(*axis_point),
        gp_Dir(*axis_dir)
    )

    cylinder = BRepPrimAPI_MakeCylinder(axis, radius, depth).Shape()
    result = BRepAlgoAPI_Cut(base_shape, cylinder).Shape()

    print("[CAD] Cylindrical hole cut successfully")
    return result


# =====================================================
# CREATE CONNECTOR CYLINDER (INFERRED FEATURE)
# =====================================================
def create_connector_cylinder(c1, c2):
    """
    c1, c2 = (axis_dir, center, radius, height)
    """
    axis1, center1, r1, _ = c1
    axis2, center2, r2, _ = c2

    # Direction between two cylinders
    conn_dir = center2 - center1
    length = np.linalg.norm(conn_dir)

    if length < 1e-6:
        raise ValueError("Cylinder centers too close")

    conn_dir = conn_dir / length

    # Infer connector radius
    conn_radius = min(r1, r2) * 0.8

    axis = gp_Ax2(
        gp_Pnt(*center1),
        gp_Dir(*conn_dir)
    )

    connector = BRepPrimAPI_MakeCylinder(
        axis,
        conn_radius,
        length
    ).Shape()

    print("[CAD] Connector cylinder created")
    return connector
