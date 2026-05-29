# AirPods Max Inspired Visor Glasses CAD Specification

This document is the design source of truth for the visor glasses. Agents must read this before changing `model_builder.py` for this product.

The previous generated model was unacceptable because it skipped the CAD design phase. It built separate capsule bars and a lens slab, then hoped the result would look like eyewear. That is not the correct design method. This product must be designed from clear views, dimensions, and functional constraints first.

## Source and Assumptions

Official Apple AirPods Max dimensions used only as inspiration:

- Width: 168.6 mm
- Depth: 83.4 mm
- Height: 187.3 mm
- Source: Apple AirPods Max tech specs, https://support.apple.com/121205

Apple does not publish the exact headband spline, section radii, or canopy curvature. Therefore this design uses the AirPods Max width and soft continuous headband language as inspiration, not as an exact copy.

## Design Intent

Create two physical parts:

1. **Frame body**: a single continuous white/cream glasses frame that crosses the face, clears the eyebrows, rises around the nose, and wraps behind both ears with rigid non-folding arms.
2. **Lens insert**: a separate smoky/metallic mesh panel with perforations. It fits into the frame opening as a removable/replaceable insert.

The style should feel like an AirPods Max headband rotated down onto the face:

- thick soft rounded perimeter
- clean continuous U-shaped wrap in bird's-eye view
- minimal visible mechanical detail
- large visor opening
- visible eyebrows above the top edge
- sculpted nose clearance
- very rounded edges, no sharp slab corners

## Coordinate System

Use this coordinate system consistently:

- X axis: left/right across the face.
- Y axis: front/back from face to ears.
- Z axis: vertical.
- Origin: center of the face, centered between eyes.
- Face-on view: X/Z plane.
- Bird's-eye/top view: X/Y plane.
- Side view: Y/Z plane.

Positive Y goes backward toward the ears.

## Overall Package Dimensions

These are the target dimensions for the complete assembly:

| Dimension | Target |
| --- | ---: |
| Overall front width, outer frame | 168.6 mm |
| Overall front height, outer frame | 54.0 mm |
| Overall depth, front face to rear hook | 125.0 mm |
| Maximum frame thickness/depth at front | 10.0 mm |
| Arm section width | 9.0 mm |
| Arm section height | 8.0 mm |
| Lens insert visible width | 144.0 mm |
| Lens insert visible height | 30.0 mm |
| Lens insert thickness | 2.2 mm |
| Frame-to-lens clearance per side | 0.4 mm |
| Nominal all-edge rounding | 2.0-4.0 mm depending feature size |

## Part 1: Frame Body

### Function

The frame body holds the lens insert, defines the style, clears the nose and eyebrows, and wraps around the head/ears without hinges.

### Style Contribution

This is the main AirPods Max inspired element. It should read as one soft continuous band, not separate bars. The front should look like a sculpted visor frame. The arms should flow out of the side radius and continue behind the ear.

### Face-On View Dimensions

Outer frame envelope:

| Feature | Dimension / Position |
| --- | ---: |
| Outer width | 168.6 mm |
| Outer left X | -84.3 mm |
| Outer right X | +84.3 mm |
| Outer top Z at center | +24.0 mm |
| Outer top Z at sides | +21.0 mm |
| Outer bottom Z left/right | -24.0 mm |
| Nose bridge cut peak Z | -5.0 mm |
| Nose clearance width | 34.0 mm |
| Side lobe radius | 27.0 mm |
| Top brow rail visible thickness | 10.0 mm |
| Bottom rail visible thickness | 10.0 mm |
| Side rail visible thickness | 12.0 mm |

Lens window/opening:

| Feature | Dimension / Position |
| --- | ---: |
| Opening width | 148.0 mm |
| Opening left X | -74.0 mm |
| Opening right X | +74.0 mm |
| Opening top Z at center | +14.0 mm |
| Opening top Z at sides | +12.0 mm |
| Opening bottom Z left/right | -14.0 mm |
| Opening nose arch peak Z | -4.0 mm |
| Opening nose arch width | 32.0 mm |

Eyebrow visibility rule:

- The frame top edge must sit below the eyebrow line.
- Assume eyebrow line at approximately Z = +31 mm.
- Outer frame highest point should stay at or below Z = +25 mm.
- The lens window top should stay at or below Z = +15 mm.

Nose clearance rule:

- Central lower frame must arch upward over the nose.
- Nose cut width: 34 mm.
- Nose arch peak: Z = -5 mm.
- No lens insert or frame material should occupy the central nose clearance below this curve.

### Bird's-Eye / Top View Dimensions

The frame must not be a flat straight slab. It should be a shallow U-shaped visor that wraps around the face.

Top-view front frame centerline:

| Point | X | Y |
| --- | ---: | ---: |
| Center front | 0 mm | 0 mm |
| Quarter left | -42 mm | +4 mm |
| Left side | -84.3 mm | +16 mm |
| Quarter right | +42 mm | +4 mm |
| Right side | +84.3 mm | +16 mm |

Approximate front curvature:

- Chord width: 168.6 mm.
- Side setback from center: 16 mm.
- Approximate arc radius: about 230-260 mm.
- The front band should gently bow around the face.

Arm paths in top view:

| Feature | Left X/Y | Right X/Y |
| --- | ---: | ---: |
| Arm start at frame | -80, +16 | +80, +16 |
| Temple mid point | -86, +65 | +86, +65 |
| Ear contact point | -74, +100 | +74, +100 |
| Rear hook end | -62, +125 | +62, +125 |

Arm design:

- Arms are rigid and non-folding.
- Arms must visually flow from the side frame, not appear as disconnected sticks.
- Rear hook curves inward behind the ear.
- No hinge detail in this version.

### Side View Dimensions

| Feature | Target |
| --- | ---: |
| Front frame vertical height | 54 mm |
| Front frame depth/thickness | 10 mm |
| Lens insert set-back from front surface | 2.0 mm |
| Lens insert thickness | 2.2 mm |
| Arm vertical centerline | around Z = +2 mm to +8 mm |
| Ear hook rear should not drop below | Z = -8 mm |

Side-view style:

- Frame should have soft pill-shaped section, not square extrusion.
- Arm should taper slightly toward rear.
- Ear hook end should be rounded.

### Frame Cross-Sections

Use rounded/soft sections everywhere.

| Area | Section |
| --- | --- |
| Brow rail | rounded rectangle, 10 mm tall x 10 mm deep |
| Lower rail | rounded rectangle, 10 mm tall x 10 mm deep |
| Side lobes | rounded rectangle / blended oval, 12 mm wide x 10 mm deep |
| Arms | rounded rectangle, 9 mm wide x 8 mm high |
| Ear hook ends | rounded cap, radius 4-5 mm |

### Required Rounding

| Edge type | Radius |
| --- | ---: |
| Large outer front frame perimeter | 4.0 mm |
| Lens window inner perimeter | 2.0 mm |
| Nose clearance edge | 2.5 mm |
| Front/back face edges | 1.5-2.0 mm |
| Arm long edges | 1.5-2.0 mm |
| Arm end cap | 4.0 mm |
| Lens insert perimeter | 0.8-1.2 mm |
| Lens hole edge | 0.15-0.3 mm if practical |

## Part 2: Mesh Lens Insert

### Function

The lens insert fills the visor opening and provides the perforated mesh visual. It must remain a separate part from the frame.

### Style Contribution

The dark perforated insert contrasts with the soft white frame. The mesh should look technical and breathable, similar to the AirPods Max canopy/net language but adapted as a lens.

### Lens Envelope Dimensions

| Feature | Dimension |
| --- | ---: |
| Overall insert width | 144.0 mm |
| Overall insert height | 30.0 mm |
| Thickness | 2.2 mm |
| Corner radius / side capsule radius | 15.0 mm |
| Nose clearance cut width | 28.0 mm |
| Nose clearance peak Z | -4.0 mm |
| Fit clearance to frame | 0.4 mm per side |

Lens placement:

- Lens is centered in X.
- Lens sits slightly behind front frame surface.
- Lens should not cover eyebrows.
- Lens lower central area must clear the nose bridge.

### Mesh / Hole Pattern

Use a staggered circular-hole pattern.

| Feature | Dimension |
| --- | ---: |
| Hole diameter | 2.0 mm |
| Horizontal pitch | 4.8 mm |
| Vertical pitch | 4.15 mm |
| Row offset | 2.4 mm every other row |
| Outer hole margin | 3.0 mm minimum |
| Nose cut hole margin | 2.5 mm minimum |

Expected hole count:

- Approximately 140-180 visible holes depending exact clipping around perimeter and nose cut.
- Holes must cut fully through the lens insert.
- Holes should not appear outside the lens body.

## Fusion Tools / API Functions Required

Agents should use CAD tools in this order.

### Layout Sketches

Use:

- Face-on master sketch on XZ plane.
- Top-view master sketch on XY plane.
- Optional side-view/reference sketches.

API objects:

- `component.sketches.add(...)`
- `sketch.sketchCurves.sketchLines`
- `sketch.sketchCurves.sketchArcs`
- `sketch.sketchCurves.sketchFittedSplines` if using smooth curves
- `sketch.profiles`

### Frame Modeling

Preferred CAD method:

1. Create a continuous outer front frame blank from a face-on profile.
2. Cut lens window.
3. Cut nose clearance.
4. Add U-shaped top-view curvature if practical.
5. Add arms using sweep or lofted rounded sections.
6. Join arms to frame.
7. Fillet all edges.

API feature families:

- Extrude for initial front blank and cutouts.
- Sweep for arms and optionally for softer frame rails.
- Combine/Join for arms into frame.
- Fillet for final soft edges.

### Lens Modeling

Preferred CAD method:

1. Create lens insert capsule profile.
2. Cut nose clearance.
3. Generate staggered hole circles.
4. Cut holes through lens body.
5. Apply dark smoky appearance.
6. Fillet lens perimeter lightly.

API feature families:

- Extrude new body for lens.
- Extrude cut for mesh holes.
- Fillet for lens edge.
- Appearance assignment.

## Implementation Strategy For Agents

Do not build this as scattered bars.

Use this hierarchy:

```text
AirPods Max Visor Glasses
  FLM_Frame_OnePiece
    front frame blank
    lens opening cut
    nose clearance cut
    left rigid arm
    right rigid arm
    all-edge fillets
  FLM_Lens_Insert_Perforated
    lens blank
    nose clearance cut
    staggered mesh cuts
    soft lens edge fillets
```

If the Fusion API implementation cannot produce the full compound curved frame in one step, build a flat face-on version first, then add top-view curvature in the next iteration. Do not compromise the part breakdown or dimensions.

## Verification Checklist

Before calling a model acceptable, verify these items.

### Body Count

- Exactly one generated frame body.
- Exactly one generated lens insert body.
- No loose capsule bars.
- No duplicate old generated bodies.
- No random construction bodies visible.

### Face-On View

- Outer width is 168.6 mm.
- Eyebrows would remain visible above the frame.
- Lens opening is centered.
- Nose cut is centered and rises cleanly.
- Lower rail does not cross through the nose area.
- Lens insert fits within frame opening.
- Mesh holes are visible and cut through the lens.

### Bird's-Eye View

- Front frame is shallow U-shaped, not a perfectly flat straight slab.
- Arms flow from the frame sides.
- Arms wrap behind ears.
- Arms are connected to the frame.
- Arms do not look like detached sticks.

### Side View

- Lens insert sits behind/in the frame, not floating far away.
- Front frame has reasonable thickness.
- Arms align with the side frame.
- Ear hook ends are rounded.

### Rounding

- Outer frame edges are rounded.
- Inner lens window edges are rounded.
- Nose clearance edge is rounded.
- Arm edges are rounded.
- Lens insert perimeter is lightly rounded.
- No sharp slab-like corners remain.

### Mesh

- Holes are circular.
- Holes are staggered.
- Holes are clipped inside the lens boundary.
- Holes do not cut through frame.
- Hole count is roughly 140-180.

### Styling

- Frame is warm white/off-white.
- Lens is darker smoky/mesh color.
- The visual language is soft, minimal, and AirPods-Max-inspired.

## What Went Wrong In The First Attempts

First attempt:

- Built the frame as many independent capsules.
- Result: scattered bars around a lens slab.
- Lesson: continuous frames should start as one blank with cutouts.

Second attempt:

- Improved by making a front blank, but the geometry still read as a side/top U frame instead of a face-worn visor.
- Arms appeared as disconnected or poorly integrated shapes.
- Lens was still too slab-like and not clearly an inset mesh.

Required correction:

- Follow this spec view-by-view.
- Model the face-on eyewear shape first.
- Confirm body count and dimensions before adding style details.

