from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.Interface import Interface_Static

def export_step(shape, output_path):
    """
    Exports a CAD shape to STEP format
    """
    # Set STEP schema (AP203 / AP214)
    Interface_Static.SetCVal("write.step.schema", "AP214")

    step_writer = STEPControl_Writer()
    step_writer.Transfer(shape, STEPControl_AsIs)

    status = step_writer.Write(output_path)

    if status != 1:
        raise RuntimeError("STEP export failed")

    print(f"[STEP EXPORT] Saved STEP file to {output_path}")
