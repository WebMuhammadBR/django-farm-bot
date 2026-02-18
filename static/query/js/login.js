const passwordInput = document.getElementById("id_password");
const showPasswordCheckbox = document.getElementById("id_show_password");

if (passwordInput && showPasswordCheckbox) {
    const syncPasswordVisibility = () => {
        passwordInput.type = showPasswordCheckbox.checked ? "text" : "password";
    };

    showPasswordCheckbox.addEventListener("change", syncPasswordVisibility);
    syncPasswordVisibility();
}
