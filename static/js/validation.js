function validateForm() {
    var password = document.forms["signupForm"]["psw"].value;
    var confirmPassword = document.forms["signupForm"]["psw-repeat"].value;
    if (password !== confirmPassword) {
        alert("Passwords do not match.");
        return false;
    }
    return true;
}
