export function initGroupsView() {
    fetchGroupsBySize();
    fetchGroupsByPoint();
    fetchGroupsByChain();
}

async function fetchGroupsBySize() {
    try {
        const response = await fetch('/api/groups/by_size');
        const data = await response.json();
        populateSizesTable(data);
    } catch (error) {
        console.error('Error fetching groups by size:', error);
    }
}

async function fetchGroupsByPoint() {
    try {
        const response = await fetch('/api/groups/by_point');
        const data = await response.json();
        populatePointsGroupTable(data);
    } catch (error) {
        console.error('Error fetching groups by point:', error);
    }
}

async function fetchGroupsByChain() {
    try {
        const response = await fetch('/api/groups/by_chain');
        const data = await response.json();
        populateChainsTable(data);
    } catch (error) {
        console.error('Error fetching groups by chain:', error);
    }
}

function populateSizesTable(data) {
    const columns = [
        { key: 'size', transform: (val) => parseFloat(val).toFixed(4) },
        { key: 'count' }
    ];
    const entries = Object.entries(data).map(([size, sections]) => ({ size, sections, count: sections.length }));
    populateTable('sizes-table', entries, columns, 'count', 'desc');
    document.getElementById('sizes-count').textContent = entries.length;
}

function populatePointsGroupTable(data) {
    const columns = [
        { key: 'pointId' },
        { key: 'count' }
    ];
    const entries = Object.entries(data).map(([pointId, sections]) => ({ pointId, sections, count: sections.length }));
    populateTable('points-group-table', entries, columns, 'count', 'desc');
    document.getElementById('points-group-count').textContent = entries.length;
}

function populateChainsTable(data) {
    const columns = [
        { key: 'name' },
        { key: 'count' }
    ];
    const entries = data.map(chain => ({ ...chain, count: chain.sections.length }));
    populateTable('chains-table', entries, columns, 'count', 'desc');
    document.getElementById('chains-count').textContent = entries.length;
}

function populateTable(tableId, data, columns, initialSortKey, initialSortOrder) {
    const table = document.getElementById(tableId);
    const tableBody = table.getElementsByTagName('tbody')[0];
    const tableHead = table.getElementsByTagName('thead')[0];
    tableBody.innerHTML = '';

    let sortKey = initialSortKey;
    let sortOrder = initialSortOrder;

    function sortData(key) {
        if (sortKey === key) {
            sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
        } else {
            sortKey = key;
            sortOrder = 'asc';
        }

        data.sort((a, b) => {
            const valA = a[sortKey];
            const valB = b[sortKey];

            if (valA < valB) {
                return sortOrder === 'asc' ? -1 : 1;
            }
            if (valA > valB) {
                return sortOrder === 'asc' ? 1 : -1;
            }
            return 0;
        });

        updateSortIndicators();
        renderTable();
    }

    function updateSortIndicators() {
        tableHead.querySelectorAll('th').forEach((th, index) => {
            const column = columns[index];
            if (column) {
                th.classList.remove('asc', 'desc');
                if (column.key === sortKey) {
                    th.classList.add(sortOrder);
                }
            }
        });
    }

    function renderTable() {
        tableBody.innerHTML = '';
        data.forEach(item => {
            const row = tableBody.insertRow();
            row.dataset.sections = JSON.stringify(item.sections);
            columns.forEach(column => {
                const cell = row.insertCell();
                const value = item[column.key];
                cell.textContent = column.transform ? column.transform(value) : value;
            });
        });
    }

    tableHead.querySelectorAll('th').forEach((th, index) => {
        const column = columns[index];
        if (column) {
            th.classList.add('sortable');
            th.addEventListener('click', () => sortData(column.key));
        }
    });
    
    sortData(sortKey);
}

export function initGroupsEventListeners() {
    const groupTables = ['sizes-table', 'points-group-table', 'chains-table'];

    groupTables.forEach(tableId => {
        const table = document.getElementById(tableId);
        if (table) {
            table.addEventListener('mouseover', (event) => {
                const row = event.target.closest('tr');
                if (row && row.dataset.sections) {
                    const sections = JSON.parse(row.dataset.sections);
                    sections.forEach(id => GEOMETOR.setElementHover(id, true));
                }
            });

            table.addEventListener('mouseout', (event) => {
                const row = event.target.closest('tr');
                if (row && row.dataset.sections) {
                    const sections = JSON.parse(row.dataset.sections);
                    sections.forEach(id => GEOMETOR.setElementHover(id, false));
                }
            });
        }
    });
}

