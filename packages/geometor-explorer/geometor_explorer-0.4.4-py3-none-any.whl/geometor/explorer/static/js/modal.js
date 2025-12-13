export const modal = {
    init: () => {
        const modalEl = document.getElementById('modal');
        const closeBtn = document.querySelector('.close-btn');

        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                modalEl.style.display = 'none';
            });
        }

        window.addEventListener('click', (event) => {
            if (event.target == modalEl) {
                modalEl.style.display = 'none';
            }
        });
    },

    show: (title, content, onsubmit) => {
        const modalEl = document.getElementById('modal');
        const modalTitle = document.getElementById('modal-title');
        const modalBody = document.getElementById('modal-body');

        modalTitle.textContent = title;
        modalBody.innerHTML = content;

        const form = modalBody.querySelector('form');
        if (form) {
            form.onsubmit = (event) => {
                event.preventDefault();
                const formData = new FormData(form);
                const data = Object.fromEntries(formData.entries());
                if (onsubmit) {
                    onsubmit(data);
                }
                modalEl.style.display = 'none';
            };
        }

        modalEl.style.display = 'block';
    }
};
