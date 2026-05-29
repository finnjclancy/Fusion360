# Feature Recipes Deep Guide

This document explains how agents should choose and implement common Fusion feature types.

## Operation Choice

Most solid features use an operation:

- `NewBodyFeatureOperation`: creates a separate solid.
- `JoinFeatureOperation`: adds material to an existing body.
- `CutFeatureOperation`: removes material.
- `IntersectFeatureOperation`: keeps overlapping material.

Default choices:

- Base shape: `NewBodyFeatureOperation`.
- Holes, slots, engravings, pockets: `CutFeatureOperation`.
- Bosses, ribs, raised text: `JoinFeatureOperation`.
- Separate parts: `NewBodyFeatureOperation`.

## Extrude

Use extrude for prismatic features from a 2D profile:

- Blocks
- Plates
- Cylinders
- Holes
- Slots
- Bosses
- Pockets

Pattern:

```python
extrudes = component.features.extrudeFeatures
extrude_input = extrudes.createInput(profile, operation)
extrude_input.setDistanceExtent(False, adsk.core.ValueInput.createByReal(distance_cm))
feature = extrudes.add(extrude_input)
```

For through cuts, prefer an extent that guarantees it passes through the body. A simple robust fallback is to cut deeper than the body height in both directions if supported by the chosen extent API.

## Revolve

Use revolve for axisymmetric shapes:

- Bowls
- Cones
- Pulleys
- Wheels
- Turned parts
- Grooves around a cylinder

Inputs:

- Profile
- Axis line
- Operation
- Angle

Agents should draw a clean cross-section on a plane containing the revolve axis. Avoid revolve when a simple cylinder extrude is enough.

## Sweep

Use sweep when a profile follows a path:

- Pipes/tubes along a curve
- Cable channels
- Handles
- O-rings
- Decorative ribs

Inputs:

- Profile sketch
- Path sketch/curve
- Operation

Sweep is more fragile than extrude/revolve. Keep paths simple and avoid self-intersections.

## Loft

Use loft to blend between profiles:

- Organic transitions
- Tapered adapters
- Rectangular-to-round transitions
- Smooth handles

Inputs:

- Two or more profiles
- Optional rails/centerline
- Operation

Loft can fail if profiles have incompatible topology or twisting. For symmetrical parts, consider lofting a portion and mirroring.

## Hole Feature

Use Fusion's hole feature when the user needs:

- Counterbore
- Countersink
- Thread
- Tapped holes
- Hole standards
- Parametric hole definitions

For simple through holes, sketch circles and cut extrude. It is easier for agents to control and debug.

## Shell

Use shell for hollowing a body:

- Open boxes
- Housings
- Covers
- Containers

Key decisions:

- Which face is removed?
- What wall thickness?
- Should all edges be filleted before or after shell?

Shell can fail on complex geometry or tight radii. If shell fails, build walls explicitly from sketch profiles.

## Fillet

Use fillet for rounded edges.

Default:

- Simple block: fillet all body edges.
- Functional part: fillet only requested or safe edges.

Validate:

- Fillet radius should be smaller than nearby feature sizes.
- Fillet can fail around holes/slots if too large.

## Chamfer

Use chamfer for bevels.

Common requests:

- "bevel the edges"
- "make the edge less sharp"
- "add a 45 degree chamfer"

Chamfers are often better than fillets for printable parts that need a flat angled edge.

## Pattern

Use patterns for repeated geometry:

- Hole arrays
- Vent slots
- Teeth
- Ribs
- Pins

Types:

- Rectangular pattern
- Circular pattern
- Pattern on path

Prefer patterning features rather than sketch geometry when the repeated operation is a modeled feature. For simple holes in this rebuild workflow, generating repeated circle profiles directly can be simpler and more deterministic.

## Generated Slots and Capsules

For user-editable sketches, Fusion's slot helpers are useful.

For deterministic generated rebuilds, prefer manual capsule geometry:

1. Calculate the slot centerline from start and end points.
2. Calculate a perpendicular vector.
3. Draw two side lines.
4. Draw two semicircular end arcs.
5. Use the closed profile for extrude/cut.

This avoids automatic sketch constraints that can cause `VCS_SKETCH_OVER_CONSTRAINTS`.

## Mirror

Use mirror for symmetric parts:

- Brackets
- Handles
- Left/right features
- Repeated holes across a centerline

Mirroring bodies or features is often safer than manually duplicating asymmetric code.

## Combine

Use combine for boolean operations between bodies:

- Cut body A using body B as a tool.
- Join multiple bodies.
- Intersect two solids.

Keep tool bodies named and delete or hide them after use unless the user wants them visible.

## Split

Use split when the request says:

- "cut this in half"
- "separate the lid"
- "make a removable cap"
- "divide into two parts"

Split can use a plane, sketch curve, surface, or body as the splitting tool.

## Text Features

Raised text:

- Create text in a sketch.
- Convert to profiles if needed.
- Extrude join by a small depth.

Engraved text:

- Create text on a face/sketch plane.
- Extrude cut a shallow depth.

Keep text simple. Font availability can vary.

## Agent Decision Tree

1. Is the shape constant along one direction? Use extrude.
2. Is the shape rotationally symmetric? Use revolve.
3. Does a profile follow a curve? Use sweep.
4. Does it blend between different profiles? Use loft.
5. Is material removed by a simple outline? Use extrude cut.
6. Is the part hollowed? Use shell or explicit walls.
7. Is a detail repeated? Use pattern or generated repeated profiles.
8. Is the part symmetric? Use mirror or symmetric coordinates.

## References

- Autodesk, API samples list: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/SampleList.htm
- Autodesk, ExtrudeFeatures.createInput: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/ExtrudeFeatures_createInput.htm
- Autodesk, Loft feature sample: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/LoftFeatureSample_Sample.htm
- Autodesk, Getting Started with Fusion API: https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-D93DF10F-4209-4073-A2A0-4FA8788C8709
