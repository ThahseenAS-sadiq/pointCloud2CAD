from OCC.Core.StlAPI import StlAPI_Reader
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Sewing, BRepBuilderAPI_MakeSolid
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_SHELL
from OCC.Core.TopoDS import TopoDS_Shell
from OCC.Core.IFSelect import IFSelect_RetDone


def mesh_to_solid(mesh_stl, output_step):
    print("[SOLID] Reading STL...")

    reader = StlAPI_Reader()
    shape = reader.ReadFile(mesh_stl)
    if not reader.ReadFile(mesh_stl):
        raise RuntimeError("Failed to read STL file")

    shape = reader.Shape()

    print("[SOLID] Sewing mesh...")
    sewing = BRepBuilderAPI_Sewing(1e-3)
    sewing.Add(shape)
    sewing.Perform()
    sewed_shape = sewing.SewedShape()

    print("[SOLID] Extracting shell...")
    explorer = TopExp_Explorer(sewed_shape, TopAbs_SHELL)

    if not explorer.More():
        raise RuntimeError("No shell found — mesh is not watertight")

    shell = TopoDS_Shell(explorer.Current())

    print("[SOLID] Creating solid...")
    solid_maker = BRepBuilderAPI_MakeSolid(shell)
    solid = solid_maker.Solid()

    print("[SOLID] Exporting STEP...")
    writer = STEPControl_Writer()
    writer.Transfer(solid, STEPControl_AsIs)

    status = writer.Write(output_step)
    if status != IFSelect_RetDone:
        raise RuntimeError("STEP export failed")

    print("[SOLID] STEP solid saved:", output_step)
