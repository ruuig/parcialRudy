// 🧹 Cerrar mensajes flash automáticamente luego de 5 segundos
window.addEventListener("DOMContentLoaded", () => {
  const flashMessages = document.querySelectorAll(".flash .alert-success, .flash .alert-info, .flash .alert-warning, .flash .alert-danger");
  flashMessages.forEach((msg) => {
    setTimeout(() => {
      msg.style.display = "none";
    }, 5000); // 
  });
});

document.addEventListener("submit", function (e) {
  const form = e.target;
  const requiredFields = form.querySelectorAll("[required]");
  let valid = true;

  requiredFields.forEach(field => {
    if (!field.value.trim()) {
      field.classList.add("is-invalid");
      valid = false;
    } else {
      field.classList.remove("is-invalid");
    }
  });

  if (!valid) {
    e.preventDefault(); // 
  }
});
