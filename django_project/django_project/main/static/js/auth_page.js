function toggleForm() {
    const signup = document.getElementById('signup-form')
    const login = document.getElementById('login-form')

    if (signup.classList.contains('active')) {
        signup.classList.remove('active')
        login.classList.add('active')
    } else {
        login.classList.remove('active')
        signup.classList.add('active')
    }
}