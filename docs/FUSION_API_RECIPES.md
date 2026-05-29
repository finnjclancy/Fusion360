# Fusion API Recipes for Agents

These recipes are for agents modifying `FusionLiveModel`. They are intentionally practical: use them as starting points, then check Autodesk's API pages when adding a feature family that is not already used in this project.

## Baseline Imports

```python
import json
import os
import traceback

import adsk.core
import adsk.fusion
```

## Get the Active Design

```python
def _active_design():
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    if design:
        return design

    app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    return adsk.fusion.Design.cast(app.activeProduct)
```

Use this when a model request should work even if no design document is active.

## Convert Millimeters to Fusion Internal Units

```python
def _mm(value):
    return float(value) / 10.0
```

Fusion raw length values are centimeters. A value of `2` passed to a length input means `2 cm`, not `2 mm`.

## Create a ValueInput

Calculated value:

```python
height = adsk.core.ValueInput.createByReal(_mm(height_mm))
```

User-facing expression:

```python
height = adsk.core.ValueInput.createByString(f'{height_mm} mm')
```

Prefer strings for user parameters and command inputs. Prefer real values for calculated geometry.

## Build in a Safe Component

Some documents cannot contain child components. Use this pattern instead of assuming `occurrences.addNewComponent` will work.

```python
def _create_component(root_component, component_name):
    transform = adsk.core.Matrix3D.create()
    occurrence = root_component.occurrences.addNewComponent(transform)
    occurrence.name = component_name
    occurrence.component.name = component_name
    return occurrence.component


def _model_component(root_component, component_name):
    try:
        return _create_component(root_component, component_name)
    except RuntimeError:
        return root_component
```

Do not rename the root component in the fallback path.

## Delete Generated Geometry by Name

```python
def _delete_named_items(component, names):
    for body_index in range(component.bRepBodies.count - 1, -1, -1):
        body = component.bRepBodies.item(body_index)
        if body.name in names:
            body.deleteMe()

    for sketch_index in range(component.sketches.count - 1, -1, -1):
        sketch = component.sketches.item(sketch_index)
        if sketch.name in names:
            sketch.deleteMe()
```

Delete from the end of collections to avoid index shifting.

## Draw a Centered Rectangle

```python
def _draw_centered_rectangle(sketch, length_cm, width_cm):
    corner_a = adsk.core.Point3D.create(-length_cm / 2, -width_cm / 2, 0)
    corner_b = adsk.core.Point3D.create(length_cm / 2, width_cm / 2, 0)
    sketch.sketchCurves.sketchLines.addTwoPointRectangle(corner_a, corner_b)
```

Use this for blocks, plates, brackets, bases, panels, and any rectangular sketch profile.

## Extrude a Profile into a New Body

```python
def _extrude_profile(component, profile, height_cm):
    extrudes = component.features.extrudeFeatures
    extrude_input = extrudes.createInput(
        profile,
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
    )
    extrude_input.setDistanceExtent(False, adsk.core.ValueInput.createByReal(height_cm))
    extrude = extrudes.add(extrude_input)
    return extrude.bodies.item(0)
```

Use `NewBodyFeatureOperation` for independent solids. Use join/cut/intersect operations only when the request clearly needs modifying an existing body.

## Create a Basic Rounded Block

```python
design = _active_design()
root = design.rootComponent
component = _model_component(root, 'Fusion Live Model')

sketch = component.sketches.add(component.xYConstructionPlane)
sketch.name = 'Fusion Live Base Sketch'

_draw_centered_rectangle(sketch, _mm(80), _mm(40))
body = _extrude_profile(component, sketch.profiles.item(0), _mm(12))
body.name = 'Rounded block'
_fillet_body(component, body, _mm(4))
```

This is the current model pattern.

## Fillet Edges

Current working project pattern:

```python
def _fillet_body(component, body, radius_cm):
    if radius_cm <= 0:
        return

    edge_collection = adsk.core.ObjectCollection.create()
    for edge_index in range(body.edges.count):
        edge_collection.add(body.edges.item(edge_index))

    fillet_input = component.features.filletFeatures.createInput()
    fillet_input.addConstantRadiusEdgeSet(
        edge_collection,
        adsk.core.ValueInput.createByReal(radius_cm),
        True,
    )
    component.features.filletFeatures.add(fillet_input)
```

Note: Autodesk marks `FilletFeatureInput.addConstantRadiusEdgeSet` as retired and recommends newer edge-set input methods. The current code uses the older method because it is simple and works in this add-in. For major fillet work, check the current fillet docs and update this helper.

## Apply a Simple Color Appearance

```python
def _appearance_from_spec(design, spec):
    style = spec.get('style', {})
    color = style.get('color', {})

    red = int(color.get('red', 42))
    green = int(color.get('green', 126))
    blue = int(color.get('blue', 210))
    alpha = int(color.get('alpha', 255))

    appearance_name = style.get('appearance_name', 'Fusion Live Color')
    appearance = design.appearances.itemByName(appearance_name)
    if not appearance:
        app = adsk.core.Application.get()
        library = app.materialLibraries.itemByName('Fusion 360 Appearance Library')
        if not library:
            raise RuntimeError('Fusion 360 Appearance Library was not found. Search available material libraries before calling appearances.itemByName.')
        source = library.appearances.itemByName('Paint - Enamel Glossy (White)')
        appearance = design.appearances.addByCopy(source, appearance_name)

    color_property = appearance.appearanceProperties.itemByName('Color')
    if color_property:
        color_property.value = adsk.core.Color.create(red, green, blue, alpha)

    return appearance
```

Then:

```python
body.appearance = _appearance_from_spec(design, spec)
```

For metal, plastic, glass, rubber, wood, or textured materials, copy a more suitable base appearance from a Fusion appearance library and then customize it.

Important: do not assume the exact library name `Fusion 360 Appearance Library` is available in every install/session. Production code should scan `app.materialLibraries` for a usable source appearance and skip styling gracefully if none exists.

## Add User Parameters

Use this when the user wants dimensions visible in Fusion's parameter dialog.

```python
def _upsert_user_parameter(design, name, expression, units, comment=''):
    parameters = design.userParameters
    existing = parameters.itemByName(name)
    if existing:
        existing.expression = expression
        existing.comment = comment
        return existing

    return parameters.add(
        name,
        adsk.core.ValueInput.createByString(expression),
        units,
        comment,
    )
```

Example:

```python
_upsert_user_parameter(design, 'live_length', '80 mm', 'mm', 'FusionLiveModel length')
```

Use parameters only when they add value. JSON is simpler for chat-driven rebuilds.

## Add a Command Button

Command buttons belong in `commands/<command_name>/entry.py`.

Core pattern:

```python
cmd_def = ui.commandDefinitions.addButtonDefinition(
    CMD_ID,
    CMD_NAME,
    CMD_DESCRIPTION,
    ICON_FOLDER,
)
futil.add_handler(cmd_def.commandCreated, command_created)

workspace = ui.workspaces.itemById('FusionSolidEnvironment')
panel = workspace.toolbarPanels.itemById('SolidScriptsAddinsPanel')
control = panel.controls.addCommand(cmd_def, 'ScriptsManagerCommand', False)
control.isPromoted = True
```

Then:

```python
def command_created(args):
    futil.add_handler(args.command.execute, command_execute, local_handlers=local_handlers)


def command_execute(args):
    summary = model_builder.build_from_spec()
    ui.messageBox(summary, 'Fusion Live Model')
```

If a command creates inputs, define them in `command_created` and read them in `command_execute`.

## Add Command Inputs

Use command inputs when the user wants Fusion-native controls instead of chat/spec edits.

Examples of useful input types:

- `ValueCommandInput` for dimensions.
- `StringValueCommandInput` for names.
- `BoolValueCommandInput` for toggles.
- `DropDownCommandInput` for mode/style selection.
- `SelectionCommandInput` for selecting faces, edges, bodies, or sketches.
- `TableCommandInput` for repeated items like hole lists.
- `TabCommandInput` and `GroupCommandInput` for organized dialogs.

For this project, command inputs are secondary to chat-driven JSON edits.

## Build a Palette Later

A palette can provide an in-Fusion side panel. Use it for chat, status, preview settings, and persistent controls.

Architecture:

```text
HTML/JS palette
  sends action + JSON data
Python palette_incoming handler
  validates action
  updates JSON or calls model builder
Fusion API
  rebuilds geometry
Python returns status to HTML
```

Do not try to call `adsk` APIs from JavaScript. Palette JavaScript communicates with Python; Python talks to Fusion.

## Shape Request Patterns

### "Make a block / plate / base"

Use rectangle sketch plus extrude. Add fillets/chamfers after extrude.

Spec fields:

```json
{
  "shape": "rounded_block",
  "length_mm": 80,
  "width_mm": 40,
  "height_mm": 12,
  "fillet_radius_mm": 4
}
```

### "Make a cylinder / disk / peg"

Use circle sketch plus extrude.

Implementation outline:

```python
sketch = component.sketches.add(component.xYConstructionPlane)
center = adsk.core.Point3D.create(0, 0, 0)
sketch.sketchCurves.sketchCircles.addByCenterRadius(center, _mm(diameter_mm) / 2)
body = _extrude_profile(component, sketch.profiles.item(0), _mm(height_mm))
```

### "Add a hole"

Good options:

- Sketch a circle on a face or construction plane and create a cut extrude.
- Use Fusion's hole feature API for more parametric hole types.

For simple through holes, sketch-plus-cut is usually easier for agents to reason about.

### "Make it hollow"

Use shell feature logic. Add a `wall_thickness_mm` field to `design_spec.json`. Choose which face to remove if the user asks for an open box; otherwise shell all sides if appropriate.

### "Round only some edges"

Do not fillet all body edges. Identify edges by geometry:

- Top perimeter edges.
- Vertical edges.
- Edges around a selected face.
- Edges matching direction or bounding box position.

For anything ambiguous, implement named selection logic or ask the user which edges.

### "Change color/material"

If the user asks for color, update `style.color`.

If the user asks for engineering material like aluminum, steel, plastic, rubber, or wood:

1. Apply a physical material if mass/engineering properties matter.
2. Apply an appearance if visible styling matters.

Appearance only is enough for "make it blue", "make it glossy", or "make it look metallic."

## Request-to-Code Checklist

Before editing:

- Is this just dimensions/style? Edit `design_spec.json`.
- Does it need new geometry? Add fields to `design_spec.json` and code to `model_builder.py`.
- Does it need Fusion UI controls? Edit/add command modules.
- Does it need a persistent panel? Use a palette.
- Does it need selected geometry? Add `SelectionCommandInput` or document the expected selected object.

After editing:

```zsh
python3 -m py_compile /Users/finn/Documents/Projects/Scripts/FusionLiveModel/model_builder.py
python3 -m json.tool /Users/finn/Documents/Projects/Scripts/FusionLiveModel/design_spec.json
```

Then tell Finn:

- Click `Rebuild Live Model` if only model/spec changed.
- Toggle add-in off/on if command registration changed.
- Restart Fusion if the add-in list or manifest changed.

## Source Links

- Scripts/add-ins: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/WritingDebugging_UM.htm
- Commands: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/Commands_UM.htm
- Command inputs: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/CommandInputs_UM.htm
- Palettes: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/Palettes_UM.htm
- Units: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/Units_UM.htm
- ValueInput: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/ValueInput.htm
- Sketch rectangle: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/SketchLines_addTwoPointRectangle.htm
- Extrude input: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/ExtrudeFeatures_createInput.htm
- Fillets: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/FilletFeatures_add.htm
- Appearances: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/Appearances_addByCopy.htm
- User parameters: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/UserParameters_add.htm
