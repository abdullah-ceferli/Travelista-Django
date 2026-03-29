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

async function loadUserMessages() { 
    const container = document.getElementById('user-comments')
    if (!container) return

    try {
        const response = await fetch('/api/user-messages/')
        const data = await response.json()

        if (data.results && data.results.length > 0) {
            const displayCount = String(data.count).padStart(2, '0');
            let userMessagesHtml = `<h4>${displayCount} Comments</h4>`

            data.results.forEach(item => {
                const imgPath = item.user_img ? item.user_img : '/static/img/default-user.png'
                
                userMessagesHtml += `
                <div class="comment-list">
                    <div class="single-comment">
                        <div class="user">
                            <div class="thumb">
                                <img src="${imgPath}" alt="${item.name}">
                            </div>
                            <div class="desc">
                                <h5><a href="#">${item.name}</a></h5>
                                <p class="date">${item.created_at || 'Just now'}</p>
                                <p class="comment">
                                    ${item.message}
                                </p>
                            </div>
                        </div>
                        <div class="reply-btn">
                            <a href="#" class="btn-reply text-uppercase">reply</a>
                        </div>
                    </div>
                </div>`
            })

            container.innerHTML = userMessagesHtml;
        } 
        else {
            container.innerHTML = '<h4>00 Comments</h4><p>No user messages available.</p>'
        }
    } 
    catch (error) {
        console.error("Error loading user messages:", error)
        container.innerHTML = '<p>Error loading comments.</p>'
    }
}