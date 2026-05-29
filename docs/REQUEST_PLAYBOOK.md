# Request Playbook for Coding Agents

This playbook explains how to turn Finn's natural language requests into precise changes in this Fusion add-in.

## Default Loop

1. Read `AGENTS.md`.
2. Read `design_spec.json`.
3. Read the relevant parts of `model_builder.py`.
4. Decide whether the request is a spec-only change or a code change.
5. Edit the smallest set of files.
6. Run syntax and JSON checks.
7. Tell Finn exactly what changed and whether to click `Rebuild Live Model` or restart/toggle the add-in.

## First Classification

Classify every user request into one of these buckets:

| Bucket | Examples | File to edit |
| --- | --- | --- |
| Dimension change | "make it longer", "20 mm tall" | `design_spec.json` |
| Appearance change | "make it red", "matte black" | `design_spec.json`, maybe `model_builder.py` |
| Existing feature change | "bigger fillet", "smaller holes" | `design_spec.json` |
| New feature | "add four holes", "add a slot" | `design_spec.json` and `model_builder.py` |
| New base shape | "make it a tube", "make a bracket" | `design_spec.json` and `model_builder.py` |
| UI workflow | "add a control", "make a panel" | command/palette files |
| Repo/docs task | "push this", "document this" | Git/docs files |

When unsure, prefer a simple spec change if it can satisfy the request.

## How to Interpret Common Words

| User wording | CAD meaning |
| --- | --- |
| longer | increase X dimension / `length_mm` |
| wider | increase Y dimension / `width_mm` |
| taller / thicker | increase Z dimension / `height_mm` |
| rounded corners | fillet vertical and/or all body edges |
| sharper | reduce fillet radius or use chamfer |
| bevel | chamfer edges |
| hollow | shell body |
| hole through it | cut extrude through all |
| mounting holes | usually corner holes with margin from edges |
| slot | obround cut with length and width |
| raised text | emboss / join text |
| engraved text | cut text into top face |
| metal | metallic appearance, maybe physical material |
| transparent | transparent appearance with opacity |
| centered | position `{ "x_mm": 0, "y_mm": 0 }` |
| on top | sketch/use top face or highest Z plane |
| flush | same plane/face, no offset |

## Coordinate Convention

Unless the user says otherwise:

- X = length direction.
- Y = width direction.
- Z = height direction.
- Origin = center of the base object.
- Base sketch is centered on the XY plane.
- Positive Z is upward.

For a rectangular base:

- Left/right edges are at `x = +/- length_mm / 2`.
- Front/back edges are at `y = +/- width_mm / 2`.
- Top face is at `z = height_mm`.

## Default Assumptions

Use these defaults when the user omits details:

- Units: millimeters.
- Base shape: rounded rectangular block.
- Holes: through holes cut normal to the top face.
- Hole placement: centered unless user says corner/mounting.
- Corner mounting hole margin: 8 mm or 15 percent of the smaller dimension, whichever is smaller.
- Fillet target: all body edges for simple blocks.
- Color: appearance only, not physical material, unless engineering material matters.
- Rebuild: delete and recreate generated add-in geometry.

State important assumptions in the final response, especially for hole placement and feature orientation.

## Spec-Only Examples

### User says: "Make it 120 long, 50 wide, 10 tall"

Change:

```json
{
  "length_mm": 120,
  "width_mm": 50,
  "height_mm": 10
}
```

No Python code change needed.

### User says: "Make it red with more rounded corners"

Change:

```json
{
  "fillet_radius_mm": 8,
  "style": {
    "appearance_name": "Fusion Live Red",
    "color": {
      "red": 220,
      "green": 40,
      "blue": 40,
      "alpha": 255
    }
  }
}
```

No Python code change needed unless the requested finish/material is not implemented.

## Code Change Examples

### Add One Center Hole

Spec:

```json
{
  "features": [
    {
      "type": "through_hole",
      "name": "center hole",
      "diameter_mm": 8,
      "position": { "x_mm": 0, "y_mm": 0 }
    }
  ]
}
```

Implementation approach:

1. After creating the body, create a new sketch on the XY plane or top face.
2. Draw a circle at `position`.
3. Cut extrude through the body.
4. Name the sketch and feature with a generated prefix.
5. Add the names to cleanup logic.

### Add Four Mounting Holes

Spec:

```json
{
  "features": [
    {
      "type": "corner_holes",
      "name": "mounting holes",
      "diameter_mm": 4,
      "margin_mm": 8
    }
  ]
}
```

Calculate positions:

```text
x = +/- (length_mm / 2 - margin_mm)
y = +/- (width_mm / 2 - margin_mm)
```

Then sketch four circles and cut them through the body.

### Make a Tube

Spec:

```json
{
  "shape": {
    "type": "tube",
    "outer_diameter_mm": 40,
    "inner_diameter_mm": 28,
    "height_mm": 60
  }
}
```

Implementation approach:

1. Sketch two concentric circles.
2. Extrude the annular profile.
3. Apply style.
4. Optional: fillet top/bottom rim edges.

### Make an Open Box

Spec:

```json
{
  "shape": {
    "type": "open_box",
    "length_mm": 100,
    "width_mm": 60,
    "height_mm": 40,
    "wall_thickness_mm": 3,
    "fillet_radius_mm": 4
  }
}
```

Implementation choices:

- Simple route: create outer block, shell from top face.
- More explicit route: sketch wall profiles and extrude.

Use shell when possible, but face selection can be brittle. If shell face selection is hard, use explicit sketch geometry.

## When to Ask for Clarification

Ask only if the request cannot be implemented safely with a reasonable assumption.

Ask for clarification when:

- The user wants a feature on a specific face but does not identify which face.
- The user references an external object/image/file that is not available.
- The user wants precise fit with real hardware but does not provide dimensions.
- A destructive operation could delete user-created geometry.
- The model needs thread standards, tolerances, or manufacturing constraints.

Otherwise, make a conservative assumption and proceed.

## Validation Commands

Run after Python changes:

```zsh
python3 -m py_compile /Users/finn/Documents/Projects/Scripts/FusionLiveModel/FusionLiveModel.py /Users/finn/Documents/Projects/Scripts/FusionLiveModel/config.py /Users/finn/Documents/Projects/Scripts/FusionLiveModel/commands/__init__.py /Users/finn/Documents/Projects/Scripts/FusionLiveModel/commands/commandDialog/entry.py /Users/finn/Documents/Projects/Scripts/FusionLiveModel/model_builder.py
```

Run after JSON changes:

```zsh
python3 -m json.tool /Users/finn/Documents/Projects/Scripts/FusionLiveModel/design_spec.json
python3 -m json.tool /Users/finn/Documents/Projects/Scripts/FusionLiveModel/FusionLiveModel.manifest
```

Run before Git commits:

```zsh
git status --short --branch
git diff --stat
```

## Final Response Pattern

Keep the final response short and actionable:

```text
Updated the model to add four 4 mm mounting holes, 8 mm from each corner.

Changed:
- design_spec.json
- model_builder.py

Validation passed: Python compiles and JSON is valid.

In Fusion, click Rebuild Live Model.
```

If command registration changed:

```text
Toggle the FusionLiveModel add-in off and on, then use the new button.
```

If only builder/spec changed:

```text
No restart needed; click Rebuild Live Model.
```

## GitHub Workflow

This repository is public:

```text
https://github.com/finnjclancy/Fusion360
```

Local folder:

```text
/Users/finn/Documents/Projects/Scripts/FusionLiveModel
```

When the user asks to save/publish changes:

1. Check `git status --short --branch`.
2. Stage only relevant files.
3. Commit with a concise message.
4. Push to `origin/main` unless the user asks for a branch/PR.

