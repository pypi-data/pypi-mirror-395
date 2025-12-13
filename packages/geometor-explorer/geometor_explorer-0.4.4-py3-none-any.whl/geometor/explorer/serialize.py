"""
Browser-specific serialization for the Model class.
"""
from __future__ import annotations
import sympy as sp
import sympy.geometry as spg

from geometor.model.sections import Section
from geometor.model.chains import Chain
from geometor.model.wedges import Wedge
from geometor.model.utils import clean_expr, spread
from geometor.model.polynomials import Polynomial

def _spread(l1: spg.Line, l2: spg.Line):
    """calculate the spread of two lines"""
    a1, a2, a3 = l1.coefficients
    b1, b2, b3 = l2.coefficients
    # only the first two coefficients are used
    spread_val = ((a1 * b2 - a2 * b1) ** 2) / ((a1**2 + a2**2) * (b1**2 + b2**2))
    return spread_val


def _create_section_from_points(points, model):
    """Helper function to create a Section object from points."""
    section = Section(points)
    lengths_val = [l.evalf() for l in section.lengths]
    ratio_val = section.ratio.evalf()
    return {
        'type': 'section',
        'points': [model[p].ID for p in section.points],
        'lengths': [float(l) for l in lengths_val],
        'decimal_lengths': [f'{l:.4f}' for l in lengths_val],
        'latex_lengths': [sp.latex(l) for l in section.lengths],
        'ratio': float(ratio_val),
        'decimal_ratio': f'{ratio_val:.4f}',
        'latex_ratio': sp.latex(section.ratio),
        'is_golden': section.is_golden,
    }

def to_browser_dict(model):
    """
    Serializes the model to a dictionary format suitable for a browser-based
    application, preserving the order of creation.

    This method creates a dictionary containing the model's name and a single
    list of 'elements'. Each item in the list represents a geometric element
    in the order it was added to the model. This format is easy for a web
    client to parse and render sequentially.

    Each element dictionary includes:
    - A 'type' field (e.g., 'point', 'line').
    - Data relevant to the element type, including floating-point values for
      rendering and LaTeX expressions for display.
    """
    browser_elements = []

    for el, data in model.items():
        # Skip elements without a ID, as they cannot be referenced
        if not data.ID:
            continue

        element_dict = {
            'ID': data.ID,
            'classes': list(data.classes),
            'parents': [model[p].ID for p in data.parents.keys() if p in model and model[p].ID],
            'ancestors': model.get_ancestors_IDs(el).get(data.ID, {}),
            'guide': data.guide,
        }

        if isinstance(el, spg.Point):
            element_dict.update({
                'type': 'point',
                'x': float(el.x.evalf()),
                'y': float(el.y.evalf()),
                'latex_x': sp.latex(clean_expr(el.x)),
                'latex_y': sp.latex(clean_expr(el.y)),
            })

        elif isinstance(el, spg.Line):
            segment = spg.Segment(el.p1, el.p2)
            length_val = segment.length.evalf()
            element_dict.update({
                'type': 'line',
                'pt1': model[el.p1].ID,
                'pt2': model[el.p2].ID,
                'equation': str(el.equation()),
                'latex_equation': sp.latex(el.equation()),
                'latex_coefficients': [sp.latex(clean_expr(c)) for c in el.coefficients],
                'length': float(length_val),
                'decimal_length': f'{length_val:.4f}',
                'latex_length': sp.latex(segment.length),
            })

        elif isinstance(el, spg.Circle):
            radius_val = el.radius.evalf()
            h_val = el.center.x.evalf()
            k_val = el.center.y.evalf()
            element_dict.update({
                'type': 'circle',
                'center': model[el.center].ID,
                'radius_pt': model[data.pt_radius].ID,
                'radius': float(radius_val),
                'decimal_radius': f'{radius_val:.4f}',
                'latex_radius': sp.latex(el.radius),
                'h': float(h_val),
                'decimal_h': f'{h_val:.4f}',
                'latex_h': sp.latex(clean_expr(el.center.x)),
                'k': float(k_val),
                'decimal_k': f'{k_val:.4f}',
                'latex_k': sp.latex(clean_expr(el.center.y)),
                'equation': str(el.equation()),
                'latex_equation': sp.latex(el.equation()),
            })

        elif isinstance(el, spg.Polygon):
            lengths_val = [s.length.evalf() for s in el.sides]
            angles_val = {p: a.evalf() for p, a in el.angles.items()}
            area_val = el.area.evalf()
            
            spreads = {}
            vertices = el.vertices
            for i, v in enumerate(vertices):
                prev_v = vertices[i - 1]
                next_v = vertices[(i + 1) % len(vertices)]
                l1 = spg.Line(v, prev_v)
                l2 = spg.Line(v, next_v)
                spreads[model[v].ID] = sp.latex(clean_expr(_spread(l1, l2)))

            element_dict.update({
                'type': 'polygon',
                'points': [model[p].ID for p in el.vertices],
                'lengths': [float(l) for l in lengths_val],
                'decimal_lengths': [f'{l:.4f}' for l in lengths_val],
                'latex_lengths': [sp.latex(clean_expr(s.length)) for s in el.sides],
                'angles': {model[p].ID: float(a) for p, a in angles_val.items()},
                'degree_angles': {model[p].ID: f'{a * 180 / sp.pi:.3f}°' for p, a in angles_val.items()},
                'latex_angles': {model[p].ID: sp.latex(clean_expr(a)) for p, a in el.angles.items()},
                'spreads': spreads,
                'area': float(area_val),
                'decimal_area': f'{area_val:.4f}',
                'latex_area': sp.latex(clean_expr(el.area)),
            })

        elif isinstance(el, spg.Segment):
            length_val = el.length.evalf()
            element_dict.update({
                'type': 'segment',
                'pt1': model[el.p1].ID,
                'pt2': model[el.p2].ID,
                'points': [model[p].ID for p in [el.p1, el.p2]],
                'length': float(length_val),
                'decimal_length': f'{length_val:.4f}',
                'latex_length': sp.latex(el.length),
            })

        elif isinstance(el, Wedge):
            radius_val = el.circle.radius.evalf()
            radians_val = el.radians.evalf()
            element_dict.update({
                'type': 'wedge',
                'center': model[el.pt_center].ID,
                'radius_pt': model[el.pt_radius].ID,
                'start_ray_pt': model[el.start_ray.p2].ID,
                'end_ray_pt': model[el.sweep_ray.p2].ID,
                'radius': float(radius_val),
                'decimal_radius': f'{radius_val:.4f}',
                'latex_radius': sp.latex(el.circle.radius),
                'radians': float(radians_val),
                'degrees': f'{radians_val * 180 / sp.pi:.3f}°',
                'latex_radians': sp.latex(el.radians),
            })

        elif isinstance(el, (Section, sp.FiniteSet)):
            points = list(el.args) if isinstance(el, sp.FiniteSet) else el.points
            section_dict = _create_section_from_points(points, model)
            element_dict.update(section_dict)

        elif isinstance(el, Chain):
            element_dict.update({
                'type': 'chain',
                'points': [model[p].ID for p in el.points],
                'segments': [[model[s.p1].ID, model[s.p2].ID] for s in el.segments],
                'flow': el.flow,
            })
        
        elif isinstance(el, sp.Expr) and data.object == el:  # Check if it's a polynomial expression from a Polynomial element
            if isinstance(data, Polynomial):
                element_dict.update({
                    'type': 'polynomial',
                    'coeffs': [str(c) for c in data.coeffs],
                    'latex_equation': sp.latex(el),
                })
        
        else:
            # Skip unknown types
            continue

        browser_elements.append(element_dict)

    return {
        'name': model.name,
        'elements': browser_elements,
    }
