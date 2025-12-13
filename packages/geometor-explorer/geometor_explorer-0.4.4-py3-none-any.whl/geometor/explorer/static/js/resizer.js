export function initResizer() {
    const resizer = document.getElementById('resizer');
    const aside = document.querySelector('aside');
    const body = document.querySelector('body');

    let isResizing = false;

    resizer.addEventListener('mousedown', (e) => {
        isResizing = true;
        document.addEventListener('mousemove', handleMouseMove);
        document.addEventListener('mouseup', () => {
            isResizing = false;
            document.removeEventListener('mousemove', handleMouseMove);
        });
    });

    function handleMouseMove(e) {
        if (!isResizing) return;
        const newWidth = window.innerWidth - e.clientX;
        body.style.gridTemplateColumns = `1fr 5px ${newWidth}px`;
    }
}

