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

Fix:

- Use known base appearances.
- Log available appearance properties.
- Apply to body and clear face overrides if necessary.
- Use unique appearance names for distinct colors.

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

