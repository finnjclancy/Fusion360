# Fusion Live Model

This add-in rebuilds a simple Fusion model from `design_spec.json`.

Agent-facing documentation lives in:

- `AGENTS.md`
- `docs/FUSION_AGENT_GUIDE.md`
- `docs/FUSION_API_RECIPES.md`
- `docs/FUSION_SPEC_SCHEMA.md`
- `docs/REQUEST_PLAYBOOK.md`
- `docs/SKETCH_CONSTRAINTS_AND_DIMENSIONS.md`
- `docs/FEATURE_RECIPES_DEEP.md`
- `docs/GEOMETRY_TARGETING.md`
- `docs/PARAMETRIC_MODELING.md`
- `docs/API_OBJECT_GLOSSARY.md`
- `docs/EXPORT_AND_MANUFACTURING.md`
- `docs/ERROR_COOKBOOK.md`
- `docs/PALETTE_LIVE_WORKFLOW.md`
- `docs/DESIGN_INTENT_RULES.md`
- `docs/SOURCE_RELIABILITY.md`
- `docs/AIRPODS_MAX_VISOR_CAD_SPEC.md`

## First run

1. In Fusion, open Utilities > Scripts and Add-Ins.
2. Select the Add-Ins tab.
3. Select FusionLiveModel.
4. Turn on Run.
5. In the Design workspace, click Rebuild Live Model.

## How edits work

Tell Codex what you want changed. Codex updates `design_spec.json` or the model-building Python code, then you click Rebuild Live Model in Fusion to see it.
