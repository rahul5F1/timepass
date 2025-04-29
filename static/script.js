const container = document.getElementById("container");
const registerBtn = document.getElementById("register");
const loginBtn = document.getElementById("login");

registerBtn.addEventListener("click", () => {
  container.classList.add("active");
});

loginBtn.addEventListener("click", () => {
  container.classList.remove("active");
});

function validateRegistrationForm() {
  const password = document.getElementById("reg_password").value;
  const confirmPassword = document.getElementById("reg_confirm_password").value;
  const errorMsg = document.getElementById("regError");

  if (password !== confirmPassword) {
    errorMsg.textContent = "Passwords do not match!";
    errorMsg.style.display = "block";
    return false; // prevent form submission
  }

  errorMsg.style.display = "none";
  return true; // allow form submission
}