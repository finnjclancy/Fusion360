# Export and Manufacturing Notes

Agents may be asked to export models for printing, sharing, CNC, laser cutting, or CAD exchange. This document explains format choices and API entry points.

## Format Choices

Use:

- `.f3d`: native Fusion archive; best for preserving Fusion data/timeline.
- `.step` or `.stp`: neutral CAD exchange for solid bodies.
- `.stl`: mesh export for 3D printing.
- `.3mf`: modern 3D printing/manufacturing mesh package.
- `.obj`: mesh export with geometry/texture-style data.
- `.dxf`: 2D profile/sketch export for laser/CNC workflows.

Do not commit large exported CAD files by default. `.gitignore` excludes common exports so they are committed intentionally.

## Export Manager

Fusion's `Design` exposes an export manager:

```python
export_mgr = design.exportManager
```

Common options include:

- `createSTEPExportOptions`
- `createFusionArchiveExportOptions`
- `createSTLExportOptions`

Exporting usually follows:

```python
options = export_mgr.createSTEPExportOptions(file_path, component)
export_mgr.execute(options)
```

## STEP Export

Use STEP when another CAD tool needs editable solid geometry.

Typical targets:

- Manufacturers
- Engineers
- CAD exchange
- Assemblies/components

Prefer exporting a component when possible.

## STL Export

Use STL when slicing for 3D printing.

STL is a mesh, not editable solid CAD. It does not preserve timeline, parameters, sketches, or exact analytic surfaces.

If export quality matters, check STL export option properties in current Autodesk docs before implementing.

## DXF Export

Use DXF for 2D profiles:

- Laser cutting
- Plasma/waterjet cutting
- CNC 2D toolpaths
- Flat patterns

DXF export is typically sketch or drawing oriented, not a full solid export replacement.

## Export Folder Convention

If adding export automation, use:

```text
/Users/finn/Documents/Projects/Scripts/FusionLiveModel/exports
```

Add generated export files only when the user explicitly asks.

## Agent Safety

- Ask before overwriting exports unless the filename is clearly generated.
- Include units in filenames when useful.
- Prefer timestamped filenames for repeated exports.
- Do not export hidden construction/tool bodies unless the user asks.
- For manufacturing, ask for tolerances/clearance/material when dimensions matter.

## References

- Autodesk, ExportManager object: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/ExportManager.htm
- Autodesk, ExportManager sample: https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/ExportManager_Sample.htm
- Autodesk, Export designs: https://help.autodesk.com/view/fusion360/enu/?guid=ASM-EXPORT-DESIGN
- Autodesk, Export format options: https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/Export-format-options-for-Fusion-360.html

