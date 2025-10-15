// Animaciones al aparecer
const animateElements = document.querySelectorAll('.animate-on-scroll');
const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if(entry.isIntersecting){
            entry.target.classList.add('fade-in');
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.2 });
animateElements.forEach(el => observer.observe(el));

// Filtro dinámico (opcional)
document.addEventListener('DOMContentLoaded', () => {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const cards = document.querySelectorAll('.noticia-card');

    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const category = btn.dataset.category;
            cards.forEach(card => {
                if(category === 'all' || card.dataset.category === category){
                    card.style.display = 'block';
                    setTimeout(() => card.classList.add('fade-in'), 50);
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
});

// Validación simple de contacto
const contactForm = document.getElementById('contactForm');
const formMessage = document.getElementById('formMessage');

if(contactForm){
    contactForm.addEventListener('submit', e => {
        e.preventDefault();

        const nombre = document.getElementById('nombre').value.trim();
        const email = document.getElementById('email').value.trim();
        const asunto = document.getElementById('asunto').value.trim();
        const mensaje = document.getElementById('mensaje').value.trim();

        if(nombre === '' || email === '' || asunto === '' || mensaje === ''){
            formMessage.innerHTML = '<div class="alert alert-danger">Por favor, completa todos los campos.</div>';
            return;
        }

        // Simulación de envío
        formMessage.innerHTML = '<div class="alert alert-success">¡Mensaje enviado correctamente! Gracias por contactarnos.</div>';

        // Limpiar campos
        contactForm.reset();
    });
}

// Animación al aparecer
document.addEventListener('DOMContentLoaded', () => {
    const elements = document.querySelectorAll('.animate-on-scroll');
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if(entry.isIntersecting){
                entry.target.classList.add('visible');
            }
        });
    }, {threshold: 0.2});

    elements.forEach(el => observer.observe(el));
});
