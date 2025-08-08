const passwordInput = document.getElementById("password");
const confirmPasswordInput = document.getElementById("confirmPassword");
const usernameInput = document.getElementById("username");
const emailInput = document.getElementById("email");
const submitBtn = document.getElementById("submitBtn");
const togglePasswordBtn = document.getElementById("togglePassword");
const toggleConfirmBtn = document.getElementById("toggleConfirm");

window.onload = () => {
  // Limpiar campos
  usernameInput.value = "";
  emailInput.value = "";
  passwordInput.value = "";
  confirmPasswordInput.value = "";

  // Desactivar confirmación de contraseña
  confirmPasswordInput.disabled = true;

  // Limpiar mensajes de error
  document.getElementById("emailError").textContent = "";
  document.getElementById("passwordMatchError").textContent = "";
  const recaptchaError = document.getElementById("recaptchaError");
  if (recaptchaError) recaptchaError.textContent = "";

  // Quitar clases de validación
  ["longitud", "mayuscula", "minuscula", "numero", "especial"].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.classList.remove("valid");
  });

  // Desactivar botón de envío
  submitBtn.disabled = true;
};

function validateFields() {
  const username = usernameInput.value.trim();
  const email = emailInput.value.trim();
  const password = passwordInput.value;
  const confirmPassword = confirmPasswordInput.value;
  const recaptchaValid = validateRecaptcha();
  let passwordIsValid = false;

  const valitations = {
    longitud: /.{8,}/.test(password),
    mayuscula: /[A-Z]/.test(password),
    minuscula: /[a-z]/.test(password),
    numero: /[0-9]/.test(password),
    especial: /[!@#$%^&*(),\.?":{}|<>]/.test(password)
  };

  for (const [id, valid] of Object.entries(valitations)) {
    const element = document.getElementById(id);
    element.classList.toggle("valid", valid);
  }

  // Validación de email
  const emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  emailError.textContent = emailValid ? "" : "Formato de email inválido";

  // Validación de confirmación de contraseña
  const passwordsMatch = password === confirmPassword;
  passwordMatchError.textContent = passwordsMatch ? "" : "Las contraseñas no coinciden";
  
  // Habilitar campo de confirmación solo si la contraseña es válida
  passwordIsValid = Object.values(valitations).every(v => v === true);
  confirmPasswordInput.disabled = !passwordIsValid;
 
  const allSet = username !== "" && email !== "" && password !== "" && confirmPassword !== "";
  submitBtn.disabled = !(passwordIsValid && allSet && passwordsMatch && emailValid && recaptchaValid);

}

function validateRecaptcha() {
  const recaptchaResponse = document.querySelector("#g-recaptcha-response").value;
  return recaptchaResponse.trim() !== "";
}
function onRecaptchaExpired() {
  validateFields(); // Vuelve a validar todo
}
// Escuchar cambios en todos los campos
[usernameInput, emailInput, passwordInput, confirmPasswordInput].forEach(input => {
  input.addEventListener("input", validateFields);
});

togglePasswordBtn.addEventListener("click", () => {
  const isPasswordVisible = passwordInput.type === "text";
  passwordInput.type = isPasswordVisible ? "password" : "text";
  togglePasswordBtn.textContent = isPasswordVisible ? "👁️" : "🙈";
});

toggleConfirmBtn.addEventListener("click", () => {
  const isConfirmVisible = confirmPasswordInput.type === "text";
  confirmPasswordInput.type = isConfirmVisible ? "password" : "text";
  toggleConfirmBtn.textContent = isConfirmVisible ? "👁️" : "🙈";
});
