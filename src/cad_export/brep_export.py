from OCC.Core.BRepTools import breptools_Write

def export_brep(shape, output_path):
    """
    Exports a B-Rep shape to a .brep file
    """
    success = breptools_Write(shape, output_path)

    if not success:
        raise RuntimeError("B-Rep export failed")

    print(f"[B-REP EXPORT] Saved B-Rep to {output_path}")
