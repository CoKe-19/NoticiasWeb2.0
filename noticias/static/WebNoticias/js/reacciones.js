document.addEventListener("DOMContentLoaded", () => {
  const reacciones = document.querySelector(".reacciones");
  if (!reacciones) return;

  const url = reacciones.dataset.url;
  const conteoDiv = document.getElementById("conteo-reacciones");

  // Actualiza visualmente la reacción activa
  function actualizarActiva(tipo, accion) {
    const botones = reacciones.querySelectorAll(".btn-reaccion");
    botones.forEach((b) => {
      if (accion === "removed") {
        b.classList.remove("activa");
      } else {
        b.classList.toggle("activa", b.dataset.tipo === tipo);
      }
    });
  }

  // Enviar reacción al servidor
  reacciones.addEventListener("click", (e) => {
    const boton = e.target.closest(".btn-reaccion");
    if (!boton) return;

    const tipo = boton.dataset.tipo;

    fetch(url, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({ tipo }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (!data.success) return;

        // 🔥 Actualiza los conteos en vivo
        const c = data.counts;
        conteoDiv.innerHTML = `
          <div class="conteo-item"><span>❤️</span> <strong>${c.like}</strong></div>
          <div class="conteo-item"><span>😍</span> <strong>${c.love}</strong></div>
          <div class="conteo-item"><span>😂</span> <strong>${c.funny}</strong></div>
          <div class="conteo-item"><span>😮</span> <strong>${c.wow}</strong></div>
          <div class="conteo-item"><span>😢</span> <strong>${c.sad}</strong></div>
          <div class="conteo-item"><span>😡</span> <strong>${c.angry}</strong></div>
        `;

        // 🔄 Marca o quita reacción activa en vivo
        actualizarActiva(tipo, data.accion);

        // 💥 Animación suave
        boton.classList.add("react-anim");
        setTimeout(() => boton.classList.remove("react-anim"), 250);
      })
      .catch((err) => console.error("Error al reaccionar:", err));
  });
});

// Token CSRF
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
