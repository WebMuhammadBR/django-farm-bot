const passwordInput = document.getElementById("id_password");
const showPasswordCheckbox = document.getElementById("id_show_password");

if (passwordInput && showPasswordCheckbox) {
    showPasswordCheckbox.addEventListener("change", () => {
        passwordInput.type = showPasswordCheckbox.checked ? "text" : "password";
    });
}
