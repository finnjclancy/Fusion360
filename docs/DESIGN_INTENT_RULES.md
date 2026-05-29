# Design Intent Rules

Design intent is the reason a model changes correctly when dimensions change. Agents should not only make geometry that looks right once; they should make geometry that rebuilds predictably.

## General Rules

- Keep the origin meaningful.
- Center symmetric base shapes on the origin.
- Use X for length, Y for width, Z for height.
- Use millimeters in specs and user-facing docs.
- Use stable names for generated objects.
- Delete only generated objects.
- Keep sketches simple.
- Prefer parameters for important dimensions when adding parametric behavior.
- Prefer feature operations over low-level B-Rep edits.
- Build large/simple features before small/detail features.
- Apply cosmetic fillets/chamfers near the end unless they are part of functional geometry.

## Rebuild Determinism

A rebuild should produce the same model from the same spec every time.

To keep rebuild deterministic:

- Do not depend on random values.
- Do not depend on current camera/view.
- Do not depend on current selection unless the command explicitly asks for selection.
- Do not depend on collection index order for old geometry.
- Use named generated objects and predictable cleanup.

## Generated Object Naming

Recommended prefix:

```text
FLM_
```

Examples:

- `FLM_BaseSketch`
- `FLM_MainBody`
- `FLM_CenterHoleSketch`
- `FLM_MountingHoleCut`

The current project has older names for compatibility. New features should move toward prefixed names.

## Feature Order

Recommended order:

1. Base body.
2. Primary cutouts.
3. Secondary bosses/ribs.
4. Patterns/mirrors.
5. Shell, if requested and reliable for the part.
6. Fillets/chamfers.
7. Text/labels.
8. Appearance/material.
9. Export.

If shell fails after details, try shelling before details.

## Manufacturing Awareness

For 3D printing:

- Avoid razor-thin walls.
- Ask for clearance/tolerance when parts fit together.
- Avoid unsupported tiny features if print orientation matters.
- Consider chamfers on bottom edges.

For CNC/laser:

- Use DXF for 2D profiles.
- Avoid inside sharp corners if milling.
- Ask for tool diameter if pockets/slots matter.

For assemblies:

- Use separate components when Fusion document type allows it.
- Use meaningful component names.
- Avoid building separate parts as loose bodies unless intentional.

## User Geometry Safety

Finn may manually edit the Fusion file. Agents must avoid deleting user work.

Safe deletion:

- Generated body/sketch names.
- Generated prefix.
- Components created by the add-in.

Unsafe deletion:

- All bodies in root component.
- All sketches in document.
- Any body with an unknown name.
- User-selected geometry unless the user explicitly requested it.

## Assumptions To State

Tell Finn assumptions when they matter:

- Which face a feature was placed on.
- Hole positions/margins.
- Whether dimensions are interpreted as overall or internal.
- Whether a style is appearance-only or physical material.
- Whether a model is rebuilt from scratch or updated parametrically.

## Quality Bar

Before finishing:

- Spec is valid JSON.
- Python compiles.
- Units are correct.
- Generated names are stable.
- Rebuild cleanup is scoped.
- Final instructions tell Finn what to click in Fusion.

