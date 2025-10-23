document.addEventListener('DOMContentLoaded', () => {

  // ==========================
  // 🌀 Animación al aparecer al hacer scroll
  // ==========================
  const animateElements = document.querySelectorAll('.animate-on-scroll');

  if (animateElements.length > 0) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
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
  }

  // ===========================
  // 🔔 Toasts / Alertas automáticas (desde la izquierda, 1s)
  // ===========================
  const toasts = document.querySelectorAll("#toast-container .toast-message");

  toasts.forEach(toast => {
    // Colores según tipo
    if (toast.classList.contains("success")) toast.style.backgroundColor = "#28a745";
    else if (toast.classList.contains("error") || toast.classList.contains("danger")) toast.style.backgroundColor = "#dc3545";
    else if (toast.classList.contains("warning")) toast.style.backgroundColor = "#ffc107";
    else toast.style.backgroundColor = "#17a2b8";

    // Estilos base (entra desde la izquierda)
    toast.style.opacity = 0;
    toast.style.transform = "translateX(-100%)";
    toast.style.transition = "opacity 0.4s ease, transform 0.4s ease";

    // Entrada suave
    requestAnimationFrame(() => {
      toast.style.opacity = 1;
      toast.style.transform = "translateX(0)";
    });

    // Desaparecer automáticamente después de 1 s
    setTimeout(() => {
      toast.style.opacity = 0;
      toast.style.transform = "translateX(-100%)";
      setTimeout(() => toast.remove(), 400);
    }, 1500);
  });
});

// ✨ Scroll suave en enlaces internos
document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener("click", e => {
    e.preventDefault();
    document.querySelector(link.getAttribute("href")).scrollIntoView({ 
      behavior: "smooth" 
    });
  });
});

// 🌈 Transición de color al hacer hover en botones
document.querySelectorAll("button, .btn").forEach(btn => {
  btn.addEventListener("mouseenter", () => btn.style.filter = "brightness(1.2)");
  btn.addEventListener("mouseleave", () => btn.style.filter = "brightness(1)");
});

