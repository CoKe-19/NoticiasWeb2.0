document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("formPostulacion");
  if (!form) return;

  form.addEventListener("submit", () => {
    alert("✅ Tu postulación fue enviada. Un administrador revisará tu solicitud pronto.");
  });
});
