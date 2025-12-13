# Polynomial Rendering in GEOMETOR Explorer

This document captures the rendering knowledge from the `polynumbers` project for integration into `geometor.explorer`.

## Background from `polynumbers`

The original `polynumbers` project used `matplotlib` for rendering. The process involved:

1.  **Generating Points:** For a given polynomial and a range (e.g., x from -2 to 2), a large number of x-values were generated.
2.  **Evaluating Polynomial:** The polynomial was evaluated at each x-value to get the corresponding y-value.
3.  **Plotting:** `matplotlib` was used to plot the resulting set of (x, y) points, connecting them with lines to form the curve.

While effective for analysis, this approach is not ideal for the SVG-based rendering in `geometor.explorer` because it can generate a very large number of points and SVG elements, leading to performance issues.

## Proposed SVG Rendering Strategy

For `geometor.explorer`, we will adopt a more efficient and SVG-native approach using **Bézier curves**.

### SVG Path with Bézier Curves

A polynomial curve can be approximated by a series of connected cubic Bézier curve segments. An SVG `<path>` element can be used to draw this.

A cubic Bézier curve is defined by four points:
-   P₀: Start point
-   P₁: First control point
-   P₂: Second control point
-   P₃: End point

The SVG path command for a cubic Bézier is `C x₁ y₁, x₂ y₂, x₃ y₃`, where `(x₁, y₁)` are the coordinates of P₁, `(x₂, y₂)` are for P₂, and `(x₃ y₃)` are for P₃. The start point (P₀) is the end point of the previous path segment.

### Implementation Plan

1.  **Backend:** The `Polynomial` element in the model will be serialized with its coefficients.
2.  **Frontend (JavaScript):**
    -   A JavaScript function will receive the polynomial's coefficients.
    -   It will calculate a series of points along the curve within the current viewport.
    -   For each segment between two points on the curve, it will calculate the two control points needed to create a smooth Bézier curve that approximates that segment. The control points can be determined using the derivative of the polynomial at the start and end points of the segment.
    -   It will then construct the `d` attribute for an SVG `<path>` element by chaining these `C` commands together.
    -   This path will be added to the SVG canvas to render the polynomial.

This approach will result in a much more compact and performant SVG representation of the polynomial curves compared to plotting thousands of individual points and lines.
