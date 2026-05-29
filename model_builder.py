import json
import os
import traceback

import adsk.core
import adsk.fusion


SPEC_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'design_spec.json')


def _mm(value):
    # Fusion stores raw distance values in centimeters.
    return float(value) / 10.0


def _load_spec():
    with open(SPEC_PATH, 'r', encoding='utf-8') as spec_file:
        return json.load(spec_file)


def _active_design():
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    if design:
        return design

    app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    return adsk.fusion.Design.cast(app.activeProduct)


def _delete_named_items(component, names):
    for body_index in range(component.bRepBodies.count - 1, -1, -1):
        body = component.bRepBodies.item(body_index)
        if body.name in names:
            body.deleteMe()

    for sketch_index in range(component.sketches.count - 1, -1, -1):
        sketch = component.sketches.item(sketch_index)
        if sketch.name in names:
            sketch.deleteMe()


def _delete_previous_component(root_component, component_name):
    occurrences = root_component.occurrences
    for index in range(occurrences.count - 1, -1, -1):
        occurrence = occurrences.item(index)
        if occurrence.name == component_name or occurrence.component.name == component_name:
            occurrence.deleteMe()


def _create_component(root_component, component_name):
    transform = adsk.core.Matrix3D.create()
    occurrence = root_component.occurrences.addNewComponent(transform)
    occurrence.name = component_name
    occurrence.component.name = component_name
    return occurrence.component


def _model_component(root_component, component_name):
    try:
        return _create_component(root_component, component_name)
    except RuntimeError:
        return root_component


def _draw_centered_rectangle(sketch, length_cm, width_cm):
    corner_a = adsk.core.Point3D.create(-length_cm / 2, -width_cm / 2, 0)
    corner_b = adsk.core.Point3D.create(length_cm / 2, width_cm / 2, 0)
    sketch.sketchCurves.sketchLines.addTwoPointRectangle(corner_a, corner_b)


def _extrude_profile(component, profile, height_cm):
    extrudes = component.features.extrudeFeatures
    extrude_input = extrudes.createInput(
        profile,
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
    )
    extrude_input.setDistanceExtent(False, adsk.core.ValueInput.createByReal(height_cm))
    extrude = extrudes.add(extrude_input)
    return extrude.bodies.item(0)


def _fillet_body(component, body, radius_cm):
    if radius_cm <= 0:
        return

    edge_collection = adsk.core.ObjectCollection.create()
    for edge_index in range(body.edges.count):
        edge_collection.add(body.edges.item(edge_index))

    fillet_input = component.features.filletFeatures.createInput()
    fillet_input.addConstantRadiusEdgeSet(
        edge_collection,
        adsk.core.ValueInput.createByReal(radius_cm),
        True,
    )
    component.features.filletFeatures.add(fillet_input)


def _appearance_from_spec(design, spec):
    style = spec.get('style', {})
    color = style.get('color', {})

    red = int(color.get('red', 42))
    green = int(color.get('green', 126))
    blue = int(color.get('blue', 210))
    alpha = int(color.get('alpha', 255))

    appearance_name = style.get('appearance_name', 'Fusion Live Color')
    appearance = design.appearances.itemByName(appearance_name)
    if not appearance:
        app = adsk.core.Application.get()
        library = app.materialLibraries.itemByName('Fusion 360 Appearance Library')
        source = library.appearances.itemByName('Paint - Enamel Glossy (White)')
        appearance = design.appearances.addByCopy(source, appearance_name)

    color_property = appearance.appearanceProperties.itemByName('Color')
    if color_property:
        color_property.value = adsk.core.Color.create(red, green, blue, alpha)

    return appearance


def _apply_style(design, body, spec):
    try:
        body.appearance = _appearance_from_spec(design, spec)
    except Exception:
        app = adsk.core.Application.get()
        app.log('FusionLiveModel appearance failed:\n' + traceback.format_exc())


def build_from_spec():
    spec = _load_spec()
    design = _active_design()
    root = design.rootComponent

    component_name = spec.get('component_name', 'Fusion Live Model')
    body_name = spec.get('body_name', 'Rounded block')
    sketch_name = 'Fusion Live Base Sketch'

    length_mm = spec.get('length_mm', 80)
    width_mm = spec.get('width_mm', 40)
    height_mm = spec.get('height_mm', 12)
    fillet_radius_mm = spec.get('fillet_radius_mm', 4)

    _delete_previous_component(root, component_name)
    _delete_named_items(root, {body_name, sketch_name})
    component = _model_component(root, component_name)

    sketch = component.sketches.add(component.xYConstructionPlane)
    sketch.name = sketch_name
    _draw_centered_rectangle(sketch, _mm(length_mm), _mm(width_mm))

    body = _extrude_profile(component, sketch.profiles.item(0), _mm(height_mm))
    body.name = body_name

    _fillet_body(component, body, _mm(fillet_radius_mm))
    _apply_style(design, body, spec)

    return f'Rebuilt {component_name}\n{length_mm} mm x {width_mm} mm x {height_mm} mm'
