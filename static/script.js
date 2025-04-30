const container = document.getElementById("container");
const registerBtn = document.getElementById("register");
const loginBtn = document.getElementById("login");
registerBtn.addEventListener("click", () => container.classList.add("active"));
loginBtn.addEventListener("click", () => container.classList.remove("active"));
const forgotPasswordLink = document.getElementById("forgotPasswordLink");

// if (forgotPasswordLink) {
//   forgotPasswordLink.addEventListener("click", function(e) {
//     e.preventDefault(); // Prevent link navigation
//     openResetPopup();
//   });

// }
// console.log("hio")
forgotPasswordLink.addEventListener("click", function (e) {
  // console.log("hi")
  e.preventDefault(); // Prevent link navigation
  openResetPopup();
})


function validateRegistrationForm() {
  const password = document.getElementById("reg_password").value;
  const confirmPassword = document.getElementById("reg_confirm_password").value;
  const errorMsg = document.getElementById("regError");
  if (password !== confirmPassword) {
    errorMsg.style.display = "block";
    return false;
  }
  errorMsg.style.display = "none";
  return true;
}

function openResetPopup() {
  // console.log("hloo")
  document.getElementById("container").style.display = "none";
  document.getElementById("resetPopup").style.display = "flex";
  // document.getElementById("resetError").style.display = "none";
  // document.getElementById("passwordFields").style.display = "none";
}

function closeResetPopup() {
  // document.getElementById("resetPopup").style.display = "flex";

  // let email=document.getElementById('reset_email').value;
  // let security_question=document.getElementById('reset_question').value;
  // let security_answer=document.getElementById('reset_answer').value;
  // console.log(email,security_question,security_answer)
  document.getElementById("resetForm").reset();
  // document.getElementById("resetError").style.display = "none";
  // document.getElementById("passwordFields").style.display = "none";
}

async function handleReset(event) {
  event.preventDefault();
  const email = document.getElementById("reset_email").value;
  const question = document.getElementById("reset_question").value;
  const answer = document.getElementById("reset_answer").value;
  const errorMsg = document.getElementById("resetError");
  const passwordFields = document.getElementById("passwordFields");
  // const newPass = document.getElementById("new_password").value;
  // const confirmPass = document.getElementById("confirm_new_password").value;
  if (passwordFields.style.display === "none") {
    console.log("hiji")
    // First step: verify
    const res = await fetch("/verify_data", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, question, answer })
    });
    const data = await res.json();
    if (data.success) {
      passwordFields.style.display = "block";
      errorMsg.style.display = "none";
    } else {
      errorMsg.textContent = data.message;
      errorMsg.style.display = "block";
    }
  } else {
    const newPass = document.getElementById("new_password").value;
    const confirmPass = document.getElementById("confirm_new_password").value;
    // Second step: update password
    if (newPass !== confirmPass) {
      errorMsg.textContent = "Passwords do not match!";
      errorMsg.style.display = "block";
      return;
    }
    const res = await fetch("/reset_password", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email,newPass})
    });
    const data = await res.json();
    if (data.success) {
      alert("Password reset successful. Please log in.");
      closeResetPopup();
    } else {
      errorMsg.textContent = data.message;
      errorMsg.style.display = "block";
    }
  }
}

let closeResetPass=()=>{
  document.getElementById('resetPopup').style.display="none"
  document.getElementById('container').style.display="flex"
}
