from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.Core.gp import gp_Ax2, gp_Pnt, gp_Dir
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut

def cut_cylindrical_hole(base_shape, axis_point, axis_dir, radius, depth=100):
    """
    Creates a cylindrical hole and subtracts it from the CAD solid
    """
    axis = gp_Ax2(
        gp_Pnt(*axis_point),
        gp_Dir(*axis_dir)
    )

    cylinder = BRepPrimAPI_MakeCylinder(axis, radius, depth).Shape()
    cut_shape = BRepAlgoAPI_Cut(base_shape, cylinder).Shape()

    print("[HOLE] Cylindrical hole cut successfully")
    return cut_shape
