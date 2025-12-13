// NOTE: INVERTED Y-AXIS
// The SVG coordinate system has its origin (0,0) at the top-left corner,
// with the y-axis extending downwards. To align with standard mathematical
// conventions where the y-axis extends upwards, all y-values for SVG
// attributes (e.g., y1, y2, cy) are negated.

// The viewBox attribute is also adjusted to handle this inversion.
// The third parameter of the viewBox, `y`, is set to a negative value
// to effectively flip the coordinate system vertically, ensuring that
// positive y-values are plotted above the x-axis.

const SVG_NS = "http://www.w3.org/2000/svg";

function renderHighlight(el, points) {
    let highlightEl = document.createElementNS(SVG_NS, 'polyline');
    let pt1, pt2;

    switch (el.type) {
        case 'point':
            pt1 = el;
            pt2 = el;
            break;
        case 'line':
            pt1 = points[el.pt1];
            pt2 = points[el.pt2];
            break;
        case 'circle':
            pt1 = points[el.center];
            pt2 = points[el.radius_pt];
            break;
        default:
            return;
    }

    if (pt1 && pt2) {
        highlightEl.setAttribute('points', `${pt1.x},${-pt1.y} ${pt2.x},${-pt2.y}`);
        highlightEl.id = `highlight-${el.ID}`;
        highlightEl.classList.add('highlight-segment');
        highlightEl.style.display = 'none';
        GEOMETOR.highlightsContainer.appendChild(highlightEl);
    }
}

export function renderElement(el, points) {
    let svgEl;
    let pointsStr;
    switch (el.type) {
        case 'line':
            svgEl = document.createElementNS(SVG_NS, 'line');
            const pt1 = points[el.pt1];
            const pt2 = points[el.pt2];
            svgEl.setAttribute('x1', pt1.x - 1000 * (pt2.x - pt1.x));
            svgEl.setAttribute('y1', -(pt1.y - 1000 * (pt2.y - pt1.y)));
            svgEl.setAttribute('x2', pt1.x + 1000 * (pt2.x - pt1.x));
            svgEl.setAttribute('y2', -(pt1.y + 1000 * (pt2.y - pt1.y)));
            renderHighlight(el, points);
            break;
        case 'circle':
            svgEl = document.createElementNS(SVG_NS, 'circle');
            const center = points[el.center];
            svgEl.setAttribute('cx', center.x);
            svgEl.setAttribute('cy', -center.y);
            svgEl.setAttribute('r', el.radius);
            svgEl.setAttribute('fill', 'none');
            renderHighlight(el, points);
            break;
        case 'polygon':
            svgEl = document.createElementNS(SVG_NS, 'polygon');
            pointsStr = el.points.map(p_ID => {
                const p = points[p_ID];
                return `${p.x},${-p.y}`;
            }).join(' ');
            svgEl.setAttribute('points', pointsStr);
            break;
        case 'segment':
        case 'section':
        case 'chain':
            svgEl = document.createElementNS(SVG_NS, 'polyline');
            pointsStr = el.points.map(p_ID => {
                const p = points[p_ID];
                return `${p.x},${-p.y}`;
            }).join(' ');
            svgEl.setAttribute('points', pointsStr);
            break;
        case 'polynomial':
            svgEl = renderPolynomial(el);
            break;
    }

    if (svgEl) {
        svgEl.id = el.ID;
        svgEl.classList.add(el.type);
        el.classes.forEach(c => svgEl.classList.add(c));
        if (el.guide) {
            svgEl.classList.add('guide');
        }
        if (['polygon', 'segment', 'section', 'chain'].includes(el.type)) {
            svgEl.dataset.category = 'graphics';
            GEOMETOR.graphicsContainer.appendChild(svgEl);
        } else {
            svgEl.dataset.category = 'elements';
            GEOMETOR.elementsContainer.appendChild(svgEl);
        }
    }
}

export function renderPoint(el) {
    const circle = document.createElementNS(SVG_NS, 'circle');
    circle.id = el.ID;
    circle.setAttribute('cx', el.x);
    circle.setAttribute('cy', -el.y);
    circle.setAttribute('r', 0.02);
    circle.dataset.category = 'points';
    el.classes.forEach(c => circle.classList.add(c));
    if (el.guide) {
        circle.classList.add('guide');
    }
    GEOMETOR.pointsContainer.appendChild(circle);
    renderHighlight(el);
}

function evaluatePolynomial(coeffs, x) {
    let result = 0;
    // Ensure coeffs are parsed as floats for calculation
    const numericCoeffs = coeffs.map(c => {
        if (typeof c === 'string' && c.includes('sqrt')) {
            // Basic parsing for sqrt(5) or similar patterns.
            // A more robust solution might be needed for complex expressions.
            const num = parseFloat(c.match(/(\d+)/)[0]);
            return Math.sqrt(num);
        }
        return parseFloat(c);
    });

    for (let i = 0; i < numericCoeffs.length; i++) {
        result += numericCoeffs[i] * Math.pow(x, numericCoeffs.length - 1 - i);
    }
    return result;
}

function generatePolynomialPointsString(el) {
    const coeffs = el.coeffs;
    const viewBox = GEOMETOR.svg.getAttribute('viewBox').split(' ').map(Number);
    const [minX, , viewWidth] = viewBox;
    const maxX = minX + viewWidth;

    const svgWidth = GEOMETOR.svg.clientWidth;
    // Calculate step size to have roughly one point per pixel
    const step = viewWidth / svgWidth;

    let points = [];
    for (let x = minX; x <= maxX; x += step) {
        const y = evaluatePolynomial(coeffs, x);
        points.push(`${x},${-y}`);
    }
    return points.join(' ');
}

function renderPolynomial(el) {
    const svgEl = document.createElementNS(SVG_NS, 'polyline');
    svgEl.setAttribute('points', generatePolynomialPointsString(el));
    svgEl.setAttribute('fill', 'none');
    return svgEl;
}

export function updatePolynomials() {
    const polys = GEOMETOR.graphicsContainer.querySelectorAll('.polynomial');
    polys.forEach(polyEl => {
        const elData = GEOMETOR.modelData.elements.find(e => e.ID === polyEl.id);
        if (elData) {
            polyEl.setAttribute('points', generatePolynomialPointsString(elData));
        }
    });
}


export function scaleCircles() {
    const svgRect = GEOMETOR.svg.getBoundingClientRect();
    if (svgRect.width === 0) return;

    const currentViewBox = GEOMETOR.svg.getAttribute('viewBox').split(' ').map(Number);
    const viewBoxWidth = currentViewBox[2];
    const unitsPerPixel = viewBoxWidth / svgRect.width;
    const desiredRadiusPixels = 5;
    const newRadius = desiredRadiusPixels * unitsPerPixel;

    const circles = GEOMETOR.pointsContainer.querySelectorAll('circle');
    circles.forEach(circle => {
        circle.setAttribute('r', newRadius);
    });
}


export function fitConstruction() {
    const points = GEOMETOR.modelData.elements.filter(el => el.type === 'point');
    if (points.length === 0) return;

    let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;

    points.forEach(p => {
        minX = Math.min(minX, p.x);
        maxX = Math.max(maxX, p.x);
        minY = Math.min(minY, p.y);
        maxY = Math.max(maxY, p.y);
    });

    const circles = GEOMETOR.modelData.elements.filter(el => el.type === 'circle');
    circles.forEach(c => {
        const center = GEOMETOR.modelData.elements.find(p => p.ID === c.center);
        if (center) {
            minX = Math.min(minX, center.x - c.radius);
            maxX = Math.max(maxX, center.x + c.radius);
            minY = Math.min(minY, center.y - c.radius);
            maxY = Math.max(maxY, center.y + c.radius);
        }
    });

    if (minX === Infinity) {
        minX = -1;
        maxX = 1;
        minY = -1;
        maxY = 1;
    }

    const padding = 0.1;
    const width = maxX - minX;
    const height = maxY - minY;
    const paddedWidth = width * (1 + padding);
    const paddedHeight = height * (1 + padding);
    const centerX = minX + width / 2;
    const centerY = minY + height / 2;

    const svgAspectRatio = GEOMETOR.svg.clientWidth / GEOMETOR.svg.clientHeight;
    const constructionAspectRatio = paddedWidth / paddedHeight;

    let viewBoxWidth, viewBoxHeight;
    if (svgAspectRatio > constructionAspectRatio) {
        viewBoxHeight = paddedHeight;
        viewBoxWidth = paddedHeight * svgAspectRatio;
    } else {
        viewBoxWidth = paddedWidth;
        viewBoxHeight = paddedWidth / svgAspectRatio;
    }

    const viewBoxX = centerX - viewBoxWidth / 2;
    const viewBoxY = -centerY - viewBoxHeight / 2;

    GEOMETOR.svg.setAttribute('viewBox', `${viewBoxX} ${viewBoxY} ${viewBoxWidth} ${viewBoxHeight}`);
    scaleCircles();
}

export function initSvgEventListeners() {
    GEOMETOR.svg.addEventListener('wheel', (event) => {
        event.preventDefault();
        const currentViewBox = GEOMETOR.svg.getAttribute('viewBox').split(' ').map(Number);
        let [x, y, width, height] = currentViewBox;
        const scaleFactor = event.deltaY > 0 ? 1.1 : 1 / 1.1;
        const { clientX, clientY } = event;
        const svgRect = GEOMETOR.svg.getBoundingClientRect();
        const svgX = clientX - svgRect.left;
        const svgY = clientY - svgRect.top;
        const mousePoint = {
            x: x + (svgX / svgRect.width) * width,
            y: y + (svgY / svgRect.height) * height
        };
        width *= scaleFactor;
        height *= scaleFactor;
        x = mousePoint.x - (svgX / svgRect.width) * width;
        y = mousePoint.y - (svgY / svgRect.height) * height;
        GEOMETOR.svg.setAttribute('viewBox', `${x} ${y} ${width} ${height}`);
        scaleCircles();
        updatePolynomials();
    });


    let isPanning = false;
    let startPoint = { x: 0, y: 0 };

    GEOMETOR.svg.addEventListener('mousedown', (event) => {
        isPanning = true;
        startPoint = { x: event.clientX, y: event.clientY };
        GEOMETOR.svg.style.cursor = 'grabbing';
    });

    GEOMETOR.svg.addEventListener('mousemove', (event) => {
        if (!isPanning) return;
        const svgRect = GEOMETOR.svg.getBoundingClientRect();
        const currentViewBox = GEOMETOR.svg.getAttribute('viewBox').split(' ').map(Number);
        let [x, y, width, height] = currentViewBox;
        const dx = (event.clientX - startPoint.x) * (width / svgRect.width);
        const dy = (event.clientY - startPoint.y) * (height / svgRect.height);
        x -= dx;
        y -= dy;
        GEOMETOR.svg.setAttribute('viewBox', `${x} ${y} ${width} ${height}`);
        startPoint = { x: event.clientX, y: event.clientY };
        updatePolynomials();
    });

    GEOMETOR.svg.addEventListener('mouseup', () => {
        isPanning = false;
        GEOMETOR.svg.style.cursor = 'default';
    });

    GEOMETOR.svg.addEventListener('mouseleave', () => {
        isPanning = false;
        GEOMETOR.svg.style.cursor = 'default';
    });

    document.addEventListener('mouseover', (event) => {
        const target = event.target;
        if (target.namespaceURI === SVG_NS && target.id && target.id !== 'drawing') {
            if (target.parentElement) {
                target.parentElement.appendChild(target);
            }
            GEOMETOR.isPositionedByTable = false;
            GEOMETOR.setElementHover(target.id, true);
            if (GEOMETOR.modelData.elements) {
                const elementData = GEOMETOR.modelData.elements.find(el => el.ID === target.id);
                GEOMETOR.updateHoverCard(elementData);
            }
        }
    });

    document.addEventListener('mouseout', (event) => {
        const target = event.target;
        if (target.namespaceURI === SVG_NS && target.id) {
            GEOMETOR.setElementHover(target.id, false);
            GEOMETOR.hoverCard.style.display = 'none';
        }
    });
}