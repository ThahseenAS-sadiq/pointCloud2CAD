from OCC.Core.IntTools import IntTools_FaceFace
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.TopExp import TopExp_Explorer

def intersect_faces(shape):
    """
    Finds intersections between faces in a B-Rep shape
    Returns list of intersection edges
    """
    faces = []
    explorer = TopExp_Explorer(shape, TopAbs_FACE)

    while explorer.More():
        faces.append(explorer.Current())
        explorer.Next()

    intersections = []

    for i in range(len(faces)):
        for j in range(i + 1, len(faces)):
            ff = IntTools_FaceFace()
            ff.Perform(faces[i], faces[j])

            if ff.IsDone():
                curves = ff.Lines()
                for k in range(1, curves.Length() + 1):
                    intersections.append(curves.Value(k))

    print(f"[TOPOLOGY] Found {len(intersections)} intersection curves")
    
    return intersections
