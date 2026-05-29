# Fusion Agent Guide

This document teaches AI coding agents how to work on Finn's Fusion add-in. It combines the current local project structure with Autodesk's official Fusion API documentation.

## Goal

The add-in should let Finn work conversationally:

1. Finn describes a model change in chat.
2. An agent edits `design_spec.json` and/or `model_builder.py`.
3. Finn clicks `Rebuild Live Model` in Fusion.
4. Fusion rebuilds the active design from the updated spec/code.

The first implementation is intentionally simple: a Python add-in with one command button. A future version can add an HTML palette for an in-Fusion chat panel, but the reliable base workflow is file edit plus manual rebuild.

## Current File Map

```text
FusionLiveModel/
  AGENTS.md
  FusionLiveModel.py
  FusionLiveModel.manifest
  config.py
  design_spec.json
  model_builder.py
  commands/
    __init__.py
    commandDialog/
      entry.py
      resources/
    paletteShow/
      entry.py        # inactive template sample
    paletteSend/
      entry.py        # inactive template sample
  lib/
    fusionAddInUtils/
  docs/
    FUSION_AGENT_GUIDE.md
    FUSION_API_RECIPES.md
    FUSION_SPEC_SCHEMA.md
    REQUEST_PLAYBOOK.md
    SKETCH_CONSTRAINTS_AND_DIMENSIONS.md
    FEATURE_RECIPES_DEEP.md
    GEOMETRY_TARGETING.md
    PARAMETRIC_MODELING.md
    API_OBJECT_GLOSSARY.md
    EXPORT_AND_MANUFACTURING.md
    ERROR_COOKBOOK.md
    PALETTE_LIVE_WORKFLOW.md
    DESIGN_INTENT_RULES.md
    SOURCE_RELIABILITY.md
```

Important files:

- `FusionLiveModel.py` is Fusion's add-in entry point. Fusion calls `run(context)` and `stop(context)`.
- `commands/__init__.py` decides which command modules are active.
- `commands/commandDialog/entry.py` creates the `Rebuild Live Model` toolbar button.
- `model_builder.py` contains the modeling logic.
- `design_spec.json` is the editable model specification.
- `docs/FUSION_SPEC_SCHEMA.md` defines how future JSON fields should be named and structured.
- `docs/REQUEST_PLAYBOOK.md` maps Finn's natural-language requests to code/spec changes.
- The other files in `docs/` cover sketch constraints, feature choices, geometry targeting, parameters, exports, errors, palettes, and design intent.
- `docs/SOURCE_RELIABILITY.md` separates official Autodesk API facts from project conventions and CAD guidance.

## Scripts vs Add-Ins

Fusion supports scripts and add-ins. A script usually runs once and ends. An add-in can remain loaded, register toolbar buttons, respond to UI events, and optionally run on startup.

For Finn's workflow, use an add-in because:

- It can expose a persistent `Rebuild Live Model` command.
- It can later expose a palette/chat panel.
- It can reload modeling code repeatedly while Fusion stays open.

Fusion add-ins are folders containing a `.py` entry file, a `.manifest`, icons/resources, and any support modules. The add-in is created or linked through `Utilities > Scripts and Add-Ins`.

## Fusion API Mental Model

Most modeling code follows this object path:

```text
Application
  UserInterface
  activeProduct -> Design
    rootComponent -> Component
      sketches
      features
      bRepBodies
      occurrences
```

Typical Python imports:

```python
import adsk.core
import adsk.fusion
```

Typical active design lookup:

```python
app = adsk.core.Application.get()
design = adsk.fusion.Design.cast(app.activeProduct)
root = design.rootComponent
```

The root component is always important. Component creation can fail in some document types, so robust code should be able to build directly in the root component.

## Units

Fusion's raw API distance values are in centimeters. Finn should express dimensions in millimeters in `design_spec.json`, and model code should convert them:

```python
def _mm(value):
    return float(value) / 10.0
```

Use `ValueInput.createByReal(value_cm)` when the code has already calculated the number in internal units.

Use `ValueInput.createByString("12 mm")` when the user-facing expression should be preserved or when a parameter should behave like a value typed into Fusion's UI.

This matters for extrudes, fillets, holes, offsets, sketch dimensions, user parameters, and most feature inputs.

## Rebuild Strategy

This project rebuilds generated geometry rather than trying to edit every feature in place.

Current pattern:

1. Read `design_spec.json`.
2. Get the active design.
3. Delete previously generated bodies/sketches by stable names.
4. Try to create a named component.
5. If Fusion refuses because the document can only contain one component, use the root component.
6. Create sketches.
7. Create features.
8. Apply appearance.
9. Return a short message for Fusion's message box.

Stable names are critical. Generated bodies and sketches must have known names so a rebuild deletes only generated objects and does not destroy unrelated user work.

## Drawing and Modeling Concepts

### Sketches

A sketch is 2D geometry on a plane. Common sketch targets:

- `component.xYConstructionPlane`
- `component.xZConstructionPlane`
- `component.yZConstructionPlane`
- planar model faces

Common sketch geometry:

- Lines: `sketch.sketchCurves.sketchLines`
- Rectangles: `addTwoPointRectangle(...)`
- Circles: `sketch.sketchCurves.sketchCircles`
- Arcs: `sketch.sketchCurves.sketchArcs`
- Text: `SketchText`

Closed sketch loops create `Profile` objects. Solid features often consume profiles.

### Features

Features turn sketches, faces, or bodies into solid/surface changes.

Common feature families:

- Extrude: turn a profile into a prism or cut.
- Revolve: rotate a profile around an axis.
- Sweep: move a profile along a path.
- Loft: blend between multiple profiles.
- Fillet: round edges.
- Chamfer: bevel edges.
- Shell: hollow a body.
- Hole: create parametric holes.
- Pattern: duplicate bodies/features/sketch geometry.
- Combine: join, cut, or intersect bodies.
- Mirror: reflect bodies/features.

When a request is shape-driven, prefer sketches plus features over low-level BRep editing. It is easier to understand, rebuild, and teach.

## Styling and Materials

Fusion distinguishes physical materials from appearances:

- Physical materials affect engineering properties and default color.
- Appearances affect visible color/texture and can override material color.

This project currently uses appearances for color. The code copies a base appearance from the Fusion appearance library into the design and changes its color property.

Use body-level appearance for simple styling:

```python
body.appearance = appearance
```

Use face-level appearances only when a request needs different colors on different faces.

## Parameters

For reusable parametric models, prefer Fusion user parameters when dimensions should be visible/editable in Fusion's parameter dialog.

Good candidates:

- `length`
- `width`
- `height`
- `wall_thickness`
- `hole_diameter`
- `fillet_radius`

For this project, JSON is the current source of truth. Add Fusion user parameters only when the user asks for Fusion-native parametric controls or when a model becomes complex enough to benefit from expressions.

## Commands and UI Events

The active button lives in `commands/commandDialog/entry.py`.

Command registration flow:

1. `start()` creates a `ButtonDefinition` with `ui.commandDefinitions.addButtonDefinition(...)`.
2. It attaches `command_created` to `cmd_def.commandCreated`.
3. It adds the command to a toolbar panel with `panel.controls.addCommand(...)`.
4. When the user clicks the button, Fusion fires `command_created`.
5. `command_created` attaches `command_execute`.
6. `command_execute` reloads `model_builder.py` and calls `build_from_spec()`.

Keep references to event handlers. Python event handlers can be garbage collected if the add-in does not hold references. The generated `fusionAddInUtils` helper handles this via `futil.add_handler(...)`.

## Palettes and Future Chat UI

Fusion palettes are HTML panels. They can remain visible while the user interacts with Fusion, which makes them the right base for a future chat-like interface.

Important limitation: JavaScript inside a palette does not directly call the Fusion API. It sends messages to the Python add-in; Python receives those messages and calls the Fusion API.

A future palette architecture should be:

```text
HTML palette UI
  -> JavaScript sends message to Python
  -> Python validates request/spec
  -> Python updates design_spec.json or calls builder
  -> Python rebuilds model
  -> Python returns status to palette
```

For now, keep chat in Codex and use the toolbar rebuild button.

## Request Interpretation

Map user wording to code changes like this:

| User request | Preferred implementation |
| --- | --- |
| "Make it longer/taller/wider" | Edit `design_spec.json` dimensions. |
| "Make it red/blue/metal/transparent" | Edit `style` in `design_spec.json`; add appearance logic if needed. |
| "Round the corners more" | Edit `fillet_radius_mm`. |
| "Add a hole" | Add a hole spec and implement hole/extrude-cut logic in `model_builder.py`. |
| "Make it hollow" | Add shell feature logic and shell thickness spec. |
| "Make a cylinder/tube/gear/bracket" | Add a new shape mode or builder function. |
| "Add controls in Fusion" | Add command inputs or a palette. |
| "Make it update automatically" | Consider a palette or timer/file watcher, but keep manual rebuild as fallback. |

## Safety Rules for Agents

- Do not delete user-created model geometry unless it is clearly generated by this add-in.
- Prefer naming generated objects and deleting by name.
- Catch Fusion-specific runtime errors and show tracebacks during development.
- Keep functions small: load spec, create sketch, create feature, apply style.
- Do not introduce dependencies that Fusion's embedded Python cannot import.
- Avoid OS-specific code unless guarded for macOS.
- Avoid long-running work inside command events; Fusion UI can feel frozen.
- If a command UI file changes, tell Finn to toggle the add-in off/on.
- If only `model_builder.py` or `design_spec.json` changes, Finn can usually click `Rebuild Live Model` immediately.

## Troubleshooting

### Button does not appear

- Confirm `FusionLiveModel` is running in `Utilities > Scripts and Add-Ins > Add-Ins`.
- Toggle the add-in off and on.
- Restart Fusion if command registration changed.
- Check `commands/__init__.py` includes the intended command module.
- Check Python syntax with `python3 -m py_compile`.

### "Part Design documents can only contain one component"

The document does not allow child components. Build in `design.rootComponent` instead of creating an occurrence.

### "root component name cannot be changed"

Some document types prevent renaming the root component. Do not rename it; name generated bodies/sketches instead.

### Unit values are 10x wrong

The model probably passed millimeters to `createByReal`. Convert mm to cm first, or use `createByString("value mm")`.

### Geometry is duplicated

The rebuild cleanup did not delete all generated objects. Add stable names for generated sketches, bodies, features, or components and delete those names before rebuilding.

### Appearance does not change

Appearance property names can vary by base appearance. Log available properties or choose a known base appearance. Body-level appearance may be overridden by face-level appearance.

## Official Sources

- Autodesk, Creating and managing scripts/add-ins: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/WritingDebugging_UM.htm
- Autodesk, Commands user manual: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/Commands_UM.htm
- Autodesk, Command definitions: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/CommandDefinitions.htm
- Autodesk, `addButtonDefinition`: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/CommandDefinitions_addButtonDefinition.htm
- Autodesk, `commandCreated` event: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/CommandDefinition_commandCreated.htm
- Autodesk, `execute` event: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/Command_execute.htm
- Autodesk, Command inputs: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/CommandInputs_UM.htm
- Autodesk, Palettes: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/Palettes_UM.htm
- Autodesk, Units: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/Units_UM.htm
- Autodesk, `ValueInput.createByReal`: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/ValueInput_createByReal.htm
- Autodesk, `Design.rootComponent`: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/Design_rootComponent.htm
- Autodesk, `SketchLines.addTwoPointRectangle`: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/SketchLines_addTwoPointRectangle.htm
- Autodesk, `ExtrudeFeatures.createInput`: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/ExtrudeFeatures_createInput.htm
- Autodesk, Extrude feature sample: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/ExtrudeFeatureSample_Sample.htm
- Autodesk, Fillet feature docs: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/FilletFeatures_add.htm
- Autodesk, Appearances: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/Appearances_addByCopy.htm
- Autodesk, physical materials and appearances: https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-55EC2C42-60E1-48C7-B802-D2AA7AB6F0CB
- Autodesk, User parameters: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/UserParameters_add.htm
