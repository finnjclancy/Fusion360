# Parametric Modeling

This add-in currently rebuilds from JSON. Parametric Fusion modeling is the next layer: expose key dimensions as Fusion user parameters and connect sketches/features to those parameters.

## JSON vs Fusion Parameters

Use JSON when:

- Chat is the source of truth.
- The add-in rebuilds geometry.
- The model is simple.
- Finn wants fast iteration.

Use Fusion user parameters when:

- Finn wants to edit dimensions inside Fusion.
- Dimensions should appear in the Change Parameters dialog.
- Feature dimensions should reference named expressions.
- The model should remain editable without running Codex.

## User Parameter Pattern

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
_upsert_user_parameter(design, 'flm_length', '80 mm', 'mm', 'FusionLiveModel length')
```

## Naming Parameters

Use a prefix so parameters are easy to identify:

- `flm_length`
- `flm_width`
- `flm_height`
- `flm_fillet_radius`
- `flm_wall_thickness`
- `flm_hole_diameter`
- `flm_hole_margin`

Avoid generic names like `length` in shared designs because they can collide with user parameters.

## Expressions

Fusion parameters can reference other parameters:

```text
flm_width / 2
flm_length - 2 * flm_margin
```

Agents should keep expressions readable. Do not generate complex expression strings when Python-calculated coordinates are clearer.

## When to Use Sketch Dimensions

For rebuild-only geometry, procedural coordinates are fine.

For editable parametric geometry, add sketch dimensions and set their values to parameter expressions.

Example intent:

- Rectangle length dimension references `flm_length`.
- Rectangle width dimension references `flm_width`.
- Hole diameter dimensions reference `flm_hole_diameter`.
- Hole placement dimensions reference `flm_hole_margin`.

## Timeline Considerations

Fusion features create timeline entries. Rebuild-by-delete can remove and recreate features, which is simple but not the same as editing timeline parameters.

If the user wants a polished parametric template:

1. Create named user parameters.
2. Build sketches/features once.
3. On rebuild, update parameter expressions instead of deleting geometry.
4. Let Fusion recompute the timeline.

This is a larger architecture change and should be done intentionally.

## Agent Rule

Default to JSON rebuilds. Add user parameters only when the user asks for Fusion-native parametric editing or when a model becomes complex enough that parameters materially improve reliability.

## References

- Autodesk, UserParameters.add: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/UserParameters_add.htm
- Autodesk, Units user manual: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/Units_UM.htm
- Autodesk, ValueInput: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/ValueInput.htm

