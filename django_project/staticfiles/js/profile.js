function navBarLinksChilds() {
    document.querySelectorAll('.menu-has-children').forEach(function (menu) {
        let timeout
        const submenu = menu.querySelector('ul')

        menu.addEventListener('mouseenter', function () {
            clearTimeout(timeout)
            submenu.classList.add('is-visible')
        })

        menu.addEventListener('mouseleave', function () {
            timeout = setTimeout(function () {
                submenu.classList.remove('is-visible')
            }, 200)
        })
    })
}

function navBarMovement() {
    const headerSticky = document.getElementById("nav-bar")
    const navBarMainMenu = document.querySelector(".nav-bar-main-menu")

    window.addEventListener("scroll", () => {
        if (window.scrollY > 80) {
            headerSticky.classList.add("nav-bar-scrolled")
            navBarMainMenu.style.background = "transparent"
        }
        else {
            headerSticky.classList.remove("nav-bar-scrolled")
            navBarMainMenu.style.background = "rgba(255, 255, 255, 0.15)"
        }
    })
}

function smoothUp() {
    document.querySelectorAll('a[href="#"]').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault()
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            })
        })
    })
}

function toggleComments() {
    const commentsSection = document.querySelector('.profile-comments')
    const toggleButton = document.querySelector('.btn-message')

    toggleButton.addEventListener('click', function (e) {
        e.preventDefault()
        
        const isHidden = commentsSection.style.display === 'none' || commentsSection.style.display === ''
        
        if (isHidden) {
            commentsSection.style.display = 'flex'
            
            commentsSection.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start' 
            })
        } else {
            commentsSection.style.display = 'none'
        }
    })
}