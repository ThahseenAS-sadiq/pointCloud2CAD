from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Core.Geom import Geom_Surface
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE

def trim_faces(base_shape, tool_shape):
    """
    Trims CAD faces using Boolean cut operation
    Returns trimmed shape
    """
    cut = BRepAlgoAPI_Cut(base_shape, tool_shape)
    cut.Build()

    if not cut.IsDone():
        raise RuntimeError("Trimming failed")

    trimmed_shape = cut.Shape()
    print("[TRIMMING] Faces trimmed successfully")
    return trimmed_shape
