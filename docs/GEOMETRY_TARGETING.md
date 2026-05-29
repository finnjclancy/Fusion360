# Geometry Targeting and Selection

Many user requests refer to geometry semantically: "top face", "outer edges", "front", "rim", "corners". Agents need deterministic ways to translate those words into B-Rep faces and edges.

## B-Rep Mental Model

Fusion solid bodies are boundary representations:

- `BRepBody`: a solid/surface body.
- `BRepFace`: a face/surface on a body.
- `BRepEdge`: a curve where faces meet.
- `BRepVertex`: a point where edges meet.

Topology describes how faces, edges, and vertices connect. Geometry describes the actual surface/curve shape.

## Prefer Generated References First

Best targeting order:

1. Use the feature/body/sketch object just created.
2. Name generated bodies/features/sketches and retrieve them by name.
3. Use bounding boxes and geometric tests.
4. Ask the user to select geometry with `SelectionCommandInput` if exact manual targeting is needed.

Do not rely on collection index order unless the code just created the object and Fusion's API returns the created feature/body directly.

## Bounding Box Helpers

Every body has a bounding box:

```python
box = body.boundingBox
min_point = box.minPoint
max_point = box.maxPoint
```

For this project's convention:

- Top is near `maxPoint.z`.
- Bottom is near `minPoint.z`.
- Right is near `maxPoint.x`.
- Left is near `minPoint.x`.
- Back/front depend on user context; document the convention if using Y.

Use a tolerance because floating point values are not exact.

```python
TOL = 1e-6
```

## Finding Planar Faces

Use face geometry type to find planes:

```python
plane = adsk.core.Plane.cast(face.geometry)
if plane:
    normal = plane.normal
```

To find a top face, look for planar faces with normal roughly positive Z and center near the body's max Z.

Pseudocode:

```python
def is_top_face(face, body):
    plane = adsk.core.Plane.cast(face.geometry)
    if not plane:
        return False
    point = face.pointOnFace
    return plane.normal.z > 0.9 and abs(point.z - body.boundingBox.maxPoint.z) < 1e-5
```

If normal direction is inconsistent, use face evaluator normals rather than raw surface geometry where possible.

## Finding Vertical Edges

An edge is vertical if its endpoints have similar X/Y and different Z.

Pseudocode:

```python
start = edge.startVertex.geometry
end = edge.endVertex.geometry
same_xy = abs(start.x - end.x) < tol and abs(start.y - end.y) < tol
different_z = abs(start.z - end.z) > tol
```

Use vertical edges for requests like "round the four vertical corners."

## Finding Top Perimeter Edges

Top perimeter edges usually have both vertices near max Z:

```python
top_z = body.boundingBox.maxPoint.z
start_top = abs(edge.startVertex.geometry.z - top_z) < tol
end_top = abs(edge.endVertex.geometry.z - top_z) < tol
```

Use this for "round only the top edges."

## Finding Circular Edges and Rims

Cast edge geometry to circle/arc types where possible:

```python
circle = adsk.core.Circle3D.cast(edge.geometry)
arc = adsk.core.Arc3D.cast(edge.geometry)
```

Use circular edges for:

- Hole rims
- Tube rims
- Cylinder top/bottom edges
- Counterbore/countersink targeting

## Largest Face

For "put it on the biggest flat face":

1. Filter planar faces.
2. Estimate face area if available.
3. Pick the largest area.
4. Prefer upward-facing face if tied.

Be careful: face area APIs may vary. If area is not readily available, use bounding box extents as an approximation for simple rectangular faces.

## SelectionCommandInput

When the user needs exact manual targeting, add a command dialog with a `SelectionCommandInput`.

Use cases:

- "Put a hole on this face."
- "Round this edge."
- "Engrave this selected face."
- "Cut from this body using that body."

Selection input is a UI workflow change, so Finn may need to toggle the add-in after code changes.

## Avoid Fragile Targeting

Avoid:

- "use face index 0"
- "use edge index 3"
- relying on face order after feature changes
- selecting by display name when Fusion does not preserve it

Prefer:

- generated references
- named objects
- bounding-box criteria
- geometry type tests
- explicit user selection

## References

- Autodesk, Fusion Models: B-Rep and Geometry: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/BRepGeometry_UM.htm
- Autodesk, Fusion API object model PDF: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/ExtraFiles/Fusion.pdf

