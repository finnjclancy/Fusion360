# Agent Instructions for FusionLiveModel

This folder is a Fusion Python add-in. It exists so Finn can describe model changes in chat, an AI coding agent updates the code or JSON spec, and Finn clicks `Rebuild Live Model` in Fusion to see the result.

Read these files before changing behavior:

- `docs/FUSION_AGENT_GUIDE.md` - Fusion API mental model, project architecture, safe workflow, and source links.
- `docs/FUSION_API_RECIPES.md` - Copyable coding patterns for common modeling requests.
- `docs/FUSION_SPEC_SCHEMA.md` - JSON spec contract and recommended future schema.
- `docs/REQUEST_PLAYBOOK.md` - Natural-language request translation rules and examples.
- `docs/SKETCH_CONSTRAINTS_AND_DIMENSIONS.md` - sketch design intent, dimensions, and constraints.
- `docs/FEATURE_RECIPES_DEEP.md` - deeper guidance for extrude, revolve, sweep, loft, holes, shell, fillet, chamfer, patterns, and combine.
- `docs/GEOMETRY_TARGETING.md` - how to find top faces, vertical edges, rims, largest faces, and when to use selection inputs.
- `docs/PARAMETRIC_MODELING.md` - when and how to use Fusion user parameters.
- `docs/API_OBJECT_GLOSSARY.md` - quick definitions of common Fusion API objects.
- `docs/EXPORT_AND_MANUFACTURING.md` - export formats and manufacturing notes.
- `docs/ERROR_COOKBOOK.md` - common Fusion API failures and fixes.
- `docs/PALETTE_LIVE_WORKFLOW.md` - future in-Fusion HTML palette architecture.
- `docs/DESIGN_INTENT_RULES.md` - modeling rules for robust rebuilds.
- `docs/SOURCE_RELIABILITY.md` - what is official Autodesk API fact versus project convention or modeling guidance.
- `design_spec.json` - Current model parameters and style values.
- `model_builder.py` - The model-building implementation.
- `commands/commandDialog/entry.py` - The Fusion toolbar command that reloads `model_builder.py`.

## Current Workflow

1. User describes a change in chat.
2. Prefer editing `design_spec.json` for dimensions, names, colors, and simple options.
3. Edit `model_builder.py` only when the request needs new geometry, new feature types, different rebuild behavior, or richer styling.
4. Run a syntax check:

   ```zsh
   python3 -m py_compile /Users/finn/Documents/Projects/Scripts/FusionLiveModel/model_builder.py /Users/finn/Documents/Projects/Scripts/FusionLiveModel/commands/commandDialog/entry.py
   ```

5. Tell Finn to click `Rebuild Live Model` in Fusion.

The command reloads `model_builder.py` every time it runs, so changes to that file normally do not require restarting Fusion. Changes to command registration, command names, toolbar placement, or manifest data may require toggling the add-in off and on, or restarting Fusion.

## Project-Specific Rules

- Keep this add-in at `/Users/finn/Documents/Projects/Scripts/FusionLiveModel`.
- Do not place project files in `/Users/finn/Documents/Projects/Scripts/Testing`.
- Do not delete Fusion-generated folders unless the user explicitly asks.
- Keep `FusionLiveModel.py` as the add-in entry point.
- Keep the visible command named `Rebuild Live Model` unless the user asks to rename it.
- Use millimeters in `design_spec.json`.
- Convert millimeters to Fusion internal length units before creating raw geometry. Fusion internal length units are centimeters.
- Use `ValueInput.createByString("12 mm")` when preserving user-facing expressions matters; use `ValueInput.createByReal(mm / 10)` for calculated values.
- Use stable names for generated bodies and sketches so rebuilds can delete and recreate only generated geometry.
- Be careful with components: some Fusion documents only allow one component. The current code falls back to building in the root component.
- Never assume a child component can be created. Catch `RuntimeError` or build in `design.rootComponent` when necessary.
- Do not hide tracebacks from the user. Fusion errors should be shown in a message box or logged with `app.log`.
- Use `docs/REQUEST_PLAYBOOK.md` to map Finn's wording to CAD operations.
- Use `docs/FUSION_SPEC_SCHEMA.md` before adding new JSON fields.

## What Is Active

Fusion's generated template included palette sample folders. They are currently inactive because `commands/__init__.py` registers only:

```python
from .commandDialog import entry as rebuildModel
```

The active behavior is:

- `FusionLiveModel.py` starts/stops registered commands.
- `commands/commandDialog/entry.py` creates the toolbar button and reloads `model_builder`.
- `model_builder.py` reads `design_spec.json` and rebuilds geometry.

## Before Finishing Any Change

- Run `python3 -m py_compile` on touched Python files.
- Run `python3 -m json.tool` on touched JSON files.
- Explain which file changed and what Finn should click in Fusion.
- If a change affects command UI rather than model logic, tell Finn to toggle the add-in off/on or restart Fusion.
