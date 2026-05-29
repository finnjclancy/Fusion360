# FusionLiveModel Spec Schema

This document defines how agents should represent Finn's model requests in `design_spec.json`. The schema is intentionally human-readable JSON, not a strict validator yet. Treat it as the contract between chat requests and `model_builder.py`.

## Core Principles

- Keep measurements in millimeters.
- Keep angles in degrees.
- Keep colors as 0-255 RGBA values.
- Prefer additive fields over changing old meanings.
- Preserve backward compatibility with the current simple block spec.
- Use explicit names for generated items so rebuild cleanup is safe.
- Do not store Fusion internal centimeter values in JSON.
- Do not store Python expressions in JSON unless the project later adds a safe expression parser.

## Current Minimal Spec

```json
{
  "component_name": "Fusion Live Model",
  "body_name": "Rounded block",
  "length_mm": 80,
  "width_mm": 40,
  "height_mm": 12,
  "fillet_radius_mm": 4,
  "style": {
    "appearance_name": "Fusion Live Blue",
    "color": {
      "red": 42,
      "green": 126,
      "blue": 210,
      "alpha": 255
    }
  }
}
```

Agents must keep this format working.

## Recommended Expanded Spec Shape

When the model becomes more complex, evolve toward this shape:

```json
{
  "schema_version": 1,
  "model_name": "Fusion Live Model",
  "rebuild": {
    "delete_generated": true,
    "generated_prefix": "FLM_"
  },
  "units": {
    "length": "mm",
    "angle": "deg"
  },
  "shape": {
    "type": "rounded_block",
    "length_mm": 80,
    "width_mm": 40,
    "height_mm": 12,
    "fillet_radius_mm": 4
  },
  "features": [],
  "style": {
    "appearance_name": "Fusion Live Blue",
    "color": {
      "red": 42,
      "green": 126,
      "blue": 210,
      "alpha": 255
    },
    "finish": "glossy"
  }
}
```

Use this expanded structure when adding multiple shapes, repeated features, named operations, or user-editable feature lists.

## Naming Fields

Use these fields consistently:

- `model_name`: overall design or generated component name.
- `component_name`: backward-compatible generated component name.
- `body_name`: generated primary body name.
- `generated_prefix`: prefix for generated bodies/sketches/features, recommended `FLM_`.
- `name`: stable human-readable name for a feature, body, sketch, or operation.

Do not rename Fusion's root component. Some document types reject it.

## Shape Types

Use `shape.type` when more than one base shape exists.

Recommended values:

- `rounded_block`
- `box`
- `open_box`
- `cylinder`
- `tube`
- `bracket`
- `plate`
- `custom_sketch`

Keep the old top-level fields working for `rounded_block`.

## Dimensions

Recommended dimension naming:

- `length_mm`
- `width_mm`
- `height_mm`
- `diameter_mm`
- `outer_diameter_mm`
- `inner_diameter_mm`
- `radius_mm`
- `wall_thickness_mm`
- `fillet_radius_mm`
- `chamfer_distance_mm`
- `offset_mm`
- `depth_mm`
- `spacing_mm`
- `margin_mm`

Avoid ambiguous names like `size`, `amount`, `thickness` without units.

## Positions

Use a clear coordinate object:

```json
{
  "x_mm": 0,
  "y_mm": 0,
  "z_mm": 0
}
```

For 2D sketch placement, use:

```json
{
  "x_mm": 20,
  "y_mm": -10
}
```

For repeated locations:

```json
{
  "points": [
    { "x_mm": -20, "y_mm": 0 },
    { "x_mm": 20, "y_mm": 0 }
  ]
}
```

## Feature List

When the user asks for added geometry or operations, use a `features` array:

```json
{
  "features": [
    {
      "type": "through_hole",
      "name": "center mounting hole",
      "diameter_mm": 8,
      "position": { "x_mm": 0, "y_mm": 0 }
    },
    {
      "type": "corner_holes",
      "name": "four mounting holes",
      "diameter_mm": 4,
      "margin_mm": 8
    }
  ]
}
```

Recommended feature `type` values:

- `through_hole`
- `blind_hole`
- `counterbore_hole`
- `countersink_hole`
- `corner_holes`
- `slot`
- `pocket`
- `boss`
- `rib`
- `fillet`
- `chamfer`
- `shell`
- `pattern`
- `mirror`
- `text_emboss`
- `text_engrave`

## Holes

Simple through hole:

```json
{
  "type": "through_hole",
  "name": "center hole",
  "diameter_mm": 8,
  "position": { "x_mm": 0, "y_mm": 0 }
}
```

Corner holes:

```json
{
  "type": "corner_holes",
  "name": "mounting holes",
  "diameter_mm": 4,
  "margin_mm": 7
}
```

For holes, agents should usually sketch circles on the base sketch plane and cut through the body. Use Fusion's hole feature only when the user needs hole standards, counterbores, countersinks, or thread data.

## Slots

```json
{
  "type": "slot",
  "name": "mounting slot",
  "length_mm": 24,
  "width_mm": 6,
  "position": { "x_mm": 0, "y_mm": 0 },
  "angle_deg": 0,
  "operation": "cut"
}
```

Slots can be modeled as two circles plus connecting lines in a sketch, then cut extruded.

## Text

Embossed text:

```json
{
  "type": "text_emboss",
  "name": "logo text",
  "text": "FINN",
  "height_mm": 8,
  "depth_mm": 1,
  "position": { "x_mm": 0, "y_mm": 0 },
  "angle_deg": 0
}
```

Engraved text:

```json
{
  "type": "text_engrave",
  "name": "label",
  "text": "REV A",
  "height_mm": 4,
  "depth_mm": 0.5,
  "position": { "x_mm": 0, "y_mm": -12 },
  "angle_deg": 0
}
```

## Style

Basic color:

```json
{
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

Suggested optional style fields:

- `finish`: `matte`, `satin`, `glossy`, `metallic`, `transparent`
- `material`: `aluminum`, `steel`, `plastic`, `rubber`, `wood`
- `opacity`: 0-1 if transparency support is implemented

Only add behavior for style fields that `model_builder.py` actually implements.

## Operations

Use these operation strings when a feature changes a body:

- `new_body`
- `join`
- `cut`
- `intersect`

Map them to Fusion's `FeatureOperations` constants in Python.

## Agent Decision Rules

1. If the request only changes numbers or color, edit the existing fields.
2. If the request adds one simple repeatable feature, add a `features` entry and implement that type.
3. If the request changes the whole base object, add or change `shape.type`.
4. If the request asks for a UI control, update command inputs or palette code, not only JSON.
5. If the request is ambiguous, make a conservative assumption and state it in the final response.

## Backward Compatibility

`model_builder.py` should continue accepting the current top-level fields:

- `component_name`
- `body_name`
- `length_mm`
- `width_mm`
- `height_mm`
- `fillet_radius_mm`
- `style`

When adding `shape`, read from `shape` first and fall back to top-level fields.

## Validation Expectations

Agents should validate obvious invalid values in Python before calling Fusion APIs:

- Lengths must be positive.
- Fillet radius must be non-negative.
- Hole diameters must be positive and smaller than the relevant body dimension.
- Wall thickness must be positive and smaller than half of the smallest dimension.
- RGBA color channels must be integers from 0 to 255.
- Angles should be numeric.

Raise `ValueError` with a clear message if the spec is invalid. The command wrapper shows tracebacks in Fusion during development.

