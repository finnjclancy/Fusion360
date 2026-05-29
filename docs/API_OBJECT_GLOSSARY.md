# Fusion API Object Glossary

This glossary explains the objects agents will see most often.

## `adsk.core.Application`

Top-level Fusion application object.

Use for:

- Getting the active product/document.
- Accessing the user interface.
- Logging.
- Creating new documents.

Pattern:

```python
app = adsk.core.Application.get()
```

## `UserInterface`

Fusion UI object.

Use for:

- Message boxes.
- Command definitions.
- Toolbar panels.
- Palettes.

Pattern:

```python
ui = app.userInterface
```

## `Design`

The active Fusion design product.

Use for:

- Root component.
- Export manager.
- User parameters.
- Appearance/material collections.

Pattern:

```python
design = adsk.fusion.Design.cast(app.activeProduct)
```

## `Component`

A component contains sketches, bodies, construction geometry, and features.

Important properties:

- `sketches`
- `features`
- `bRepBodies`
- `occurrences`
- construction planes/axes

Use `design.rootComponent` when in doubt.

## `Occurrence`

An instance of a component in an assembly.

Agents often create child components with:

```python
root.occurrences.addNewComponent(transform)
```

But this can fail in Part Design documents. Always support fallback to the root component.

## `Sketch`

2D geometry on a plane or face. Sketch profiles drive many features.

Important properties:

- `sketchCurves`
- `sketchDimensions`
- `geometricConstraints`
- `profiles`

## `Profile`

A closed region in a sketch. Extrudes, revolves, sweeps, and lofts often consume profiles.

If `sketch.profiles.count == 0`, the sketch is probably open or invalid for solid creation.

## `BRepBody`

A solid or surface body.

Use for:

- Naming generated geometry.
- Applying appearances.
- Getting faces/edges.
- Exporting bodies/components.

## `BRepFace`

A face on a body.

Use for:

- Sketching on a face.
- Selecting top/bottom/side faces.
- Shell face removal.
- Face-level appearances.

## `BRepEdge`

An edge between faces.

Use for:

- Fillets.
- Chamfers.
- Finding rims.
- Finding top/vertical edges.

## `Feature`

A timeline/modeling operation, such as extrude, fillet, shell, hole, pattern, combine.

Feature inputs configure the operation; adding the input creates the feature.

## `ValueInput`

Wrapper for numeric or expression inputs.

Use:

```python
adsk.core.ValueInput.createByReal(value_cm)
adsk.core.ValueInput.createByString('12 mm')
```

## `ObjectCollection`

A Fusion collection used to pass multiple entities into feature inputs.

Example:

```python
edges = adsk.core.ObjectCollection.create()
edges.add(edge)
```

## `Matrix3D`

Transform matrix for placement/orientation.

Used when creating occurrences or transforming geometry.

## `Point3D` and `Vector3D`

Core geometry primitives.

Use `Point3D` for positions and `Vector3D` for directions/normals.

## `Plane`, `Circle3D`, `Arc3D`, etc.

Geometry objects returned from B-Rep faces/edges.

Use casts to check geometry type:

```python
plane = adsk.core.Plane.cast(face.geometry)
circle = adsk.core.Circle3D.cast(edge.geometry)
```

## `CommandDefinition`

Describes a UI command button.

Created with:

```python
ui.commandDefinitions.addButtonDefinition(...)
```

## `Command`

A live command instance created when a user clicks a command definition.

Attach handlers to:

- `execute`
- `inputChanged`
- `validateInputs`
- `destroy`

## `Palette`

Persistent HTML UI panel. Useful for future chat/control interface.

JavaScript talks to Python through `adsk.fusionSendData`; Python talks to Fusion through the API.

## References

- Autodesk, Fusion API reference manual: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/ReferenceManual_UM.htm
- Autodesk, Fusion API object model PDF: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/ExtraFiles/Fusion.pdf
- Autodesk, Getting Started with Fusion API: https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-D93DF10F-4209-4073-A2A0-4FA8788C8709

