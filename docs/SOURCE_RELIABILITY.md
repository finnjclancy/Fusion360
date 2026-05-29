# Source Reliability and Provenance

This repository contains two kinds of agent documentation:

1. Official Autodesk Fusion API facts.
2. Project-specific conventions for this add-in.

Agents must distinguish between them. Autodesk documentation is the source of truth for API names, method signatures, object behavior, units, events, and export options. Project conventions are the source of truth for how this repository chooses to structure specs, rebuilds, naming, and chat-driven workflow.

## Official Sources Used

These are primary sources from Autodesk:

- Fusion API User's Manual: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/UserManualIndex_UM.htm
- Fusion API Reference Manual: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/ReferenceManual_UM.htm
- API Samples list: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/SampleList.htm
- Official Autodesk Fusion 360 GitHub organization: https://github.com/AutodeskFusion360
- Scripts and add-ins: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/WritingDebugging_UM.htm
- Python add-in template and command patterns: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/Commands_UM.htm
- Command inputs: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/CommandInputs_UM.htm
- Palettes and browser command inputs: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/Palettes_UM.htm
- Palette HTML-to-Python event: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/Palette_incomingFromHTML.htm
- Units in Fusion: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/Units_UM.htm
- Documents, products, components, occurrences, and proxies: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/ComponentsProxies_UM.htm
- Fusion B-Rep and geometry: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/BRepGeometry_UM.htm
- Sketch object: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/Sketch.htm
- Sketch dimensions object: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/SketchDimensions.htm
- Sketch rectangle API: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/SketchLines_addTwoPointRectangle.htm
- Extrude feature input: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/ExtrudeFeatures_createInput.htm
- Loft feature sample: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/LoftFeatureSample_Sample.htm
- ExportManager object: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/ExportManager.htm
- ExportManager sample: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/ExportManager_Sample.htm
- User parameters: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/UserParameters_add.htm
- ValueInput: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/ValueInput.htm
- Export designs help: https://help.autodesk.com/view/fusion360/enu/?guid=ASM-EXPORT-DESIGN
- Export format options: https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/Export-format-options-for-Fusion-360.html

## What Is Official API Fact

These statements in the docs are grounded in Autodesk's official documentation:

- Fusion scripts and add-ins are supported extension mechanisms.
- Add-ins can register commands and UI controls.
- Command definitions, command events, and command inputs are the supported command UI mechanism.
- Palettes are HTML-based persistent UI panels.
- Palette JavaScript communicates with Python through Fusion's palette HTML event mechanism, not by directly calling Fusion API objects.
- Fusion Design API internal database units include centimeters for length and radians for angles.
- A Fusion `Design` has a `rootComponent`.
- Components contain sketches, features, bodies, and occurrences.
- Sketches contain sketch curves, profiles, sketch dimensions, and constraints.
- Solid model topology is represented with B-Rep bodies, faces, edges, and vertices.
- The ExportManager creates export option objects and executes exports.
- User parameters and `ValueInput` are official API concepts.

## What Is Project Convention

These are not Autodesk requirements. They are local rules for this repository:

- Keep this add-in at `/Users/finn/Documents/Projects/Scripts/FusionLiveModel`.
- Keep chat-driven editable values in `design_spec.json`.
- Use millimeters in `design_spec.json`.
- Use `Rebuild Live Model` as the visible command.
- Rebuild generated geometry by deleting named generated items and recreating them.
- Use stable generated names and/or `FLM_` prefixes.
- Prefer JSON edits for simple changes and Python edits for new geometry.
- Use the expanded spec shape proposed in `FUSION_SPEC_SCHEMA.md`.
- Use the coordinate convention X = length, Y = width, Z = height.
- Prefer manual rebuild as the reliable first workflow.
- Treat the palette/chat panel as a future enhancement.

## What Is Engineering Guidance

These are pragmatic CAD/API recommendations inferred from Autodesk docs and normal Fusion modeling practice. They should be treated as guidance, not API guarantees:

- Prefer simple sketches with clear design intent.
- Prefer sketches plus features over low-level B-Rep edits for ordinary parts.
- Avoid relying on face/edge collection indexes for old geometry.
- Use bounding boxes and geometry type checks for semantic targeting.
- Apply cosmetic fillets/chamfers late unless they affect functional geometry.
- Use shell carefully; explicit wall geometry can be more reliable if shell fails.
- Use sketch-plus-cut for simple holes; use Fusion's hole feature for counterbores, countersinks, threads, and standards.
- Use user parameters when Fusion-native editability matters.

## Reliability Rules For Future Agents

When adding or changing docs:

1. If describing an API object, method, property, event, or unit behavior, cite or verify Autodesk docs first.
2. If describing this repo's workflow, label it as project convention.
3. If making a modeling recommendation, label it as guidance.
4. Do not invent method names. Look them up in the Autodesk reference manual or inspect a working sample.
5. If an Autodesk API is marked retired/deprecated, mention that and prefer the current API when implementing new code.
6. Test in Fusion when possible; Python syntax checks do not prove API calls work at runtime.
7. Keep tracebacks visible during development so failures can be corrected from real Fusion behavior.

## Current Confidence By Document

| Document | Source basis | Reliability note |
| --- | --- | --- |
| `FUSION_AGENT_GUIDE.md` | Autodesk API docs plus project conventions | Reliable for workflow; API details should be checked when implementing new methods. |
| `FUSION_API_RECIPES.md` | Working local code plus Autodesk docs | Reliable for existing rounded-block workflow; expand recipes with tested code as features are added. |
| `FUSION_SPEC_SCHEMA.md` | Project convention | Local schema proposal, not Autodesk-defined. |
| `REQUEST_PLAYBOOK.md` | Project convention plus CAD guidance | Good instruction layer for agents, not an Autodesk source. |
| `SKETCH_CONSTRAINTS_AND_DIMENSIONS.md` | Autodesk sketch docs plus CAD guidance | Reliable conceptually; exact method use should be checked in reference docs. |
| `FEATURE_RECIPES_DEEP.md` | Autodesk samples/reference plus CAD guidance | Reliable as decision guidance; implement with official method docs. |
| `GEOMETRY_TARGETING.md` | Autodesk B-Rep docs plus project targeting guidance | Reliable conceptually; exact geometry casts/evaluators should be tested in Fusion. |
| `PARAMETRIC_MODELING.md` | Autodesk parameters/units docs plus project guidance | Reliable for user-parameter direction. |
| `API_OBJECT_GLOSSARY.md` | Autodesk reference/object model | Reliable as glossary; not a replacement for reference manual. |
| `EXPORT_AND_MANUFACTURING.md` | Autodesk ExportManager/export docs plus manufacturing guidance | Reliable for format choice and API entry point. |
| `ERROR_COOKBOOK.md` | Real project errors plus Fusion API behavior | Reliable for known local errors; update as new errors appear. |
| `PALETTE_LIVE_WORKFLOW.md` | Autodesk palette docs plus future project architecture | Reliable for palette communication model; implementation still needed. |
| `DESIGN_INTENT_RULES.md` | CAD guidance plus project convention | Reliable as modeling policy, not API reference. |

