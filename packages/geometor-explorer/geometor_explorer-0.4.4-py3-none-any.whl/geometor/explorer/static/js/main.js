import { modal } from './modal.js';
import { fitConstruction, renderElement, renderPoint, scaleCircles, initSvgEventListeners, updatePolynomials } from './svg.js';
import { initGroupsView, initGroupsEventListeners } from './groups.js';
import { initResizer } from './resizer.js';
import { TL_DRAW, setPoint, setLine, setCircle } from './Animate.js';

window.GEOMETOR = window.GEOMETOR || {};

document.addEventListener('DOMContentLoaded', () => {
    modal.init();
    initResizer();
    initGroupsEventListeners();

    GEOMETOR.tables = {};

    function showHourglassCursor() {
        document.body.style.cursor = 'wait';
        GEOMETOR.svg.style.cursor = 'wait';
    }

    function hideHourglassCursor() {
        document.body.style.cursor = 'default';
        GEOMETOR.svg.style.cursor = 'default';
    }

    GEOMETOR.svg = document.getElementById('drawing');
    GEOMETOR.graphicsContainer = document.getElementById('graphics');
    GEOMETOR.highlightsContainer = document.getElementById('highlights');
    GEOMETOR.elementsContainer = document.getElementById('elements');
    GEOMETOR.pointsContainer = document.getElementById('points');
    GEOMETOR.hoverCard = document.getElementById('hover-card');
    GEOMETOR.tables.points = document.querySelector('#points-table tbody');
    GEOMETOR.tables.structures = document.querySelector('#structures-table tbody');
    GEOMETOR.tables.graphics = document.querySelector('#graphics-table tbody');
    GEOMETOR.tables.chrono = document.querySelector('#chrono-table tbody');
    const statusFilename = document.getElementById('status-filename');
    const statusSelected = document.getElementById('status-selected');
    const statusMessage = document.getElementById('status-message');
    let currentFilename = '';
    let isDirty = false;

    function updateStatus(message, isError = false) {
        statusMessage.textContent = message;
        statusMessage.classList.toggle('error', isError);
    }

    function updateFilenameDisplay() {
        statusFilename.textContent = currentFilename || 'Unsaved Model';
    }

    function loadConstructions() {
        showHourglassCursor();
        updateStatus('Loading constructions...');
        fetch('/api/constructions')
            .then(response => response.json())
            .then(files => {
                // TODO: hook in the new file dialog
            })
            .finally(() => {
                hideHourglassCursor();
                updateStatus('Ready');
            });
    }

    GEOMETOR.selectedPoints = [];
    GEOMETOR.modelData = {};
    GEOMETOR.isPositionedByTable = false;

    function renderModel(data, skipAnimation = false) {
        const oldGoldenSectionIds = (GEOMETOR.modelData.elements || [])
            .filter(el => el.type === 'section' && el.classes.includes('golden'))
            .map(el => el.ID)
            .sort();

        GEOMETOR.modelData = data;
        GEOMETOR.graphicsContainer.innerHTML = '';
        GEOMETOR.highlightsContainer.innerHTML = '';
        GEOMETOR.elementsContainer.innerHTML = '';
        GEOMETOR.pointsContainer.innerHTML = '';
        GEOMETOR.tables.points.innerHTML = '';
        GEOMETOR.tables.structures.innerHTML = '';
        GEOMETOR.tables.graphics.innerHTML = '';
        GEOMETOR.tables.chrono.innerHTML = '';

        const points = {};

        if (data.elements) {
            data.elements.forEach(el => {
                if (el.type === 'point') {
                    points[el.ID] = el;
                }
            });
        }

        if (data.elements) {
            data.elements.forEach(el => {
                if (el.type === 'point') {
                    renderPoint(el);
                    addPointToTable(el);
                } else {
                    renderElement(el, points);
                    if (['line', 'circle'].includes(el.type)) {
                        addStructureToTable(el);
                    } else {
                        addGraphicToTable(el);
                    }
                }
                addChronologicalRow(el);
                if (animationEnabled) {
                    const svgEl = document.getElementById(el.ID);
                    if (svgEl) {
                        gsap.set(svgEl, { autoAlpha: 0 });
                    }
                }
            });
        }
        
            document.getElementById('points-count').textContent = GEOMETOR.tables.points.rows.length;
            document.getElementById('structures-count').textContent = GEOMETOR.tables.structures.rows.length;
            document.getElementById('graphics-count').textContent = GEOMETOR.tables.graphics.rows.length;
        GEOMETOR.selectedPoints.forEach(ID => {
            const svgPoint = document.getElementById(ID);
            const tableRow = GEOMETOR.tables.points.querySelector(`tr[data-id="${ID}"]`);
            const chronoRow = GEOMETOR.tables.chrono.querySelector(`tr[data-id="${ID}"]`);
            if (svgPoint) svgPoint.classList.add('selected');
            if (tableRow) tableRow.classList.add('highlight');
            if (chronoRow) chronoRow.classList.add('highlight');
        });

        scaleCircles();

        const newGoldenSectionIds = (data.elements || [])
            .filter(el => el.type === 'section' && el.classes.includes('golden'))
            .map(el => el.ID)
            .sort();

        if (JSON.stringify(oldGoldenSectionIds) !== JSON.stringify(newGoldenSectionIds)) {
            initGroupsView();
        }
        if (animationEnabled && !skipAnimation) {
            animateConstruction();
        } else {
            gsap.set('#drawing g > *', { autoAlpha: 1 });
        }
    }

    function addPointToTable(el) {
        const row = GEOMETOR.tables.points.insertRow();
        row.dataset.id = el.ID;
        const IDCell = row.insertCell();
        const xCell = row.insertCell();
        const yCell = row.insertCell();
        const classCell = row.insertCell();
        const guideCell = row.insertCell();
        const actionCell = row.insertCell();

        IDCell.innerHTML = el.ID;
        katex.render(el.latex_x, xCell);
        xCell.title = el.x.toFixed(4);
        katex.render(el.latex_y, yCell);
        yCell.title = el.y.toFixed(4);
        classCell.innerHTML = el.classes.join(', ');
        guideCell.innerHTML = el.guide ? '✓' : '';

        actionCell.innerHTML = `<button class="edit-btn" data-id="${el.ID}"><span class="material-icons">edit</span></button><button class="delete-btn" data-id="${el.ID}"><span class="material-icons">delete</span></button>`;

        const svgEl = document.getElementById(el.ID);
        if (svgEl) {
            const color = window.getComputedStyle(svgEl).getPropertyValue('fill');
            IDCell.style.color = color;
        }
    }

    function addStructureToTable(el) {
        const row = GEOMETOR.tables.structures.insertRow();
        row.dataset.id = el.ID;
        const IDCell = row.insertCell();
        const classCell = row.insertCell();
        const guideCell = row.insertCell();
        const deleteCell = row.insertCell();

        IDCell.innerHTML = el.ID;
        classCell.innerHTML = el.classes.join(', ');
        guideCell.innerHTML = el.guide ? '✓' : '';
        deleteCell.innerHTML = `<button class="edit-btn" data-id="${el.ID}"><span class="material-icons">edit</span></button><button class="delete-btn" data-id="${el.ID}"><span class="material-icons">delete</span></button>`;

        const svgEl = document.getElementById(el.ID);
        if (svgEl) {
            const color = window.getComputedStyle(svgEl).getPropertyValue('stroke');
            IDCell.style.color = color;
        }
    }

    function addGraphicToTable(el) {
        const row = GEOMETOR.tables.graphics.insertRow();
        row.dataset.id = el.ID;
        const IDCell = row.insertCell();
        const classCell = row.insertCell();
        const deleteCell = row.insertCell();

        IDCell.innerHTML = el.ID;
        classCell.innerHTML = el.classes.join(', ');
        deleteCell.innerHTML = `<button class="edit-btn" data-id="${el.ID}"><span class="material-icons">edit</span></button><button class="delete-btn" data-id="${el.ID}"><span class="material-icons">delete</span></button>`;

        const svgEl = document.getElementById(el.ID);
        if (svgEl) {
            let color = window.getComputedStyle(svgEl).getPropertyValue('stroke');
            if (svgEl.classList.contains('golden')) {
                color = 'gold';
            }
            IDCell.style.color = color;
        }
    }

    function addChronologicalRow(el) {
        const row = GEOMETOR.tables.chrono.insertRow();
        row.dataset.id = el.ID;
        const isGiven = el.classes && el.classes.includes('given');
        
        const IDCell = row.insertCell();
        const classCell = row.insertCell();
        const guideCell = row.insertCell();
        const deleteCell = row.insertCell();

        IDCell.innerHTML = el.ID;
        classCell.innerHTML = el.classes.join(', ');
        guideCell.innerHTML = el.guide ? '✓' : '';
        if (el.type !== 'point' && !isGiven) {
            deleteCell.innerHTML = `<button class="edit-btn" data-id="${el.ID}"><span class="material-icons">edit</span></button><button class="delete-btn" data-id="${el.ID}"><span class="material-icons">delete</span></button>`;
        }

        const svgEl = document.getElementById(el.ID);
        if (svgEl) {
            let color;
            if (el.type === 'point') {
                color = window.getComputedStyle(svgEl).getPropertyValue('fill');
            } else {
                color = window.getComputedStyle(svgEl).getPropertyValue('stroke');
                if (color === 'none' || color === '') {
                    color = window.getComputedStyle(svgEl).getPropertyValue('fill');
                }
                if (svgEl.classList.contains('golden')) {
                    color = 'gold';
                }
            }
            IDCell.style.color = color;
        }
    }

    const lineBtn = document.getElementById('line-btn');
    const circleBtn = document.getElementById('circle-btn');
    const pbBtn = document.getElementById('pb-btn');
    const abBtn = document.getElementById('ab-btn');
    const segmentBtn = document.getElementById('segment-btn');
    const sectionBtn = document.getElementById('section-btn');
    const polygonBtn = document.getElementById('polygon-btn');

    function updateConstructionButtons() {
        const numPoints = GEOMETOR.selectedPoints.length;
        lineBtn.disabled = numPoints !== 2;
        circleBtn.disabled = numPoints !== 2;
        pbBtn.disabled = numPoints !== 2;
        abBtn.disabled = numPoints !== 3;
        segmentBtn.disabled = numPoints !== 2;
        sectionBtn.disabled = numPoints !== 3;
        polygonBtn.disabled = numPoints < 2;

        [lineBtn, circleBtn, pbBtn, abBtn, segmentBtn, sectionBtn, polygonBtn].forEach(btn => {
            if (btn.disabled) {
                btn.classList.remove('btn-enabled');
            } else {
                btn.classList.add('btn-enabled');
            }
        });
    }

    function updateSelectedPointsDisplay() {
        statusSelected.textContent = `Selected: ${GEOMETOR.selectedPoints.join(', ')}`;
    }

    function toggleSelection(ID) {
        const index = GEOMETOR.selectedPoints.indexOf(ID);
        if (index > -1) {
            GEOMETOR.selectedPoints.splice(index, 1);
        } else {
            GEOMETOR.selectedPoints.push(ID);
        }
        renderModel(GEOMETOR.modelData, true);
        updateConstructionButtons();
        updateSelectedPointsDisplay();
    }

    function clearSelection() {
        GEOMETOR.selectedPoints = [];
        renderModel(GEOMETOR.modelData, true);
        updateConstructionButtons();
        updateSelectedPointsDisplay();
    }

    GEOMETOR.pointsContainer.addEventListener('click', (event) => {
        const target = event.target;
        if (target.tagName === 'circle' && target.id) {
            toggleSelection(target.id);
        }
    });

    GEOMETOR.tables.points.addEventListener('click', (event) => {
        const row = event.target.closest('tr');
        if (row && row.dataset.id) {
            toggleSelection(row.dataset.id);
        }
    });

    lineBtn.addEventListener('click', () => {
        if (GEOMETOR.selectedPoints.length === 2) {
            const [pt1, pt2] = GEOMETOR.selectedPoints;
            showHourglassCursor();
            updateStatus('Constructing line...');
            fetch('/api/construct/line', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ pt1, pt2 }),
            })
            .then(response => response.json())
            .then(data => {
                renderModel(data);
                clearSelection();
                isDirty = true;
            })
            .finally(() => {
                hideHourglassCursor();
                updateStatus('Ready');
            });
        }
    });

    circleBtn.addEventListener('click', () => {
        if (GEOMETOR.selectedPoints.length === 2) {
            const [pt1, pt2] = GEOMETOR.selectedPoints;
            showHourglassCursor();
            updateStatus('Constructing circle...');
            fetch('/api/construct/circle', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ pt1, pt2 }),
            })
            .then(response => response.json())
            .then(data => {
                renderModel(data);
                clearSelection();
                isDirty = true;
            })
            .finally(() => {
                hideHourglassCursor();
                updateStatus('Ready');
            });
        }
    });

    pbBtn.addEventListener('click', () => {
        if (GEOMETOR.selectedPoints.length === 2) {
            const [pt1, pt2] = GEOMETOR.selectedPoints;
            showHourglassCursor();
            updateStatus('Constructing perpendicular bisector...');
            fetch('/api/construct/perpendicular_bisector', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ pt1, pt2 }),
            })
            .then(response => response.json())
            .then(data => {
                renderModel(data);
                clearSelection();
                isDirty = true;
            })
            .finally(() => {
                hideHourglassCursor();
                updateStatus('Ready');
            });
        }
    });

    abBtn.addEventListener('click', () => {
        if (GEOMETOR.selectedPoints.length === 3) {
            const [pt1, vertex, pt3] = GEOMETOR.selectedPoints;
            showHourglassCursor();
            updateStatus('Constructing angle bisector...');
            fetch('/api/construct/angle_bisector', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ pt1, vertex, pt3 }),
            })
            .then(response => response.json())
            .then(data => {
                renderModel(data);
                clearSelection();
                isDirty = true;
            })
            .finally(() => {
                hideHourglassCursor();
                updateStatus('Ready');
            });
        }
    });

    function constructPoly(endpoint, points) {
        showHourglassCursor();
        updateStatus('Constructing polygon...');
        fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ points: points }),
        })
        .then(response => response.json())
        .then(data => {
            renderModel(data);
            clearSelection();
            isDirty = true;
        })
        .finally(() => {
            hideHourglassCursor();
            updateStatus('Ready');
        });
    }

    segmentBtn.addEventListener('click', () => {
        if (GEOMETOR.selectedPoints.length === 2) {
            constructPoly('/api/set/segment', GEOMETOR.selectedPoints);
        }
    });

    sectionBtn.addEventListener('click', () => {
        if (GEOMETOR.selectedPoints.length === 3) {
            constructPoly('/api/set/section', GEOMETOR.selectedPoints);
        }
    });

    polygonBtn.addEventListener('click', () => {
        if (GEOMETOR.selectedPoints.length >= 2) {
            constructPoly('/api/set/polygon', GEOMETOR.selectedPoints);
        }
    });

    const pointBtn = document.getElementById('point-btn');
    pointBtn.addEventListener('click', () => {
        const content = `
            <form>
                <label for="x">X Coordinate:</label>
                <input type="text" id="x" name="x" value="0" required>
                <label for="y">Y Coordinate:</label>
                <input type="text" id="y" name="y" value="0" required>
                <button type="submit">Add Point</button>
            </form>
        `;

        modal.show('Add Point', content, (data) => {
            showHourglassCursor();
            updateStatus('Constructing point...');
            fetch('/api/construct/point', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ x: data.x, y: data.y }),
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw new Error(err.message) });
                }
                return response.json();
            })
            .then(data => {
                renderModel(data);
                isDirty = true;
                updateStatus('Ready');
            })
            .catch(error => {
                updateStatus(error.message, true);
            })
            .finally(() => {
                hideHourglassCursor();
            });
        });
    });

    const polynomialBtn = document.getElementById('polynomial-btn');
    polynomialBtn.addEventListener('click', () => {
        const content = `
            <form>
                <label for="coeffs">Coefficients (comma-separated):</label>
                <input type="text" id="coeffs" name="coeffs" value="1, -1, -1" required>
                <button type="submit">Add Polynomial</button>
            </form>
        `;

        modal.show('Add Polynomial', content, (data) => {
            showHourglassCursor();
            updateStatus('Constructing polynomial...');
            fetch('/api/construct/polynomial', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ coeffs: data.coeffs }),
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw new Error(err.message) });
                }
                return response.json();
            })
            .then(data => {
                renderModel(data);
                isDirty = true;
                updateStatus('Ready');
            })
            .catch(error => {
                updateStatus(error.message, true);
            })
            .finally(() => {
                hideHourglassCursor();
            });
        });
    });

    GEOMETOR.updateHoverCard = function(element) {
        if (!element) {
            GEOMETOR.hoverCard.style.display = 'none';
            return;
        }

        let content = `<p><span class="ID">${element.ID}</span> ${element.type}`;
        if (element.classes && element.classes.length > 0) {
            content += ` <span class="classes">(${element.classes.join(', ')})</span>`;
        }
        content += `</p>`;

        if (element.type === 'point') {
            content += '<hr>';
            let table = '<table><tbody>';
            let x_div = document.createElement('div');
            katex.render(`${element.latex_x}`, x_div);
            table += `<tr><td>x</td><td class="latex">${x_div.innerHTML}</td><td class="decimal">${element.x.toFixed(4)}</td></tr>`;
            let y_div = document.createElement('div');
            katex.render(`${element.latex_y}`, y_div);
            table += `<tr><td>y</td><td class="latex">${y_div.innerHTML}</td><td class="decimal">${element.y.toFixed(4)}</td></tr>`;
            if (element.parents && element.parents.length > 0) {
                table += `<tr><td>str</td><td colspan="2">${element.parents.join('<br>')}</td></tr>`;
            }
            table += '</tbody></table>';
            content += table;
        } else if (element.type === 'line' || element.type === 'circle') {
            content += '<hr>';
            let table = '<table><tbody>';
            if (element.type === 'circle') {
                table += `<tr><td>ctr</td><td colspan="2">${element.center}</td></tr>`;
                const h = document.createElement('div');
                katex.render(`${element.latex_h}`, h);
                table += `<tr><td>h</td><td class="latex">${h.innerHTML}</td><td class="decimal">${element.decimal_h}</td></tr>`;
                const k = document.createElement('div');
                katex.render(`${element.latex_k}`, k);
                table += `<tr><td>k</td><td class="latex">${k.innerHTML}</td><td class="decimal">${element.decimal_k}</td></tr>`;
                const radius = document.createElement('div');
                katex.render(`${element.latex_radius}`, radius);
                table += `<tr><td>r</td><td class="latex">${radius.innerHTML}</td><td class="decimal">${element.decimal_radius}</td></tr>`;
            }
            if (element.type === 'line') {
                const length = document.createElement('div');
                katex.render(`${element.latex_length}`, length);
                table += `<tr><td>len</td><td class="latex">${length.innerHTML}</td><td class="decimal">${element.decimal_length}</td></tr>`;
            }
            const equation = document.createElement('div');
            katex.render(element.latex_equation, equation);
            table += `<tr><td>eq</td><td colspan="2">${equation.innerHTML}</td></tr>`;
            if (element.latex_coefficients) {
                const coefficients = document.createElement('div');
                katex.render(element.latex_coefficients.join(', '), coefficients);
                table += `<tr><td>coef</td><td colspan="2">${coefficients.innerHTML}</td></tr>`;
            }
            if (element.parents && element.parents.length > 0) {
                table += `<tr><td>pts</td><td colspan="2">${element.parents.join(', ')}</td></tr>`;
            }
            table += '</tbody></table>';
            content += table;
        } else if (element.type === 'segment') {
            content += '<hr>';
            const length = document.createElement('div');
            katex.render(`l = ${element.latex_length}`, length);
            content += `<span>${length.innerHTML}</span> <span class="decimal">(${element.decimal_length})</span>`;
        } else if (element.type === 'section') {
            content += '<hr>';
            let table = '<table><tbody>';
            for (let i = 0; i < element.parents.length - 1; i++) {
                const p1 = element.parents[i];
                const p2 = element.parents[i+1];
                const decimal = element.decimal_lengths[i];
                table += `<tr><td>${p1} ${p2}</td><td class="latex"></td><td class="decimal">${decimal}</td></tr>`;
            }
            table += `<tr><td>ratio</td><td class="latex-ratio"></td><td class="decimal">${element.decimal_ratio}</td></tr>`;
            table += '</tbody></table>';
            content += table;

        } else if (element.type === 'wedge') {
            content += '<hr>';
            const radius = document.createElement('div');
            katex.render(`r = ${element.latex_radius}`, radius);
            content += `<span>${radius.innerHTML}</span> <span class="decimal">(${element.decimal_radius})</span>`;
            const radians = document.createElement('div');
            katex.render(`rad = ${element.latex_radians}`, radians);
            content += `<span>${radians.innerHTML}</span> <span class="decimal">(${element.degrees})</span>`;
        } else if (element.type === 'polygon') {
            content += '<hr>';
            let table = '<table><thead><tr><th>Seg</th><th>Sym</th><th>Dec</th></tr></thead><tbody>';
            for (let i = 0; i < element.parents.length; i++) {
                const p1 = element.parents[i];
                const p2 = element.parents[(i + 1) % element.parents.length];
                const decimal = element.decimal_lengths[i];
                table += `<tr><td>${p1} ${p2}</td><td class="latex"></td><td class="decimal">${decimal}</td></tr>`;
            }
            table += '</tbody></table>';
            content += table;

            let angleTable = '<table><thead><tr><th>Vert</th><th>Alg</th><th>Deg</th><th>Spread</th></tr></thead><tbody>';
            for (const p of element.parents) {
                const algValue = element.latex_angles[p] || '';
                const degValue = element.degree_angles[p] || '';
                const spreadValue = element.spreads[p] || '';
                
                angleTable += `<tr><td>${p}</td><td class="latex-angle">${algValue}</td><td class="decimal">${degValue}</td><td class="latex-spread">${spreadValue}</td></tr>`;
            }
            angleTable += '</tbody></table>';
            content += angleTable;

            const area = document.createElement('div');
            katex.render(`Area = ${element.latex_area}`, area);
            content += `<span>${area.innerHTML}</span> <span class="decimal">(${element.decimal_area})</span>`;
        }

        GEOMETOR.hoverCard.innerHTML = content;

        if (element.type === 'section') {
            const latexCells = GEOMETOR.hoverCard.querySelectorAll('.latex');
            latexCells.forEach((cell, i) => {
                katex.render(element.latex_lengths[i], cell);
            });
            const ratioCell = GEOMETOR.hoverCard.querySelector('.latex-ratio');
            if (ratioCell) {
                katex.render(element.latex_ratio, ratioCell);
            }
        } else if (element.type === 'polygon') {
            const latexCells = GEOMETOR.hoverCard.querySelectorAll('.latex');
            latexCells.forEach((cell, i) => {
                katex.render(element.latex_lengths[i], cell);
            });
            const latexAngleCells = GEOMETOR.hoverCard.querySelectorAll('.latex-angle');
            latexAngleCells.forEach(cell => {
                katex.render(cell.textContent, cell);
            });
            const latexSpreadCells = GEOMETOR.hoverCard.querySelectorAll('.latex-spread');
            latexSpreadCells.forEach(cell => {
                katex.render(cell.textContent, cell);
            });
        }

        const svgEl = document.getElementById(element.ID);
        if (svgEl) {
            let color;
            if (element.type === 'point') {
                color = window.getComputedStyle(svgEl).getPropertyValue('fill');
            } else {
                color = window.getComputedStyle(svgEl).getPropertyValue('stroke');
                if (color === 'none' || color === '') {
                    color = window.getComputedStyle(svgEl).getPropertyValue('fill');
                }
                if (svgEl.classList.contains('golden')) {
                    color = 'gold';
                }
            }
            const idSpan = GEOMETOR.hoverCard.querySelector('.ID');
            idSpan.style.color = color;
            idSpan.style.fontWeight = 'bold';
        }

        GEOMETOR.hoverCard.style.display = 'block';
    }

    function getAncestorIds(ancestors) {
        if (!ancestors) {
            return [];
        }
        let allIds = [];
        function recurse(ancestorObj) {
            let ids = Object.keys(ancestorObj);
            allIds = allIds.concat(ids);
            ids.forEach(id => {
                if (ancestorObj[id]) {
                    recurse(ancestorObj[id]);
                }
            });
        }
        recurse(ancestors);
        return allIds;
    }

    GEOMETOR.setElementHover = function(ID, hoverState) {
        if (!GEOMETOR.modelData.elements) {
            return;
        }
        const elementData = GEOMETOR.modelData.elements.find(el => el.ID === ID);
        if (!elementData) return;

        if (ancestorsOnHover) {
            if (hoverState) {
                const ancestorIds = getAncestorIds(elementData.ancestors);
                ancestorIds.push(ID);
                GEOMETOR.modelData.elements.forEach(el => {
                    const svgEl = document.getElementById(el.ID);
                    if (svgEl) {
                        if (ancestorIds.includes(el.ID)) {
                            gsap.set(svgEl, { autoAlpha: 1 });
                        } else {
                            gsap.set(svgEl, { autoAlpha: 0 });
                        }
                    }
                });
            } else {
                GEOMETOR.modelData.elements.forEach(el => {
                    const svgEl = document.getElementById(el.ID);
                    if (svgEl) {
                        gsap.set(svgEl, { autoAlpha: 1 });
                    }
                });
            }
        }

        const svgElement = document.getElementById(ID);
        const pointsRow = GEOMETOR.tables.points.querySelector(`tr[data-id="${ID}"]`);
        const structuresRow = GEOMETOR.tables.structures.querySelector(`tr[data-id="${ID}"]`);
        const graphicsRow = GEOMETOR.tables.graphics.querySelector(`tr[data-id="${ID}"]`);
        const chronoRow = GEOMETOR.tables.chrono.querySelector(`tr[data-id="${ID}"]`);

        const highlightElement = document.getElementById(`highlight-${ID}`);

        const action = hoverState ? 'add' : 'remove';
        if (svgElement) {
            svgElement.classList[action]('hover');
            svgElement.classList[action]('hover-target');
            if (hoverState) {
                gsap.set(svgElement, { autoAlpha: 1 });
            } else {
                if (!animationEnabled && !ancestorsOnHover) {
                    const category = svgElement.dataset.category;
                    let table;
                    if (category === 'points') table = GEOMETOR.tables.points;
                    if (category === 'elements') table = GEOMETOR.tables.structures;
                    if (category === 'graphics') table = GEOMETOR.tables.graphics;

                    if (table) {
                        const section = table.closest('.collapsible-section');
                        if (section && section.classList.contains('hide-elements')) {
                            gsap.set(svgElement, { autoAlpha: 0 });
                        } else {
                            gsap.set(svgElement, { autoAlpha: 1 });
                        }
                    }
                } else if (animationEnabled) {
                    const elementIndex = GEOMETOR.modelData.elements.findIndex(el => el.ID === ID);
                    const currentStep = Math.floor(TL_DRAW.progress() * GEOMETOR.modelData.elements.length);
                    if (elementIndex >= currentStep) {
                        gsap.set(svgElement, { autoAlpha: 0 });
                    } else {
                        gsap.set(svgElement, { autoAlpha: 1 });
                    }
                }
            }
        }
        if (pointsRow) pointsRow.classList[action]('row-hover');
        if (structuresRow) structuresRow.classList[action]('row-hover');
        if (graphicsRow) graphicsRow.classList[action]('row-hover');
        if (chronoRow) chronoRow.classList[action]('row-hover');
        if (highlightElement) highlightElement.style.display = hoverState ? 'inline' : 'none';

        let parentIDs = [];
        if (elementData.type === 'line') {
            parentIDs = [elementData.pt1, elementData.pt2];
        } else if (elementData.type === 'circle') {
            parentIDs = [elementData.center, elementData.radius_pt];
        }

        if (!ancestorsOnHover) {
            parentIDs.forEach(parentID => {
                if (parentID) {
                    GEOMETOR.setElementHover(parentID, hoverState);
                }
            });
        }
    }

    function transformPoint(svg, x, y) {
        const pt = svg.createSVGPoint();
        pt.x = x;
        pt.y = y;
        const screenCTM = svg.getScreenCTM();
        if (screenCTM) {
            return pt.matrixTransform(screenCTM);
        }
        return null;
    }

    Object.values(GEOMETOR.tables).forEach(tableBody => {
        tableBody.addEventListener('mouseover', (event) => {
            const row = event.target.closest('tr');
            if (row && row.dataset.id) {
                const ID = row.dataset.id;
                GEOMETOR.setElementHover(ID, true);

                const elementData = GEOMETOR.modelData.elements.find(el => el.ID === ID);
                const svgElement = document.getElementById(ID);
                if (elementData && svgElement) {
                    GEOMETOR.updateHoverCard(elementData);
                    GEOMETOR.isPositionedByTable = true;

                    let screenPoint;

                    if (elementData.type === 'point') {
                        screenPoint = transformPoint(GEOMETOR.svg, elementData.x, elementData.y);
                    } else if (elementData.type === 'line') {
                        const pt1 = GEOMETOR.modelData.elements.find(p => p.ID === elementData.pt1);
                        const pt2 = GEOMETOR.modelData.elements.find(p => p.ID === elementData.pt2);
                        if (pt1 && pt2) {
                            const bbx = Math.max(pt1.x, pt2.x);
                            const bby = Math.max(pt1.y, pt2.y);
                            screenPoint = transformPoint(GEOMETOR.svg, bbx, bby);
                        }
                    } else if (elementData.type === 'circle') {
                        const center = GEOMETOR.modelData.elements.find(p => p.ID === elementData.center);
                        if (center) {
                            const bbx = center.x + elementData.radius * 0.8;
                            const bby = center.y + elementData.radius * 0.8;
                            screenPoint = transformPoint(GEOMETOR.svg, bbx, bby);
                        }
                    } else if (elementData.type === 'polygon' || elementData.type === 'segment' || elementData.type === 'section') {
                        const parentPoints = elementData.parents.map(pID => GEOMETOR.modelData.elements.find(p => p.ID === pID)).filter(p => p && p.type === 'point');
                        if (parentPoints.length > 0) {
                            const xs = parentPoints.map(p => p.x);
                            const ys = parentPoints.map(p => p.y);
                            const bbx = Math.max(...xs);
                            const bby = Math.max(...ys);
                            screenPoint = transformPoint(GEOMETOR.svg, bbx, bby);
                        }
                    } else if (elementData.parents && elementData.parents.length > 0) {
                        const parentPoints = elementData.parents.map(pID => GEOMETOR.modelData.elements.find(p => p.ID === pID)).filter(p => p && p.type === 'point');
                        if (parentPoints.length > 0) {
                            const totalX = parentPoints.reduce((sum, p) => sum + p.x, 0);
                            const totalY = parentPoints.reduce((sum, p) => sum + p.y, 0);
                            const midX = totalX / parentPoints.length;
                            const midY = totalY / parentPoints.length;
                            screenPoint = transformPoint(GEOMETOR.svg, midX, midY);
                        }
                    }

                    if (screenPoint) {
                        GEOMETOR.hoverCard.style.left = `${screenPoint.x + 15}px`;
                        GEOMETOR.hoverCard.style.top = `${screenPoint.y + 15}px`;
                    } else {
                        const elemRect = svgElement.getBoundingClientRect();
                        GEOMETOR.hoverCard.style.left = `${elemRect.right + 10}px`;
                        GEOMETOR.hoverCard.style.top = `${elemRect.top}px`;
                    }
                }
            }
        });

        tableBody.addEventListener('mouseout', (event) => {
            const row = event.target.closest('tr');
            if (row && row.dataset.id) {
                GEOMETOR.setElementHover(row.dataset.id, false);
            }
            GEOMETOR.hoverCard.style.display = 'none';
        });

        tableBody.addEventListener('click', (event) => {
            const button = event.target.closest('button');
            if (!button) return;

            const ID = button.dataset.id;
            if (!ID) return;

            if (button.classList.contains('delete-btn')) {
                showHourglassCursor();
                fetch(`/api/model/dependents?ID=${ID}`)
                    .then(response => response.json())
                    .then(dependents => {
                        let message = `Are you sure you want to delete ${ID}?`;
                        if (dependents.length > 0) {
                            message += `\n\nThe following elements will also be deleted: ${dependents.join(', ')}`;
                        }

                        if (confirm(message)) {
                            updateStatus('Deleting element...');
                            fetch('/api/model/delete', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ ID: ID }),
                            })
                            .then(response => response.json())
                            .then(data => {
                                renderModel(data);
                                isDirty = true;
                            })
                            .finally(() => {
                                hideHourglassCursor();
                                updateStatus('Ready');
                            });
                        } else {
                            hideHourglassCursor();
                        }
                    })
                    .catch(() => {
                        hideHourglassCursor();
                    });
            } else if (button.classList.contains('edit-btn')) {
                const element = GEOMETOR.modelData.elements.find(el => el.ID === ID);
                if (element) {
                    const content = `
                        <form>
                            <label for="classes">Classes:</label>
                            <input type="text" id="classes" name="classes" value="${element.classes.join(', ')}">
                            <label for="guide">Guide:</label>
                            <input type="checkbox" id="guide" name="guide" ${element.guide ? 'checked' : ''}>
                            <button type="submit">Save</button>
                        </form>
                    `;
                    modal.show(`Edit Element ${ID}`, content, (data) => {
                        showHourglassCursor();
                        updateStatus('Editing element...');
                        fetch('/api/model/edit', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ 
                                ID: ID, 
                                classes: data.classes,
                                guide: data.guide === 'on'
                            }),
                        })
                        .then(response => response.json())
                        .then(data => {
                            renderModel(data);
                            isDirty = true;
                        })
                        .finally(() => {
                            hideHourglassCursor();
                            updateStatus('Ready');
                        });
                    });
                }
            }
        });
    });

    GEOMETOR.tables.chrono.addEventListener('click', (event) => {
        const row = event.target.closest('tr');
        if (row && row.dataset.id) {
            const elementData = GEOMETOR.modelData.elements.find(el => el.ID === row.dataset.id);
            if (elementData && elementData.type === 'point') {
                toggleSelection(row.dataset.id);
            }
        }
    });

    document.addEventListener('mousemove', (event) => {
        if (GEOMETOR.hoverCard.style.display === 'block' && !GEOMETOR.isPositionedByTable) {
            GEOMETOR.hoverCard.style.left = `${event.clientX + 15}px`;
            GEOMETOR.hoverCard.style.top = `${event.clientY + 15}px`;
        }
    });
    
    document.addEventListener('mouseout', (event) => {
        const target = event.target;
        if (target.namespaceURI === "http://www.w3.org/2000/svg" && target.id) {
            GEOMETOR.hoverCard.style.display = 'none';
        }
    });

    const resizeObserver = new ResizeObserver(scaleCircles);
    resizeObserver.observe(GEOMETOR.svg);

    showHourglassCursor();
    updateStatus('Loading model...');
    fetch('/api/model')
        .then(response => response.json())
        .then(data => {
            renderModel(data);
        })
        .finally(() => {
            hideHourglassCursor();
            updateStatus('Ready');
        });

    const settingsBtn = document.getElementById('settings-btn');
    const settingsModal = document.getElementById('settings-modal');
    const themeToggle = document.getElementById('theme-toggle');
    const ancestorsToggle = document.getElementById('ancestors-toggle');
    const analysisToggle = document.getElementById('analysis-toggle');
    const ancestorsBtn = document.getElementById('ancestors-btn');

    let ancestorsOnHover = false;

    settingsBtn.addEventListener('click', () => {
        settingsModal.style.display = 'block';
    });

    settingsModal.querySelector('.close-btn').addEventListener('click', () => {
        settingsModal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target == settingsModal) {
            settingsModal.style.display = 'none';
        }
    });

    themeToggle.addEventListener('change', () => {
        GEOMETOR.svg.classList.toggle('light-theme', themeToggle.checked);
        localStorage.setItem('svg-theme', themeToggle.checked ? 'light' : 'dark');
    });

    ancestorsToggle.addEventListener('change', () => {
        ancestorsOnHover = ancestorsToggle.checked;
        ancestorsBtn.classList.toggle('active', ancestorsOnHover);
    });

    ancestorsBtn.addEventListener('click', () => {
        ancestorsOnHover = !ancestorsOnHover;
        ancestorsToggle.checked = ancestorsOnHover;
        ancestorsBtn.classList.toggle('active', ancestorsOnHover);
    });

    analysisToggle.addEventListener('click', () => {
        fetch('/api/analysis/toggle', {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            if (data.analysis_enabled) {
                analysisToggle.classList.add('active');
            } else {
                analysisToggle.classList.remove('active');
            }
        });
    });

    const savedSvgTheme = localStorage.getItem('svg-theme');
    if (savedSvgTheme === 'light') {
        GEOMETOR.svg.classList.add('light-theme');
        themeToggle.checked = true;
    }

    const categoryViewBtn = document.getElementById('category-view-btn');
    const chronoViewBtn = document.getElementById('chrono-view-btn');
    const groupsViewBtn = document.getElementById('groups-view-btn');
    const categoryView = document.getElementById('category-view');
    const chronologicalView = document.getElementById('chronological-view');
    const groupsView = document.getElementById('groups-view');

    categoryViewBtn.addEventListener('click', () => {
        categoryView.style.display = 'flex';
        chronologicalView.style.display = 'none';
        groupsView.style.display = 'none';
        categoryViewBtn.classList.add('active');
        chronoViewBtn.classList.remove('active');
        groupsViewBtn.classList.remove('active');
    });

    chronoViewBtn.addEventListener('click', () => {
        categoryView.style.display = 'none';
        chronologicalView.style.display = 'flex';
        groupsView.style.display = 'none';
        chronoViewBtn.classList.add('active');
        categoryViewBtn.classList.remove('active');
        groupsViewBtn.classList.remove('active');
    });

    groupsViewBtn.addEventListener('click', () => {
        categoryView.style.display = 'none';
        chronologicalView.style.display = 'none';
        groupsView.style.display = 'flex';
        groupsViewBtn.classList.add('active');
        categoryViewBtn.classList.remove('active');
        chronoViewBtn.classList.remove('active');
    });

    const collapseBtns = document.querySelectorAll('.collapse-btn');
    collapseBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const section = btn.closest('.collapsible-section');
            section.classList.toggle('collapsed');
            
            const isCollapsed = section.classList.contains('collapsed');
            btn.querySelector('.material-icons').textContent = isCollapsed ? 'expand_more' : 'expand_less';
            
            const tableContainer = section.querySelector('.table-container');
            tableContainer.style.display = isCollapsed ? 'none' : '';
        });
    });

    const toggleVisBtns = document.querySelectorAll('.toggle-vis-btn');
    toggleVisBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            if (animationEnabled) return;
            
            const section = btn.closest('.collapsible-section');
            section.classList.toggle('hide-elements');
            const isHidden = section.classList.contains('hide-elements');
            btn.querySelector('.material-icons').textContent = isHidden ? 'visibility_off' : 'visibility';

            let category = section.querySelector('h3').textContent.toLowerCase().split(' ')[2];
            if (category === 'structures') {
                category = 'elements';
            }

            const elementsToToggle = document.querySelectorAll(`#drawing [data-category="${category}"]`);
            gsap.to(elementsToToggle, { autoAlpha: isHidden ? 0 : 1, duration: 0.5 });
        });
    });

    const newBtn = document.getElementById('new-btn');
    const openBtn = document.getElementById('open-btn');
    const saveBtn = document.getElementById('save-btn');
    const saveAsBtn = document.getElementById('save-as-btn');
    const fileInput = document.getElementById('file-input');
    const newModelModal = document.getElementById('new-model-modal');
    const newBlankBtn = document.getElementById('new-blank-btn');
    const newDefaultBtn = document.getElementById('new-default-btn');
    const newEquidistantBtn = document.getElementById('new-equidistant-btn');

    function showNewModelModal() {
        newModelModal.style.display = 'block';
    }

    function hideNewModelModal() {
        newModelModal.style.display = 'none';
    }

    newBtn.addEventListener('click', () => {
        if (isDirty) {
            if (confirm('Are you sure you want to start a new construction? Any unsaved changes will be lost.')) {
                showNewModelModal();
            }
        } else {
            showNewModelModal();
        }
    });

    function createNewModel(template) {
        hideNewModelModal();
        showHourglassCursor();
        updateStatus('Creating new model...');
        fetch('/api/model/new', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ template: template }),
        })
            .then(response => response.json())
            .then(data => {
                renderModel(data);
                clearSelection();
                currentFilename = 'untitled.json';
                updateFilenameDisplay();
                isDirty = false;
            })
            .finally(() => {
                hideHourglassCursor();
                updateStatus('Ready');
            });
    }

    newBlankBtn.addEventListener('click', () => createNewModel('blank'));
    newDefaultBtn.addEventListener('click', () => createNewModel('default'));
    newEquidistantBtn.addEventListener('click', () => createNewModel('equidistant'));

    newModelModal.querySelector('.close-btn').addEventListener('click', hideNewModelModal);

    openBtn.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const content = e.target.result;
                showHourglassCursor();
                updateStatus('Loading file...');
                fetch('/api/model/load', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ content: content }),
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success === false) {
                        updateStatus(`Error loading file: ${data.message}`, true);
                    } else {
                        renderModel(data);
                        clearSelection();
                        currentFilename = file.name;
                        updateFilenameDisplay();
                        isDirty = false;
                        updateStatus('Ready');
                    }
                })
                .finally(() => {
                    hideHourglassCursor();
                });
            };
            reader.readAsText(file);
        }
        event.target.value = null;
    });

    function save(filename) {
        showHourglassCursor();
        updateStatus('Saving file...');
        fetch('/api/model/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filename: filename }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateStatus('File saved successfully.');
                currentFilename = filename;
                updateFilenameDisplay();
                updateFilenameDisplay();
                loadConstructions();
                isDirty = false;
            } else {
                updateStatus(`Error saving file: ${data.message}`, true);
            }
        })
        .finally(() => {
            hideHourglassCursor();
        });
    }

    function saveAs() {
        const filename = prompt('Enter filename:', currentFilename || 'construction.json');
        if (filename) {
            save(filename);
        }
    }

    saveBtn.addEventListener('click', () => {
        if (currentFilename && currentFilename !== 'untitled.json') {
            save(currentFilename);
        } else {
            saveAs();
        }
    });

    saveAsBtn.addEventListener('click', () => {
        saveAs();
    });

    initSvgEventListeners();
    loadConstructions();
    updateFilenameDisplay();
    updateSelectedPointsDisplay();

    document.addEventListener('keydown', (event) => {
        if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
            return;
        }

        const key = event.key;
        let btn;

        switch (key) {
            case 'l':
                btn = lineBtn;
                break;
            case 'c':
                btn = circleBtn;
                break;
            case 'p':
                btn = pointBtn;
                break;
            case 's':
                btn = segmentBtn;
                break;
            case 'S':
                btn = sectionBtn;
                break;
            case 'y':
                btn = polygonBtn;
                break;
            case 'f':
                fitConstruction();
                break;
            case 'ArrowUp':
                TL_DRAW.progress(0).pause();
                playPauseBtn.innerHTML = '<span class="material-icons">play_arrow</span>';
                break;
            case 'ArrowDown':
                TL_DRAW.progress(1).pause();
                playPauseBtn.innerHTML = '<span class="material-icons">play_arrow</span>';
                break;
            case 'ArrowLeft':
                stepBackward();
                break;
            case 'ArrowRight':
                stepForward();
                break;
        }

        if (btn && !btn.disabled) {
            btn.click();
        }
    });

    const playPauseBtn = document.getElementById('play-pause-btn');
    const timelineSlider = document.getElementById('timeline-slider');
    const animationToggle = document.getElementById('animation-toggle');
    const startBtn = document.getElementById('start-btn');
    const stepBackBtn = document.getElementById('step-back-btn');
    const stepFwdBtn = document.getElementById('step-fwd-btn');
    const endBtn = document.getElementById('end-btn');
    let animationEnabled = animationToggle.checked;

    function animateConstruction() {
        const elements = GEOMETOR.modelData.elements;
        if (!elements || elements.length === 0) return;

        TL_DRAW.clear();

        let scrub = { step: 0 };

        TL_DRAW.to(scrub, {
            step: elements.length,
            duration: elements.length * 0.5,
            ease: `steps(${elements.length})`,
            onUpdate: () => {
                const currentStep = Math.floor(scrub.step);

                elements.forEach((el, index) => {
                    const domElement = document.getElementById(el.ID);
                    if (domElement) {
                        const isVisible = index < currentStep;
                        gsap.set(domElement, { autoAlpha: isVisible ? 1 : 0 });

                        const isHighlighted = index === currentStep - 1;
                        GEOMETOR.setElementHover(el.ID, isHighlighted);
                    }
                });
            },
            onComplete: () => {
                elements.forEach(el => {
                    const domElement = document.getElementById(el.ID);
                    if (domElement) gsap.set(domElement, { autoAlpha: 1 });
                    GEOMETOR.setElementHover(el.ID, false);
                });
            },
            onReverseComplete: () => {
                elements.forEach(el => {
                    const domElement = document.getElementById(el.ID);
                    if (domElement) gsap.set(domElement, { autoAlpha: 0 });
                    GEOMETOR.setElementHover(el.ID, false);
                });
            }
        });

        timelineSlider.max = 100;
        TL_DRAW.eventCallback("onUpdate", () => {
            timelineSlider.value = TL_DRAW.progress() * 100;
        });
    }

    playPauseBtn.addEventListener('click', () => {
        if (TL_DRAW.paused()) {
            TL_DRAW.play();
            playPauseBtn.innerHTML = '<span class="material-icons">pause</span>';
        } else {
            TL_DRAW.pause();
            playPauseBtn.innerHTML = '<span class="material-icons">play_arrow</span>';
        }
    });

        timelineSlider.addEventListener('input', () => {

            TL_DRAW.progress(timelineSlider.value / 100).pause();

        });

    

        function stepForward() {

            const elements = GEOMETOR.modelData.elements;

            if (!elements || elements.length === 0) return;

            const numElements = elements.length;

            const currentProgress = TL_DRAW.progress();

            const epsilon = 1e-9;

    

            if (currentProgress === 1) return;

    

            const val = currentProgress * numElements;

            let targetStep = Math.ceil(val);

    

            if (Math.abs(val - Math.round(val)) < epsilon) {

                targetStep = Math.round(val) + 1;

            }

    

            if (targetStep > numElements) {

                targetStep = numElements;

            }

    

            TL_DRAW.progress(targetStep / numElements).pause();

            playPauseBtn.innerHTML = '<span class="material-icons">play_arrow</span>';

        }

    

        function stepBackward() {

            const elements = GEOMETOR.modelData.elements;

            if (!elements || elements.length === 0) return;

            const numElements = elements.length;

            const currentProgress = TL_DRAW.progress();

            const epsilon = 1e-9;

    

            if (currentProgress === 0) return;

    

            const val = currentProgress * numElements;

            let targetStep = Math.floor(val);

    

            if (Math.abs(val - Math.round(val)) < epsilon) {

                targetStep = Math.round(val) - 1;

            }

    

            if (targetStep < 0) {

                targetStep = 0;

            }

    

            TL_DRAW.progress(targetStep / numElements).pause();

            playPauseBtn.innerHTML = '<span class="material-icons">play_arrow</span>';

        }

    

        startBtn.addEventListener('click', () => {

            TL_DRAW.progress(0).pause();

            playPauseBtn.innerHTML = '<span class="material-icons">play_arrow</span>';

        });

    

        stepBackBtn.addEventListener('click', stepBackward);

    

        stepFwdBtn.addEventListener('click', stepForward);

    

        endBtn.addEventListener('click', () => {

            TL_DRAW.progress(1).pause();

            playPauseBtn.innerHTML = '<span class="material-icons">play_arrow</span>';

        });

    

        animationToggle.addEventListener('change', () => {

            animationEnabled = animationToggle.checked;

            renderModel(GEOMETOR.modelData);

        });


});
