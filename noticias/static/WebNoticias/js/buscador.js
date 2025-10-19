document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("#buscador");
  const input = document.querySelector("#input-busqueda");
  const resultados = document.querySelector("#resultados-busqueda");
  let timeout = null;

  if (!form || !input || !resultados) return;

  // Evita que se recargue la página en cualquier caso
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    ejecutarBusqueda(input.value.trim());
  });

  // Detecta escritura
  input.addEventListener("input", () => {
    clearTimeout(timeout);
    const query = input.value.trim();
    if (query.length < 2) {
      resultados.classList.add("d-none");
      resultados.innerHTML = "";
      return;
    }

    timeout = setTimeout(() => ejecutarBusqueda(query), 300);
  });

  // Cierra los resultados al hacer clic fuera
  document.addEventListener("click", (e) => {
    if (!resultados.contains(e.target) && e.target !== input) {
      resultados.classList.add("d-none");
    }
  });

  // 🔍 Función para ejecutar la búsqueda AJAX
  function ejecutarBusqueda(query) {
    if (!query) return;

    fetch(`/buscar/?q=${encodeURIComponent(query)}`, {
      headers: { "X-Requested-With": "XMLHttpRequest" },
    })
      .then((res) => res.text())
      .then((html) => {
        resultados.innerHTML = html;
        resultados.classList.remove("d-none");
      })
      .catch((err) => {
        console.error("Error al buscar:", err);
        resultados.innerHTML =
          "<p class='text-danger text-center p-2'>Error al buscar 😕</p>";
        resultados.classList.remove("d-none");
      });
  }
});
