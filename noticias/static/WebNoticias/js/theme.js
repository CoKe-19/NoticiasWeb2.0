document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.getElementById("theme-toggle");
  const body = document.body;
  const icon = toggleBtn.querySelector("i");

  // --- Configuración inicial ---
  const savedTheme = localStorage.getItem("theme");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

  if (savedTheme === "dark" || (!savedTheme && prefersDark)) {
    body.classList.add("dark-mode");
    icon.classList.replace("bi-moon", "bi-sun");
  }

  // --- Animación suave ---
  body.style.transition = "background-color 0.4s ease, color 0.4s ease";

  // --- Evento de cambio ---
  toggleBtn.addEventListener("click", () => {
    const isDark = body.classList.toggle("dark-mode");
    icon.classList.toggle("bi-moon", !isDark);
    icon.classList.toggle("bi-sun", isDark);

    // Animación visual breve en el botón
    toggleBtn.classList.add("theme-anim");
    setTimeout(() => toggleBtn.classList.remove("theme-anim"), 300);

    // Guardar preferencia
    localStorage.setItem("theme", isDark ? "dark" : "light");
  });
});
