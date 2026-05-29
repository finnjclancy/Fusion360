# Sketch Constraints and Dimensions

Agents should build sketches that communicate design intent. A sketch that looks right but is unconstrained can move unpredictably when a dimension changes.

## Core Rule

Prefer simple sketches with a small number of dimensions and clear constraints. Avoid creating many loose curves and hoping profiles remain stable.

## Use Constraints For Relationships

Common design relationships:

- Coincident: endpoints touch or a point lies on another curve.
- Horizontal/Vertical: line direction is locked.
- Parallel/Perpendicular: line relationship is locked.
- Equal: repeated lengths/radii stay equal.
- Concentric: circles/arcs share a center.
- Tangent: arcs/circles blend with lines or other curves.
- Symmetry: mirrored geometry stays balanced around a construction line.
- Midpoint: a point stays at the midpoint of a line.
- Fix: last resort for reference geometry, not a substitute for design intent.

## Use Dimensions For Size and Position

Dimensions should express what Finn cares about:

- Overall length, width, height.
- Hole diameter.
- Distance from edge to hole center.
- Slot length and width.
- Offset from centerline.
- Angle of a feature.

Do not over-dimension. If constraints already define something, adding a dimension can overconstrain the sketch.

## Fusion API Objects

Sketches expose:

```python
sketch.sketchCurves
sketch.geometricConstraints
sketch.sketchDimensions
```

`SketchDimensions` supports methods like:

- `addDistanceDimension`
- `addDiameterDimension`
- `addRadialDimension`
- `addAngularDimension`
- `addConcentricCircleDimension`

Use `ValueInput.createByString("20 mm")` for dimension values when possible. It preserves human-readable units and can later be replaced with named parameter expressions.

## Recommended Modeling Pattern

For generated models in this add-in:

1. Center the base sketch on the origin.
2. Use symmetric points or coordinates around the origin.
3. Name the sketch with a stable generated name.
4. Add only the geometry needed for the profile.
5. Prefer dimensions/parameters when the sketch needs to remain editable in Fusion.
6. Use procedural coordinates for simple generated sketches when robust enough.

The current block uses procedural coordinates instead of sketch dimensions because the add-in rebuilds from JSON. That is acceptable for simple generated geometry.

## When to Add Explicit Sketch Dimensions

Add explicit dimensions when:

- Finn wants the model editable through Fusion's parameter/dimension UI.
- A sketch is complex enough that constraints express important design intent.
- The feature should update through Fusion timeline edits, not only through rebuild.
- The code creates a sketch that users may manually inspect or modify.

Do not add sketch dimensions just to duplicate JSON values if the sketch is deleted and recreated every rebuild.

## Overconstraint Avoidance

If Fusion reports that a sketch is overconstrained:

1. Remove redundant dimensions first.
2. Check whether automatic constraints already define the relationship.
3. Use construction geometry to reduce competing constraints.
4. Dimension from a centerline/origin instead of multiple edges.
5. Rebuild the sketch simpler if it becomes hard to reason about.

## Underconstraint Avoidance

If a sketch profile moves unexpectedly:

1. Anchor it to the origin or projected geometry.
2. Add dimensions for primary size and position.
3. Add constraints for relationships.
4. Avoid freehand spline/control-point geometry unless the request needs it.

## Agent Defaults

Unless the user says otherwise:

- Use the XY plane for base sketches.
- Center base shapes on the origin.
- Use construction centerlines for symmetry.
- Use one dimension for each primary size.
- Use equal constraints for repeated circles/holes if building editable sketches.
- Use named parameters for important dimensions if adding parametric support.

## References

- Autodesk, Sketch object: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/Sketch.htm
- Autodesk, SketchDimensions object: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/SketchDimensions.htm
- Autodesk, Sketches in Fusion: https://help.autodesk.com/view/fusion360/ENU/?contextId=SKT-3D-SKETCH
- Autodesk, Sketch constraints tutorial: https://www.autodesk.com/products/fusion-360/blog/mastering-sketch-constraints-autodesk-fusion-tutorial/

