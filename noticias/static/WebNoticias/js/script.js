document.addEventListener('DOMContentLoaded', () => {

    // ==========================
    // Animación al aparecer al hacer scroll
    // ==========================
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if(entry.isIntersecting){
                entry.target.style.opacity = 1;
                entry.target.style.transform = 'translateY(0)';
                entry.target.style.transition = 'all 0.6s ease-out';
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });

    animateElements.forEach(el => {
        el.style.opacity = 0;
        el.style.transform = 'translateY(30px)';
        observer.observe(el);
    });

    // ==========================
    // Filtro dinámico de noticias
    // ==========================
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

    // ==========================
    // Toasts / Alertas automáticas
    // ==========================
    const toasts = document.querySelectorAll('#toast-container .toast-message');

    toasts.forEach(toast => {
        // Colores según tipo
        if(toast.classList.contains('success')) toast.style.backgroundColor = '#28a745';
        else if(toast.classList.contains('error') || toast.classList.contains('danger')) toast.style.backgroundColor = '#dc3545';
        else if(toast.classList.contains('warning')) toast.style.backgroundColor = '#ffc107';
        else toast.style.backgroundColor = '#17a2b8'; // info por defecto

        toast.style.color = '#fff';
        toast.style.padding = '12px 18px';
        toast.style.marginBottom = '0.5rem';
        toast.style.borderRadius = '8px';
        toast.style.boxShadow = '0 4px 12px rgba(0,0,0,0.2)';
        toast.style.opacity = 0;
        toast.style.transform = 'translateY(-20px)';
        toast.style.transition = 'opacity 0.5s ease, transform 0.5s ease';

        // Animar entrada
        setTimeout(() => {
            toast.style.opacity = 1;
            toast.style.transform = 'translateY(0)';
        }, 100);

        // Desaparecer automáticamente después de 3 segundos
        setTimeout(() => {
            toast.style.opacity = 0;
            toast.style.transform = 'translateY(-20px)';
            setTimeout(() => toast.remove(), 500);
        }, 3000);
    });

});
