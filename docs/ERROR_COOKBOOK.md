# Error Cookbook

Fusion API errors are often runtime errors shown in a popup. Keep tracebacks visible during development.

## Part Design documents can only contain one component

Cause:

The code called `root_component.occurrences.addNewComponent(...)` in a document type that does not allow child components.

Fix:

Build directly in `design.rootComponent`.

Rule:

Never assume child components are allowed. Use `_model_component` fallback.

## root component name cannot be changed

Cause:

The code tried to assign `root_component.name = ...`.

Fix:

Do not rename the root component. Name bodies, sketches, and features instead.

## No profile found

Cause:

The sketch did not create a closed profile.

Fix:

- Check lines/circles/arcs form closed loops.
- Avoid duplicate overlapping lines.
- Use `sketch.profiles.count` before indexing.
- Simplify the sketch.

## VCS_SKETCH_OVER_CONSTRAINTS from addCenterToCenterSlot

Cause:

Fusion's `Sketch.addCenterToCenterSlot(...)` can automatically add slot constraints/dimensions. In generated sketches, especially repeated angled or vertical rails, this can throw:

```text
RuntimeError: 3 : VCS_SKETCH_OVER_CONSTRAINTS - Sketch geometry is over constrained
```

This happened in the glasses model when `_slot_profile` used `addCenterToCenterSlot` for generated frame rails.

Fix:

- For rebuild-generated capsule/slot rails, do not use Fusion's auto-constrained slot helper.
- Manually draw the capsule from two sketch lines and two sketch arcs.
- Use existing sketch endpoints when creating the arcs/lines so the profile closes.
- Keep explicit constraints out of this generated helper unless the user needs editable sketch dimensions.

Project pattern:

```python
top_line = lines.addByTwoPoints(start_left, end_left)
end_arc = arcs.addByThreePoints(top_line.endSketchPoint, end_outer, end_right)
bottom_line = lines.addByTwoPoints(end_arc.endSketchPoint, start_right)
arcs.addByThreePoints(bottom_line.endSketchPoint, start_outer, top_line.startSketchPoint)
```

Rule:

Use Fusion's slot helper for interactive/editable sketches. Use manual capsule geometry for deterministic generated rebuilds.

## Visual failure: scattered rails instead of one frame

Cause:

The first glasses generator attempted to build the front frame from many separate capsule bars and combine them afterward. The result was visually wrong: separate rounded bars around the lens instead of one coherent glasses frame. This is a CAD strategy failure rather than a syntax/API failure.

Fix:

- Build the main front shape as one solid blank.
- Cut the lens opening from that blank.
- Cut the nose clearance from that blank.
- Add arms afterward and join/combine them into the frame.
- Keep the lens insert as a separate body.

Rule:

For continuous eyewear/frame geometry, prefer "blank body plus cut openings" over "many bars plus combine." Use bars only for secondary details that truly are separate rails.

## Fillet fails

Common causes:

- Radius too large.
- Edge collection includes edges that cannot support the radius.
- Adjacent holes/slots are too close.
- Geometry is already too small/complex.

Fix:

- Validate radius before calling Fusion.
- Fillet selected edge groups instead of all edges.
- Reduce radius.
- Apply fillets before/after certain cuts depending on geometry.

## Shell fails

Common causes:

- Wall thickness too large.
- Complex faces or tight fillets.
- Bad face selection.
- Body has geometry Fusion cannot offset cleanly.

Fix:

- Reduce wall thickness.
- Shell before adding small details.
- Use explicit wall sketches instead of shell.
- Simplify the body.

## Units are 10x wrong

Cause:

The code passed millimeters to `createByReal`, but Fusion expects centimeters.

Fix:

Use:

```python
adsk.core.ValueInput.createByReal(mm / 10.0)
```

or:

```python
adsk.core.ValueInput.createByString(f'{mm} mm')
```

## Appearance does not update

Common causes:

- Wrong appearance property name.
- Existing appearance is reused with stale values.
- Face appearance overrides body appearance.
- Source appearance is not available in the library.
- `app.materialLibraries.itemByName('Fusion 360 Appearance Library')` can return `None` in some Fusion installs/sessions, causing `AttributeError: 'NoneType' object has no attribute 'appearances'`.

Fix:

- Do not assume one exact material library name exists.
- Search preferred material library names first, then scan available material libraries for any source appearance.
- If no source appearance is available, skip styling and log a warning instead of failing the rebuild.
- Use known base appearances when available.
- Log available appearance properties.
- Apply to body and clear face overrides if necessary.
- Use unique appearance names for distinct colors.

Debugging note from the glasses model:

```text
AttributeError: 'NoneType' object has no attribute 'appearances'
```

This happened when `_appearance` assumed `app.materialLibraries.itemByName('Fusion 360 Appearance Library')` returned a library. The fix was to add a `_source_appearance(app)` helper that searches multiple library names and falls back to the first available appearance.

## Command button does not appear

Common causes:

- Add-in is not running.
- Python syntax error.
- Command registration changed but add-in was not restarted.
- Wrong workspace/panel ID.

Fix:

- Run `python3 -m py_compile`.
- Toggle add-in off/on.
- Restart Fusion.
- Check `commands/__init__.py`.

## Code changes do not show up

If `model_builder.py` changed:

- Click `Rebuild Live Model`; the command reloads this module.

If command registration changed:

- Toggle add-in off/on or restart Fusion.

If manifest changed:

- Restart Fusion.

## Export fails

Common causes:

- Body/component is invalid.
- Export path is not writable.
- STL translation fails on complex/bad geometry.
- Hidden/tool bodies are included unintentionally.

Fix:

- Export STEP/F3D as fallback.
- Export a single named body/component.
- Simplify geometry.
- Save to a known local writable folder.

## Handler stops firing

Cause:

Python event handler was garbage collected.

Fix:

Keep handler references. In this project, use `futil.add_handler(..., local_handlers=local_handlers)` for command-instance handlers.

## Agent Response Rule

When Finn reports an error:

1. Ask for or read the traceback.
2. Patch the smallest failing layer.
3. Explain the root cause in plain language.
4. Tell Finn whether to click rebuild or restart/toggle the add-in.
